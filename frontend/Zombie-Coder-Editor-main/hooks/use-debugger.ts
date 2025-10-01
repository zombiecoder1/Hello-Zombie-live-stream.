"use client"

import { useState, useCallback } from "react"

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

export function useDebugger() {
  const [breakpoints, setBreakpoints] = useState<Breakpoint[]>([])
  const [debugSession, setDebugSession] = useState<DebugSession | null>(null)

  const toggleBreakpoint = useCallback((file: string, line: number) => {
    setBreakpoints((prev) => {
      const existing = prev.find((bp) => bp.file === file && bp.line === line)
      if (existing) {
        return prev.filter((bp) => !(bp.file === file && bp.line === line))
      } else {
        return [...prev, { file, line, enabled: true }]
      }
    })
  }, [])

  const startDebugging = useCallback(() => {
    setDebugSession({
      isActive: true,
      isPaused: false,
      callStack: [
        { function: "main", file: "/src/App.tsx", line: 15 },
        { function: "handleClick", file: "/src/components/Button.tsx", line: 8 },
      ],
      variables: [
        { name: "count", value: "0", type: "number" },
        { name: "isLoading", value: "false", type: "boolean" },
        { name: "user", value: "{ name: 'John', age: 30 }", type: "object" },
      ],
    })
  }, [])

  const stopDebugging = useCallback(() => {
    setDebugSession(null)
  }, [])

  return {
    breakpoints,
    debugSession,
    toggleBreakpoint,
    startDebugging,
    stopDebugging,
  }
}
