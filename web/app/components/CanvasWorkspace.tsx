"use client";

import React, { useState } from "react";
import { useTrainerContext, SyntaxEvalResult, GeminiResponse } from "../context/TrainerContext";
import { Sparkles, Code, Cpu, Layers, BookOpen, Clock, CheckCircle, RotateCcw, Loader2 } from "lucide-react";

interface CanvasWorkspaceProps {
  activeTool: string;
  selectedModule: string;
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
          <div className="bg-[#7f1d1d]/30 border border-[#ef4444] text-[#ef4444] p-3.5 rounded-md text-xs font-mono">
            ⚠️ {error}
          </div>
        )}

        {/* TOOL 1: Real Grade Analytics Dashboard */}
        {activeTool === "analytics" && (
          <div className="space-y-5">
            <div className="flex items-center justify-between border-b border-[#222222] pb-4">
              <div>
                <h2 className="text-xl font-bold text-white flex items-center gap-2.5">
                  <Layers className="w-5 h-5 text-[#0070f3]" />
                  Master&apos;s Grade Readiness Heatmap
                </h2>
                <p className="text-xs text-[#888888] mt-1">
                  Topic-by-topic percentage breakdown computed by Python Grade Analytics Engine
                </p>
              </div>
              <div className="bg-[#111111] border border-[#00e599]/30 text-[#00e599] font-bold text-xs px-3.5 py-1.5 rounded-md">
                {analyticsData?.predicted_grade || (loading ? "Syncing..." : "--")}
              </div>
            </div>

            <div className="bg-[#0a0a0a] border border-[#222222] rounded-lg p-6 space-y-4">
              {analyticsData?.topic_grades && analyticsData.topic_grades.length > 0 ? (
                analyticsData.topic_grades.map((item, idx) => (
                  <div key={idx} className="space-y-1.5">
                    <div className="flex justify-between text-xs">
                      <span className="text-[#e2e8f0] font-medium">{item.topic_name}</span>
                      <span style={{ color: item.color_hex }} className="font-semibold font-mono">
                        {item.score_percentage}% ({item.grade_label})
                      </span>
                    </div>
                    <div className="w-full bg-[#111111] h-2 rounded-full overflow-hidden border border-[#222222]">
                      <div
                        className="h-full rounded-full transition-all duration-300"
                        style={{ width: `${item.score_percentage}%`, backgroundColor: item.color_hex }}
                      />
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-xs text-[#888888] text-center py-6">
                  {loading ? "Loading analytics..." : "No analytics data available"}
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
                <h2 className="text-xl font-bold text-white flex items-center gap-2.5">
                  <Clock className="w-5 h-5 text-[#00e599]" />
                  Daily 15-Minute Micro-Study Power Session ({routineData?.date_str || "Today"})
                </h2>
                <p className="text-xs text-[#888888] mt-1">Structured 3-task daily routine generated by DailyRoutineGenerator</p>
              </div>
            </div>

            <div className="space-y-3">
              {(routineData?.tasks || []).map((task, idx) => (
                <div key={idx} className="bg-[#0a0a0a] border border-[#222222] border-l-4 border-l-[#00e599] rounded-r-md p-4">
                  <h3 className="text-sm font-bold text-white">{task.title}</h3>
                  <p className="text-xs text-[#888888] mt-1">{task.details}</p>
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
                <h2 className="text-xl font-bold text-white flex items-center gap-2.5">
                  <BookOpen className="w-5 h-5 text-[#a855f7]" />
                  SuperMemo SM-2 SRS Flashcards
                </h2>
                <p className="text-xs text-[#888888] mt-1">
                  {currentDeck && !isDeckCompleted
                    ? `Card ${flashcardIndex + 1} of ${currentDeck.cards.length}`
                    : currentDeck
                    ? `Deck Review Completed! (${currentDeck.cards.length} of ${currentDeck.cards.length} Cards)`
                    : "Loading SRS Decks..."}
                </p>
              </div>

              {/* Deck Selector Pills */}
              <div className="flex items-center gap-1.5 bg-[#0a0a0a] border border-[#222222] p-1 rounded-md">
                {flashcardDecks.map((deck) => (
                  <button
                    key={deck.id}
                    onClick={() => {
                      setSelectedDeckId(deck.id);
                      setFlashcardIndex(0);
                      setFlashcardFlipped(false);
                    }}
                    className={`px-3 py-1 rounded text-xs font-medium transition-all ${
                      activeDeckId === deck.id
                        ? "bg-[#1f1f1f] text-white border border-[#333333]"
                        : "text-[#888888] hover:text-white"
                    }`}
                  >
                    {deck.title.split(" ")[0]} Deck
                  </button>
                ))}
              </div>
            </div>

            {/* Active Card vs Deck Completed Screen */}
            {currentDeck && !isDeckCompleted && currentCard ? (
              <>
                <div
                  onClick={() => setFlashcardFlipped(!flashcardFlipped)}
                  className="bg-[#0a0a0a] border border-[#222222] hover:border-[#0070f3] rounded-lg p-10 min-h-[240px] flex flex-col justify-center items-center text-center cursor-pointer transition-colors"
                >
                  <div className="text-xs font-semibold text-[#0070f3] uppercase tracking-wider mb-3">
                    {flashcardFlipped ? "Answer / Back" : "Question / Front (Click to Flip)"}
                  </div>

                  {!flashcardFlipped ? (
                    <div className="text-lg font-bold text-white">{currentCard.prompt}</div>
                  ) : (
                    <div className="space-y-3 max-w-xl">
                      <div className="text-base font-semibold text-[#00e599] whitespace-pre-line">
                        {currentCard.answer}
                      </div>
                      {currentCard.analogy && (
                        <div className="text-xs text-[#888888] bg-[#111111] p-3 rounded-md border border-[#222222]">
                          🏛️ Analogy: {currentCard.analogy}
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {flashcardFlipped && (
                  <div className="flex justify-center gap-2.5">
                    {[0, 2, 4, 5].map((q) => (
                      <button
                        key={q}
                        onClick={() => handleNextFlashcard(q)}
                        className="btn-next-secondary text-xs px-4 py-2"
                      >
                        Rating {q} ({q === 5 ? "Perfect" : q === 4 ? "Good" : q === 2 ? "Hard" : "Forgot"})
                      </button>
                    ))}
                  </div>
                )}
              </>
            ) : currentDeck ? (
              /* Deck Completed Screen */
              <div className="bg-[#0a0a0a] border border-[#222222] rounded-lg p-8 text-center space-y-4">
                <div className="w-12 h-12 bg-[#00e599]/15 text-[#00e599] rounded-full flex items-center justify-center mx-auto border border-[#00e599]/30">
                  <CheckCircle className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white">
                    🎉 Deck Mastered: {currentDeck.title}!
                  </h3>
                  <p className="text-xs text-[#888888] mt-1">
                    You reviewed all {currentDeck.cards.length} flashcards in this deck. SuperMemo SM-2 intervals updated in backend.
                  </p>
                </div>

                <div className="flex justify-center gap-3 pt-2">
                  <button
                    onClick={() => {
                      setFlashcardIndex(0);
                      setFlashcardFlipped(false);
                    }}
                    className="btn-next-secondary text-xs px-4 py-2 flex items-center gap-1.5"
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                    <span>Review Again</span>
                  </button>
                </div>
              </div>
            ) : null}
          </div>
        )}

        {/* TOOL 4: Real Anti-Copilot Syntax Gym */}
        {activeTool === "syntax" && (
          <div className="space-y-5">
            <div className="flex items-center justify-between border-b border-[#222222] pb-4">
              <div>
                <h2 className="text-xl font-bold text-white flex items-center gap-2.5">
                  <Code className="w-5 h-5 text-[#0070f3]" />
                  {activeModuleData.title}
                </h2>
                <p className="text-xs text-[#888888] mt-1">Anti-Copilot Syntax Gym — Evaluated by Python NoCompilerExamMode AST Sandbox</p>
              </div>
            </div>

            <div className="bg-[#0a0a0a] border border-[#222222] rounded-lg p-5 space-y-4">
              <label className="text-xs text-[#888888] font-medium block">
                Type out the Python implementation for {activeModuleData.title} from memory:
              </label>
              <textarea
                key={selectedModule}
                defaultValue={activeModuleData.code}
                onChange={(e) => setSyntaxCode(e.target.value)}
                rows={8}
                className="w-full bg-[#111111] border border-[#2e2e2e] rounded-md p-3.5 text-xs font-mono text-white focus:outline-none focus:border-[#0070f3]"
              />

              <button
                onClick={handleEvaluateSyntax}
                disabled={syntaxEvaluating}
                className="btn-next-primary text-xs px-4 py-2 flex items-center gap-2"
              >
                {syntaxEvaluating ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    <span>Evaluating AST...</span>
                  </>
                ) : (
                  <span>Check Code AST & Execution</span>
                )}
              </button>

              {syntaxError && (
                <div className="bg-[#7f1d1d]/30 border border-[#ef4444] p-3.5 rounded-md text-xs font-mono text-[#ef4444]">
                  ❌ {syntaxError}
                </div>
              )}

              {syntaxFeedback && (
                <div className="bg-[#111111] border border-[#2e2e2e] p-3.5 rounded-md text-xs font-mono text-[#e2e8f0] space-y-1">
                  <div className="font-bold text-white">
                    Score: {syntaxFeedback.score || 100}% | AST Valid: {syntaxFeedback.ast_valid ? "YES" : "NO"}
                  </div>
                  <div className="text-[#00e599]">{syntaxFeedback.feedback}</div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TOOL 5: Live Gemini 3.5 Flash Socratic AI Tutor */}
        {activeTool === "socratic" && (
          <div className="space-y-5">
            <div className="flex items-center justify-between border-b border-[#222222] pb-4">
              <div>
                <h2 className="text-xl font-bold text-white flex items-center gap-2.5">
                  <Sparkles className="w-5 h-5 text-[#00e599]" />
                  Live Gemini 3.5 Flash Socratic AI Tutor
                </h2>
                <p className="text-xs text-[#888888] mt-1">Direct REST API connection to Google Gemini 3.5 Flash model</p>
              </div>
            </div>

            <div className="bg-[#0a0a0a] border border-[#222222] rounded-lg p-5 space-y-4">
              <input
                type="text"
                value={aiQuery}
                onChange={(e) => setAiQuery(e.target.value)}
                placeholder="Ask any code or math question (e.g. How do Kalman Filters balance sensor noise?)..."
                className="w-full bg-[#111111] border border-[#2e2e2e] rounded-md p-3.5 text-xs text-white focus:outline-none focus:border-[#00e599]"
              />

              <button
                onClick={handleAskGemini}
                disabled={aiLoading}
                className="btn-next-primary text-xs px-4 py-2 flex items-center gap-2"
              >
                {aiLoading ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin text-black" />
                    <span>Consulting Gemini 3.5...</span>
                  </>
                ) : (
                  <span>Ask Gemini Socratic AI</span>
                )}
              </button>

              {aiError && (
                <div className="bg-[#7f1d1d]/30 border border-[#ef4444] p-3.5 rounded-md text-xs font-mono text-[#ef4444]">
                  ❌ {aiError}
                </div>
              )}

              {aiResponse && (
                <div className="bg-[#111111] border border-[#2e2e2e] p-4 rounded-md text-xs font-mono text-[#e2e8f0] space-y-3">
                  <div>
                    <span className="font-bold text-[#0070f3]">🏛️ Intuitive Analogy:</span>
                    <p className="text-[#e2e8f0] mt-0.5">{aiResponse.analogy}</p>
                  </div>
                  <div>
                    <span className="font-bold text-[#eab308]">💡 Conceptual Hint:</span>
                    <p className="text-[#e2e8f0] mt-0.5">{aiResponse.conceptual_hint}</p>
                  </div>
                  <div>
                    <span className="font-bold text-[#00e599]">❓ Socratic Guided Question:</span>
                    <p className="text-[#00e599] mt-0.5">{aiResponse.socratic_question}</p>
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
                <h2 className="text-xl font-bold text-white flex items-center gap-2.5">
                  <Cpu className="w-5 h-5 text-[#3b82f6]" />
                  Virtual ROS 2 Node Architecture Visualizer
                </h2>
                <p className="text-xs text-[#888888] mt-1">Live Node graphs & Forward Kinematics computed by VirtualROS2Sandbox</p>
              </div>
            </div>

            <div className="bg-[#0a0a0a] border border-[#222222] rounded-lg p-5 font-mono text-xs text-[#e2e8f0] space-y-4">
              <div className="text-white font-bold">Active ROS 2 Node Graph:</div>
              <pre className="text-[#888888] bg-[#111111] p-3 rounded border border-[#222222] whitespace-pre-wrap">
                {ros2Data?.architecture || "Loading ROS 2 node graph..."}
              </pre>

              <div className="border-t border-[#222222] pt-4 text-white font-bold">
                Stream (`ros2 topic echo /joint_states`):
              </div>
              <div className="text-[#00e599] bg-[#111111] p-3 rounded border border-[#222222]">
                {JSON.stringify(ros2Data?.topic_stream || [], null, 2)}
              </div>

              <div className="border-t border-[#222222] pt-4 text-white font-bold">
                2-DOF Robot Arm Forward Kinematics Calculation:
              </div>
              <div className="bg-[#111111] p-3 rounded border border-[#222222]">
                {JSON.stringify(ros2Data?.kinematics || {}, null, 2)}
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
};
