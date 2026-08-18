"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AuthProvider, useAuth } from "../../context/AuthContext";
import { TrainerProvider } from "../../context/TrainerContext";
import AuthHeader from "../components/AuthHeader";
import AuthHero from "../components/AuthHero";
import { formatAuthError } from "../utils/formatError";
import { CheckCircle2, ChevronRight, LogOut, Key } from "lucide-react";

function ForgotPasswordScreen() {
  const {
    user,
    loading,
    resetPasswordWithEmail,
    signOutUser,
  } = useAuth();
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (!loading && user) {
      window.location.href = "/";
    }
  }, [user, loading, router]);

  const handleResetSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMsg(null);
    setIsSubmitting(true);
    try {
      await resetPasswordWithEmail(email);
      setSuccessMsg("Password reset email sent to " + email);
    } catch (err: unknown) {
      setError(formatAuthError(err));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen w-full bg-[#000000] text-white flex flex-col justify-between relative overflow-x-hidden">
      <AuthHeader />

      <main className="relative z-10 flex-1 flex flex-col md:flex-row items-center justify-between px-6 md:px-12 lg:px-20 max-w-7xl mx-auto w-full gap-8 my-4">
        <AuthHero />

        {/* Right Side: Reset Password Form */}
        <div className="w-full max-w-sm space-y-6">
          <div className="space-y-1">
            <h1 className="text-[26px] font-bold tracking-tight text-white leading-tight">
              {user && !user.isAnonymous ? "Account" : "Reset Password"}
            </h1>
            <p className="text-xs text-[#888888]">
              {user && !user.isAnonymous
                ? "Manage your active session."
                : "Enter your email to receive a recovery link."}
            </p>
          </div>

          {/* Feedback Banners */}
          {error && (
            <div className="text-xs text-[#ef4444] font-mono py-1">
              ⚠️ {error}
            </div>
          )}

          {successMsg && (
            <div className="text-xs text-white font-mono py-1 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-[#0070f3]" />
              <span>{successMsg}</span>
            </div>
          )}

          {user && !user.isAnonymous ? (
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-[#111111] border border-[#333333] flex items-center justify-center font-bold text-sm">
                  {user.email ? user.email.charAt(0).toUpperCase() : "S"}
                </div>
                <div className="min-w-0">
                  <p className="text-sm font-semibold text-white truncate">
                    {user.displayName || user.email?.split("@")[0]}
                  </p>
                  <p className="text-xs font-mono text-[#888888] truncate">{user.email}</p>
                </div>
              </div>

              <div className="space-y-2.5 pt-2">
                <Link
                  href="/"
                  className="w-full h-11 bg-white text-black font-semibold hover:bg-[#e5e5e5] border border-white transition-all py-3 rounded-none text-xs flex items-center justify-center gap-2"
                >
                  <span>Launch Workspace</span>
                  <ChevronRight className="w-4 h-4" />
                </Link>

                <button
                  onClick={signOutUser}
                  className="w-full h-11 bg-[#111111] text-white font-medium hover:bg-[#1a1a1a] border border-[#2e2e2e] hover:border-[#444444] transition-all py-3 rounded-none text-xs flex items-center justify-center gap-2"
                >
                  <LogOut className="w-3.5 h-3.5" />
                  <span>Sign Out</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-5">
              {/* Dedicated Route Navigation Bar */}
              <div className="grid grid-cols-3 p-0.5 bg-[#0a0a0a] border border-[#222222] rounded-none text-xs">
                <Link
                  href="/auth/signin"
                  className="py-2 rounded-none font-medium text-center transition-all text-[#888888] hover:text-white"
                >
                  Sign In
                </Link>
                <Link
                  href="/auth/signup"
                  className="py-2 rounded-none font-medium text-center transition-all text-[#888888] hover:text-white"
                >
                  Sign Up
                </Link>
                <Link
                  href="/auth/forgot"
                  className="py-2 rounded-none font-semibold text-center transition-all bg-white text-black"
                >
                  Reset
                </Link>
              </div>

              <form onSubmit={handleResetSubmit} className="space-y-3.5">
                <div className="space-y-1">
                  <label className="text-xs text-[#888888] block">Registered Account Email</label>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="name@example.com"
                    className="w-full h-11 bg-[#0d0d0d] border border-[#2a2a2a] focus:border-[#0070f3] focus:outline-none text-white rounded-none py-3 px-3.5 text-xs font-mono transition-colors"
                  />
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting || loading}
                  className="w-full h-11 bg-white text-black font-semibold hover:bg-[#e5e5e5] border border-white rounded-none text-xs flex items-center justify-center gap-2 transition-all mt-2"
                >
                  {isSubmitting ? (
                    <div className="w-4 h-4 border-2 border-black/30 border-t-black rounded-none animate-spin" />
                  ) : (
                    <span>Send Recovery Email</span>
                  )}
                </button>
              </form>

              <div className="pt-2 border-t border-[#222222] flex items-center justify-between text-xs font-mono">
                <Link href="/auth/signin" className="text-[#888888] hover:text-white text-[11px]">
                  ← Back to Sign In
                </Link>
                <Link href="/auth/signup" className="text-white hover:underline text-[11px]">
                  Create new account →
                </Link>
              </div>
            </div>
          )}
        </div>
      </main>

      <footer className="relative z-10 w-full max-w-7xl mx-auto px-6 py-4 text-xs text-[#666666]">
        <p>Coding Trainer AI</p>
      </footer>
    </div>
  );
}

export default function ForgotPasswordPage() {
  return (
    <AuthProvider>
      <TrainerProvider>
        <ForgotPasswordScreen />
      </TrainerProvider>
    </AuthProvider>
  );
}
