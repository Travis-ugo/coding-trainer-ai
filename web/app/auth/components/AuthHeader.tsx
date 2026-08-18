"use client";

import React from "react";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export default function AuthHeader() {
  return (
    <header className="relative z-10 w-full max-w-7xl mx-auto px-6 py-6 flex items-center justify-between">
      <Link
        href="/"
        className="flex items-center gap-2 text-xs text-[#888888] hover:text-white transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Studio</span>
      </Link>
    </header>
  );
}
