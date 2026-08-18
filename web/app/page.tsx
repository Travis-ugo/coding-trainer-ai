"use client";

import React from "react";
import { AuthProvider } from "./context/AuthContext";
import { TrainerProvider, useTrainerContext } from "./context/TrainerContext";
import { TopToolbar } from "./components/TopToolbar";
import { LeftSidebar } from "./components/LeftSidebar";
import { CanvasWorkspace } from "./components/CanvasWorkspace";
import { RightPropertiesPanel } from "./components/RightPropertiesPanel";

function MainStudioWorkspace() {
  const { activeTool, setActiveTool, selectedModule, setSelectedModule } = useTrainerContext();

  return (
    <div className="flex flex-col h-screen w-screen bg-[#000000] overflow-hidden select-none">
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
  return (
    <AuthProvider>
      <TrainerProvider>
        <MainStudioWorkspace />
      </TrainerProvider>
    </AuthProvider>
  );
}

