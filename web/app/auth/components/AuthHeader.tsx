"use client";

import React from "react";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export default function AuthHeader() {
  return (
    <header className="relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 md:px-8 py-4 sm:py-6 flex items-center justify-between overflow-hidden">
      <Link
        href="/"
        className="flex items-center gap-2 text-xs text-[#888888] hover:text-white transition-colors"
      >
        <ArrowLeft className="w-4 h-4 shrink-0" />
        <span>Back to Studio</span>
      </Link>
    </header>
  );
}
