"use client";

import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { TrainerProvider, useTrainerContext } from "./context/TrainerContext";
import { TopToolbar } from "./components/TopToolbar";
import { LeftSidebar } from "./components/LeftSidebar";
import { CanvasWorkspace } from "./components/CanvasWorkspace";
import { RightPropertiesPanel } from "./components/RightPropertiesPanel";

function MainStudioWorkspace() {
  const { user, loading } = useAuth();
  const router = useRouter();
  const { activeTool, setActiveTool, selectedModule, setSelectedModule } = useTrainerContext();

  useEffect(() => {
    if (!loading && !user) {
      window.location.href = "/auth/signin";
    }
  }, [user, loading]);

  if (loading) {
    return (
      <div className="h-screen w-screen bg-[#000000] flex flex-col items-center justify-center text-white space-y-3 font-mono text-xs">
        <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-none animate-spin" />
        <p className="text-[#888888]">Loading Coding Trainer AI...</p>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="flex flex-col h-screen w-screen bg-[#000000] overflow-hidden">
      {/* Top App Bar Toolbar */}
      <TopToolbar
        activeTool={activeTool}
        setActiveTool={setActiveTool}
        aiActive={true}
      />

      {/* 3-Pane Workspace Layout */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Navigator & Layers Tree */}
        <LeftSidebar
          activeTool={activeTool}
          setActiveTool={setActiveTool}
          selectedModule={selectedModule}
          setSelectedModule={setSelectedModule}
        />

        {/* Center Main Canvas */}
        <CanvasWorkspace
          activeTool={activeTool}
          selectedModule={selectedModule}
        />

        {/* Right Properties Inspector */}
        <RightPropertiesPanel />
      </div>
    </div>
  );
}

export default function Page() {
  return <MainStudioWorkspace />;
}

