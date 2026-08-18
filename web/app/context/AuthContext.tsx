"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import {
  User,
  onAuthStateChanged,
  signInWithPopup,
  signInWithRedirect,
  getRedirectResult,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  sendPasswordResetEmail,
  signInAnonymously,
  signOut,
  updateProfile,
} from "firebase/auth";
import { doc, setDoc, serverTimestamp } from "firebase/firestore";
import { auth, db, googleProvider } from "../../lib/firebase";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signInWithGoogle: () => Promise<void>;
  signInWithEmail: (e: string, p: string) => Promise<void>;
  signUpWithEmail: (e: string, p: string) => Promise<void>;
  resetPasswordWithEmail: (e: string) => Promise<void>;
  signInAnonymouslyUser: () => Promise<void>;
  signOutUser: () => Promise<void>;
  updateUserProfile: (photoURL: string, displayName?: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Sync user profile data to Firestore
  const syncUserToFirestore = async (currentUser: User) => {
    if (!currentUser || !currentUser.uid) return;
    try {
      const userRef = doc(db, "users", currentUser.uid);
      await setDoc(
        userRef,
        {
          uid: currentUser.uid,
          email: currentUser.email || (currentUser.isAnonymous ? "guest@trainer.ai" : ""),
          displayName: currentUser.displayName || (currentUser.isAnonymous ? "Guest Student" : "MSc Student"),
          photoURL: currentUser.photoURL || "",
          isAnonymous: currentUser.isAnonymous,
          providerId: currentUser.providerData[0]?.providerId || (currentUser.isAnonymous ? "anonymous" : "password"),
          updated_at: serverTimestamp(),
        },
        { merge: true }
      );
    } catch (fsErr: any) {
      if (fsErr?.code !== "permission-denied" && fsErr?.message?.indexOf("permission") === -1) {
        console.warn("Firestore user profile sync notice:", fsErr);
      }
    }
  };

  useEffect(() => {
    // Process redirect result if page returned from Google OAuth redirect
    getRedirectResult(auth)
      .then((res) => {
        if (res?.user) {
          setUser(res.user);
          syncUserToFirestore(res.user).catch((err) => {
            console.warn("Redirect profile sync notice:", err);
          });
        }
      })
      .catch((err) => {
        console.warn("Redirect sign-in notice:", err);
      });

    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      if (currentUser) {
        setUser(currentUser);
        syncUserToFirestore(currentUser).catch((err) => {
          console.warn("Firestore user profile sync notice:", err);
        });
      } else {
        setUser(null);
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const signInWithGoogle = async () => {
    setLoading(true);
    try {
      const res = await signInWithPopup(auth, googleProvider);
      if (res.user) {
        setUser(res.user);
        syncUserToFirestore(res.user).catch((err) => {
          console.warn("Firestore user profile sync notice:", err);
        });
      }
    } catch (err: any) {
      if (
        err?.code === "auth/popup-blocked" ||
        err?.code === "auth/cancelled-popup-request" ||
        err?.message?.includes("Cross-Origin-Opener-Policy")
      ) {
        await signInWithRedirect(auth, googleProvider);
      } else if (err?.code === "auth/popup-closed-by-user") {
        console.log("Google sign-in popup was closed by user.");
      } else {
        throw err;
      }
    } finally {
      setLoading(false);
    }
  };

  const signInWithEmail = async (email: string, pass: string) => {
    setLoading(true);
    try {
      const res = await signInWithEmailAndPassword(auth, email, pass);
      if (res.user) {
        setUser(res.user);
        syncUserToFirestore(res.user).catch((err) => {
          console.warn("Firestore user profile sync notice:", err);
        });
      }
    } finally {
      setLoading(false);
    }
  };

  const signUpWithEmail = async (email: string, pass: string) => {
    setLoading(true);
    try {
      const res = await createUserWithEmailAndPassword(auth, email, pass);
      if (res.user) {
        setUser(res.user);
        syncUserToFirestore(res.user).catch((err) => {
          console.warn("Firestore user profile sync notice:", err);
        });
      }
    } finally {
      setLoading(false);
    }
  };

  const resetPasswordWithEmail = async (email: string) => {
    setLoading(true);
    try {
      await sendPasswordResetEmail(auth, email);
    } finally {
      setLoading(false);
    }
  };

  const signInAnonymouslyUser = async () => {
    setLoading(true);
    try {
      const res = await signInAnonymously(auth);
      if (res.user) {
        setUser(res.user);
        syncUserToFirestore(res.user).catch((err) => {
          console.warn("Firestore user profile sync notice:", err);
        });
      }
    } catch (err: unknown) {
      console.warn("Guest sign-in attempt:", err);
      throw new Error("Guest access is currently disabled on Firebase. Please use Google or Email Sign In.");
    } finally {
      setLoading(false);
    }
  };

  const signOutUser = async () => {
    setLoading(true);
    try {
      await signOut(auth);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const updateUserProfile = async (photoURL: string, displayName?: string) => {
    if (!auth.currentUser) return;
    setLoading(true);
    try {
      await updateProfile(auth.currentUser, {
        photoURL,
        displayName: displayName ?? auth.currentUser.displayName ?? undefined,
      });
      // Force refresh user reference
      setUser({ ...auth.currentUser });
      await syncUserToFirestore(auth.currentUser);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        signInWithGoogle,
        signInWithEmail,
        signUpWithEmail,
        resetPasswordWithEmail,
        signInAnonymouslyUser,
        signOutUser,
        updateUserProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};


export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
