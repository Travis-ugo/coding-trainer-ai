"use client";

import React, { useState } from "react";
import Link from "next/link";
import { MousePointer, Layout, Code, Bot, Layers, User as UserIcon, LogOut } from "lucide-react";
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
}) => {
  const { user, signOutUser } = useAuth();
  const [showMonitor, setShowMonitor] = useState(false);

  return (
    <header className="h-16 bg-[#000000] border-b border-[#222222] px-6 flex items-center justify-between shrink-0">
      {/* Left App Logo */}
      <div className="flex items-center gap-3">
        <div className="w-[42px] h-[42px] bg-white text-black font-bold rounded-none flex items-center justify-center text-sm tracking-tighter shrink-0 border border-white">
          ▲
        </div>
        <div className="flex items-center gap-2 text-xs">
          <span className="font-bold text-white tracking-wide">
            coding-trainer-ai
          </span>
        </div>
      </div>

      {/* Center Outer Framing Rectangle with Distinct Inner Buttons */}
      <div className="flex items-center h-[42px] bg-[#0a0a0a] border border-[#222222] rounded-none p-[4px] gap-1.5 shrink-0">
        <button
          onClick={() => setActiveTool("analytics")}
          className={`h-[32px] px-3.5 rounded-none text-xs font-medium flex items-center gap-1.5 transition-all ${
            activeTool === "analytics"
              ? "bg-[#1f1f1f] text-white border border-[#333333] shadow-sm"
              : "text-[#888888] hover:text-white"
          }`}
        >
          <MousePointer className="w-3.5 h-3.5" />
          <span>Analytics</span>
        </button>

        <button
          onClick={() => setActiveTool("routine")}
          className={`h-[32px] px-3.5 rounded-none text-xs font-medium flex items-center gap-1.5 transition-all ${
            activeTool === "routine"
              ? "bg-[#1f1f1f] text-white border border-[#333333] shadow-sm"
              : "text-[#888888] hover:text-white"
          }`}
        >
          <Layout className="w-3.5 h-3.5" />
          <span>Routine</span>
        </button>

        <button
          onClick={() => setActiveTool("srs")}
          className={`h-[32px] px-3.5 rounded-none text-xs font-medium flex items-center gap-1.5 transition-all ${
            activeTool === "srs"
              ? "bg-[#1f1f1f] text-white border border-[#333333] shadow-sm"
              : "text-[#888888] hover:text-white"
          }`}
        >
          <Layers className="w-3.5 h-3.5" />
          <span>Flashcards</span>
        </button>

        <button
          onClick={() => setActiveTool("syntax")}
          className={`h-[32px] px-3.5 rounded-none text-xs font-medium flex items-center gap-1.5 transition-all ${
            activeTool === "syntax"
              ? "bg-[#1f1f1f] text-white border border-[#333333] shadow-sm"
              : "text-[#888888] hover:text-white"
          }`}
        >
          <Code className="w-3.5 h-3.5" />
          <span>Syntax Gym</span>
        </button>

        <button
          onClick={() => setActiveTool("socratic")}
          className={`h-[32px] px-3.5 rounded-none text-xs font-medium flex items-center gap-1.5 transition-all ${
            activeTool === "socratic"
              ? "bg-[#1f1f1f] text-white border border-[#333333] shadow-sm"
              : "text-[#888888] hover:text-white"
          }`}
        >
          <Bot className="w-3.5 h-3.5" />
          <span>AI Tutor</span>
        </button>
      </div>

      {/* Right Actions & Outer User Identity Framing Box */}
      <div className="flex items-center gap-3 shrink-0">
        {/* Dedicated Auth Outer Box */}
        <Link
          href="/auth"
          className="h-[42px] flex items-center gap-2 bg-[#0a0a0a] hover:bg-[#141414] border border-[#222222] hover:border-[#333333] text-white px-3.5 rounded-none text-xs font-medium transition-all"
        >
          {user?.photoURL ? (
            <img src={user.photoURL} alt="Avatar" className="w-4 h-4 object-cover rounded-none border border-[#0070f3]" />
          ) : (
            <UserIcon className="w-3.5 h-3.5 text-[#0070f3]" />
          )}
          <span className="max-w-[120px] truncate font-mono text-[11px]">
            {user ? (user.isAnonymous ? "Guest Student" : user.displayName || user.email?.split("@")[0] || "Student") : "Sign In / Auth"}
          </span>
        </Link>

        {user && !user.isAnonymous && (
          <button
            onClick={signOutUser}
            title="Sign Out"
            className="w-[42px] h-[42px] flex items-center justify-center text-[#888888] hover:text-[#ef4444] bg-[#0a0a0a] hover:bg-[#141414] border border-[#222222] hover:border-[#333333] rounded-none transition-colors"
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
