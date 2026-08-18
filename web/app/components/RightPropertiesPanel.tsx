"use client";

import React from "react";
import { useTrainerContext } from "../context/TrainerContext";
import { Award, Zap, Clock, CheckCircle2, ChevronRight } from "lucide-react";

export const RightPropertiesPanel: React.FC = () => {
  const { analyticsData, loading } = useTrainerContext();

  const distinctionBadges = (analyticsData?.topic_grades || [])
    .filter((g) => g.score_percentage >= 70)
    .map((g) => {
      const parts = g.topic_name.split(" ");
      return parts.length > 2 ? `${parts[0]} ${parts[1]}` : g.topic_name;
    });

  return (
    <aside className="w-72 bg-[#0a0a0a] border-l border-[#222222] flex flex-col h-[calc(100vh-3.5rem)] shrink-0">
      {/* Dashboard Inspector Header */}
      <div className="px-4 py-3 border-b border-[#222222] text-xs font-semibold text-[#888888] uppercase tracking-wider flex items-center justify-between">
        <span>Degree Metrics</span>
        <ChevronRight className="w-3.5 h-3.5 text-[#666666]" />
      </div>

      {/* Inspector Details */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6 text-xs">
        {/* Master's Degree Status Box */}
        <div>
          <div className="text-[10px] font-semibold text-[#666666] uppercase tracking-wider mb-2">
            Degree Predicted Status
          </div>
          <div className="bg-[#111111] border border-[#222222] p-4 rounded-none space-y-2.5">
            <div className="flex items-center justify-between">
              <span className="text-[#888888]">Target Level:</span>
              <span className="font-bold text-[#00e599]">
                {analyticsData?.predicted_grade || (loading ? "Syncing..." : "--")}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-[#888888]">Predicted Score:</span>
              <span className="font-semibold text-white font-mono">
                {analyticsData?.overall_percentage != null ? `${analyticsData.overall_percentage.toFixed(1)}%` : "--"}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-[#888888]">Pass Threshold:</span>
              <span className="font-semibold text-[#3b82f6] font-mono">50.0% Pass</span>
            </div>
          </div>
        </div>

        {/* Distinction Badges Showcase */}
        <div>
          <div className="text-[10px] font-semibold text-[#666666] uppercase tracking-wider mb-2 flex items-center justify-between">
            <span>Distinction Badges ({analyticsData?.distinction_badges_count ?? distinctionBadges.length} Earned)</span>
            <Award className="w-3.5 h-3.5 text-[#00e599]" />
          </div>
          {distinctionBadges.length > 0 ? (
            <div className="grid grid-cols-2 gap-2">
              {distinctionBadges.map((badge, idx) => (
                <div
                  key={idx}
                  className="bg-[#111111] border border-[#222222] p-2 rounded-none text-[11px] flex items-center gap-1.5 text-white"
                >
                  <CheckCircle2 className="w-3 h-3 text-[#00e599] shrink-0" />
                  <span className="truncate">{badge}</span>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-[11px] text-[#888888] bg-[#111111] p-3 rounded-none border border-[#222222]">
              {loading ? "Syncing badges..." : "No distinction badges earned yet"}
            </div>
          )}
        </div>

        {/* Pacing & Timing Metrics */}
        <div>
          <div className="text-[10px] font-semibold text-[#666666] uppercase tracking-wider mb-2 flex items-center justify-between">
            <span>Pacing Metrics</span>
            <Clock className="w-3.5 h-3.5 text-[#0070f3]" />
          </div>
          <div className="bg-[#111111] border border-[#222222] p-3.5 rounded-none space-y-2">
            <div className="flex justify-between items-center text-[11px]">
              <span className="text-[#888888]">Avg Time / Q:</span>
              <span className="font-semibold text-white font-mono">
                {analyticsData ? "45s (Optimal)" : "--"}
              </span>
            </div>
            <div className="flex justify-between items-center text-[11px]">
              <span className="text-[#888888]">Pacing Status:</span>
              <span className="font-bold text-[#00e599]">
                {analyticsData?.predicted_grade ? "UK Distinction Pace" : "--"}
              </span>
            </div>

          </div>
        </div>

        {/* Power Streak */}
        <div>
          <div className="text-[10px] font-semibold text-[#666666] uppercase tracking-wider mb-2 flex items-center justify-between">
            <span>Power Streak</span>
            <Zap className="w-3.5 h-3.5 text-[#eab308]" />
          </div>
          <div className="bg-[#111111] border border-[#222222] p-3.5 rounded-none flex items-center justify-between">
            <span className="text-white font-medium">
              {analyticsData?.streak_days != null ? `${analyticsData.streak_days} Days Streak` : "--"}
            </span>
            <span className="text-[10px] bg-[#eab308]/15 border border-[#eab308]/30 text-[#eab308] font-bold px-2 py-0.5 rounded-none">
              🔥 Active
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
};
