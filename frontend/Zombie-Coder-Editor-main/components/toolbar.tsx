"use client"

import { Bot, Terminal, Settings, Search, GitBranch, Play, Bug, Puzzle, Mic, MicOff, AlertTriangle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"

interface ToolbarProps {
  onTogglePanel: (panel: "ai" | "git" | "extensions" | "debugger" | null) => void
  onToggleTerminal: () => void
  onToggleVoice: () => void
  onToggleErrors: () => void
  activePanel: "ai" | "git" | "extensions" | "debugger" | null
  terminalOpen: boolean
  voiceInputOpen: boolean
  errorPanelOpen: boolean
  isListening: boolean
  errorCount: number
  warningCount: number
}

export function Toolbar({
  onTogglePanel,
  onToggleTerminal,
  onToggleVoice,
  onToggleErrors,
  activePanel,
  terminalOpen,
  voiceInputOpen,
  errorPanelOpen,
  isListening,
  errorCount,
  warningCount,
}: ToolbarProps) {
  return (
    <div className="h-12 bg-[#323233] border-b border-[#3c3c3c] flex items-center justify-between px-4">
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2">
          <div className="text-2xl">🧟‍♂️</div>
          <div className="text-lg font-bold text-green-400">ZombieCoder</div>
          <div className="text-xs text-gray-400 bg-green-900/20 px-2 py-1 rounded">AI Edition</div>
        </div>
      </div>

      <div className="flex items-center gap-1">
        <Button
          variant="ghost"
          size="sm"
          className={cn(
            "h-8 px-3 text-gray-300 hover:text-white hover:bg-[#464647]",
            activePanel === "ai" && "bg-[#464647] text-white",
          )}
          onClick={() => onTogglePanel(activePanel === "ai" ? null : "ai")}
        >
          <Bot className="h-4 w-4 mr-2" />
          AI Assistant
        </Button>

        <Button
          variant="ghost"
          size="sm"
          className={cn(
            "h-8 px-3 text-gray-300 hover:text-white hover:bg-[#464647] relative",
            isListening && "bg-red-600 text-white animate-pulse",
          )}
          onClick={onToggleVoice}
        >
          {isListening ? <MicOff className="h-4 w-4 mr-2" /> : <Mic className="h-4 w-4 mr-2" />}
          Voice (বাংলা)
        </Button>

        <Button
          variant="ghost"
          size="sm"
          className={cn(
            "h-8 px-3 text-gray-300 hover:text-white hover:bg-[#464647]",
            activePanel === "git" && "bg-[#464647] text-white",
          )}
          onClick={() => onTogglePanel(activePanel === "git" ? null : "git")}
        >
          <GitBranch className="h-4 w-4 mr-2" />
          Git
        </Button>

        <Button
          variant="ghost"
          size="sm"
          className={cn(
            "h-8 px-3 text-gray-300 hover:text-white hover:bg-[#464647]",
            activePanel === "debugger" && "bg-[#464647] text-white",
          )}
          onClick={() => onTogglePanel(activePanel === "debugger" ? null : "debugger")}
        >
          <Bug className="h-4 w-4 mr-2" />
          Debug
        </Button>

        <Button
          variant="ghost"
          size="sm"
          className={cn(
            "h-8 px-3 text-gray-300 hover:text-white hover:bg-[#464647]",
            terminalOpen && "bg-[#464647] text-white",
          )}
          onClick={onToggleTerminal}
        >
          <Terminal className="h-4 w-4 mr-2" />
          Terminal
        </Button>

        <Button
          variant="ghost"
          size="sm"
          className={cn(
            "h-8 px-3 text-gray-300 hover:text-white hover:bg-[#464647] relative",
            errorPanelOpen && "bg-[#464647] text-white",
          )}
          onClick={onToggleErrors}
        >
          <AlertTriangle className="h-4 w-4 mr-2" />
          Problems
          {(errorCount > 0 || warningCount > 0) && (
            <div className="flex gap-1 ml-2">
              {errorCount > 0 && (
                <Badge variant="destructive" className="h-4 text-xs px-1">
                  {errorCount}
                </Badge>
              )}
              {warningCount > 0 && (
                <Badge variant="secondary" className="h-4 text-xs px-1 bg-yellow-600">
                  {warningCount}
                </Badge>
              )}
            </div>
          )}
        </Button>

        <Button
          variant="ghost"
          size="sm"
          className={cn(
            "h-8 px-3 text-gray-300 hover:text-white hover:bg-[#464647]",
            activePanel === "extensions" && "bg-[#464647] text-white",
          )}
          onClick={() => onTogglePanel(activePanel === "extensions" ? null : "extensions")}
        >
          <Puzzle className="h-4 w-4 mr-2" />
          Extensions
        </Button>

        <Button variant="ghost" size="sm" className="h-8 px-3 text-gray-300 hover:text-white hover:bg-[#464647]">
          <Search className="h-4 w-4 mr-2" />
          Search
        </Button>

        <Button variant="ghost" size="sm" className="h-8 px-3 text-gray-300 hover:text-white hover:bg-[#464647]">
          <Play className="h-4 w-4 mr-2" />
          Run
        </Button>

        <Button variant="ghost" size="sm" className="h-8 px-3 text-gray-300 hover:text-white hover:bg-[#464647]">
          <Settings className="h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}
