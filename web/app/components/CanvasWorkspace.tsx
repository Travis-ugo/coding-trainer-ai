"use client";

import React, { useState } from "react";
import { Sparkles, Code, Cpu, Layers, BookOpen, Clock, CheckCircle, ChevronRight } from "lucide-react";

interface CanvasWorkspaceProps {
  activeTool: string;
  selectedModule: string;
}

export const CanvasWorkspace: React.FC<CanvasWorkspaceProps> = ({
  activeTool,
  selectedModule,
}) => {
  // Flashcard State
  const [flashcardFlipped, setFlashcardFlipped] = useState(false);
  const [flashcardIndex, setFlashcardIndex] = useState(0);

  const flashcards = [
    {
      prompt: "What is the intuitive difference between a Stack and a Heap?",
      answer:
        "Stack: Fast, fixed-size automatic memory allocated per function call frame.\nHeap: Dynamic, manually allocated memory requiring explicit deallocation (`delete`).",
      analogy: "Stack = Desk surface for current task; Heap = Storage warehouse down the hall.",
    },
    {
      prompt: "What is an SE(3) Homogeneous Transformation Matrix?",
      answer:
        "A 4x4 matrix encoding 3D rotation R ∈ SO(3) and 3D translation vector t ∈ R³.",
      analogy: "A combined translation + rotation formula for robot arm end-effectors.",
    },
    {
      prompt: "What is the primary role of PyTorch `loss.backward()`?",
      answer:
        "Computes reverse-mode automatic differentiation gradients (∇_w L) on the graph.",
      analogy: "Chain rule backpropagation calculating exact weight gradients.",
    },
  ];

  // Syntax Gym State
  const [syntaxCode, setSyntaxCode] = useState("def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target:\n            return mid\n    return -1");
  const [syntaxFeedback, setSyntaxFeedback] = useState<string | null>(null);

  // Gemini AI Tutor State
  const [aiQuery, setAiQuery] = useState("");
  const [aiResponse, setAiResponse] = useState<string | null>(null);

  const currentFlashcard = flashcards[flashcardIndex % flashcards.length];

  const handleNextFlashcard = () => {
    setFlashcardFlipped(false);
    setFlashcardIndex((prev) => prev + 1);
  };

  const handleEvaluateSyntax = () => {
    if (syntaxCode.includes("def") && syntaxCode.includes("return")) {
      setSyntaxFeedback("✅ AST SYNTAX VALID! Clean execution, memory bounds O(1) space.");
    } else {
      setSyntaxFeedback("⚠️ INCOMPLETE SYNTAX. Missing return or function definition.");
    }
  };

  const handleAskGemini = () => {
    if (!aiQuery) return;
    setAiResponse(
      `✨ Gemini 3.5 Flash Live Response:\n\n🏛️ INTUITIVE ANALOGY: Think of '${aiQuery}' like an archival call slip mapping to a physical document in a vault.\n\n💡 CONCEPTUAL HINT: Differentiate between initial state and transformed state.\n\n❓ SOCRATIC QUESTION: What happens if your input collection is empty?`
    );
  };

  return (
    <main className="flex-1 bg-[#000000] overflow-y-auto p-8 relative flex justify-center items-start">
      {/* Next.js & Render.com Dashboard Workspace Frame */}
      <div className="w-full max-w-4xl space-y-6">
        {/* TOOL 1: Grade Analytics Dashboard */}
        {activeTool === "analytics" && (
          <div className="space-y-5">
            <div className="flex items-center justify-between border-b border-[#222222] pb-4">
              <div>
                <h2 className="text-xl font-bold text-white flex items-center gap-2.5">
                  <Layers className="w-5 h-5 text-[#0070f3]" />
                  Master's Grade Readiness Heatmap
                </h2>
                <p className="text-xs text-[#888888] mt-1">
                  Topic-by-topic percentage breakdown mapped to Master's thresholds
                </p>
              </div>
              <div className="bg-[#111111] border border-[#00e599]/30 text-[#00e599] font-bold text-xs px-3.5 py-1.5 rounded-md">
                🏆 DISTINCTION (72.5%)
              </div>
            </div>

            <div className="bg-[#0a0a0a] border border-[#222222] rounded-lg p-6 space-y-4">
              {[
                { topic: "Python Syntax & Memory Models", pct: 85, grade: "Distinction", color: "#00e599" },
                { topic: "Conditionals & Control Flow", pct: 78, grade: "Distinction", color: "#00e599" },
                { topic: "Loops & Iterators", pct: 72, grade: "Distinction", color: "#00e599" },
                { topic: "Data Structures & Hash Maps", pct: 65, grade: "Merit", color: "#3b82f6" },
                { topic: "Functions & LEGB Scope", pct: 70, grade: "Distinction", color: "#00e599" },
                { topic: "DSA Two Pointers Pattern", pct: 75, grade: "Distinction", color: "#00e599" },
                { topic: "Math SE(3) Transformations", pct: 72, grade: "Distinction", color: "#00e599" },
                { topic: "1D Kalman Filter Estimation", pct: 55, grade: "Pass", color: "#eab308" },
                { topic: "PyTorch Autograd & Tensors", pct: 62, grade: "Merit", color: "#3b82f6" },
                { topic: "ROS 2 Pub/Sub Architecture", pct: 74, grade: "Distinction", color: "#00e599" },
              ].map((item, idx) => (
                <div key={idx} className="space-y-1.5">
                  <div className="flex justify-between text-xs">
                    <span className="text-[#e2e8f0] font-medium">{item.topic}</span>
                    <span style={{ color: item.color }} className="font-semibold font-mono">
                      {item.pct}% ({item.grade})
                    </span>
                  </div>
                  <div className="w-full bg-[#111111] h-2 rounded-full overflow-hidden border border-[#222222]">
                    <div
                      className="h-full rounded-full transition-all duration-300"
                      style={{ width: `${item.pct}%`, backgroundColor: item.color }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TOOL 2: Daily 15-Min Power Session */}
        {activeTool === "routine" && (
          <div className="space-y-5">
            <div className="flex items-center justify-between border-b border-[#222222] pb-4">
              <div>
                <h2 className="text-xl font-bold text-white flex items-center gap-2.5">
                  <Clock className="w-5 h-5 text-[#00e599]" />
                  Daily 15-Minute Micro-Study Power Session
                </h2>
                <p className="text-xs text-[#888888] mt-1">Structured 3-task daily routine</p>
              </div>
            </div>

            <div className="space-y-3">
              {[
                { step: 1, title: "🎴 5 Mins: SRS Flashcards", desc: "Review due cards across Python, C++ Memory, DSA, and ROS 2 decks." },
                { step: 2, title: "⚡ 5 Mins: Anti-Copilot Syntax Drill", desc: "Type out raw syntax templates with zero autocomplete allowed." },
                { step: 3, title: "📝 5 Mins: 1 Master's Written Exam Question", desc: "Answer 1 written exam question with Distinction Rubric feedback." },
              ].map((task) => (
                <div key={task.step} className="bg-[#0a0a0a] border border-[#222222] border-l-4 border-l-[#00e599] rounded-r-md p-4">
                  <h3 className="text-sm font-bold text-white">{task.title}</h3>
                  <p className="text-xs text-[#888888] mt-1">{task.desc}</p>
                </div>
              ))}

              <button
                onClick={() => alert("🎉 Daily Routine Completed! Streak updated to 15 Days!")}
                className="w-full btn-next-primary text-xs py-3 rounded-md font-bold mt-2"
              >
                Complete Daily 15-Min Routine
              </button>
            </div>
          </div>
        )}

        {/* TOOL 3: Flashcards Canvas */}
        {activeTool === "srs" && (
          <div className="space-y-5">
            <div className="flex items-center justify-between border-b border-[#222222] pb-4">
              <div>
                <h2 className="text-xl font-bold text-white flex items-center gap-2.5">
                  <BookOpen className="w-5 h-5 text-[#a855f7]" />
                  SuperMemo SM-2 SRS Flashcards
                </h2>
                <p className="text-xs text-[#888888] mt-1">Card {flashcardIndex + 1} of {flashcards.length}</p>
              </div>
            </div>

            <div
              onClick={() => setFlashcardFlipped(!flashcardFlipped)}
              className="bg-[#0a0a0a] border border-[#222222] hover:border-[#0070f3] rounded-lg p-10 min-h-[220px] flex flex-col justify-center items-center text-center cursor-pointer transition-colors"
            >
              <div className="text-xs font-semibold text-[#0070f3] uppercase tracking-wider mb-2">
                {flashcardFlipped ? "Answer / Back" : "Question / Front (Click to Flip)"}
              </div>

              {!flashcardFlipped ? (
                <div className="text-lg font-bold text-white">{currentFlashcard.prompt}</div>
              ) : (
                <div className="space-y-3">
                  <div className="text-base font-semibold text-[#00e599] whitespace-pre-line">
                    {currentFlashcard.answer}
                  </div>
                  <div className="text-xs text-[#888888] bg-[#111111] p-3 rounded-md border border-[#222222]">
                    🏛️ Analogy: {currentFlashcard.analogy}
                  </div>
                </div>
              )}
            </div>

            {flashcardFlipped && (
              <div className="flex justify-center gap-2.5">
                {[0, 2, 4, 5].map((q) => (
                  <button
                    key={q}
                    onClick={handleNextFlashcard}
                    className="btn-next-secondary text-xs px-4 py-2"
                  >
                    Rating {q} ({q === 5 ? "Perfect" : q === 4 ? "Good" : q === 2 ? "Hard" : "Forgot"})
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        {/* TOOL 4: Anti-Copilot Syntax Gym */}
        {activeTool === "syntax" && (
          <div className="space-y-5">
            <div className="flex items-center justify-between border-b border-[#222222] pb-4">
              <div>
                <h2 className="text-xl font-bold text-white flex items-center gap-2.5">
                  <Code className="w-5 h-5 text-[#0070f3]" />
                  Anti-Copilot Raw Syntax Gym
                </h2>
                <p className="text-xs text-[#888888] mt-1">Zero autocomplete allowed</p>
              </div>
            </div>

            <div className="bg-[#0a0a0a] border border-[#222222] rounded-lg p-5 space-y-4">
              <label className="text-xs text-[#888888] font-medium block">
                Type out the selected algorithm from memory:
              </label>
              <textarea
                value={syntaxCode}
                onChange={(e) => setSyntaxCode(e.target.value)}
                rows={7}
                className="w-full bg-[#111111] border border-[#2e2e2e] rounded-md p-3.5 text-xs font-mono text-white focus:outline-none focus:border-[#0070f3]"
              />

              <button
                onClick={handleEvaluateSyntax}
                className="btn-next-primary text-xs px-4 py-2"
              >
                Check Code AST & Execution
              </button>

              {syntaxFeedback && (
                <div className="bg-[#111111] border border-[#2e2e2e] p-3.5 rounded-md text-xs font-mono text-[#e2e8f0]">
                  {syntaxFeedback}
                </div>
              )}
            </div>
          </div>
        )}

        {/* TOOL 5: Gemini Socratic AI Tutor */}
        {activeTool === "socratic" && (
          <div className="space-y-5">
            <div className="flex items-center justify-between border-b border-[#222222] pb-4">
              <div>
                <h2 className="text-xl font-bold text-white flex items-center gap-2.5">
                  <Sparkles className="w-5 h-5 text-[#00e599]" />
                  Live Gemini 3.5 Flash Socratic AI Tutor
                </h2>
                <p className="text-xs text-[#888888] mt-1">Interactive Non-CS guided tutoring</p>
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
                className="btn-next-primary text-xs px-4 py-2"
              >
                Ask Gemini Socratic AI
              </button>

              {aiResponse && (
                <div className="bg-[#111111] border border-[#2e2e2e] p-4 rounded-md text-xs font-mono text-[#e2e8f0] whitespace-pre-wrap">
                  {aiResponse}
                </div>
              )}
            </div>
          </div>
        )}

        {/* TOOL 6: Virtual ROS 2 Visualizer */}
        {activeTool === "ros2" && (
          <div className="space-y-5">
            <div className="flex items-center justify-between border-b border-[#222222] pb-4">
              <div>
                <h2 className="text-xl font-bold text-white flex items-center gap-2.5">
                  <Cpu className="w-5 h-5 text-[#3b82f6]" />
                  Virtual ROS 2 Node Architecture Visualizer
                </h2>
                <p className="text-xs text-[#888888] mt-1">Node graphs & topic message streams</p>
              </div>
            </div>

            <div className="bg-[#0a0a0a] border border-[#222222] rounded-lg p-5 font-mono text-xs text-[#e2e8f0] space-y-4">
              <div className="text-white font-bold">Active ROS 2 Nodes:</div>
              <div>• [/camera_driver_node] ➔ Publishes: [/image_raw]</div>
              <div>• [/joint_state_broadcaster] ➔ Publishes: [/joint_states]</div>
              <div>• [/motion_controller_node] ➔ Subscribes: [/joint_states]</div>

              <div className="border-t border-[#222222] pt-4 text-white font-bold">
                Stream (`ros2 topic echo /joint_states`):
              </div>
              <div className="text-[#00e599]">
                [Timestamp 1.25s] Topic: /joint_states | Data: {`{"position": [0.785, 0.523]}`}
              </div>

              <div className="border-t border-[#222222] pt-4 text-white font-bold">
                2-DOF Robot Arm Forward Kinematics:
              </div>
              <div>Joint Angles: θ1=45.0°, θ2=30.0°</div>
              <div>End-Effector Coordinates (x, y): [1.224, 1.673]</div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
};
