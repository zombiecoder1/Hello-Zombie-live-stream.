"use client"

import { useState, useRef, useEffect } from "react"
import { Terminal, Plus, X, ChevronDown, Settings, Trash2, SplitSquareVertical } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { cn } from "@/lib/utils"

interface TerminalTab {
  id: string
  name: string
  type: "powershell" | "cmd" | "bash" | "git-bash" | "wsl"
  content: string[]
}

interface TerminalEnhancedProps {
  onClose?: () => void
}

export function TerminalEnhanced({ onClose }: TerminalEnhancedProps) {
  const [terminals, setTerminals] = useState<TerminalTab[]>([
    {
      id: "1",
      name: "powershell 1",
      type: "powershell",
      content: ["Windows PowerShell", "Copyright (C) Microsoft Corporation. All rights reserved.", "", "PS C:\\>"],
    },
  ])
  const [activeTerminal, setActiveTerminal] = useState("1")
  const [currentInput, setCurrentInput] = useState("")
  const [mainTab, setMainTab] = useState("terminal")
  const inputRef = useRef<HTMLInputElement>(null)
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [terminals, activeTerminal])

  const terminalTypes = [
    { id: "powershell", name: "PowerShell (Default)", icon: "⚡" },
    { id: "cmd", name: "Command Prompt", icon: "💻" },
    { id: "bash", name: "Git Bash", icon: "🐚" },
    { id: "wsl", name: "Ubuntu (WSL)", icon: "🐧" },
  ]

  const createNewTerminal = (type: TerminalTab["type"] = "powershell") => {
    const count = terminals.filter((t) => t.type === type).length + 1
    const newTerminal: TerminalTab = {
      id: Date.now().toString(),
      name: `${type} ${count}`,
      type,
      content: getWelcomeMessage(type),
    }
    setTerminals([...terminals, newTerminal])
    setActiveTerminal(newTerminal.id)
  }

  const getWelcomeMessage = (type: TerminalTab["type"]): string[] => {
    switch (type) {
      case "powershell":
        return [
          "Windows PowerShell",
          "Copyright (C) Microsoft Corporation. All rights reserved.",
          "",
          "Try the new cross-platform PowerShell https://aka.ms/pscore6",
          "",
          "PS C:\\>",
        ]
      case "cmd":
        return [
          "Microsoft Windows [Version 10.0.22000.1696]",
          "(c) Microsoft Corporation. All rights reserved.",
          "",
          "C:\\>",
        ]
      case "bash":
        return ["Welcome to Git Bash", "", "user@computer MINGW64 ~", "$"]
      case "wsl":
        return ["Welcome to Ubuntu 22.04.2 LTS", "", "user@computer:~$"]
      default:
        return [""]
    }
  }

  const closeTerminal = (id: string) => {
    if (terminals.length === 1) return
    const newTerminals = terminals.filter((t) => t.id !== id)
    setTerminals(newTerminals)
    if (activeTerminal === id) {
      setActiveTerminal(newTerminals[0].id)
    }
  }

  const executeCommand = (command: string) => {
    const terminal = terminals.find((t) => t.id === activeTerminal)
    if (!terminal) return

    const prompt = terminal.type === "powershell" ? "PS C:\\>" : terminal.type === "cmd" ? "C:\\>" : "$"
    let output: string[] = []

    if (command.trim() === "") {
      output = []
    } else if (command.toLowerCase() === "clear" || command.toLowerCase() === "cls") {
      setTerminals(terminals.map((t) => (t.id === activeTerminal ? { ...t, content: getWelcomeMessage(t.type) } : t)))
      setCurrentInput("")
      return
    } else if (command.toLowerCase() === "help") {
      output = [
        "Available commands:",
        "  help     - Show this help",
        "  clear    - Clear terminal",
        "  ls/dir   - List files",
        "  pwd      - Current directory",
        "  echo     - Print message",
      ]
    } else if (command.toLowerCase() === "ls" || command.toLowerCase() === "dir") {
      output = [
        "Directory: C:\\Users\\ZombieCoder",
        "",
        "Mode  LastWriteTime  Name",
        "----  -------------  ----",
        "d---- 01/15/2024     src",
        "d---- 01/15/2024     components",
        "----- 01/15/2024     package.json",
        "----- 01/15/2024     README.md",
      ]
    } else if (command.toLowerCase() === "pwd") {
      output = ["C:\\Users\\ZombieCoder\\Projects"]
    } else if (command.toLowerCase().startsWith("echo ")) {
      output = [command.substring(5)]
    } else {
      output = [`'${command}' is not recognized as an internal or external command.`]
    }

    setTerminals(
      terminals.map((t) =>
        t.id === activeTerminal
          ? {
              ...t,
              content: [...t.content, `${prompt} ${command}`, ...output, "", prompt],
            }
          : t,
      ),
    )
    setCurrentInput("")
  }

  const currentTerminal = terminals.find((t) => t.id === activeTerminal)

  return (
    <div className="h-full bg-[#1e1e1e] border-t border-[#3c3c3c] flex flex-col">
      <Tabs value={mainTab} onValueChange={setMainTab} className="flex-1 flex flex-col">
        {/* Main Tabs Header */}
        <div className="h-9 border-b border-[#3c3c3c] flex items-center justify-between px-2">
          <TabsList className="h-7 bg-transparent">
            <TabsTrigger value="problems" className="h-7 px-3 text-xs data-[state=active]:bg-[#464647]">
              PROBLEMS
            </TabsTrigger>
            <TabsTrigger value="output" className="h-7 px-3 text-xs data-[state=active]:bg-[#464647]">
              OUTPUT
            </TabsTrigger>
            <TabsTrigger value="debug" className="h-7 px-3 text-xs data-[state=active]:bg-[#464647]">
              DEBUG CONSOLE
            </TabsTrigger>
            <TabsTrigger value="terminal" className="h-7 px-3 text-xs data-[state=active]:bg-[#464647]">
              TERMINAL
            </TabsTrigger>
            <TabsTrigger value="ports" className="h-7 px-3 text-xs data-[state=active]:bg-[#464647]">
              PORTS
            </TabsTrigger>
          </TabsList>

          <div className="flex items-center gap-1">
            {onClose && (
              <Button variant="ghost" size="sm" className="h-6 w-6 p-0" onClick={onClose}>
                <X className="h-3 w-3" />
              </Button>
            )}
          </div>
        </div>

        {/* Problems Tab */}
        <TabsContent value="problems" className="flex-1 m-0">
          <div className="h-full flex items-center justify-center text-gray-500 text-sm">
            <div className="text-center">
              <p className="mb-2">No problems detected</p>
              <p className="text-xs text-gray-600">Your code looks clean! 🧟‍♂️</p>
            </div>
          </div>
        </TabsContent>

        {/* Output Tab */}
        <TabsContent value="output" className="flex-1 m-0">
          <ScrollArea className="h-full p-4">
            <div className="font-mono text-xs text-gray-400 space-y-1">
              <div>[ZombieCoder] Output panel initialized</div>
              <div>[AI Agent] Bengali NLP ready</div>
              <div>[Local Model] Loading complete</div>
            </div>
          </ScrollArea>
        </TabsContent>

        {/* Debug Console Tab */}
        <TabsContent value="debug" className="flex-1 m-0">
          <ScrollArea className="h-full p-4">
            <div className="font-mono text-xs text-gray-400">
              <div>Debug console ready</div>
              <div className="text-gray-600 mt-2">Start debugging to see output</div>
            </div>
          </ScrollArea>
        </TabsContent>

        {/* Terminal Tab */}
        <TabsContent value="terminal" className="flex-1 m-0 flex flex-col">
          {/* Terminal Selector */}
          <div className="h-9 border-b border-[#3c3c3c] flex items-center justify-between px-2">
            <div className="flex items-center gap-1 flex-1 overflow-x-auto">
              {terminals.map((terminal) => (
                <div
                  key={terminal.id}
                  className={cn(
                    "flex items-center gap-2 px-2 py-1 text-xs cursor-pointer rounded group",
                    activeTerminal === terminal.id ? "bg-[#464647]" : "hover:bg-[#3c3c3c]",
                  )}
                  onClick={() => setActiveTerminal(terminal.id)}
                >
                  <Terminal className="h-3 w-3" />
                  <span>{terminal.name}</span>
                  {terminals.length > 1 && (
                    <X
                      className="h-3 w-3 opacity-0 group-hover:opacity-100 hover:text-red-400 transition-opacity"
                      onClick={(e) => {
                        e.stopPropagation()
                        closeTerminal(terminal.id)
                      }}
                    />
                  )}
                </div>
              ))}
            </div>

            <div className="flex items-center gap-1">
              {/* Terminal Type Selector */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm" className="h-6 px-2 text-xs">
                    <ChevronDown className="h-3 w-3" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-64 bg-[#2d2d30] border-[#3c3c3c]">
                  {terminalTypes.map((type) => (
                    <DropdownMenuItem
                      key={type.id}
                      className="text-xs cursor-pointer"
                      onClick={() => createNewTerminal(type.id as TerminalTab["type"])}
                    >
                      <span className="mr-2">{type.icon}</span>
                      {type.name}
                    </DropdownMenuItem>
                  ))}
                  <DropdownMenuSeparator className="bg-[#3c3c3c]" />
                  <DropdownMenuItem className="text-xs">
                    <SplitSquareVertical className="h-3 w-3 mr-2" />
                    Split Terminal
                  </DropdownMenuItem>
                  <DropdownMenuItem className="text-xs">
                    <Settings className="h-3 w-3 mr-2" />
                    Configure Terminal Settings
                  </DropdownMenuItem>
                  <DropdownMenuItem className="text-xs">Select Default Profile</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>

              <Button variant="ghost" size="sm" className="h-6 w-6 p-0" onClick={() => createNewTerminal()}>
                <Plus className="h-3 w-3" />
              </Button>

              <Button
                variant="ghost"
                size="sm"
                className="h-6 w-6 p-0"
                onClick={() => currentTerminal && closeTerminal(currentTerminal.id)}
              >
                <Trash2 className="h-3 w-3" />
              </Button>
            </div>
          </div>

          {/* Terminal Content */}
          <ScrollArea className="flex-1" ref={scrollRef}>
            <div className="p-3 font-mono text-sm">
              {currentTerminal?.content.map((line, i) => (
                <div key={i} className="text-gray-300 whitespace-pre">
                  {line}
                </div>
              ))}
              <div className="flex items-center">
                <span className="text-green-400 mr-2">
                  {currentTerminal?.type === "powershell"
                    ? "PS C:\\>"
                    : currentTerminal?.type === "cmd"
                      ? "C:\\>"
                      : "$"}
                </span>
                <input
                  ref={inputRef}
                  type="text"
                  value={currentInput}
                  onChange={(e) => setCurrentInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      executeCommand(currentInput)
                    }
                  }}
                  className="flex-1 bg-transparent outline-none text-gray-300"
                  placeholder="Type a command..."
                  autoFocus
                />
              </div>
            </div>
          </ScrollArea>
        </TabsContent>

        {/* Ports Tab */}
        <TabsContent value="ports" className="flex-1 m-0">
          <div className="h-full flex items-center justify-center text-gray-500 text-sm">
            <div className="text-center">
              <p className="mb-2">No forwarded ports</p>
              <p className="text-xs text-gray-600">Your local ports will appear here</p>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
