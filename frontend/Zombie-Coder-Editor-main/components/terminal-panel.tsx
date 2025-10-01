"use client"

import { useState } from "react"
import { Terminal, Plus, X, ChevronDown } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"

interface TerminalTab {
  id: string
  name: string
  content: string[]
}

export function TerminalPanel() {
  const [tabs, setTabs] = useState<TerminalTab[]>([
    {
      id: "1",
      name: "Terminal 1",
      content: ["ZombieCoder Terminal v1.0.0", "Type 'help' for available commands", ""],
    },
  ])
  const [activeTab, setActiveTab] = useState("1")
  const [currentInput, setCurrentInput] = useState("")

  const handleCommand = (command: string) => {
    const newTabs = tabs.map((tab) => {
      if (tab.id === activeTab) {
        const output = executeCommand(command)
        return {
          ...tab,
          content: [...tab.content, `$ ${command}`, ...output, ""],
        }
      }
      return tab
    })
    setTabs(newTabs)
    setCurrentInput("")
  }

  const executeCommand = (cmd: string): string[] => {
    const command = cmd.trim().toLowerCase()

    if (command === "help") {
      return [
        "Available commands:",
        "  help     - Show this help message",
        "  clear    - Clear terminal",
        "  ls       - List files",
        "  pwd      - Print working directory",
        "  echo     - Echo text",
      ]
    } else if (command === "clear") {
      const newTabs = tabs.map((tab) => (tab.id === activeTab ? { ...tab, content: [] } : tab))
      setTabs(newTabs)
      return []
    } else if (command === "ls") {
      return ["src/", "public/", "package.json", "README.md"]
    } else if (command === "pwd") {
      return ["/workspace/zombiecoder"]
    } else if (command.startsWith("echo ")) {
      return [command.substring(5)]
    } else if (command === "") {
      return []
    } else {
      return [`Command not found: ${command}`]
    }
  }

  const addNewTerminal = () => {
    const newId = (tabs.length + 1).toString()
    setTabs([
      ...tabs,
      {
        id: newId,
        name: `Terminal ${newId}`,
        content: ["ZombieCoder Terminal v1.0.0", ""],
      },
    ])
    setActiveTab(newId)
  }

  const closeTerminal = (id: string) => {
    if (tabs.length === 1) return
    const newTabs = tabs.filter((t) => t.id !== id)
    setTabs(newTabs)
    if (activeTab === id) {
      setActiveTab(newTabs[0].id)
    }
  }

  return (
    <div className="h-full bg-[#1e1e1e] border-t border-[#3c3c3c] flex flex-col">
      <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
        {/* Terminal Tabs Header */}
        <div className="h-9 border-b border-[#3c3c3c] flex items-center justify-between px-2">
          <div className="flex items-center gap-2 flex-1 overflow-x-auto">
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
          </div>

          <div className="flex items-center gap-1">
            <Button variant="ghost" size="sm" className="h-6 w-6 p-0" onClick={addNewTerminal}>
              <Plus className="h-3 w-3" />
            </Button>
            <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
              <ChevronDown className="h-3 w-3" />
            </Button>
          </div>
        </div>

        {/* Terminal Content */}
        <TabsContent value="problems" className="flex-1 m-0">
          <div className="h-full flex items-center justify-center text-gray-500 text-sm">No problems detected</div>
        </TabsContent>

        <TabsContent value="output" className="flex-1 m-0">
          <ScrollArea className="h-full p-4">
            <div className="font-mono text-xs text-gray-400">Output panel - Agent activities will appear here</div>
          </ScrollArea>
        </TabsContent>

        <TabsContent value="debug" className="flex-1 m-0">
          <ScrollArea className="h-full p-4">
            <div className="font-mono text-xs text-gray-400">Debug console ready</div>
          </ScrollArea>
        </TabsContent>

        <TabsContent value="terminal" className="flex-1 m-0">
          <div className="h-full flex flex-col">
            {/* Terminal Selector */}
            <div className="h-8 border-b border-[#3c3c3c] flex items-center px-2 gap-1">
              {tabs.map((tab) => (
                <div
                  key={tab.id}
                  className={cn(
                    "flex items-center gap-2 px-2 py-1 text-xs cursor-pointer rounded",
                    activeTab === tab.id ? "bg-[#464647]" : "hover:bg-[#3c3c3c]",
                  )}
                  onClick={() => setActiveTab(tab.id)}
                >
                  <Terminal className="h-3 w-3" />
                  <span>{tab.name}</span>
                  {tabs.length > 1 && (
                    <X
                      className="h-3 w-3 hover:text-red-400"
                      onClick={(e) => {
                        e.stopPropagation()
                        closeTerminal(tab.id)
                      }}
                    />
                  )}
                </div>
              ))}
            </div>

            {/* Terminal Content */}
            <ScrollArea className="flex-1 p-3">
              <div className="font-mono text-sm">
                {tabs
                  .find((t) => t.id === activeTab)
                  ?.content.map((line, i) => (
                    <div key={i} className="text-gray-300">
                      {line}
                    </div>
                  ))}
                <div className="flex items-center text-green-400">
                  <span className="mr-2">$</span>
                  <input
                    type="text"
                    value={currentInput}
                    onChange={(e) => setCurrentInput(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") {
                        handleCommand(currentInput)
                      }
                    }}
                    className="flex-1 bg-transparent outline-none text-gray-300"
                    placeholder="Type a command..."
                    autoFocus
                  />
                </div>
              </div>
            </ScrollArea>
          </div>
        </TabsContent>

        <TabsContent value="ports" className="flex-1 m-0">
          <div className="h-full p-4">
            <div className="text-sm text-gray-400">No forwarded ports</div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

function cn(...classes: any[]) {
  return classes.filter(Boolean).join(" ")
}
