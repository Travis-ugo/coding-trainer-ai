"use client";

import React, { useState } from "react";
import Link from "next/link";
import { MousePointer, Layout, Code, Bot, Sparkles, Layers, User as UserIcon, LogOut, ShieldCheck, Activity } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { ActivityLogModal } from "./ActivityLogModal";

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
  const { user, signOutUser } = useAuth();
  const [showMonitor, setShowMonitor] = useState(false);

  return (
    <header className="h-14 bg-[#000000] border-b border-[#222222] px-5 flex items-center justify-between shrink-0">
      {/* Left App Logo & Breadcrumbs */}
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-white text-black font-bold rounded-none flex items-center justify-center text-xs tracking-tighter">
          ▲
        </div>
        <div className="flex items-center gap-2 text-xs">
          <span className="font-bold text-white">
            coding-trainer-ai
          </span>
          <span className="text-[#666666]">/</span>
          <span className="text-[#a1a1a1]">master-studio</span>
          <span className="bg-[#111111] border border-[#2e2e2e] text-[#a1a1a1] text-[10px] font-mono px-2 py-0.5 rounded-none">
            v2.5 production
          </span>
        </div>
      </div>

      {/* Center Box Rectangle Button Navigation Bar */}
      <div className="flex items-center bg-[#0a0a0a] border border-[#222222] rounded-none p-1 gap-1">
        <button
          onClick={() => setActiveTool("analytics")}
          className={`px-3 py-1.5 rounded-none text-xs font-medium flex items-center gap-1.5 transition-all ${
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
          className={`px-3 py-1.5 rounded-none text-xs font-medium flex items-center gap-1.5 transition-all ${
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
          className={`px-3 py-1.5 rounded-none text-xs font-medium flex items-center gap-1.5 transition-all ${
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
          className={`px-3 py-1.5 rounded-none text-xs font-medium flex items-center gap-1.5 transition-all ${
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
          className={`px-3 py-1.5 rounded-none text-xs font-medium flex items-center gap-1.5 transition-all ${
            activeTool === "socratic"
              ? "bg-[#1f1f1f] text-white border border-[#333333]"
              : "text-[#888888] hover:text-white"
          }`}
        >
          <Bot className="w-3.5 h-3.5" />
          <span>AI Tutor</span>
        </button>
      </div>

      {/* Right Actions & User Identity Link to Dedicated Auth Screen */}
      <div className="flex items-center gap-3">
        {/* Live Activity & Session Monitor Toggle Button */}
        <button
          onClick={() => setShowMonitor(true)}
          className="flex items-center gap-1.5 bg-[#00e599]/10 hover:bg-[#00e599]/20 border border-[#00e599]/40 text-[#00e599] px-2.5 py-1.5 rounded-none text-xs font-mono font-medium transition-all"
        >
          <span className="w-2 h-2 rounded-full bg-[#00e599] animate-pulse" />
          <Activity className="w-3.5 h-3.5" />
          <span>Live Monitor</span>
        </button>

        {aiActive && (
          <div className="hidden sm:flex items-center gap-1.5 bg-[#111111] text-white border border-[#333333] px-2.5 py-1 rounded-none text-xs font-medium">
            <Sparkles className="w-3.5 h-3.5 text-[#0070f3]" />
            <span>Gemini 3.5 Active</span>
          </div>
        )}

        {/* Dedicated Auth Page Direct Link */}
        <Link
          href="/auth"
          className="flex items-center gap-2 bg-[#111111] hover:bg-[#1f1f1f] border border-[#2e2e2e] hover:border-[#444444] text-white px-3 py-1.5 rounded-none text-xs font-medium transition-all"
        >
          {user?.photoURL ? (
            <img src={user.photoURL} alt="Avatar" className="w-4 h-4 object-cover rounded-none border border-[#0070f3]" />
          ) : (
            <UserIcon className="w-3.5 h-3.5 text-[#0070f3]" />
          )}
          <span className="max-w-[120px] truncate font-mono text-[11px]">
            {user ? (user.isAnonymous ? "Guest Student" : user.displayName || user.email?.split("@")[0] || "Student") : "Sign In / Auth"}
          </span>
          <ShieldCheck className="w-3.5 h-3.5 text-[#0070f3] ml-0.5" />
        </Link>

        {user && !user.isAnonymous && (
          <button
            onClick={signOutUser}
            title="Sign Out"
            className="p-1.5 text-[#888888] hover:text-[#ef4444] bg-[#111111] hover:bg-[#1f1f1f] border border-[#2e2e2e] rounded-none transition-colors"
          >
            <LogOut className="w-3.5 h-3.5" />
          </button>
        )}

        <ActivityLogModal
          isOpen={showMonitor}
          onClose={() => setShowMonitor(false)}
        />
      </div>
    </header>
  );
};
