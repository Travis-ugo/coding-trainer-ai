"use client";

import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { LogIn, UserPlus, Sparkles, X, Mail, Lock, ShieldCheck, KeyRound, ArrowLeft, CheckCircle2 } from "lucide-react";

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
}

type AuthMode = "signin" | "signup" | "forgot";

export const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose }) => {
  const {
    signInWithGoogle,
    signInWithEmail,
    signUpWithEmail,
    resetPasswordWithEmail,
    signInAnonymouslyUser,
    user,
  } = useAuth();

  const [mode, setMode] = useState<AuthMode>("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMsg(null);
    if (!email.trim()) {
      setError("Please enter your registered email address.");
      return;
    }
    setSubmitting(true);
    try {
      await resetPasswordWithEmail(email.trim());
      setSuccessMsg("Password reset link sent! Check your email inbox.");
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to send reset link";
      setError(msg);
    } finally {
      setSubmitting(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMsg(null);
    setSubmitting(true);
    try {
      if (mode === "forgot") {
        await resetPasswordWithEmail(email);
        setSuccessMsg("Password reset email sent! Check your inbox.");
      } else if (mode === "signup") {
        await signUpWithEmail(email, password);
        onClose();
      } else {
        await signInWithEmail(email, password);
        onClose();
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Authentication failed";
      setError(msg);
    } finally {
      setSubmitting(false);
    }
  };

  const handleGoogleSignIn = async () => {
    setError(null);
    try {
      await signInWithGoogle();
      onClose();
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Google Sign-In failed";
      setError(msg);
    }
  };

  const handleGuestSignIn = async () => {
    setError(null);
    try {
      await signInAnonymouslyUser();
      onClose();
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Guest login failed";
      setError(msg);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-[#0a0a0a] border border-[#222222] rounded-none max-w-md w-full p-6 shadow-2xl space-y-5 relative text-xs">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-[#888888] hover:text-white transition-colors"
        >
          <X className="w-4 h-4" />
        </button>

        {/* Modal Header */}
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-[#00e599] font-bold">
            <ShieldCheck className="w-4 h-4" />
            <span>Firebase Master&apos;s Studio Identity</span>
          </div>
          <h2 className="text-lg font-bold text-white">
            {mode === "forgot"
              ? "Reset Account Password"
              : mode === "signup"
              ? "Create MSc Student Account"
              : "Sign In to Coding Trainer AI"}
          </h2>
          <p className="text-[#888888]">
            Sync your SRS memory intervals, degree grade metrics, and syntax AST drills across devices.
          </p>
        </div>

        {user && (
          <div className="bg-[#111111] border border-[#222222] p-3 rounded-none text-[#a1a1a1]">
            Currently signed in as:{" "}
            <span className="font-mono text-white font-semibold">
              {user.isAnonymous ? "Guest Student (Anonymous)" : user.email || user.uid}
            </span>
          </div>
        )}

        {error && (
          <div className="bg-[#7f1d1d]/30 border border-[#ef4444] text-[#ef4444] p-3 rounded-none font-mono">
            ⚠️ {error}
          </div>
        )}

        {successMsg && (
          <div className="bg-[#00e599]/10 border border-[#00e599]/40 text-[#00e599] p-3 rounded-none font-mono">
            ✓ {successMsg}
          </div>
        )}

        {/* Google OAuth Button */}
        <button
          onClick={handleGoogleSignIn}
          className="w-full btn-google-auth py-2.5 rounded-none font-medium flex items-center justify-center gap-2 transition-all text-white"
        >
          <svg className="w-4 h-4" viewBox="0 0 24 24">
            <path
              fill="#EA4335"
              d="M12 5c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.3 1.7 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.3 9 5 12 5z"
            />
            <path
              fill="#4285F4"
              d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z"
            />
            <path
              fill="#FBBC05"
              d="M5.6 14.8c-.2-.7-.4-1.5-.4-2.3s.2-1.6.4-2.3L1.9 7.3C.7 9.7 0 12 0 14.8s.7 5.1 1.9 7.5l3.7-2.9z"
            />
            <path
              fill="#34A853"
              d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3 0-5.5-2.3-6.4-5.2L1.9 16c1.8 3.7 5.6 7 10.1 7z"
            />
          </svg>
          <span>Continue with Google</span>
        </button>

        <div className="text-center pt-1">
          <a
            href="/auth"
            className="text-[11px] text-[#0070f3] hover:underline inline-flex items-center gap-1 font-mono"
          >
            <span>Open Dedicated Auth Hub Screen →</span>
          </a>
        </div>

        <div className="flex items-center gap-3 my-2">
          <div className="flex-1 h-[1px] bg-[#222222]" />
          <span className="text-[10px] text-[#666666] uppercase tracking-wider font-semibold font-mono">Or Email</span>
          <div className="flex-1 h-[1px] bg-[#222222]" />
        </div>

        {/* Email/Password Form */}
        <form onSubmit={handleSubmit} className="space-y-3">
          <div className="space-y-1">
            <label className="text-[#888888] font-medium block">Email Address</label>
            <div className="relative">
              <Mail className="w-3.5 h-3.5 absolute left-3 top-3 text-[#666666]" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="student@university.ac.uk"
                className="w-full bg-[#111111] border border-[#2e2e2e] focus:border-[#0070f3] rounded-none py-2 pl-9 pr-3 text-white focus:outline-none font-mono"
              />
            </div>
          </div>

          {mode !== "forgot" && (
            <div className="space-y-1">
              <div className="flex items-center justify-between">
                <label className="text-[#888888] font-medium block">Password</label>
                {mode === "signin" && (
                  <button
                    type="button"
                    onClick={() => { setMode("forgot"); setError(null); setSuccessMsg(null); }}
                    className="text-[11px] text-[#0070f3] hover:underline font-mono"
                  >
                    Forgot?
                  </button>
                )}
              </div>
              <div className="relative">
                <Lock className="w-3.5 h-3.5 absolute left-3 top-3 text-[#666666]" />
                <input
                  type="password"
                  required
                  minLength={6}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••••"
                  className="w-full bg-[#111111] border border-[#2e2e2e] focus:border-[#0070f3] rounded-none py-2 pl-9 pr-3 text-white focus:outline-none font-mono"
                />
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={submitting}
            className="w-full btn-next-primary py-2.5 rounded-none text-xs font-semibold flex items-center justify-center gap-2 mt-4"
          >
            {submitting ? (
              <div className="w-4 h-4 border-2 border-black/30 border-t-black rounded-none animate-spin" />
            ) : mode === "forgot" ? (
              <>
                <KeyRound className="w-3.5 h-3.5" />
                <span>Send Reset Link</span>
              </>
            ) : mode === "signup" ? (
              <>
                <UserPlus className="w-3.5 h-3.5" />
                <span>Create Student Account</span>
              </>
            ) : (
              <>
                <LogIn className="w-3.5 h-3.5" />
                <span>Sign In with Email</span>
              </>
            )}
          </button>
        </form>

        {/* Modal Footer & Mode Toggles */}
        <div className="pt-3 border-t border-[#222222] flex items-center justify-between text-[11px]">
          {mode === "forgot" ? (
            <button
              type="button"
              onClick={() => {
                setMode("signin");
                setError(null);
                setSuccessMsg(null);
              }}
              className="text-[#0070f3] hover:underline flex items-center gap-1 font-mono font-medium"
            >
              <ArrowLeft className="w-3 h-3" />
              <span>Back to Sign In</span>
            </button>
          ) : (
            <button
              type="button"
              onClick={() => {
                setMode(mode === "signup" ? "signin" : "signup");
                setError(null);
                setSuccessMsg(null);
              }}
              className="text-[#0070f3] hover:underline font-mono"
            >
              {mode === "signup" ? "Already registered? Sign In" : "Need an account? Create one"}
            </button>
          )}

          <button
            type="button"
            onClick={handleGuestSignIn}
            className="text-[#888888] hover:text-white flex items-center gap-1 font-mono"
          >
            <Sparkles className="w-3 h-3 text-[#00e599]" />
            <span>Guest Pass</span>
          </button>
        </div>
      </div>
    </div>
  );
};


