"use client";

import React, { useState } from "react";
import { TopToolbar } from "./components/TopToolbar";
import { LeftSidebar } from "./components/LeftSidebar";
import { CanvasWorkspace } from "./components/CanvasWorkspace";
import { RightPropertiesPanel } from "./components/RightPropertiesPanel";

export default function Page() {
  const [activeTool, setActiveTool] = useState<string>("analytics");
  const [selectedModule, setSelectedModule] = useState<string>("py_mod_01");

  return (
    <div className="flex flex-col h-screen w-screen bg-[#1e1e1e] overflow-hidden select-none">
      {/* Top Figma App Bar Toolbar */}
      <TopToolbar
        activeTool={activeTool}
        setActiveTool={setActiveTool}
        aiActive={true}
      />

      {/* 3-Pane Figma Workspace Layout */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Navigator & Layers Tree */}
        <LeftSidebar
          activeTool={activeTool}
          setActiveTool={setActiveTool}
          selectedModule={selectedModule}
          setSelectedModule={setSelectedModule}
        />

        {/* Center Infinite Main Canvas */}
        <CanvasWorkspace
          activeTool={activeTool}
          selectedModule={selectedModule}
        />

        {/* Right Properties & Inspector Panel */}
        <RightPropertiesPanel />
      </div>
    </div>
  );
}
