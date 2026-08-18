"use client";

import React, { createContext, useContext, useEffect, useState, useCallback } from "react";
import { doc, setDoc, serverTimestamp, collection, getDocs, query, limit, orderBy } from "firebase/firestore";
import { db } from "../../lib/firebase";
import { useAuth } from "./AuthContext";

export interface LoginRecord {
  id: string;
  timestamp: string;
  email: string;
  provider: string; // "google.com" | "password" | "anonymous"
  status: "SUCCESS" | "FAILED" | "LOGOUT";
  userAgent: string;
}

export interface SessionRecord {
  sessionId: string;
  startTime: string;
  lastActive: string;
  durationSeconds: number;
  status: "ACTIVE" | "ENDED";
  device: string;
  userEmail: string;
}

export interface LogEntry {
  id: string;
  timestamp: string;
  level: "INFO" | "SUCCESS" | "WARN" | "ERROR";
  category: "AUTH" | "SESSION" | "NAVIGATION" | "API" | "SYNTAX";
  message: string;
  details?: Record<string, unknown> | string;
}

interface SessionContextType {
  sessionId: string;
  sessionDuration: number;
  activeSessionsCount: number;
  logins: LoginRecord[];
  sessions: SessionRecord[];
  logs: LogEntry[];
  logEvent: (
    category: LogEntry["category"],
    level: LogEntry["level"],
    message: string,
    details?: Record<string, unknown> | string
  ) => void;
  clearLogs: () => void;
}

const SessionContext = createContext<SessionContextType | undefined>(undefined);

const STORAGE_KEY_LOGS = "coding_trainer_activity_logs";
const STORAGE_KEY_LOGINS = "coding_trainer_login_history";
const STORAGE_KEY_SESSIONS = "coding_trainer_sessions";

export const SessionProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useAuth();

  const [sessionId] = useState<string>(() => `sess_${Math.random().toString(36).substring(2, 9)}_${Date.now().toString(36)}`);
  const [startTime] = useState<number>(() => Date.now());
  const [sessionDuration, setSessionDuration] = useState<number>(0);
  const [activeSessionsCount, setActiveSessionsCount] = useState<number>(1);

  const [logins, setLogins] = useState<LoginRecord[]>([]);
  const [sessions, setSessions] = useState<SessionRecord[]>([]);
  const [logs, setLogs] = useState<LogEntry[]>([]);

  // Function to print formatted logs to browser console & record in state
  const logEvent = useCallback(
    (
      category: LogEntry["category"],
      level: LogEntry["level"],
      message: string,
      details?: Record<string, unknown> | string
    ) => {
      const entry: LogEntry = {
        id: `log_${Date.now()}_${Math.random().toString(36).substring(2, 6)}`,
        timestamp: new Date().toLocaleTimeString(),
        level,
        category,
        message,
        details,
      };

      // Formatted console printout
      const badgeColors: Record<LogEntry["category"], string> = {
        AUTH: "background: #0070f3; color: white;",
        SESSION: "background: #00e599; color: black;",
        NAVIGATION: "background: #7928ca; color: white;",
        API: "background: #f5a623; color: black;",
        SYNTAX: "background: #ff0080; color: white;",
      };

      console.log(
        `%c[${category}]%c [${level}] ${message}`,
        `${badgeColors[category]} font-weight: bold; padding: 2px 5px; border-radius: 2px;`,
        "color: #888; font-weight: bold;",
        details || ""
      );

      setLogs((prev) => [entry, ...prev.slice(0, 199)]);
    },
    []
  );

  const clearLogs = () => {
    setLogs([]);
  };

  // Load stored logins & sessions on mount
  useEffect(() => {
    try {
      const savedLogs = localStorage.getItem(STORAGE_KEY_LOGS);
      if (savedLogs) setLogs(JSON.parse(savedLogs));

      const savedLogins = localStorage.getItem(STORAGE_KEY_LOGINS);
      if (savedLogins) setLogins(JSON.parse(savedLogins));

      const savedSessions = localStorage.getItem(STORAGE_KEY_SESSIONS);
      if (savedSessions) setSessions(JSON.parse(savedSessions));
    } catch {
      // Ignore storage errors
    }
  }, []);

  // Save logs to localStorage
  useEffect(() => {
    try {
      if (logs.length > 0) {
        localStorage.setItem(STORAGE_KEY_LOGS, JSON.stringify(logs.slice(0, 100)));
      }
    } catch {}
  }, [logs]);

  // Save logins to localStorage
  useEffect(() => {
    try {
      if (logins.length > 0) {
        localStorage.setItem(STORAGE_KEY_LOGINS, JSON.stringify(logins.slice(0, 50)));
      }
    } catch {}
  }, [logins]);

  // Save sessions to localStorage
  useEffect(() => {
    try {
      if (sessions.length > 0) {
        localStorage.setItem(STORAGE_KEY_SESSIONS, JSON.stringify(sessions.slice(0, 50)));
      }
    } catch {}
  }, [sessions]);

  // Session Duration Ticker & Heartbeat
  useEffect(() => {
    logEvent("SESSION", "INFO", `Session initialized: ${sessionId}`, {
      sessionId,
      startTime: new Date(startTime).toLocaleTimeString(),
      userAgent: typeof navigator !== "undefined" ? navigator.userAgent : "SSR",
    });

    const timer = setInterval(() => {
      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      setSessionDuration(elapsed);
    }, 1000);

    return () => clearInterval(timer);
  }, [sessionId, startTime, logEvent]);

  // Track User Logins & Auth State transitions
  useEffect(() => {
    if (!user) {
      logEvent("AUTH", "INFO", "User state: Unauthenticated / Signed Out");
      return;
    }

    const providerId = user.providerData[0]?.providerId || (user.isAnonymous ? "anonymous" : "password");
    const userEmail = user.email || (user.isAnonymous ? "Guest Account" : user.uid);

    logEvent("AUTH", "SUCCESS", `User Signed In: ${userEmail}`, {
      uid: user.uid,
      email: user.email,
      providerId,
      isAnonymous: user.isAnonymous,
    });

    const newLoginRecord: LoginRecord = {
      id: `login_${Date.now()}`,
      timestamp: new Date().toLocaleString(),
      email: userEmail,
      provider: providerId === "google.com" ? "Google OAuth" : providerId === "anonymous" ? "Guest Pass" : "Email & Password",
      status: "SUCCESS",
      userAgent: typeof navigator !== "undefined" ? navigator.userAgent.split(") ")[0] + ")" : "Unknown Device",
    };

    setLogins((prev) => {
      // Prevent duplicate rapid logs for same user
      if (prev.length > 0 && prev[0].email === userEmail && Date.now() - new Date(prev[0].timestamp).getTime() < 3000) {
        return prev;
      }
      return [newLoginRecord, ...prev];
    });

    // Update active sessions list
    const currentSessionRecord: SessionRecord = {
      sessionId,
      startTime: new Date(startTime).toLocaleTimeString(),
      lastActive: new Date().toLocaleTimeString(),
      durationSeconds: sessionDuration,
      status: "ACTIVE",
      device: typeof navigator !== "undefined" ? navigator.platform : "Desktop",
      userEmail,
    };

    setSessions((prev) => {
      const exists = prev.some((s) => s.sessionId === sessionId);
      if (exists) {
        return prev.map((s) => (s.sessionId === sessionId ? { ...s, lastActive: new Date().toLocaleTimeString(), durationSeconds: sessionDuration } : s));
      }
      return [currentSessionRecord, ...prev];
    });

    // Record session heartbeat to Firestore if online
    const userRef = doc(db, "users", user.uid, "sessions", sessionId);
    setDoc(
      userRef,
      {
        sessionId,
        userEmail,
        providerId,
        started_at: serverTimestamp(),
        last_heartbeat: serverTimestamp(),
        status: "ACTIVE",
      },
      { merge: true }
    ).catch(() => {});
  }, [user?.uid, sessionId, startTime, logEvent]);

  return (
    <SessionContext.Provider
      value={{
        sessionId,
        sessionDuration,
        activeSessionsCount,
        logins,
        sessions,
        logs,
        logEvent,
        clearLogs,
      }}
    >
      {children}
    </SessionContext.Provider>
  );
};

export const useSession = () => {
  const context = useContext(SessionContext);
  if (!context) {
    throw new Error("useSession must be used within a SessionProvider");
  }
  return context;
};
