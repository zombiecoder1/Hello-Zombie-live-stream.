"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { TerminalIcon, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"

interface TerminalLine {
  id: string
  type: "input" | "output" | "error"
  content: string
  timestamp: Date
}

export function Terminal() {
  const [lines, setLines] = useState<TerminalLine[]>([
    {
      id: "1",
      type: "output",
      content: "Welcome to Cursor AI Terminal",
      timestamp: new Date(),
    },
    {
      id: "2",
      type: "output",
      content: 'Type "help" for available commands',
      timestamp: new Date(),
    },
  ])
  const [currentInput, setCurrentInput] = useState("")
  const [commandHistory, setCommandHistory] = useState<string[]>([])
  const [historyIndex, setHistoryIndex] = useState(-1)
  const inputRef = useRef<HTMLInputElement>(null)
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [lines])

  const executeCommand = (command: string) => {
    const newLines: TerminalLine[] = [
      ...lines,
      {
        id: Date.now().toString(),
        type: "input",
        content: `$ ${command}`,
        timestamp: new Date(),
      },
    ]

    // Simple command simulation
    let output = ""
    let type: "output" | "error" = "output"

    switch (command.toLowerCase().trim()) {
      case "help":
        output = `Available commands:
  help     - Show this help message
  clear    - Clear terminal
  ls       - List files
  pwd      - Show current directory
  date     - Show current date
  echo     - Echo text`
        break
      case "clear":
        setLines([])
        return
      case "ls":
        output = "src/  components/  public/  package.json  README.md"
        break
      case "pwd":
        output = "/workspace/cursor-ai-editor"
        break
      case "date":
        output = new Date().toString()
        break
      default:
        if (command.startsWith("echo ")) {
          output = command.substring(5)
        } else if (command.trim() === "") {
          return
        } else {
          output = `Command not found: ${command}`
          type = "error"
        }
    }

    newLines.push({
      id: (Date.now() + 1).toString(),
      type,
      content: output,
      timestamp: new Date(),
    })

    setLines(newLines)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (currentInput.trim()) {
      setCommandHistory([...commandHistory, currentInput])
      executeCommand(currentInput)
      setCurrentInput("")
      setHistoryIndex(-1)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowUp") {
      e.preventDefault()
      if (historyIndex < commandHistory.length - 1) {
        const newIndex = historyIndex + 1
        setHistoryIndex(newIndex)
        setCurrentInput(commandHistory[commandHistory.length - 1 - newIndex])
      }
    } else if (e.key === "ArrowDown") {
      e.preventDefault()
      if (historyIndex > 0) {
        const newIndex = historyIndex - 1
        setHistoryIndex(newIndex)
        setCurrentInput(commandHistory[commandHistory.length - 1 - newIndex])
      } else if (historyIndex === 0) {
        setHistoryIndex(-1)
        setCurrentInput("")
      }
    }
  }

  return (
    <div className="h-full bg-[#1e1e1e] border-t border-[#3c3c3c] flex flex-col">
      <div className="flex items-center justify-between p-2 border-b border-[#3c3c3c]">
        <div className="flex items-center gap-2 text-sm text-gray-300">
          <TerminalIcon className="h-4 w-4" />
          Terminal
        </div>
        <Button variant="ghost" size="sm" className="h-6 w-6 p-0" onClick={() => setLines([])}>
          <X className="h-3 w-3" />
        </Button>
      </div>

      <div className="flex-1 overflow-hidden">
        <ScrollArea className="h-full" ref={scrollRef}>
          <div className="p-3 font-mono text-sm">
            {lines.map((line) => (
              <div
                key={line.id}
                className={`mb-1 ${
                  line.type === "input" ? "text-green-400" : line.type === "error" ? "text-red-400" : "text-gray-300"
                }`}
              >
                <pre className="whitespace-pre-wrap">{line.content}</pre>
              </div>
            ))}

            <form onSubmit={handleSubmit} className="flex items-center">
              <span className="text-green-400 mr-2">$</span>
              <input
                ref={inputRef}
                type="text"
                value={currentInput}
                onChange={(e) => setCurrentInput(e.target.value)}
                onKeyDown={handleKeyDown}
                className="flex-1 bg-transparent text-gray-300 outline-none font-mono"
                placeholder="Enter command..."
                autoFocus
              />
            </form>
          </div>
        </ScrollArea>
      </div>
    </div>
  )
}
