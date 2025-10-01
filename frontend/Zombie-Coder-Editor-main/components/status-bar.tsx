"use client"

import { GitBranch, Bell } from "lucide-react"

interface StatusBarProps {
  currentFile: { name: string; path: string } | null
  cursorPosition: { line: number; column: number }
}

export function StatusBar({ currentFile, cursorPosition }: StatusBarProps) {
  return (
    <div className="h-6 bg-[#007acc] text-white text-xs flex items-center justify-between px-3">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-1">
          <GitBranch className="h-3 w-3" />
          <span>main</span>
        </div>

        <div className="flex items-center gap-1">
          <span>✓</span>
          <span>No issues</span>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {currentFile && (
          <>
            <span>
              Ln {cursorPosition.line}, Col {cursorPosition.column}
            </span>
            <span>Spaces: 2</span>
            <span>UTF-8</span>
            <span>LF</span>
            <span>{getFileType(currentFile.name)}</span>
          </>
        )}

        <div className="flex items-center gap-1 cursor-pointer hover:bg-white/10 px-2 py-1 rounded">
          <span>🧟‍♂️</span>
          <span>Local AI Assistant</span>
        </div>

        <Bell className="h-3 w-3 cursor-pointer" />
      </div>
    </div>
  )
}

function getFileType(filename: string): string {
  const ext = filename.split(".").pop()?.toLowerCase()
  const typeMap: Record<string, string> = {
    ts: "TypeScript",
    tsx: "TypeScript JSX",
    js: "JavaScript",
    jsx: "JavaScript JSX",
    py: "Python",
    html: "HTML",
    css: "CSS",
    json: "JSON",
    md: "Markdown",
  }
  return typeMap[ext || ""] || "Plain Text"
}
