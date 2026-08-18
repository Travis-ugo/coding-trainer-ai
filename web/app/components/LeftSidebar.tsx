"use client";

import React from "react";
import { Folder, FileCode, Cpu, Layers, Sparkles, BookOpen, Clock, ChevronRight } from "lucide-react";
import { useTrainerContext } from "../context/TrainerContext";

interface LeftSidebarProps {
  activeTool: string;
  setActiveTool: (tool: string) => void;
  selectedModule: string;
  setSelectedModule: (mod: string) => void;
}

export const LeftSidebar: React.FC<LeftSidebarProps> = ({
  activeTool,
  setActiveTool,
  selectedModule,
  setSelectedModule,
}) => {
  const { modulesData } = useTrainerContext();

  const modules = (modulesData || []).map((m) => ({
    id: m.id,
    title: m.title.includes(":") ? m.title.split(":")[1]?.trim() || m.title : m.title,
  }));

  return (
    <aside className="w-64 bg-[#0a0a0a] border-r border-[#222222] flex flex-col h-[calc(100vh-3.5rem)] shrink-0">
      {/* Dashboard Section Header */}
      <div className="px-4 py-3 border-b border-[#222222] text-xs font-semibold text-[#888888] uppercase tracking-wider flex items-center justify-between">
        <span>Workspace Navigation</span>
        <ChevronRight className="w-3.5 h-3.5 text-[#666666]" />
      </div>

      {/* Navigation Links */}
      <div className="flex-1 overflow-y-auto p-3 space-y-5 text-xs">
        {/* Core Dashboard Views */}
        <div>
          <div className="text-[10px] font-semibold text-[#666666] uppercase tracking-wider px-2 mb-2">
            Overview
          </div>
          <div className="space-y-1">
            <button
              onClick={() => setActiveTool("analytics")}
              className={`w-full text-left px-3 py-2 rounded-none flex items-center gap-2.5 transition-all ${
                activeTool === "analytics"
                  ? "bg-[#1f1f1f] text-white border border-[#333333] font-medium"
                  : "text-[#a1a1a1] hover:bg-[#111111] hover:text-white"
              }`}
            >
              <Layers className="w-4 h-4 text-[#0070f3]" />
              <span>Grade Heatmap</span>
            </button>

            <button
              onClick={() => setActiveTool("routine")}
              className={`w-full text-left px-3 py-2 rounded-none flex items-center gap-2.5 transition-all ${
                activeTool === "routine"
                  ? "bg-[#1f1f1f] text-white border border-[#333333] font-medium"
                  : "text-[#a1a1a1] hover:bg-[#111111] hover:text-white"
              }`}
            >
              <Clock className="w-4 h-4 text-[#00e599]" />
              <span>15-Min Power Session</span>
            </button>

            <button
              onClick={() => setActiveTool("srs")}
              className={`w-full text-left px-3 py-2 rounded-none flex items-center gap-2.5 transition-all ${
                activeTool === "srs"
                  ? "bg-[#1f1f1f] text-white border border-[#333333] font-medium"
                  : "text-[#a1a1a1] hover:bg-[#111111] hover:text-white"
              }`}
            >
              <BookOpen className="w-4 h-4 text-[#a855f7]" />
              <span>SuperMemo Flashcards</span>
            </button>

            <button
              onClick={() => setActiveTool("socratic")}
              className={`w-full text-left px-3 py-2 rounded-none flex items-center gap-2.5 transition-all ${
                activeTool === "socratic"
                  ? "bg-[#1f1f1f] text-white border border-[#333333] font-medium"
                  : "text-[#a1a1a1] hover:bg-[#111111] hover:text-white"
              }`}
            >
              <Sparkles className="w-4 h-4 text-[#00e599]" />
              <span>Gemini AI Socratic Tutor</span>
            </button>

            <button
              onClick={() => setActiveTool("ros2")}
              className={`w-full text-left px-3 py-2 rounded-none flex items-center gap-2.5 transition-all ${
                activeTool === "ros2"
                  ? "bg-[#1f1f1f] text-white border border-[#333333] font-medium"
                  : "text-[#a1a1a1] hover:bg-[#111111] hover:text-white"
              }`}
            >
              <Cpu className="w-4 h-4 text-[#3b82f6]" />
              <span>Virtual ROS 2 Visualizer</span>
            </button>
          </div>
        </div>

        {/* Python Curriculum Modules */}
        <div>
          <div className="text-[10px] font-semibold text-[#666666] uppercase tracking-wider px-2 mb-2 flex justify-between items-center">
            <span>Modules (M1 - M9)</span>
            <Folder className="w-3 h-3 text-[#666666]" />
          </div>
          <div className="space-y-1">
            {modules.map((m) => (
              <button
                key={m.id}
                onClick={() => {
                  setSelectedModule(m.id);
                  setActiveTool("syntax");
                }}
                className={`w-full text-left px-3 py-1.5 rounded-none flex items-center justify-between text-xs transition-all ${
                  selectedModule === m.id && activeTool === "syntax"
                    ? "bg-[#1f1f1f] text-white border border-[#333333] font-medium"
                    : "text-[#888888] hover:bg-[#111111] hover:text-white"
                }`}
              >
                <div className="flex items-center gap-2 truncate">
                  <FileCode className="w-3.5 h-3.5 shrink-0 text-[#0070f3]" />
                  <span className="truncate">{m.title}</span>
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </aside>
  );
};
