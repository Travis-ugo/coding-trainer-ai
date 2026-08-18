"use client";

import React from "react";
import { AuthProvider } from "./context/AuthContext";
import { TrainerProvider } from "./context/TrainerContext";

export default function Providers({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <TrainerProvider>{children}</TrainerProvider>
    </AuthProvider>
  );
}
