"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AuthProvider, useAuth } from "../context/AuthContext";
import {
  Mail,
  Lock,
  Eye,
  EyeOff,
  LogIn,
  UserPlus,
  Sparkles,
  ArrowLeft,
  CheckCircle2,
  Copy,
  Check,
  LogOut,
  ChevronRight,
  Key,
  Globe,
  Flame,
  Cpu,
  Code2,
  Terminal,
  Binary,
  Atom,
  Orbit,
  Radio,
  CircuitBoard,
} from "lucide-react";

function AuthBoxScreen() {
  const {
    user,
    loading,
    signInWithGoogle,
    signInWithEmail,
    signUpWithEmail,
    resetPasswordWithEmail,
    signInAnonymouslyUser,
    signOutUser,
    updateUserProfile,
  } = useAuth();
  const { analyticsData } = useTrainerContext();

  const [activeTab, setActiveTab] = useState<"signin" | "signup" | "forgot">("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);
  const [copiedUid, setCopiedUid] = useState(false);
  const [showAvatarPicker, setShowAvatarPicker] = useState(false);
  const [customAvatarUrl, setCustomAvatarUrl] = useState("");
  const [avatarUpdating, setAvatarUpdating] = useState(false);

  const PRESET_AVATARS = [
    { label: "Scholar", url: "https://api.dicebear.com/7.x/bottts/svg?seed=msc_robotics_01" },
    { label: "Researcher", url: "https://api.dicebear.com/7.x/bottts/svg?seed=msc_scholar_02" },
    { label: "Engineer", url: "https://api.dicebear.com/7.x/bottts/svg?seed=ast_syntax_03" },
  ];

  const handleSelectAvatar = async (url: string) => {
    setError(null);
    setSuccessMsg(null);
    setAvatarUpdating(true);
    try {
      await updateUserProfile(url);
      setSuccessMsg("Avatar updated!");
      setShowAvatarPicker(false);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to update avatar";
      setError(msg);
    } finally {
      setAvatarUpdating(false);
    }
  };

  const handleGoogleSignIn = async () => {
    setError(null);
    setSuccessMsg(null);
    setGoogleLoading(true);
    try {
      await signInWithGoogle();
      setSuccessMsg("Signed in with Google!");
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Google authentication failed";
      setError(msg);
    } finally {
      setGoogleLoading(false);
    }
  };

  const handleEmailFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMsg(null);
    setIsSubmitting(true);
    try {
      if (activeTab === "forgot") {
        await resetPasswordWithEmail(email);
        setSuccessMsg("Password reset email sent!");
      } else if (activeTab === "signup") {
        await signUpWithEmail(email, password);
        setSuccessMsg("Account created!");
      } else {
        await signInWithEmail(email, password);
        setSuccessMsg("Signed in!");
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Authentication failed";
      setError(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleGuestSignIn = async () => {
    setError(null);
    setSuccessMsg(null);
    setIsSubmitting(true);
    try {
      await signInAnonymouslyUser();
      setSuccessMsg("Guest pass active!");
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Guest access failed";
      setError(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCopyUid = () => {
    if (user?.uid) {
      navigator.clipboard.writeText(user.uid);
      setCopiedUid(true);
      setTimeout(() => setCopiedUid(false), 2000);
    }
  };

  return (
    <div className="min-h-screen w-full bg-[#000000] text-white flex flex-col justify-between relative overflow-x-hidden">
      {/* Top Navigation */}
      <header className="relative z-10 w-full max-w-7xl mx-auto px-6 py-6 flex items-center justify-between">
        <Link
          href="/"
          className="flex items-center gap-2 text-xs text-[#888888] hover:text-white transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Studio</span>
        </Link>
      </header>

      {/* Main Split Auth Section (Flushed to Left Side) */}
      <main className="relative z-10 flex-1 flex flex-col md:flex-row items-center justify-between pl-2 md:pl-6 lg:pl-10 pr-6 md:pr-16 lg:pr-24 my-4 w-full gap-6">
        {/* Left Side: Flushed Large White AI Brain + Zero Gravity Tech Icons */}
        <div className="hidden md:flex flex-1 items-center justify-start relative p-0 min-h-[480px]">
          {/* Floating White Tech Icons in Zero Gravity Space */}
          <div className="absolute top-2 left-4 animate-space-float-1 text-white/80">
            <Cpu className="w-9 h-9" />
          </div>
          <div className="absolute top-8 left-1/2 animate-space-float-2 text-white/70">
            <Code2 className="w-10 h-10" />
          </div>
          <div className="absolute bottom-8 left-8 animate-space-float-3 text-white/85">
            <Terminal className="w-9 h-9" />
          </div>
          <div className="absolute bottom-12 left-2/3 animate-space-float-1 text-white/75">
            <Atom className="w-10 h-10" />
          </div>
          <div className="absolute top-1/3 left-2 animate-space-float-2 text-white/60">
            <Orbit className="w-8 h-8" />
          </div>
          <div className="absolute bottom-2 left-1/3 animate-space-float-3 text-white/90">
            <Binary className="w-9 h-9" />
          </div>
          <div className="absolute top-6 right-10 animate-space-float-1 text-white/70">
            <CircuitBoard className="w-10 h-10" />
          </div>
          <div className="absolute bottom-1/3 right-6 animate-space-float-2 text-white/80">
            <Radio className="w-8 h-8" />
          </div>

          <img
            src="/brain_illustration.jpg"
            alt="AI Brain Illustration"
            className="w-full max-w-lg lg:max-w-xl xl:max-w-2xl object-contain filter brightness-110 contrast-125 relative z-10 -ml-4"
          />
        </div>

        {/* Right Side: Auth Form Container */}
        <div className="w-full max-w-sm space-y-6">
          {/* Header Title & Subtitle (+6px larger title) */}
          <div className="space-y-1">
            <h1 className="text-[26px] font-bold tracking-tight text-white leading-tight">
              {user && !user.isAnonymous
                ? "Account"
                : activeTab === "signup"
                ? "Create Account"
                : activeTab === "forgot"
                ? "Reset Password"
                : "Sign In"}
            </h1>
            <p className="text-xs text-[#888888]">
              {user && !user.isAnonymous
                ? "Manage your session and identity."
                : "Coding Trainer AI"}
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

          {/* AUTHENTICATED USER SCREEN */}
          {user && !user.isAnonymous ? (
            <div className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <div
                    onClick={() => setShowAvatarPicker(!showAvatarPicker)}
                    className="cursor-pointer group relative shrink-0"
                  >
                    {user.photoURL ? (
                      <img
                        src={user.photoURL}
                        alt="User Avatar"
                        className="w-12 h-12 rounded-none border border-[#333333] object-cover"
                      />
                    ) : (
                      <div className="w-12 h-12 bg-[#111111] border border-[#333333] flex items-center justify-center font-bold text-sm">
                        {user.email ? user.email.charAt(0).toUpperCase() : "S"}
                      </div>
                    )}
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm font-semibold text-white truncate">
                      {user.displayName || user.email?.split("@")[0]}
                    </p>
                    <p className="text-xs font-mono text-[#888888] truncate">{user.email}</p>
                  </div>
                </div>

                {showAvatarPicker && (
                  <div className="pt-2 space-y-2">
                    <div className="grid grid-cols-3 gap-2">
                      {PRESET_AVATARS.map((item, idx) => (
                        <button
                          key={idx}
                          onClick={() => handleSelectAvatar(item.url)}
                          disabled={avatarUpdating}
                          className="bg-[#111111] border border-[#222222] hover:border-white p-2 text-center flex flex-col items-center gap-1 text-[10px] text-[#888888] hover:text-white"
                        >
                          <img src={item.url} alt={item.label} className="w-8 h-8 object-contain" />
                          <span>{item.label}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                <div className="pt-2 text-xs space-y-1.5 font-mono text-[#888888]">
                  <div className="flex items-center justify-between">
                    <span>UID:</span>
                    <button onClick={handleCopyUid} className="text-white hover:underline flex items-center gap-1">
                      <span className="truncate max-w-[120px]">{user.uid}</span>
                      {copiedUid ? <Check className="w-3 h-3 text-[#0070f3]" /> : <Copy className="w-3 h-3" />}
                    </button>
                  </div>
                </div>
              </div>

              <div className="space-y-2.5 pt-2">
                <Link
                  href="/"
                  className="w-full h-11 btn-next-primary py-3 rounded-none text-xs font-semibold flex items-center justify-center gap-2"
                >
                  <span>Launch Workspace</span>
                  <ChevronRight className="w-4 h-4" />
                </Link>

                <button
                  onClick={signOutUser}
                  className="w-full h-11 btn-next-secondary py-3 rounded-none text-xs font-medium flex items-center justify-center gap-2"
                >
                  <LogOut className="w-3.5 h-3.5" />
                  <span>Sign Out</span>
                </button>
              </div>
            </div>
          ) : (
            /* UNAUTHENTICATED FORM SCREEN - SLEEK & MINIMALIST */
            <div className="space-y-5">
              {/* Google OAuth Button (Taller h-11) */}
              <button
                onClick={handleGoogleSignIn}
                disabled={googleLoading || loading}
                className="w-full h-11 btn-google-auth py-3 px-4 rounded-none text-xs font-semibold flex items-center justify-center gap-2.5 transition-all text-white border border-[#222222] hover:border-[#333333]"
              >
                {googleLoading ? (
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-none animate-spin" />
                ) : (
                  <svg className="w-4 h-4 shrink-0" viewBox="0 0 24 24">
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
                )}
                <span>Continue with Google</span>
              </button>

              {/* Minimal Mode Tab Bar */}
              <div className="grid grid-cols-3 p-0.5 bg-[#0a0a0a] border border-[#222222] rounded-none text-xs">
                <button
                  type="button"
                  onClick={() => {
                    setActiveTab("signin");
                    setError(null);
                    setSuccessMsg(null);
                  }}
                  className={`py-2 rounded-none font-medium transition-all ${
                    activeTab === "signin"
                      ? "bg-white text-black font-semibold"
                      : "text-[#888888] hover:text-white"
                  }`}
                >
                  Sign In
                </button>

                <button
                  type="button"
                  onClick={() => {
                    setActiveTab("signup");
                    setError(null);
                    setSuccessMsg(null);
                  }}
                  className={`py-2 rounded-none font-medium transition-all ${
                    activeTab === "signup"
                      ? "bg-white text-black font-semibold"
                      : "text-[#888888] hover:text-white"
                  }`}
                >
                  Sign Up
                </button>

                <button
                  type="button"
                  onClick={() => {
                    setActiveTab("forgot");
                    setError(null);
                    setSuccessMsg(null);
                  }}
                  className={`py-2 rounded-none font-medium transition-all ${
                    activeTab === "forgot"
                      ? "bg-white text-black font-semibold"
                      : "text-[#888888] hover:text-white"
                  }`}
                >
                  Reset
                </button>
              </div>

              {/* Form Controls (Taller Input Fields & Action Button) */}
              <form onSubmit={handleEmailFormSubmit} className="space-y-3.5">
                <div className="space-y-1">
                  <label className="text-xs text-[#888888] block">Email</label>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="name@example.com"
                    className="w-full h-11 auth-input rounded-none py-3 px-3.5 text-xs font-mono"
                  />
                </div>

                {activeTab !== "forgot" && (
                  <div className="space-y-1">
                    <div className="flex items-center justify-between">
                      <label className="text-xs text-[#888888] block">Password</label>
                      {activeTab === "signin" && (
                        <button
                          type="button"
                          onClick={() => {
                            setActiveTab("forgot");
                            setError(null);
                            setSuccessMsg(null);
                          }}
                          className="text-[11px] text-[#888888] hover:text-white font-mono"
                        >
                          Forgot?
                        </button>
                      )}
                    </div>
                    <div className="relative">
                      <input
                        type={showPassword ? "text" : "password"}
                        required
                        minLength={6}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="••••••••••••"
                        className="w-full h-11 auth-input rounded-none py-3 pl-3.5 pr-9 text-xs font-mono"
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
                )}

                <button
                  type="submit"
                  disabled={isSubmitting || loading}
                  className="w-full h-11 btn-next-primary py-3 rounded-none text-xs font-semibold flex items-center justify-center gap-2 transition-all mt-2"
                >
                  {isSubmitting ? (
                    <div className="w-4 h-4 border-2 border-black/30 border-t-black rounded-none animate-spin" />
                  ) : activeTab === "forgot" ? (
                    <span>Send Reset Email</span>
                  ) : activeTab === "signup" ? (
                    <span>Create Account</span>
                  ) : (
                    <span>Sign In</span>
                  )}
                </button>
              </form>

              {/* Minimal Footer Option */}
              <div className="pt-2 border-t border-[#222222] flex items-center justify-between text-xs">
                <button
                  type="button"
                  onClick={handleGuestSignIn}
                  disabled={isSubmitting}
                  className="text-[#888888] hover:text-white flex items-center gap-1 font-mono text-[11px]"
                >
                  <Sparkles className="w-3.5 h-3.5 text-[#0070f3]" />
                  <span>Continue as Guest</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Minimal Footer */}
      <footer className="relative z-10 w-full max-w-7xl mx-auto px-6 py-4 text-xs text-[#666666]">
        <p>Coding Trainer AI</p>
      </footer>
    </div>
  );
}

import { TrainerProvider, useTrainerContext } from "../context/TrainerContext";

export default function AuthPage() {
  return (
    <AuthProvider>
      <TrainerProvider>
        <AuthBoxScreen />
      </TrainerProvider>
    </AuthProvider>
  );
}


