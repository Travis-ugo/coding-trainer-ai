"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "../../context/AuthContext";
import AuthHeader from "../components/AuthHeader";
import AuthHero from "../components/AuthHero";
import GoogleIcon from "../components/GoogleIcon";
import { formatAuthError } from "../utils/formatError";
import { Eye, EyeOff, CheckCircle2 } from "lucide-react";

export default function SignUpPage() {
  const {
    user,
    loading,
    signInWithGoogle,
    signUpWithEmail,
    signInAnonymouslyUser,
    signOutUser,
  } = useAuth();
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);

  useEffect(() => {
    if (!loading && user) {
      router.replace("/");
    }
  }, [user, loading, router]);

  const handleGoogleSignIn = async () => {
    setError(null);
    setSuccessMsg(null);
    setGoogleLoading(true);
    try {
      await signInWithGoogle();
      router.replace("/");
    } catch (err: unknown) {
      setError(formatAuthError(err));
      setGoogleLoading(false);
    }
  };

  const handleSignUpSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMsg(null);
    setIsSubmitting(true);
    try {
      await signUpWithEmail(email, password);
      router.replace("/");
    } catch (err: unknown) {
      setError(formatAuthError(err));
      setIsSubmitting(false);
    }
  };

  const handleGuestSignIn = async () => {
    setError(null);
    setSuccessMsg(null);
    setIsSubmitting(true);
    try {
      await signInAnonymouslyUser();
      router.replace("/");
    } catch (err: unknown) {
      setError(formatAuthError(err));
      setIsSubmitting(false);
    }
  };

  if (loading || user) {
    return (
      <div className="min-h-screen w-full bg-[#000000] text-white flex flex-col items-center justify-center space-y-3 font-mono text-xs">
        <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-none animate-spin" />
        <p className="text-[#888888]">
          {user ? "Redirecting to home workspace..." : "Authenticating..."}
        </p>
      </div>
    );
  }

  return (
    <div className="min-h-screen w-full max-w-full overflow-x-hidden bg-[#000000] text-white flex flex-col justify-between relative box-border">
      <AuthHeader />

      <main className="relative z-10 flex-1 flex flex-col md:flex-row items-center justify-center md:justify-between px-4 sm:px-6 md:px-10 lg:px-16 max-w-7xl mx-auto w-full gap-6 md:gap-8 my-2 sm:my-4 overflow-hidden">
        <AuthHero />

        {/* Right Side: Sign Up Form */}
        <div className="w-full max-w-sm space-y-6 mx-auto md:mx-0">
          <div className="space-y-1">
            <h1 className="text-[26px] font-bold tracking-tight text-white leading-tight">
              Create Account
            </h1>
            <p className="text-xs text-[#888888]">Join Coding Trainer AI</p>
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

          <div className="space-y-5">
            {/* Google OAuth Button */}
            <button
              onClick={handleGoogleSignIn}
              disabled={googleLoading || loading}
              className="w-full h-11 bg-[#161616] border border-[#222222] hover:border-[#4285F4] hover:bg-[#1f1f1f] text-white py-3 px-4 rounded-none text-xs font-semibold flex items-center justify-center gap-2.5 transition-all"
            >
              {googleLoading ? (
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-none animate-spin" />
              ) : (
                <GoogleIcon className="w-4 h-4 shrink-0" />
              )}
              <span>Continue with Google</span>
            </button>

            {/* Mode Bar */}
            <div className="grid grid-cols-3 p-0.5 bg-[#0a0a0a] border border-[#222222] rounded-none text-xs">
              <Link
                href="/auth/signin"
                className="py-2 rounded-none font-medium text-center transition-all text-[#888888] hover:text-white"
              >
                Sign In
              </Link>
              <Link
                href="/auth/signup"
                className="py-2 rounded-none font-semibold text-center transition-all bg-white text-black"
              >
                Sign Up
              </Link>
              <Link
                href="/auth/forgot"
                className="py-2 rounded-none font-medium text-center transition-all text-[#888888] hover:text-white"
              >
                Reset
              </Link>
            </div>

            <form onSubmit={handleSignUpSubmit} className="space-y-3.5">
              <div className="space-y-1">
                <label className="text-xs text-[#888888] block">Student or Work Email</label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="student@university.ac.uk"
                  className="w-full h-11 bg-[#0d0d0d] border border-[#2a2a2a] focus:border-[#0070f3] focus:outline-none text-white rounded-none py-3 px-3.5 text-xs font-mono transition-colors"
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs text-[#888888] block">Choose Password (min 6 chars)</label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    required
                    minLength={6}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••••••"
                    className="w-full h-11 bg-[#0d0d0d] border border-[#2a2a2a] focus:border-[#0070f3] focus:outline-none text-white rounded-none py-3 pl-3.5 pr-9 text-xs font-mono transition-colors"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-3.5 text-[#666666] hover:text-white transition-colors"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={isSubmitting || loading}
                className="w-full h-11 bg-white text-black font-semibold hover:bg-[#e5e5e5] border border-white rounded-none text-xs flex items-center justify-center gap-2 transition-all mt-2"
              >
                {isSubmitting ? (
                  <div className="w-4 h-4 border-2 border-black/30 border-t-black rounded-none animate-spin" />
                ) : (
                  <span>Create Account</span>
                )}
              </button>
            </form>

            <div className="pt-2 border-t border-[#222222] flex items-center justify-end text-xs">
              <button
                type="button"
                onClick={handleGuestSignIn}
                disabled={isSubmitting}
                className="text-white hover:underline flex items-center font-mono text-[11px]"
              >
                <span>Continue as Guest →</span>
              </button>
            </div>
          </div>
        </div>
      </main>

      <footer className="relative z-10 w-full max-w-7xl mx-auto px-6 py-4 text-xs text-[#666666]">
        <p>Coding Trainer AI</p>
      </footer>
    </div>
  );
}
