"use client";

import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { LogIn, UserPlus, Sparkles, X, Mail, Lock, ShieldCheck } from "lucide-react";

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose }) => {
  const { signInWithGoogle, signInWithEmail, signUpWithEmail, signInAnonymouslyUser, user } = useAuth();
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      if (isSignUp) {
        await signUpWithEmail(email, password);
      } else {
        await signInWithEmail(email, password);
      }
      onClose();
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
            {isSignUp ? "Create MSc Student Account" : "Sign In to Coding Trainer AI"}
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
            <span>Open Dedicated Auth Screen →</span>
          </a>
        </div>

        <div className="flex items-center gap-3 my-2">
          <div className="flex-1 h-[1px] bg-[#222222]" />
          <span className="text-[10px] text-[#666666] uppercase tracking-wider font-semibold">Or Email</span>
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

          <div className="space-y-1">
            <label className="text-[#888888] font-medium block">Password</label>
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

          <button
            type="submit"
            disabled={submitting}
            className="w-full btn-next-primary py-2.5 rounded-none text-xs font-semibold flex items-center justify-center gap-2 mt-4"
          >
            {isSignUp ? <UserPlus className="w-3.5 h-3.5" /> : <LogIn className="w-3.5 h-3.5" />}
            <span>{isSignUp ? "Create Student Account" : "Sign In with Email"}</span>
          </button>
        </form>

        {/* Modal Footer & Mode Toggles */}
        <div className="pt-2 border-t border-[#222222] flex items-center justify-between text-[11px]">
          <button
            type="button"
            onClick={() => setIsSignUp(!isSignUp)}
            className="text-[#0070f3] hover:underline"
          >
            {isSignUp ? "Already have an account? Sign In" : "Need an account? Sign Up"}
          </button>

          <button
            type="button"
            onClick={handleGuestSignIn}
            className="text-[#888888] hover:text-white flex items-center gap-1"
          >
            <Sparkles className="w-3 h-3 text-[#00e599]" />
            <span>Continue as Guest</span>
          </button>
        </div>
      </div>
    </div>
  );
};

