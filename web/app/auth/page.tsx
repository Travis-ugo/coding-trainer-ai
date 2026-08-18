"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AuthProvider, useAuth } from "../context/AuthContext";
import {
  ShieldCheck,
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
} from "lucide-react";

function AuthBoxScreen() {
  const {
    user,
    loading,
    signInWithGoogle,
    signInWithEmail,
    signUpWithEmail,
    signInAnonymouslyUser,
    signOutUser,
    updateUserProfile,
  } = useAuth();
  const { analyticsData } = useTrainerContext();


  const [activeTab, setActiveTab] = useState<"signin" | "signup">("signin");
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
    { label: "AI & Robotics Scholar", url: "https://api.dicebear.com/7.x/bottts/svg?seed=msc_robotics_01" },
    { label: "UK MSc Distinction", url: "https://api.dicebear.com/7.x/bottts/svg?seed=msc_scholar_02" },
    { label: "Syntax AST Engineer", url: "https://api.dicebear.com/7.x/bottts/svg?seed=ast_syntax_03" },
    { label: "Neural AI Researcher", url: "https://api.dicebear.com/7.x/bottts/svg?seed=neural_ai_04" },
    { label: "Autonomous Systems", url: "https://api.dicebear.com/7.x/bottts/svg?seed=ros2_robot_05" },
    { label: "Quantum AI Computing", url: "https://api.dicebear.com/7.x/bottts/svg?seed=quantum_ai_06" },
  ];

  const handleSelectAvatar = async (url: string) => {
    setError(null);
    setSuccessMsg(null);
    setAvatarUpdating(true);
    try {
      await updateUserProfile(url);
      setSuccessMsg("Avatar picture updated in Firebase Auth & Firestore!");
      setShowAvatarPicker(false);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to update avatar";
      setError(msg);
    } finally {
      setAvatarUpdating(false);
    }
  };

  const handleCustomAvatarSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!customAvatarUrl.trim()) return;
    await handleSelectAvatar(customAvatarUrl.trim());
  };


  const handleGoogleSignIn = async () => {
    setError(null);
    setSuccessMsg(null);
    setGoogleLoading(true);
    try {
      await signInWithGoogle();
      setSuccessMsg("Successfully authenticated with Google!");
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Google Authentication failed";
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
      if (activeTab === "signup") {
        await signUpWithEmail(email, password);
        setSuccessMsg("Account created successfully!");
      } else {
        await signInWithEmail(email, password);
        setSuccessMsg("Signed in successfully!");
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Authentication error occurred";
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
      setSuccessMsg("Logged in as Guest Student!");
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

  // Determine provider type badge
  const getProviderInfo = () => {
    if (!user) return null;
    if (user.isAnonymous) {
      return { label: "Guest Pass", color: "bg-[#00e599]/10 text-[#00e599] border-[#00e599]/30", icon: Sparkles };
    }
    const providerId = user.providerData[0]?.providerId;
    if (providerId === "google.com") {
      return { label: "Google OAuth 2.0", color: "bg-[#4285F4]/10 text-[#4285F4] border-[#4285F4]/30", icon: Globe };
    }
    return { label: "Verified Email", color: "bg-[#0070f3]/10 text-[#0070f3] border-[#0070f3]/30", icon: Mail };
  };

  const provider = getProviderInfo();

  return (
    <div className="min-h-screen w-full bg-[#000000] text-white flex flex-col justify-between relative overflow-x-hidden selection:bg-[#0070f3] selection:text-white">
      {/* Background Glow & Grid Patterns */}
      <div className="absolute inset-0 bg-radial-auth-glow pointer-events-none" />
      <div className="absolute inset-0 bg-grid-pattern opacity-40 pointer-events-none" />

      {/* Top Header Bar */}
      <header className="relative z-10 w-full max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">
        <Link
          href="/"
          className="flex items-center gap-2.5 text-xs text-[#a1a1a1] hover:text-white transition-colors bg-[#111111] hover:bg-[#1a1a1a] border border-[#222222] px-3.5 py-2 rounded-none font-medium"
        >
          <ArrowLeft className="w-4 h-4 text-[#0070f3]" />
          <span>Back to Master Studio</span>
        </Link>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-[#0a0a0a] border border-[#222222] px-3 py-1.5 rounded-none text-xs font-mono">
            <span className="w-2 h-2 rounded-none bg-[#00e599] animate-pulse" />
            <span className="text-[#888888]">Firebase Auth:</span>
            <span className="text-white font-semibold">Online</span>
          </div>
        </div>
      </header>

      {/* Main Center Auth Container */}
      <main className="relative z-10 flex-1 flex items-center justify-center p-4 my-8">
        <div className="w-full max-w-md">
          {/* Glassmorphic Auth Box Card */}
          <div className="glass-auth-box rounded-none p-7 space-y-6 relative overflow-hidden">
            {/* Ambient Corner Accent */}
            <div className="absolute -top-24 -right-24 w-48 h-48 bg-[#0070f3]/20 rounded-none blur-3xl pointer-events-none" />
            <div className="absolute -bottom-24 -left-24 w-48 h-48 bg-[#00e599]/15 rounded-none blur-3xl pointer-events-none" />

            {/* Header Badge & Title */}
            <div className="space-y-2 text-center">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-none bg-[#111111] border border-[#2a2a2a] text-[11px] text-[#00e599] font-medium font-mono mb-1">
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>Coding Trainer AI Auth Hub</span>
              </div>
              <h1 className="text-2xl font-bold tracking-tight text-white">
                {user && !user.isAnonymous
                  ? "Authenticated Account"
                  : "MSc AI & Robotics Student Portal"}
              </h1>
              <p className="text-xs text-[#888888] max-w-sm mx-auto leading-relaxed">
                Secure access to syntax AST drills, spaced repetition decks, and UK Master&apos;s exam simulator.
              </p>
            </div>

            {/* Feedback Banners */}
            {error && (
              <div className="bg-[#7f1d1d]/30 border border-[#ef4444] text-[#ef4444] p-3 rounded-none text-xs font-mono flex items-start gap-2 animate-in fade-in slide-in-from-top-1">
                <span className="shrink-0">⚠️</span>
                <span className="flex-1">{error}</span>
                <button onClick={() => setError(null)} className="text-[#ef4444] hover:text-white font-bold ml-1">
                  ×
                </button>
              </div>
            )}

            {successMsg && (
              <div className="bg-[#00e599]/10 border border-[#00e599]/40 text-[#00e599] p-3 rounded-none text-xs font-mono flex items-center gap-2 animate-in fade-in slide-in-from-top-1">
                <CheckCircle2 className="w-4 h-4 shrink-0" />
                <span>{successMsg}</span>
              </div>
            )}

            {/* IF USER IS LOGGED IN & NOT ANONYMOUS -> SHOW RICH AUTHENTICATED PROFILE SCREEN */}
            {user && !user.isAnonymous ? (
              <div className="space-y-5 pt-2">
                {/* Profile Card Summary Box */}
                <div className="bg-[#0d0d0d] border border-[#222222] rounded-none p-5 space-y-4 relative">
                  <div className="flex items-center gap-4">
                    {/* User Avatar Box with Clickable Edit Overlay */}
                    <div
                      onClick={() => setShowAvatarPicker(!showAvatarPicker)}
                      className="relative cursor-pointer group shrink-0"
                      title="Click to Change Avatar Picture"
                    >
                      {user.photoURL ? (
                        <img
                          src={user.photoURL}
                          alt="User Avatar"
                          className="w-14 h-14 rounded-none border-2 border-[#0070f3] group-hover:border-[#00e599] object-cover shadow-lg transition-all"
                        />
                      ) : (
                        <div className="w-14 h-14 rounded-none bg-gradient-to-br from-[#0070f3] to-[#00e599] flex items-center justify-center text-white font-bold text-xl shadow-lg border-2 border-[#0070f3] group-hover:border-[#00e599] transition-all">
                          {user.email ? user.email.charAt(0).toUpperCase() : "S"}
                        </div>
                      )}
                      <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 flex items-center justify-center text-[10px] text-white font-semibold transition-opacity">
                        Change
                      </div>
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-semibold text-sm text-white truncate">
                          {user.displayName || user.email?.split("@")[0] || "MSc Student"}
                        </span>
                        {provider && (
                          <span
                            className={`text-[10px] font-mono px-2 py-0.5 rounded-none border flex items-center gap-1 shrink-0 ${provider.color}`}
                          >
                            <provider.icon className="w-3 h-3" />
                            {provider.label}
                          </span>
                        )}
                      </div>
                      <div className="flex items-center justify-between">
                        <p className="text-xs font-mono text-[#888888] truncate">{user.email}</p>
                        <button
                          onClick={() => setShowAvatarPicker(!showAvatarPicker)}
                          className="text-[10px] font-mono text-[#0070f3] hover:underline shrink-0 ml-2 font-semibold"
                        >
                          {showAvatarPicker ? "Close Picker" : "Select Avatar"}
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Interactive Avatar Picture Picker Box */}
                  {showAvatarPicker && (
                    <div className="bg-[#111111] border border-[#2e2e2e] p-4 rounded-none space-y-3 animate-in fade-in">
                      <div className="text-xs font-semibold text-white flex items-center justify-between">
                        <span>Select Student Avatar Picture:</span>
                        {avatarUpdating && (
                          <span className="text-[10px] text-[#00e599] font-mono animate-pulse">
                            Updating Firebase...
                          </span>
                        )}
                      </div>

                      {/* Preset Gallery Grid */}
                      <div className="grid grid-cols-3 gap-2">
                        {PRESET_AVATARS.map((item, idx) => (
                          <button
                            key={idx}
                            onClick={() => handleSelectAvatar(item.url)}
                            disabled={avatarUpdating}
                            className="bg-[#0a0a0a] border border-[#222222] hover:border-[#0070f3] p-2 text-center flex flex-col items-center gap-1 transition-all group rounded-none"
                          >
                            <img src={item.url} alt={item.label} className="w-10 h-10 object-contain" />
                            <span className="text-[9px] text-[#888888] group-hover:text-white truncate w-full">
                              {item.label}
                            </span>
                          </button>
                        ))}
                      </div>

                      {/* Custom Image URL Form */}
                      <form onSubmit={handleCustomAvatarSubmit} className="pt-2 border-t border-[#222222] space-y-2">
                        <label className="text-[10px] text-[#888888] block">Or Enter Custom Image URL:</label>
                        <div className="flex gap-2">
                          <input
                            type="url"
                            value={customAvatarUrl}
                            onChange={(e) => setCustomAvatarUrl(e.target.value)}
                            placeholder="https://example.com/avatar.png"
                            className="flex-1 auth-input rounded-none px-2.5 py-1.5 text-[11px] font-mono"
                          />
                          <button
                            type="submit"
                            disabled={avatarUpdating || !customAvatarUrl.trim()}
                            className="btn-next-primary text-[11px] px-3 py-1.5 rounded-none font-semibold shrink-0"
                          >
                            Save URL
                          </button>
                        </div>
                      </form>
                    </div>
                  )}


                  <div className="border-t border-[#1f1f1f] pt-3 space-y-2 text-xs">
                    <div className="flex items-center justify-between text-[#888888]">
                      <span className="flex items-center gap-1.5">
                        <Key className="w-3.5 h-3.5 text-[#0070f3]" />
                        <span>Firebase User ID:</span>
                      </span>
                      <button
                        onClick={handleCopyUid}
                        className="flex items-center gap-1 text-white font-mono bg-[#161616] hover:bg-[#222222] border border-[#2a2a2a] px-2 py-1 rounded-none transition-colors text-[11px]"
                      >
                        <span className="truncate max-w-[130px]">{user.uid}</span>
                        {copiedUid ? <Check className="w-3 h-3 text-[#00e599]" /> : <Copy className="w-3 h-3 text-[#888888]" />}
                      </button>
                    </div>

                    <div className="flex items-center justify-between text-[#888888]">
                      <span className="flex items-center gap-1.5">
                        <Flame className="w-3.5 h-3.5 text-[#ff8800]" />
                        <span>MSc Study Streak:</span>
                      </span>
                      <span className="font-mono text-white font-semibold">
                        {analyticsData?.streak_days ? `${analyticsData.streak_days} Day${analyticsData.streak_days > 1 ? "s" : ""} (Active)` : "1 Day (Active)"}
                      </span>
                    </div>
                  </div>
                </div>


                {/* Primary Action Box Buttons Screen */}
                <div className="space-y-2.5">
                  <Link
                    href="/"
                    className="w-full btn-next-primary py-3 rounded-none text-xs font-semibold flex items-center justify-center gap-2 shadow-lg transition-all"
                  >
                    <span>Launch Studio Workspace</span>
                    <ChevronRight className="w-4 h-4" />
                  </Link>

                  <button
                    onClick={signOutUser}
                    className="w-full bg-[#111111] hover:bg-[#1f1f1f] border border-[#2e2e2e] hover:border-[#ef4444]/40 text-[#888888] hover:text-[#ef4444] py-2.5 rounded-none text-xs font-medium flex items-center justify-center gap-2 transition-all"
                  >
                    <LogOut className="w-3.5 h-3.5" />
                    <span>Sign Out of Identity Account</span>
                  </button>
                </div>
              </div>
            ) : (
              /* UNAUTHENTICATED / GUEST MODE FORM SCREEN */
              <div className="space-y-5">
                {/* PROMINENT GOOGLE AUTH BOX BUTTON SCREEN */}
                <div className="space-y-2">
                  <button
                    onClick={handleGoogleSignIn}
                    disabled={googleLoading || loading}
                    className="w-full btn-google-auth py-3 px-4 rounded-none text-xs font-semibold flex items-center justify-center gap-3 shadow-md"
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
                    <span>Continue with Google OAuth</span>
                  </button>
                  <p className="text-[10px] text-center text-[#666666]">
                    One-click single sign-on with your University or Personal Google Account
                  </p>
                </div>

                {/* Straight Line Divider */}
                <div className="flex items-center gap-3 my-1">
                  <div className="flex-1 h-[1px] bg-[#222222]" />
                  <span className="text-[10px] text-[#666666] uppercase tracking-wider font-semibold font-mono">
                    Or Use Email / Pass
                  </span>
                  <div className="flex-1 h-[1px] bg-[#222222]" />
                </div>

                {/* Auth Mode Box Tab Bar */}
                <div className="grid grid-cols-2 p-1 bg-[#0d0d0d] border border-[#222222] rounded-none text-xs">
                  <button
                    type="button"
                    onClick={() => {
                      setActiveTab("signin");
                      setError(null);
                    }}
                    className={`py-2 rounded-none font-medium transition-all ${
                      activeTab === "signin"
                        ? "bg-[#1f1f1f] text-white shadow-sm border border-[#333333]"
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
                    }}
                    className={`py-2 rounded-none font-medium transition-all ${
                      activeTab === "signup"
                        ? "bg-[#1f1f1f] text-white shadow-sm border border-[#333333]"
                        : "text-[#888888] hover:text-white"
                    }`}
                  >
                    Create Account
                  </button>
                </div>

                {/* Form Controls */}
                <form onSubmit={handleEmailFormSubmit} className="space-y-4">
                  <div className="space-y-1.5">
                    <label className="text-[11px] text-[#a1a1a1] font-medium block">
                      University or Student Email
                    </label>
                    <div className="relative">
                      <Mail className="w-4 h-4 absolute left-3.5 top-3 text-[#666666]" />
                      <input
                        type="email"
                        required
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="student@university.ac.uk"
                        className="w-full auth-input rounded-none py-2.5 pl-10 pr-4 text-xs font-mono"
                      />
                    </div>
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-[11px] text-[#a1a1a1] font-medium block">
                      Account Password
                    </label>
                    <div className="relative">
                      <Lock className="w-4 h-4 absolute left-3.5 top-3 text-[#666666]" />
                      <input
                        type={showPassword ? "text" : "password"}
                        required
                        minLength={6}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="••••••••••••"
                        className="w-full auth-input rounded-none py-2.5 pl-10 pr-10 text-xs font-mono"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-3 text-[#666666] hover:text-white transition-colors"
                      >
                        {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>

                  <button
                    type="submit"
                    disabled={isSubmitting || loading}
                    className="w-full btn-next-primary py-3 rounded-none text-xs font-semibold flex items-center justify-center gap-2 shadow-lg transition-all"
                  >
                    {isSubmitting ? (
                      <div className="w-4 h-4 border-2 border-black/30 border-t-black rounded-none animate-spin" />
                    ) : activeTab === "signup" ? (
                      <>
                        <UserPlus className="w-4 h-4" />
                        <span>Register MSc Student Account</span>
                      </>
                    ) : (
                      <>
                        <LogIn className="w-4 h-4" />
                        <span>Sign In to Student Account</span>
                      </>
                    )}
                  </button>
                </form>

                {/* Secondary Option: Guest Sign-In Button */}
                <div className="pt-3 border-t border-[#222222] flex items-center justify-between text-xs">
                  <span className="text-[#666666]">No account yet?</span>
                  <button
                    type="button"
                    onClick={handleGuestSignIn}
                    disabled={isSubmitting}
                    className="text-[#00e599] hover:underline flex items-center gap-1 font-medium"
                  >
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>Instant Guest Pass Access</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>


      {/* Footer */}
      <footer className="relative z-10 w-full max-w-7xl mx-auto px-6 py-6 text-center text-[11px] text-[#666666]">
        <p>Coding Trainer AI Studio • MSc AI & Robotics Transition Portal</p>
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

