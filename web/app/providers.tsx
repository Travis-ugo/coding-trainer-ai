"use client";

import React from "react";
import { AuthProvider } from "./context/AuthContext";
import { SessionProvider } from "./context/SessionContext";
import { TrainerProvider } from "./context/TrainerContext";

export default function Providers({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <SessionProvider>
        <TrainerProvider>{children}</TrainerProvider>
      </SessionProvider>
    </AuthProvider>
  );
}
