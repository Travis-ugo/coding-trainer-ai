"use client";

import React, { useState } from "react";
import { useSession, LogEntry } from "../context/SessionContext";
import { useAuth } from "../context/AuthContext";
import {
  X,
  Activity,
  UserCheck,
  Clock,
  Terminal,
  ShieldCheck,
  Trash2,
  Filter,
  CheckCircle2,
  AlertCircle,
  Info,
  Monitor,
} from "lucide-react";

interface ActivityLogModalProps {
  isOpen: boolean;
  onClose: () => void;
}

type TabType = "logins" | "sessions" | "logs";

export const ActivityLogModal: React.FC<ActivityLogModalProps> = ({ isOpen, onClose }) => {
  const { user } = useAuth();
  const {
    sessionId,
    sessionDuration,
    activeSessionsCount,
    logins,
    sessions,
    logs,
    clearLogs,
  } = useSession();

  const [activeTab, setActiveTab] = useState<TabType>("logins");
  const [filterCategory, setFilterCategory] = useState<string>("ALL");

  if (!isOpen) return null;

  const formatDuration = (seconds: number) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hrs.toString().padStart(2, "0")}:${mins
      .toString()
      .padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  const filteredLogs = logs.filter(
    (l) => filterCategory === "ALL" || l.category === filterCategory
  );

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 font-mono text-xs">
      <div className="bg-[#0a0a0a] border border-[#222222] rounded-none max-w-4xl w-full h-[80vh] flex flex-col shadow-2xl relative overflow-hidden">
        {/* Modal Top Header Bar */}
        <div className="bg-[#000000] border-b border-[#222222] px-5 py-3.5 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 text-[#00e599] font-bold text-xs tracking-wider">
              <span className="w-2 h-2 rounded-full bg-[#00e599] animate-pulse" />
              <span>LIVE MONITOR & SESSION DIAGNOSTICS</span>
            </div>
            <span className="text-[#333333]">|</span>
            <span className="text-[#888888] text-[11px]">
              Session: <span className="text-white font-semibold">{sessionId}</span>
            </span>
          </div>

          <button
            onClick={onClose}
            className="text-[#888888] hover:text-white transition-colors p-1"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Live Status Metric Cards Bar */}
        <div className="grid grid-cols-2 md:grid-cols-4 bg-[#111111] border-b border-[#222222] p-4 gap-3 shrink-0">
          {/* Card 1: Auth Status */}
          <div className="bg-[#0a0a0a] border border-[#222222] p-3 flex items-center gap-3">
            <div className="w-8 h-8 bg-[#0070f3]/10 border border-[#0070f3]/30 text-[#0070f3] flex items-center justify-center shrink-0">
              <ShieldCheck className="w-4 h-4" />
            </div>
            <div className="min-w-0">
              <p className="text-[10px] text-[#666666] uppercase">Current Identity</p>
              <p className="text-white font-bold truncate">
                {user ? (user.isAnonymous ? "Guest Pass" : user.email?.split("@")[0] || "Authenticated") : "Signed Out"}
              </p>
            </div>
          </div>

          {/* Card 2: Session Duration */}
          <div className="bg-[#0a0a0a] border border-[#222222] p-3 flex items-center gap-3">
            <div className="w-8 h-8 bg-[#00e599]/10 border border-[#00e599]/30 text-[#00e599] flex items-center justify-center shrink-0">
              <Clock className="w-4 h-4" />
            </div>
            <div>
              <p className="text-[10px] text-[#666666] uppercase">Session Uptime</p>
              <p className="text-[#00e599] font-bold">{formatDuration(sessionDuration)}</p>
            </div>
          </div>

          {/* Card 3: Logins Count */}
          <div className="bg-[#0a0a0a] border border-[#222222] p-3 flex items-center gap-3">
            <div className="w-8 h-8 bg-[#f5a623]/10 border border-[#f5a623]/30 text-[#f5a623] flex items-center justify-center shrink-0">
              <UserCheck className="w-4 h-4" />
            </div>
            <div>
              <p className="text-[10px] text-[#666666] uppercase">Recorded Logins</p>
              <p className="text-white font-bold">{logins.length} events</p>
            </div>
          </div>

          {/* Card 4: Active Sessions */}
          <div className="bg-[#0a0a0a] border border-[#222222] p-3 flex items-center gap-3">
            <div className="w-8 h-8 bg-[#7928ca]/10 border border-[#7928ca]/30 text-[#7928ca] flex items-center justify-center shrink-0">
              <Activity className="w-4 h-4" />
            </div>
            <div>
              <p className="text-[10px] text-[#666666] uppercase">Active Sessions</p>
              <p className="text-white font-bold">{sessions.length || activeSessionsCount} active</p>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex items-center justify-between px-5 bg-[#000000] border-b border-[#222222] shrink-0">
          <div className="flex items-center gap-1">
            <button
              onClick={() => setActiveTab("logins")}
              className={`py-3 px-4 text-xs font-semibold border-b-2 transition-all flex items-center gap-2 ${
                activeTab === "logins"
                  ? "border-[#0070f3] text-white bg-[#0a0a0a]"
                  : "border-transparent text-[#888888] hover:text-white"
              }`}
            >
              <UserCheck className="w-3.5 h-3.5" />
              <span>Logins History ({logins.length})</span>
            </button>

            <button
              onClick={() => setActiveTab("sessions")}
              className={`py-3 px-4 text-xs font-semibold border-b-2 transition-all flex items-center gap-2 ${
                activeTab === "sessions"
                  ? "border-[#00e599] text-white bg-[#0a0a0a]"
                  : "border-transparent text-[#888888] hover:text-white"
              }`}
            >
              <Monitor className="w-3.5 h-3.5" />
              <span>Sessions ({sessions.length})</span>
            </button>

            <button
              onClick={() => setActiveTab("logs")}
              className={`py-3 px-4 text-xs font-semibold border-b-2 transition-all flex items-center gap-2 ${
                activeTab === "logs"
                  ? "border-[#7928ca] text-white bg-[#0a0a0a]"
                  : "border-transparent text-[#888888] hover:text-white"
              }`}
            >
              <Terminal className="w-3.5 h-3.5" />
              <span>Real-Time Stream ({logs.length})</span>
            </button>
          </div>

          {activeTab === "logs" && (
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-1.5 text-[11px] text-[#888888]">
                <Filter className="w-3 h-3 text-[#666666]" />
                <select
                  value={filterCategory}
                  onChange={(e) => setFilterCategory(e.target.value)}
                  className="bg-[#111111] border border-[#222222] text-white py-1 px-2 focus:outline-none rounded-none text-xs"
                >
                  <option value="ALL">All Categories</option>
                  <option value="AUTH">Auth Events</option>
                  <option value="SESSION">Session Events</option>
                  <option value="NAVIGATION">Navigation</option>
                  <option value="API">API Engine</option>
                  <option value="SYNTAX">Syntax AST</option>
                </select>
              </div>

              <button
                onClick={clearLogs}
                title="Clear Logs"
                className="text-[#888888] hover:text-[#ef4444] transition-colors p-1"
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            </div>
          )}
        </div>

        {/* Tab Contents */}
        <div className="flex-1 overflow-y-auto p-5 bg-[#0a0a0a]">
          {/* Tab 1: Logins History */}
          {activeTab === "logins" && (
            <div className="space-y-3">
              {logins.length === 0 ? (
                <div className="text-center py-12 text-[#666666] space-y-2">
                  <UserCheck className="w-8 h-8 mx-auto opacity-30" />
                  <p>No login events recorded yet in this session.</p>
                </div>
              ) : (
                <div className="border border-[#222222] overflow-hidden">
                  <table className="w-full text-left text-xs border-collapse">
                    <thead>
                      <tr className="bg-[#111111] border-b border-[#222222] text-[#888888] text-[11px]">
                        <th className="py-2.5 px-3">Timestamp</th>
                        <th className="py-2.5 px-3">Identity / Email</th>
                        <th className="py-2.5 px-3">Provider</th>
                        <th className="py-2.5 px-3">Status</th>
                        <th className="py-2.5 px-3">Device / User Agent</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#1f1f1f]">
                      {logins.map((item) => (
                        <tr key={item.id} className="hover:bg-[#111111]/60 transition-colors">
                          <td className="py-2.5 px-3 text-[#888888] whitespace-nowrap">{item.timestamp}</td>
                          <td className="py-2.5 px-3 font-semibold text-white">{item.email}</td>
                          <td className="py-2.5 px-3">
                            <span className="bg-[#161616] border border-[#2e2e2e] text-[#a1a1a1] px-2 py-0.5 rounded-none text-[10px]">
                              {item.provider}
                            </span>
                          </td>
                          <td className="py-2.5 px-3">
                            <span className="inline-flex items-center gap-1 text-[#00e599]">
                              <CheckCircle2 className="w-3 h-3" />
                              <span>{item.status}</span>
                            </span>
                          </td>
                          <td className="py-2.5 px-3 text-[#666666] text-[11px] truncate max-w-[200px]">
                            {item.userAgent}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}

          {/* Tab 2: Sessions */}
          {activeTab === "sessions" && (
            <div className="space-y-3">
              <div className="border border-[#222222] overflow-hidden">
                <table className="w-full text-left text-xs border-collapse">
                  <thead>
                    <tr className="bg-[#111111] border-b border-[#222222] text-[#888888] text-[11px]">
                      <th className="py-2.5 px-3">Session ID</th>
                      <th className="py-2.5 px-3">User Identity</th>
                      <th className="py-2.5 px-3">Start Time</th>
                      <th className="py-2.5 px-3">Uptime</th>
                      <th className="py-2.5 px-3">Status</th>
                      <th className="py-2.5 px-3">Device</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#1f1f1f]">
                    <tr className="bg-[#00e599]/5 border-l-2 border-[#00e599]">
                      <td className="py-2.5 px-3 font-bold text-white flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-[#00e599] animate-pulse" />
                        <span>{sessionId}</span>
                        <span className="text-[9px] bg-[#00e599]/20 text-[#00e599] px-1.5 py-0.5 font-semibold uppercase">
                          Current Tab
                        </span>
                      </td>
                      <td className="py-2.5 px-3 text-white">
                        {user ? user.email || (user.isAnonymous ? "Guest Account" : user.uid) : "Anonymous Visitor"}
                      </td>
                      <td className="py-2.5 px-3 text-[#888888]">
                        {new Date(Date.now() - sessionDuration * 1000).toLocaleTimeString()}
                      </td>
                      <td className="py-2.5 px-3 text-[#00e599] font-semibold">
                        {formatDuration(sessionDuration)}
                      </td>
                      <td className="py-2.5 px-3 text-[#00e599] font-bold">ACTIVE</td>
                      <td className="py-2.5 px-3 text-[#888888]">
                        {typeof navigator !== "undefined" ? navigator.platform : "Desktop"}
                      </td>
                    </tr>
                    {sessions
                      .filter((s) => s.sessionId !== sessionId)
                      .map((s) => (
                        <tr key={s.sessionId} className="hover:bg-[#111111]/60 transition-colors text-[#888888]">
                          <td className="py-2.5 px-3 font-mono">{s.sessionId}</td>
                          <td className="py-2.5 px-3">{s.userEmail}</td>
                          <td className="py-2.5 px-3">{s.startTime}</td>
                          <td className="py-2.5 px-3">{formatDuration(s.durationSeconds)}</td>
                          <td className="py-2.5 px-3 text-[#a1a1a1]">{s.status}</td>
                          <td className="py-2.5 px-3">{s.device}</td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Tab 3: Real-Time Stream */}
          {activeTab === "logs" && (
            <div className="space-y-2">
              {filteredLogs.length === 0 ? (
                <div className="text-center py-12 text-[#666666] space-y-2">
                  <Terminal className="w-8 h-8 mx-auto opacity-30" />
                  <p>No activity logs recorded for category: {filterCategory}</p>
                </div>
              ) : (
                filteredLogs.map((log) => (
                  <div
                    key={log.id}
                    className="bg-[#0d0d0d] border border-[#1f1f1f] p-2.5 flex items-start gap-3 hover:border-[#333333] transition-colors"
                  >
                    <span className="text-[#555555] shrink-0 text-[11px] pt-0.5">{log.timestamp}</span>

                    <span
                      className={`text-[10px] font-bold uppercase px-2 py-0.5 shrink-0 ${
                        log.category === "AUTH"
                          ? "bg-[#0070f3]/20 text-[#0070f3] border border-[#0070f3]/40"
                          : log.category === "SESSION"
                          ? "bg-[#00e599]/20 text-[#00e599] border border-[#00e599]/40"
                          : log.category === "NAVIGATION"
                          ? "bg-[#7928ca]/20 text-[#7928ca] border border-[#7928ca]/40"
                          : log.category === "SYNTAX"
                          ? "bg-[#ff0080]/20 text-[#ff0080] border border-[#ff0080]/40"
                          : "bg-[#f5a623]/20 text-[#f5a623] border border-[#f5a623]/40"
                      }`}
                    >
                      {log.category}
                    </span>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        {log.level === "SUCCESS" && <CheckCircle2 className="w-3.5 h-3.5 text-[#00e599] shrink-0" />}
                        {log.level === "ERROR" && <AlertCircle className="w-3.5 h-3.5 text-[#ef4444] shrink-0" />}
                        {log.level === "WARN" && <AlertCircle className="w-3.5 h-3.5 text-[#f5a623] shrink-0" />}
                        {log.level === "INFO" && <Info className="w-3.5 h-3.5 text-[#0070f3] shrink-0" />}
                        <span className="text-white font-medium">{log.message}</span>
                      </div>

                      {log.details && (
                        <pre className="mt-1.5 p-2 bg-[#000000] border border-[#1a1a1a] text-[#888888] text-[10px] overflow-x-auto">
                          {typeof log.details === "string"
                            ? log.details
                            : JSON.stringify(log.details, null, 2)}
                        </pre>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-[#000000] border-t border-[#222222] px-5 py-2.5 flex items-center justify-between text-[11px] text-[#666666] shrink-0">
          <p>Coding Trainer AI — Real-time Session Telemetry & Console Logger</p>
          <p>Press Esc or click top right to close</p>
        </div>
      </div>
    </div>
  );
};
