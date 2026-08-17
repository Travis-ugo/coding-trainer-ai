"use client";

import React from "react";
import { MousePointer, Layout, Code, Bot, Sparkles, Layers } from "lucide-react";

interface TopToolbarProps {
  activeTool: string;
  setActiveTool: (tool: string) => void;
  aiActive: boolean;
}

export const TopToolbar: React.FC<TopToolbarProps> = ({
  activeTool,
  setActiveTool,
  aiActive,
}) => {
  return (
    <header className="h-14 bg-[#000000] border-b border-[#222222] px-5 flex items-center justify-between select-none shrink-0">
      {/* Left App Logo & Render Dashboard Breadcrumbs */}
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-white text-black font-bold rounded flex items-center justify-center text-xs tracking-tighter">
          ▲
        </div>
        <div className="flex items-center gap-2 text-xs">
          <span className="font-bold text-white">
            coding-trainer-ai
          </span>
          <span className="text-[#666666]">/</span>
          <span className="text-[#a1a1a1]">master-studio</span>
          <span className="bg-[#111111] border border-[#2e2e2e] text-[#00e599] text-[10px] font-mono px-2 py-0.5 rounded">
            v2.5 production
          </span>
        </div>
      </div>

      {/* Center Next.js Box Rectangle Button Navigation Bar */}
      <div className="flex items-center bg-[#0a0a0a] border border-[#222222] rounded-md p-1 gap-1">
        <button
          onClick={() => setActiveTool("analytics")}
          className={`px-3 py-1.5 rounded-md text-xs font-medium flex items-center gap-1.5 transition-all ${
            activeTool === "analytics"
              ? "bg-[#1f1f1f] text-white border border-[#333333]"
              : "text-[#888888] hover:text-white"
          }`}
        >
          <MousePointer className="w-3.5 h-3.5" />
          <span>Analytics</span>
        </button>

        <button
          onClick={() => setActiveTool("routine")}
          className={`px-3 py-1.5 rounded-md text-xs font-medium flex items-center gap-1.5 transition-all ${
            activeTool === "routine"
              ? "bg-[#1f1f1f] text-white border border-[#333333]"
              : "text-[#888888] hover:text-white"
          }`}
        >
          <Layout className="w-3.5 h-3.5" />
          <span>Routine</span>
        </button>

        <button
          onClick={() => setActiveTool("srs")}
          className={`px-3 py-1.5 rounded-md text-xs font-medium flex items-center gap-1.5 transition-all ${
            activeTool === "srs"
              ? "bg-[#1f1f1f] text-white border border-[#333333]"
              : "text-[#888888] hover:text-white"
          }`}
        >
          <Layers className="w-3.5 h-3.5" />
          <span>Flashcards</span>
        </button>

        <button
          onClick={() => setActiveTool("syntax")}
          className={`px-3 py-1.5 rounded-md text-xs font-medium flex items-center gap-1.5 transition-all ${
            activeTool === "syntax"
              ? "bg-[#1f1f1f] text-white border border-[#333333]"
              : "text-[#888888] hover:text-white"
          }`}
        >
          <Code className="w-3.5 h-3.5" />
          <span>Syntax Gym</span>
        </button>

        <button
          onClick={() => setActiveTool("socratic")}
          className={`px-3 py-1.5 rounded-md text-xs font-medium flex items-center gap-1.5 transition-all ${
            activeTool === "socratic"
              ? "bg-[#1f1f1f] text-white border border-[#333333]"
              : "text-[#888888] hover:text-white"
          }`}
        >
          <Bot className="w-3.5 h-3.5" />
          <span>AI Tutor</span>
        </button>
      </div>

      {/* Right Actions Status Badge */}
      <div className="flex items-center gap-3">
        {aiActive ? (
          <div className="flex items-center gap-1.5 bg-[#00e599]/10 text-[#00e599] border border-[#00e599]/30 px-2.5 py-1 rounded-md text-xs font-medium">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Gemini 3.5 Active</span>
          </div>
        ) : (
          <div className="text-xs text-[#888888] bg-[#111111] border border-[#222222] px-2.5 py-1 rounded-md">
            Offline Mode
          </div>
        )}
      </div>
    </header>
  );
};
