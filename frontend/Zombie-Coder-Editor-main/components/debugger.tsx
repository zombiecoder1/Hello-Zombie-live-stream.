"use client"

import { useState } from "react"
import {
  Play,
  Pause,
  Square,
  StepBackIcon as StepOver,
  StepBackIcon as StepInto,
  StepBackIcon as StepOut,
  RotateCcw,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"

interface Breakpoint {
  file: string
  line: number
  enabled: boolean
}

interface DebugSession {
  isActive: boolean
  isPaused: boolean
  currentLine?: number
  currentFile?: string
  callStack: Array<{
    function: string
    file: string
    line: number
  }>
  variables: Array<{
    name: string
    value: string
    type: string
  }>
}

interface DebuggerProps {
  breakpoints: Breakpoint[]
  debugSession: DebugSession | null
  onToggleBreakpoint: (file: string, line: number) => void
  onStartDebugging: () => void
  onStopDebugging: () => void
  currentFile: { name: string; path: string; content: string } | null
}

export function Debugger({
  breakpoints,
  debugSession,
  onToggleBreakpoint,
  onStartDebugging,
  onStopDebugging,
  currentFile,
}: DebuggerProps) {
  const [selectedTab, setSelectedTab] = useState<"breakpoints" | "variables" | "callstack" | "console">("breakpoints")

  return (
    <div className="h-full bg-[#252526] border-l border-[#3c3c3c] flex flex-col">
      <div className="p-3 border-b border-[#3c3c3c]">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-medium text-gray-300 flex items-center gap-2">🐛 ZombieCoder Debugger</h2>
          <Badge variant={debugSession?.isActive ? "destructive" : "secondary"}>
            {debugSession?.isActive ? "Active" : "Inactive"}
          </Badge>
        </div>

        <div className="flex gap-1">
          <Button
            variant="default"
            size="sm"
            className="h-7 px-2"
            onClick={debugSession?.isActive ? onStopDebugging : onStartDebugging}
          >
            {debugSession?.isActive ? (
              <>
                <Square className="h-3 w-3 mr-1" />
                Stop
              </>
            ) : (
              <>
                <Play className="h-3 w-3 mr-1" />
                Start
              </>
            )}
          </Button>

          {debugSession?.isActive && (
            <>
              <Button variant="ghost" size="sm" className="h-7 px-2">
                <Pause className="h-3 w-3 mr-1" />
                Pause
              </Button>
              <Button variant="ghost" size="sm" className="h-7 px-2">
                <StepOver className="h-3 w-3 mr-1" />
                Step Over
              </Button>
              <Button variant="ghost" size="sm" className="h-7 px-2">
                <StepInto className="h-3 w-3 mr-1" />
                Step Into
              </Button>
              <Button variant="ghost" size="sm" className="h-7 px-2">
                <StepOut className="h-3 w-3 mr-1" />
                Step Out
              </Button>
              <Button variant="ghost" size="sm" className="h-7 px-2">
                <RotateCcw className="h-3 w-3 mr-1" />
                Restart
              </Button>
            </>
          )}
        </div>
      </div>

      <div className="flex border-b border-[#3c3c3c]">
        {["breakpoints", "variables", "callstack", "console"].map((tab) => (
          <Button
            key={tab}
            variant={selectedTab === tab ? "secondary" : "ghost"}
            size="sm"
            className="h-8 px-3 rounded-none text-xs capitalize"
            onClick={() => setSelectedTab(tab as any)}
          >
            {tab}
          </Button>
        ))}
      </div>

      <ScrollArea className="flex-1 p-3">
        {selectedTab === "breakpoints" && (
          <div className="space-y-2">
            <div className="text-xs text-gray-400 mb-2">Breakpoints ({breakpoints.length})</div>
            {breakpoints.length === 0 ? (
              <div className="text-xs text-gray-500 text-center py-4">
                No breakpoints set. Click on line numbers to add breakpoints.
              </div>
            ) : (
              breakpoints.map((bp, index) => (
                <div key={index} className="flex items-center gap-2 p-2 bg-[#3c3c3c] rounded text-xs">
                  <div className={`w-2 h-2 rounded-full ${bp.enabled ? "bg-red-500" : "bg-gray-500"}`} />
                  <div className="flex-1">
                    <div className="text-white">{bp.file.split("/").pop()}</div>
                    <div className="text-gray-400">Line {bp.line}</div>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-6 w-6 p-0"
                    onClick={() => onToggleBreakpoint(bp.file, bp.line)}
                  >
                    ×
                  </Button>
                </div>
              ))
            )}
          </div>
        )}

        {selectedTab === "variables" && (
          <div className="space-y-2">
            <div className="text-xs text-gray-400 mb-2">Variables</div>
            {debugSession?.variables?.length === 0 ? (
              <div className="text-xs text-gray-500 text-center py-4">
                No variables available. Start debugging to see variables.
              </div>
            ) : (
              debugSession?.variables?.map((variable, index) => (
                <div key={index} className="p-2 bg-[#3c3c3c] rounded text-xs">
                  <div className="flex items-center justify-between">
                    <span className="text-blue-400">{variable.name}</span>
                    <Badge variant="outline" className="text-xs">
                      {variable.type}
                    </Badge>
                  </div>
                  <div className="text-gray-300 mt-1 font-mono">{variable.value}</div>
                </div>
              ))
            )}
          </div>
        )}

        {selectedTab === "callstack" && (
          <div className="space-y-2">
            <div className="text-xs text-gray-400 mb-2">Call Stack</div>
            {debugSession?.callStack?.length === 0 ? (
              <div className="text-xs text-gray-500 text-center py-4">
                No call stack available. Start debugging to see call stack.
              </div>
            ) : (
              debugSession?.callStack?.map((frame, index) => (
                <div key={index} className="p-2 bg-[#3c3c3c] rounded text-xs">
                  <div className="text-white font-medium">{frame.function}</div>
                  <div className="text-gray-400">
                    {frame.file.split("/").pop()}:{frame.line}
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {selectedTab === "console" && (
          <div className="space-y-2">
            <div className="text-xs text-gray-400 mb-2">Debug Console</div>
            <div className="bg-[#1e1e1e] p-2 rounded font-mono text-xs min-h-[200px]">
              <div className="text-green-400">ZombieCoder Debug Console</div>
              <div className="text-gray-400">Ready for debugging...</div>
            </div>
          </div>
        )}
      </ScrollArea>
    </div>
  )
}
