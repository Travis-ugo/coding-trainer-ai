"use client";

import React, { useState } from "react";
import { useTrainerContext, SyntaxEvalResult, GeminiResponse } from "../context/TrainerContext";
import { Sparkles, Code, Cpu, Layers, BookOpen, Clock, CheckCircle, RotateCcw, Loader2, HelpCircle } from "lucide-react";

interface CanvasWorkspaceProps {
  activeTool: string;
  selectedModule: string;
}

function QuestionCard({ question, index }: { question: any; index: number }) {
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState<boolean>(false);
  const [userInput, setUserInput] = useState<string>("");

  const isMCQ = Array.isArray(question.options) && question.options.length > 0;
  const isCorrect = isMCQ
    ? selectedOption === question.correct_answer
    : userInput.trim().toLowerCase() === question.correct_answer.trim().toLowerCase();

  return (
    <div className="bg-[#0a0a0a] border border-[#222222] p-4 rounded-none space-y-3 font-mono text-xs">
      <div className="flex items-center justify-between">
        <span className="font-bold text-[#0070f3]">Question {index + 1}</span>
        {submitted && (
          <span
            className={`px-2 py-0.5 text-[10px] font-bold ${
              isCorrect
                ? "bg-[#00e599]/20 text-[#00e599] border border-[#00e599]/40"
                : "bg-[#ef4444]/20 text-[#ef4444] border border-[#ef4444]/40"
            }`}
          >
            {isCorrect ? "✓ Correct!" : "❌ Needs Review"}
          </span>
        )}
      </div>

      <p className="text-white font-medium whitespace-pre-wrap leading-relaxed">{question.prompt}</p>

      {/* Multiple Choice Options */}
      {isMCQ ? (
        <div className="space-y-1.5 pt-1">
          {question.options.map((opt: string, optIdx: number) => (
            <button
              key={optIdx}
              onClick={() => {
                setSelectedOption(opt);
                setSubmitted(true);
              }}
              className={`w-full text-left p-2.5 rounded-none border text-xs transition-all ${
                submitted && opt === question.correct_answer
                  ? "bg-[#00e599]/10 border-[#00e599] text-[#00e599] font-semibold"
                  : submitted && selectedOption === opt
                  ? "bg-[#ef4444]/10 border-[#ef4444] text-[#ef4444]"
                  : selectedOption === opt
                  ? "bg-[#1f1f1f] border-white text-white"
                  : "bg-[#111111] border-[#222222] text-[#888888] hover:text-white hover:border-[#444444]"
              }`}
            >
              {opt}
            </button>
          ))}
        </div>
      ) : (
        /* Code Output or Fill-in Answer */
        <div className="space-y-2 pt-1">
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="Type your answer..."
            className="w-full bg-[#111111] border border-[#2a2a2a] focus:border-[#0070f3] text-white p-2.5 text-xs focus:outline-none"
          />
          <button
            onClick={() => setSubmitted(true)}
            className="btn-next-secondary text-xs px-3 py-1"
          >
            Check Answer
          </button>
        </div>
      )}

      {/* Explanation & Distinction Tip */}
      {submitted && (
        <div className="pt-2 border-t border-[#222222] space-y-2">
          <div className="text-[#e2e8f0] bg-[#111111] p-3 border border-[#222222] leading-relaxed">
            <span className="font-bold text-white">Explanation: </span>
            {question.explanation}
          </div>

          {question.uk_msc_distinction_tip && (
            <div className="text-[#0070f3] bg-[#0070f3]/10 p-2.5 border border-[#0070f3]/30 leading-relaxed text-[11px]">
              <span className="font-bold">🏆 MSc Distinction Tip: </span>
              {question.uk_msc_distinction_tip}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export const CanvasWorkspace: React.FC<CanvasWorkspaceProps> = ({
  activeTool,
  selectedModule,
}) => {
  const {
    modulesData,
    analyticsData,
    routineData,
    flashcardDecks,
    ros2Data,
    loading,
    error,
    rateFlashcard,
    evaluateSyntax,
    askGemini,
  } = useTrainerContext();

  // Flashcard State
  const [selectedDeckId, setSelectedDeckId] = useState<string>("");
  const [flashcardFlipped, setFlashcardFlipped] = useState(false);
  const [flashcardIndex, setFlashcardIndex] = useState(0);

  // Derive Active Deck
  const activeDeckId = selectedDeckId || (flashcardDecks[0]?.id ?? "");

  const dynamicModule = modulesData.find((m) => m.id === selectedModule);
  const activeModuleData = dynamicModule
    ? { title: dynamicModule.title, code: dynamicModule.syntax_guide }
    : { title: "Python Syntax Gym", code: "# Select a module from the left sidebar to begin AST syntax drills" };

  // Syntax Gym Code State keyed by active module
  const [syntaxCode, setSyntaxCode] = useState(activeModuleData.code);
  const [syntaxFeedback, setSyntaxFeedback] = useState<SyntaxEvalResult | null>(null);
  const [syntaxEvaluating, setSyntaxEvaluating] = useState(false);
  const [syntaxError, setSyntaxError] = useState<string | null>(null);

  // Gemini AI Tutor State
  const [aiQuery, setAiQuery] = useState("");
  const [aiResponse, setAiResponse] = useState<GeminiResponse | null>(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState<string | null>(null);

  // Flashcards Logic
  const currentDeck = flashcardDecks.find((d) => d.id === activeDeckId) || flashcardDecks[0];
  const isDeckCompleted = currentDeck ? flashcardIndex >= currentDeck.cards.length : false;
  const currentCard = currentDeck && !isDeckCompleted ? currentDeck.cards[flashcardIndex] : null;

  const handleNextFlashcard = async (rating: number) => {
    if (currentCard) {
      try {
        await rateFlashcard(currentCard.card_id, rating);
      } catch (err: unknown) {
        console.error("Failed to rate card:", err);
      }
    }
    setFlashcardFlipped(false);
    setFlashcardIndex((prev) => prev + 1);
  };

  const handleEvaluateSyntax = async () => {
    setSyntaxEvaluating(true);
    setSyntaxError(null);
    try {
      const res = await evaluateSyntax(syntaxCode);
      setSyntaxFeedback(res);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to evaluate syntax";
      setSyntaxError(msg);
    } finally {
      setSyntaxEvaluating(false);
    }
  };

  const handleAskGemini = async () => {
    if (!aiQuery) return;
    setAiLoading(true);
    setAiError(null);
    try {
      const res = await askGemini(aiQuery);
      setAiResponse(res);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to get AI response";
      setAiError(msg);
    } finally {
      setAiLoading(false);
    }
  };

  return (
    <main className="flex-1 bg-[#000000] overflow-y-auto p-8 relative flex justify-center items-start">
      <div className="w-full max-w-4xl space-y-6">
        {error && (
          <div className="bg-[#7f1d1d]/30 border border-[#ef4444] text-[#ef4444] p-3.5 rounded-none text-xs font-mono">
            ⚠️ {error}
          </div>
        )}

        {/* TOOL 1: Master's Grade Readiness Heatmap */}
        {activeTool === "analytics" && (
          <div className="space-y-5">
            <div className="flex items-center justify-between border-b border-[#222222] pb-4">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <Layers className="w-4 h-4 text-[#0070f3]" />
                  Grade Readiness Heatmap
                </h2>
                <p className="text-xs text-[#888888] mt-0.5">
                  Topic mastery breakdown.
                </p>
              </div>
            </div>

            <div className="bg-[#0a0a0a] border border-[#222222] rounded-none p-5 space-y-4">
              {analyticsData?.topic_grades && analyticsData.topic_grades.length > 0 ? (
                analyticsData.topic_grades.map((item, idx) => (
                  <div key={idx} className="space-y-1">
                    <div className="flex justify-between text-xs font-mono">
                      <span className="text-[#e2e8f0]">{item.topic_name}</span>
                      <span style={{ color: item.color_hex }} className="font-semibold">
                        {item.score_percentage}% ({item.grade_label})
                      </span>
                    </div>
                    <div className="w-full bg-[#111111] h-1.5 rounded-none overflow-hidden border border-[#222222]">
                      <div
                        className="h-full rounded-none transition-all duration-300"
                        style={{ width: `${item.score_percentage}%`, backgroundColor: item.color_hex }}
                      />
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-xs text-[#888888] text-center py-4 font-mono">
                  {loading ? "Loading analytics..." : "No analytics recorded yet"}
                </div>
              )}
            </div>
          </div>
        )}

        {/* TOOL 2: Real Daily 15-Min Power Session */}
        {activeTool === "routine" && (
          <div className="space-y-5">
            <div className="flex items-center justify-between border-b border-[#222222] pb-4">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <Clock className="w-4 h-4 text-[#0070f3]" />
                  15-Minute Study Routine ({routineData?.date_str || "Today"})
                </h2>
                <p className="text-xs text-[#888888] mt-0.5">Daily micro-study tasks.</p>
              </div>
            </div>

            <div className="space-y-2.5">
              {(routineData?.tasks || []).map((task, idx) => (
                <div key={idx} className="bg-[#0a0a0a] border border-[#222222] border-l-2 border-l-[#0070f3] rounded-none p-3.5">
                  <h3 className="text-xs font-bold text-white">{task.title}</h3>
                  <p className="text-xs text-[#888888] mt-0.5">{task.details}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TOOL 3: Real SuperMemo SM-2 Flashcards */}
        {activeTool === "srs" && (
          <div className="space-y-5">
            <div className="flex items-center justify-between border-b border-[#222222] pb-4">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <BookOpen className="w-4 h-4 text-[#a855f7]" />
                  SRS Flashcards
                </h2>
                <p className="text-xs text-[#888888] mt-0.5">
                  {currentDeck && !isDeckCompleted
                    ? `Card ${flashcardIndex + 1} of ${currentDeck.cards.length}`
                    : currentDeck
                    ? `Deck Review Completed (${currentDeck.cards.length} Cards)`
                    : "Loading SRS Decks..."}
                </p>
              </div>

              {/* Deck Selector Pills */}
              <div className="flex items-center gap-1 bg-[#0a0a0a] border border-[#222222] p-1 rounded-none">
                {flashcardDecks.map((deck) => (
                  <button
                    key={deck.id}
                    onClick={() => {
                      setSelectedDeckId(deck.id);
                      setFlashcardIndex(0);
                      setFlashcardFlipped(false);
                    }}
                    className={`px-2.5 py-1 rounded-none text-xs transition-all ${
                      activeDeckId === deck.id
                        ? "bg-[#1f1f1f] text-white border border-[#333333]"
                        : "text-[#888888] hover:text-white"
                    }`}
                  >
                    {deck.title.split(" ")[0]}
                  </button>
                ))}
              </div>
            </div>

            {/* Active Card vs Deck Completed Screen */}
            {currentDeck && !isDeckCompleted && currentCard ? (
              <>
                <div
                  onClick={() => setFlashcardFlipped(!flashcardFlipped)}
                  className="bg-[#0a0a0a] border border-[#222222] hover:border-[#0070f3] rounded-none p-8 min-h-[200px] flex flex-col justify-center items-center text-center cursor-pointer transition-colors"
                >
                  <div className="text-[10px] font-mono text-[#0070f3] uppercase tracking-wider mb-2">
                    {flashcardFlipped ? "Answer" : "Question (Click to Flip)"}
                  </div>

                  {!flashcardFlipped ? (
                    <div className="text-base font-bold text-white">{currentCard.prompt}</div>
                  ) : (
                    <div className="space-y-2 max-w-xl">
                      <div className="text-sm font-semibold text-white whitespace-pre-line">
                        {currentCard.answer}
                      </div>
                      {currentCard.analogy && (
                        <div className="text-xs text-[#888888] bg-[#111111] p-2.5 rounded-none border border-[#222222]">
                          Analogy: {currentCard.analogy}
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {flashcardFlipped && (
                  <div className="flex justify-center gap-2">
                    {[0, 2, 4, 5].map((q) => (
                      <button
                        key={q}
                        onClick={() => handleNextFlashcard(q)}
                        className="btn-next-secondary text-xs px-3 py-1.5"
                      >
                        Rating {q} ({q === 5 ? "Easy" : q === 4 ? "Good" : q === 2 ? "Hard" : "Forgot"})
                      </button>
                    ))}
                  </div>
                )}
              </>
            ) : currentDeck ? (
              /* Deck Completed Screen */
              <div className="bg-[#0a0a0a] border border-[#222222] rounded-none p-6 text-center space-y-3">
                <div className="w-10 h-10 bg-[#111111] text-white rounded-none flex items-center justify-center mx-auto border border-[#333333]">
                  <CheckCircle className="w-5 h-5 text-[#0070f3]" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-white">
                    Deck Completed: {currentDeck.title}
                  </h3>
                  <p className="text-xs text-[#888888] mt-0.5">
                    Reviewed {currentDeck.cards.length} flashcards. SuperMemo SM-2 intervals updated.
                  </p>
                </div>

                <div className="flex justify-center gap-3 pt-1">
                  <button
                    onClick={() => {
                      setFlashcardIndex(0);
                      setFlashcardFlipped(false);
                    }}
                    className="btn-next-secondary text-xs px-3 py-1.5 flex items-center gap-1.5"
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                    <span>Review Again</span>
                  </button>
                </div>
              </div>
            ) : null}
          </div>
        )}

        {/* TOOL 4: Real Teaching Module & Syntax Gym */}
        {activeTool === "syntax" && (
          <div className="space-y-6">
            <div className="flex items-center justify-between border-b border-[#222222] pb-4">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <BookOpen className="w-4 h-4 text-[#0070f3]" />
                  {activeModuleData.title}
                </h2>
                <p className="text-xs text-[#888888] mt-0.5">Interactive Concept Lecture, Examples & Practice Questions</p>
              </div>
            </div>

            {/* 1. CONCEPT EXPLANATION & LECTURE */}
            <div className="bg-[#0a0a0a] border border-[#222222] border-l-4 border-l-[#0070f3] p-4 space-y-3 font-mono text-xs">
              <div className="flex items-center gap-2 text-[#0070f3] font-bold">
                <BookOpen className="w-4 h-4" />
                <span>1. CONCEPT EXPLANATION</span>
              </div>
              <p className="text-white leading-relaxed font-medium">
                {dynamicModule?.summary || "Variables are dynamic reference labels pointing to typed objects in memory."}
              </p>

              {dynamicModule?.non_cs_analogy && (
                <div className="bg-[#111111] border border-[#222222] p-3 text-xs text-[#e2e8f0] leading-relaxed">
                  💡 <span className="font-semibold text-white">Analogy:</span> {dynamicModule.non_cs_analogy}
                </div>
              )}

              {dynamicModule?.common_traps && (
                <div className="bg-[#f5a623]/10 border border-[#f5a623]/30 p-2.5 text-[#f5a623] text-xs">
                  ⚠️ <span className="font-bold">Common Trap:</span> {dynamicModule.common_traps}
                </div>
              )}
            </div>

            {/* 2. SEVERAL CODE EXAMPLES */}
            {dynamicModule?.code_examples && dynamicModule.code_examples.length > 0 && (
              <div className="space-y-3 font-mono text-xs">
                <div className="flex items-center gap-2 text-white font-bold">
                  <Code className="w-4 h-4 text-[#00e599]" />
                  <span>2. PRACTICAL CODE EXAMPLES</span>
                </div>

                <div className="grid grid-cols-1 gap-3">
                  {dynamicModule.code_examples.map((ex, idx) => (
                    <div key={idx} className="bg-[#0a0a0a] border border-[#222222] p-4 space-y-2.5">
                      <div className="flex items-center gap-2 font-bold text-white">
                        <span className="bg-[#00e599]/20 text-[#00e599] border border-[#00e599]/30 px-1.5 py-0.5 text-[10px]">
                          EXAMPLE {idx + 1}
                        </span>
                        <span>{ex.title}</span>
                      </div>

                      {/* Code Block */}
                      <pre className="bg-[#111111] border border-[#222222] p-3 text-xs font-mono text-[#00e599] overflow-x-auto whitespace-pre-wrap">
                        {ex.code}
                      </pre>

                      {/* Expected Output */}
                      <div className="bg-[#000000] border border-[#222222] p-2.5 text-[11px] font-mono text-[#a1a1a1]">
                        <span className="text-[#666666] uppercase text-[9px] block mb-0.5">Expected Output:</span>
                        <pre className="text-white whitespace-pre-wrap">{ex.output}</pre>
                      </div>

                      {/* Explanation */}
                      <p className="text-[#888888] leading-relaxed">{ex.explanation}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 3. PRACTICE QUESTIONS AFTER EACH TOPIC LECTURE */}
            {dynamicModule?.practice_questions && dynamicModule.practice_questions.length > 0 && (
              <div className="space-y-3 pt-2 font-mono text-xs">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-white font-bold">
                    <HelpCircle className="w-4 h-4 text-[#a855f7]" />
                    <span>3. TOPIC KNOWLEDGE CHECK & QUESTIONS</span>
                  </div>
                  <span className="text-[10px] text-[#888888]">
                    {dynamicModule.practice_questions.length} Questions
                  </span>
                </div>

                <div className="space-y-4">
                  {dynamicModule.practice_questions.map((q, qIdx) => (
                    <QuestionCard key={q.id || qIdx} question={q} index={qIdx} />
                  ))}
                </div>
              </div>
            )}

            {/* 4. HANDS-ON AST SYNTAX DRILL PLAYGROUND */}
            <div className="space-y-3 pt-2 font-mono text-xs">
              <div className="flex items-center gap-2 text-white font-bold">
                <Code className="w-4 h-4 text-[#0070f3]" />
                <span>4. HANDS-ON AST SYNTAX DRILL</span>
              </div>

              <div className="bg-[#0a0a0a] border border-[#222222] rounded-none p-4 space-y-3">
                <label className="text-xs text-[#888888] font-mono block">
                  Write Python implementation:
                </label>
                <textarea
                  key={selectedModule}
                  defaultValue={activeModuleData.code}
                  onChange={(e) => setSyntaxCode(e.target.value)}
                  rows={7}
                  className="w-full bg-[#111111] border border-[#2e2e2e] rounded-none p-3 text-xs font-mono text-white focus:outline-none focus:border-[#0070f3]"
                />

                <button
                  onClick={handleEvaluateSyntax}
                  disabled={syntaxEvaluating}
                  className="btn-next-primary text-xs px-3.5 py-1.5 flex items-center gap-2"
                >
                  {syntaxEvaluating ? (
                    <>
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      <span>Evaluating AST...</span>
                    </>
                  ) : (
                    <span>Evaluate AST & Syntax</span>
                  )}
                </button>

                {syntaxError && (
                  <div className="bg-[#7f1d1d]/30 border border-[#ef4444] p-3 rounded-none text-xs font-mono text-[#ef4444]">
                    ❌ {syntaxError}
                  </div>
                )}

                {syntaxFeedback && (
                  <div className="bg-[#111111] border border-[#2e2e2e] p-3 rounded-none text-xs font-mono text-[#e2e8f0] space-y-1">
                    <div className="font-bold text-white">
                      Score: {syntaxFeedback.score || 100}% | AST Valid: {syntaxFeedback.ast_valid ? "YES" : "NO"}
                    </div>
                    <div className="text-white">{syntaxFeedback.feedback}</div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* TOOL 5: Live Gemini 3.5 Flash Socratic AI Tutor */}
        {activeTool === "socratic" && (
          <div className="space-y-5">
            <div className="flex items-center justify-between border-b border-[#222222] pb-4">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-[#0070f3]" />
                  Gemini Socratic Tutor
                </h2>
                <p className="text-xs text-[#888888] mt-0.5">Interactive Python & CS concept guidance.</p>
              </div>
            </div>

            <div className="bg-[#0a0a0a] border border-[#222222] rounded-none p-4 space-y-3">
              <input
                type="text"
                value={aiQuery}
                onChange={(e) => setAiQuery(e.target.value)}
                placeholder="Ask any code or math question..."
                className="w-full bg-[#111111] border border-[#2e2e2e] rounded-none p-3 text-xs text-white focus:outline-none focus:border-[#0070f3]"
              />

              <button
                onClick={handleAskGemini}
                disabled={aiLoading}
                className="btn-next-primary text-xs px-3.5 py-1.5 flex items-center gap-2"
              >
                {aiLoading ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin text-black" />
                    <span>Consulting Gemini...</span>
                  </>
                ) : (
                  <span>Ask Gemini</span>
                )}
              </button>

              {aiError && (
                <div className="bg-[#7f1d1d]/30 border border-[#ef4444] p-3 rounded-none text-xs font-mono text-[#ef4444]">
                  ❌ {aiError}
                </div>
              )}

              {aiResponse && (
                <div className="bg-[#111111] border border-[#2e2e2e] p-3.5 rounded-none text-xs font-mono text-[#e2e8f0] space-y-2.5">
                  <div>
                    <span className="font-bold text-[#0070f3]">Analogy:</span>
                    <p className="text-[#e2e8f0] mt-0.5">{aiResponse.analogy}</p>
                  </div>
                  <div>
                    <span className="font-bold text-[#eab308]">Hint:</span>
                    <p className="text-[#e2e8f0] mt-0.5">{aiResponse.conceptual_hint}</p>
                  </div>
                  <div>
                    <span className="font-bold text-white">Guided Question:</span>
                    <p className="text-white mt-0.5">{aiResponse.socratic_question}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TOOL 6: Real Virtual ROS 2 Visualizer */}
        {activeTool === "ros2" && (
          <div className="space-y-5">
            <div className="flex items-center justify-between border-b border-[#222222] pb-4">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <Cpu className="w-4 h-4 text-[#3b82f6]" />
                  ROS 2 Visualizer
                </h2>
                <p className="text-xs text-[#888888] mt-0.5">Node graph & forward kinematics.</p>
              </div>
            </div>

            <div className="bg-[#0a0a0a] border border-[#222222] rounded-none p-4 font-mono text-xs text-[#e2e8f0] space-y-3">
              <div className="text-white font-bold">Node Graph:</div>
              <pre className="text-[#888888] bg-[#111111] p-2.5 rounded-none border border-[#222222] whitespace-pre-wrap">
                {ros2Data?.architecture || "Loading ROS 2 graph..."}
              </pre>

              <div className="border-t border-[#222222] pt-3 text-white font-bold">
                Topic Stream (`/joint_states`):
              </div>
              <div className="text-white bg-[#111111] p-2.5 rounded-none border border-[#222222]">
                {JSON.stringify(ros2Data?.topic_stream || [], null, 2)}
              </div>

              <div className="border-t border-[#222222] pt-3 text-white font-bold">
                Forward Kinematics:
              </div>
              <div className="bg-[#111111] p-2.5 rounded-none border border-[#222222]">
                {JSON.stringify(ros2Data?.kinematics || {}, null, 2)}
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
};
