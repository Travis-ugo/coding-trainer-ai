"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { doc, setDoc, onSnapshot, serverTimestamp, getDoc } from "firebase/firestore";
import { db } from "../../lib/firebase";
import { useAuth } from "./AuthContext";

export interface TopicGrade {
  topic_id: string;
  topic_name: string;
  score_percentage: number;
  grade_label: string;
  color_hex: string;
}

export interface AnalyticsData {
  user_name: string;
  background: string;
  overall_percentage: number;
  predicted_grade: string;
  distinction_badges_count: number;
  streak_days: number;
  topic_grades: TopicGrade[];
}

export interface RoutineTask {
  title: string;
  duration_minutes: number;
  task_type: string;
  details: string;
}

export interface RoutineData {
  date_str: string;
  total_minutes: number;
  tasks: RoutineTask[];
}

export interface Flashcard {
  card_id: string;
  prompt: string;
  answer: string;
  analogy?: string;
  repetition_number?: number;
  interval_days?: number;
}

export interface FlashcardDeck {
  id: string;
  title: string;
  cards: Flashcard[];
}

export interface ROS2Data {
  architecture: string;
  topic_stream: Array<{ topic: string; data: Record<string, unknown> }>;
  kinematics: { joint_angles_deg: number[]; end_effector_xy: number[] };
}

export interface SyntaxEvalResult {
  passed: boolean;
  score: number;
  ast_valid: boolean;
  feedback: string;
}

export interface GeminiResponse {
  analogy: string;
  conceptual_hint: string;
  socratic_question: string;
}

export interface ModuleItem {
  id: string;
  title: string;
  summary: string;
  non_cs_analogy: string;
  syntax_guide: string;
  order: number;
}

interface TrainerContextType {
  activeTool: string;
  setActiveTool: (tool: string) => void;
  selectedModule: string;
  setSelectedModule: (mod: string) => void;
  modulesData: ModuleItem[];
  analyticsData: AnalyticsData | null;
  routineData: RoutineData | null;
  flashcardDecks: FlashcardDeck[];
  ros2Data: ROS2Data | null;
  loading: boolean;
  error: string | null;
  rateFlashcard: (cardId: string, rating: number) => Promise<void>;
  evaluateSyntax: (code: string) => Promise<SyntaxEvalResult>;
  askGemini: (prompt: string) => Promise<GeminiResponse>;
}

const TrainerContext = createContext<TrainerContextType | undefined>(undefined);

export const TrainerProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useAuth();

  const [activeTool, setActiveTool] = useState<string>("analytics");
  const [selectedModule, setSelectedModule] = useState<string>("py_mod_01");

  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [routineData, setRoutineData] = useState<RoutineData | null>(null);
  const [flashcardDecks, setFlashcardDecks] = useState<FlashcardDeck[]>([]);
  const [ros2Data, setRos2Data] = useState<ROS2Data | null>(null);
  const [modulesData, setModulesData] = useState<ModuleItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // 1. Listen to real-time Firestore user progress document
  useEffect(() => {
    if (!user?.uid) return;

    const userDocRef = doc(db, "users", user.uid);
    const unsubscribe = onSnapshot(
      userDocRef,
      (docSnap) => {
        if (docSnap.exists()) {
          const fsData = docSnap.data();
          setAnalyticsData((prev) => {
            if (!prev) return prev;
            return {
              ...prev,
              overall_percentage: fsData.overall_percentage ?? prev.overall_percentage,
              predicted_grade: fsData.predicted_grade ?? prev.predicted_grade,
              distinction_badges_count: fsData.distinction_badges_count ?? prev.distinction_badges_count,
              streak_days: fsData.streak_days ?? prev.streak_days,
            };
          });
        }
      },
      (err) => {
        console.warn("Firestore snapshot listener warning:", err);
      }
    );

    return () => unsubscribe();
  }, [user?.uid]);

  // 2. Initial synchronization with API engine & Firestore
  useEffect(() => {
    async function syncBackendData() {
      setLoading(true);
      setError(null);
      let fetchErrors: string[] = [];

      try {
        const resModules = await fetch("/api/modules");
        if (resModules.ok) {
          const data = await resModules.json();
          if (Array.isArray(data)) {
            setModulesData(data);
          }
        } else {
          fetchErrors.push("Modules");
        }

        const resAnalytics = await fetch("/api/analytics");
        if (resAnalytics.ok) {
          const data = await resAnalytics.json();
          setAnalyticsData(data);

          // Save/Sync initial analytics baseline to Firestore if logged in
          if (user?.uid) {
            try {
              const userRef = doc(db, "users", user.uid);
              const userSnap = await getDoc(userRef);
              if (!userSnap.exists()) {
                await setDoc(
                  userRef,
                  {
                    email: user.email || "guest@trainer.ai",
                    is_anonymous: user.isAnonymous,
                    overall_percentage: data.overall_percentage,
                    predicted_grade: data.predicted_grade,
                    distinction_badges_count: data.distinction_badges_count,
                    streak_days: data.streak_days,
                    created_at: serverTimestamp(),
                    updated_at: serverTimestamp(),
                  },
                  { merge: true }
                );
              }
            } catch (fsErr) {
              console.warn("Firestore user record init warning:", fsErr);
            }
          }
        } else {
          fetchErrors.push("Analytics");
        }

        const resRoutine = await fetch("/api/routine");
        if (resRoutine.ok) {
          const data = await resRoutine.json();
          setRoutineData(data);
        } else {
          fetchErrors.push("Routine");
        }

        const resSRS = await fetch("/api/flashcards");
        if (resSRS.ok) {
          const data = await resSRS.json();
          setFlashcardDecks(Array.isArray(data) ? data : []);
        } else {
          fetchErrors.push("Flashcards");
        }

        const resROS = await fetch("/api/ros2");
        if (resROS.ok) {
          const data = await resROS.json();
          setRos2Data(data);
        } else {
          fetchErrors.push("ROS 2");
        }
      } catch (err: unknown) {
        const msg = err instanceof Error ? err.message : "Network error connecting to API bridge";
        setError(`Failed to sync backend data: ${msg}`);
      } finally {
        setLoading(false);
        if (fetchErrors.length > 0) {
          setError(`Backend service warning: Could not fetch ${fetchErrors.join(", ")}`);
        }
      }
    }

    syncBackendData();
  }, [user?.uid]);

  const rateFlashcard = async (cardId: string, rating: number) => {
    const res = await fetch("/api/flashcards", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ card_id: cardId, rating }),
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.error || "Failed to rate flashcard");
    }

    // Persist flashcard review event directly in Firestore subcollection
    if (user?.uid) {
      try {
        const cardRef = doc(db, "users", user.uid, "flashcards", cardId);
        await setDoc(
          cardRef,
          {
            card_id: cardId,
            last_rating: rating,
            last_reviewed: serverTimestamp(),
          },
          { merge: true }
        );
      } catch (fsErr) {
        console.warn("Firestore flashcard sync warning:", fsErr);
      }
    }
  };

  const evaluateSyntax = async (code: string): Promise<SyntaxEvalResult> => {
    const res = await fetch("/api/syntax", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || "Syntax evaluation failed");
    }

    // Persist AST submission attempt and updated user performance in Firestore
    if (user?.uid) {
      try {
        const subRef = doc(db, "users", user.uid, "syntax_submissions", `sub_${Date.now()}`);
        await setDoc(subRef, {
          module_id: selectedModule,
          score: data.score || 0,
          ast_valid: data.ast_valid || false,
          feedback: data.feedback || "",
          code_length: code.length,
          timestamp: serverTimestamp(),
        });

        // Update overall percentage in user's root Firestore document
        const userRef = doc(db, "users", user.uid);
        await setDoc(
          userRef,
          {
            last_submission_score: data.score || 0,
            updated_at: serverTimestamp(),
          },
          { merge: true }
        );
      } catch (fsErr) {
        console.warn("Firestore syntax submission sync warning:", fsErr);
      }
    }

    return data;
  };


  const askGemini = async (prompt: string): Promise<GeminiResponse> => {
    const res = await fetch("/api/ai", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || "Gemini AI Tutor request failed");
    }
    return data;
  };

  return (
    <TrainerContext.Provider
      value={{
        activeTool,
        setActiveTool,
        selectedModule,
        setSelectedModule,
        modulesData,
        analyticsData,
        routineData,
        flashcardDecks,
        ros2Data,
        loading,
        error,
        rateFlashcard,
        evaluateSyntax,
        askGemini,
      }}
    >
      {children}
    </TrainerContext.Provider>
  );
};

export const useTrainerContext = () => {
  const context = useContext(TrainerContext);
  if (!context) {
    throw new Error("useTrainerContext must be used within TrainerProvider");
  }
  return context;
};

