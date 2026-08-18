"use client";

import React from "react";
import {
  Cpu,
  Code2,
  Terminal,
  Binary,
  Atom,
  Orbit,
  Radio,
  CircuitBoard,
  Database,
  Network,
  Braces,
  FileCode,
  Bot,
  Sparkles,
  Layers,
  Wifi,
  Zap,
  Workflow,
  Sliders,
} from "lucide-react";

export default function AuthHero() {
  return (
    <div className="hidden md:flex flex-1 items-center justify-center relative p-4 min-h-[420px] max-w-full overflow-hidden">
      {/* Floating White Tech Icons in Zero Gravity Space (z-20 layer) */}
      <div className="absolute top-4 left-4 z-20 animate-space-float-1 text-white/80">
        <Cpu className="w-5 h-5" />
      </div>
      <div className="absolute top-8 left-1/3 z-20 animate-space-float-2 text-white/70">
        <Code2 className="w-6 h-6" />
      </div>
      <div className="absolute top-6 left-2/3 z-20 animate-space-float-3 text-white/85">
        <Terminal className="w-5 h-5" />
      </div>
      <div className="absolute top-1/4 left-12 z-20 animate-space-float-1 text-white/75">
        <Atom className="w-6 h-6" />
      </div>
      <div className="absolute top-1/3 left-4 z-20 animate-space-float-2 text-white/60">
        <Orbit className="w-5 h-5" />
      </div>
      <div className="absolute top-1/2 left-8 z-20 animate-space-float-3 text-white/90">
        <Binary className="w-5 h-5" />
      </div>
      <div className="absolute top-10 right-14 z-20 animate-space-float-1 text-white/70">
        <CircuitBoard className="w-6 h-6" />
      </div>
      <div className="absolute top-1/3 right-10 z-20 animate-space-float-2 text-white/80">
        <Radio className="w-5 h-5" />
      </div>
      <div className="absolute bottom-12 left-6 z-20 animate-space-float-3 text-white/85">
        <Database className="w-5 h-5 text-white" />
      </div>
      <div className="absolute bottom-20 left-1/4 z-20 animate-space-float-1 text-white/85">
        <Network className="w-6 h-6" />
      </div>
      <div className="absolute bottom-8 left-1/2 z-20 animate-space-float-2 text-white/70">
        <Braces className="w-5 h-5" />
      </div>
      <div className="absolute bottom-14 right-1/3 z-20 animate-space-float-3 text-white/80">
        <FileCode className="w-5 h-5" />
      </div>
      <div className="absolute bottom-6 right-14 z-20 animate-space-float-1 text-white/90">
        <Bot className="w-6 h-6" />
      </div>
      <div className="absolute top-1/2 right-16 z-20 animate-space-float-2 text-white/65">
        <Sparkles className="w-5 h-5 text-[#0070f3]" />
      </div>
      <div className="absolute bottom-1/3 left-14 z-20 animate-space-float-3 text-white/75">
        <Layers className="w-5 h-5" />
      </div>
      <div className="absolute top-20 left-1/4 z-20 animate-space-float-1 text-white/80">
        <Wifi className="w-4 h-4" />
      </div>
      <div className="absolute bottom-24 left-1/3 z-20 animate-space-float-2 text-white/85">
        <Zap className="w-5 h-5" />
      </div>
      <div className="absolute bottom-4 right-1/4 z-20 animate-space-float-3 text-white/70">
        <Workflow className="w-5 h-5" />
      </div>
      <div className="absolute top-1/4 right-8 z-20 animate-space-float-1 text-white/60">
        <Sliders className="w-4 h-4" />
      </div>

      <img
        src="/brain_illustration.jpg"
        alt="AI Brain Illustration"
        className="w-full max-w-[260px] md:max-w-[300px] lg:max-w-[340px] object-contain relative z-10 pointer-events-none"
      />
    </div>
  );
}
