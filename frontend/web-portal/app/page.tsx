"use client"

import { useState, useRef, useEffect, useCallback } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Progress } from "@/components/ui/progress"
import {
  Shield,
  CheckCircle,
  XCircle,
  Terminal,
  Code,
  Brain,
  Lightbulb,
  Wifi,
  WifiOff,
  Database,
  Server,
  Eye,
  Scan,
  Activity,
} from "lucide-react"
import { Switch } from "@/components/ui/switch"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"

interface FileIndex {
  filePath: string
  lines: Array<{
    number: number
    content: string
    type: "code" | "comment" | "import" | "function" | "variable" | "class" | "empty"
    entities: string[]
    references: string[]
    language: string
    indentation: number
  }>
  symbols: Array<{
    name: string
    type: "function" | "variable" | "class" | "interface" | "type"
    line: number
    scope: string
  }>
  imports: Array<{
    module: string
    items: string[]
    line: number
  }>
  metadata: {
    language: string
    totalLines: number
    codeLines: number
    commentLines: number
    emptyLines: number
    lastModified: Date
    encoding: string
  }
}

interface MCPProvider {
  id: string
  name: string
  type: "local" | "cloud" | "hybrid"
  status: "connected" | "disconnected" | "error"
  latency: number
  capabilities: string[]
  modelPath?: string
  apiEndpoint?: string
}

interface AgentAction {
  id: string
  type: "suggestion" | "fix" | "refactor" | "complete" | "explain"
  line: number
  column: number
  original: string
  suggested: string
  confidence: number
  reasoning: string
  bengaliExplanation: string
  mode: "strict" | "soft"
}

export default function BengaliCopilotExtension() {
  // Core Editor State
  const [code, setCode] = useState(`// Bengali Copilot Extension - Privacy First
// File automatically indexed on open

import React from 'react';
import { useState } from 'react';

function BengaliGreeting(name) {
  // আমার সোনার বাংলা
  console.log("Hello " + name);
  return \`নমস্কার, \${name}!\`;
}

// Incomplete line - MCP will detect and suggest
const myCountry = "আমার সোনার বাংলা";
// Missing: আমি তোমায় ভালবাসি

export default BengaliGreeting;`)

  // File Indexing State
  const [fileIndex, setFileIndex] = useState<FileIndex | null>(null)
  const [isIndexing, setIsIndexing] = useState(false)
  const [indexingProgress, setIndexingProgress] = useState(0)

  // MCP & Model State
  const [mcpProviders, setMcpProviders] = useState<MCPProvider[]>([
    {
      id: "local-ollama",
      name: "Local Ollama",
      type: "local",
      status: "disconnected",
      latency: 0,
      capabilities: ["code-completion", "bengali-translation", "error-detection"],
      modelPath: "/usr/local/bin/ollama",
    },
    {
      id: "local-lmstudio",
      name: "LM Studio",
      type: "local",
      status: "disconnected",
      latency: 0,
      capabilities: ["code-generation", "refactoring"],
      modelPath: "/Applications/LM Studio.app",
    },
    {
      id: "fallback-cloud",
      name: "Cloud Fallback",
      type: "cloud",
      status: "disconnected",
      latency: 0,
      capabilities: ["full-context", "bengali-nlp"],
      apiEndpoint: "https://api.example.com/v1",
    },
  ])

  const [activeMCP, setActiveMCP] = useState<string | null>(null)
  const [detectedModels, setDetectedModels] = useState<string[]>([])

  // Agent State
  const [agentActions, setAgentActions] = useState<AgentAction[]>([])
  const [agentMode, setAgentMode] = useState<"strict" | "soft">("soft")
  const [isAgentActive, setIsAgentActive] = useState(true)

  // UI State
  const [consoleOutput, setConsoleOutput] = useState<string[]>([
    "🤖 Bengali Copilot Extension initialized",
    "🔍 File indexing system ready",
    "🌐 MCP providers scanning...",
    "🔐 Privacy-first mode: All data stays local",
    "📁 Workspace: ~/bengali-copilot/",
  ])

  // Settings State
  const [settings, setSettings] = useState({
    autoIndex: true,
    mcpFallback: true,
    agentExecution: true,
    privacyMode: true,
    bengaliSupport: true,
    localModelsOnly: false,
    strictMode: false,
  })

  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Utility Functions
  const addToConsole = useCallback((message: string) => {
    setConsoleOutput((prev) => [...prev.slice(-20), `${new Date().toLocaleTimeString()}: ${message}`])
  }, [])

  // File Indexing Functions
  const indexFile = useCallback(
    async (content: string, filePath = "current-file.js") => {
      setIsIndexing(true)
      setIndexingProgress(0)
      addToConsole("🔍 Starting file indexing...")

      // Simulate indexing progress
      const progressInterval = setInterval(() => {
        setIndexingProgress((prev) => {
          if (prev >= 100) {
            clearInterval(progressInterval)
            return 100
          }
          return prev + 20
        })
      }, 200)

      setTimeout(() => {
        const lines = content.split("\n")
        const indexedLines = lines.map((line, index) => {
          const trimmed = line.trim()
          let type: "code" | "comment" | "import" | "function" | "variable" | "class" | "empty" = "code"
          const entities: string[] = []
          const references: string[] = []

          if (trimmed === "") type = "empty"
          else if (trimmed.startsWith("//") || trimmed.startsWith("/*")) type = "comment"
          else if (trimmed.startsWith("import") || trimmed.startsWith("require")) type = "import"
          else if (trimmed.includes("function") || trimmed.includes("=>")) type = "function"
          else if (trimmed.includes("const") || trimmed.includes("let") || trimmed.includes("var")) type = "variable"
          else if (trimmed.includes("class")) type = "class"

          // Extract entities (variables, functions, etc.)
          const entityMatches = line.match(/\b[a-zA-Z_$][a-zA-Z0-9_$]*\b/g)
          if (entityMatches) entities.push(...entityMatches)

          // Extract Bengali text
          const bengaliMatches = line.match(/[\u0980-\u09FF]+/g)
          if (bengaliMatches) entities.push(...bengaliMatches)

          return {
            number: index + 1,
            content: line,
            type,
            entities,
            references,
            language: "javascript",
            indentation: line.length - line.trimStart().length,
          }
        })

        // Extract symbols
        const symbols = indexedLines
          .filter((line) => line.type === "function" || line.type === "variable" || line.type === "class")
          .map((line) => {
            const match = line.content.match(/(?:function|const|let|var|class)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)/i)
            return {
              name: match?.[1] || "unknown",
              type: line.type as "function" | "variable" | "class",
              line: line.number,
              scope: "global",
            }
          })

        // Extract imports
        const imports = indexedLines
          .filter((line) => line.type === "import")
          .map((line) => {
            const match = line.content.match(/import\s+(?:{([^}]+)}|\*\s+as\s+(\w+)|(\w+))\s+from\s+['"]([^'"]+)['"]/i)
            return {
              module: match?.[4] || "unknown",
              items: match?.[1]?.split(",").map((s) => s.trim()) || [match?.[2] || match?.[3] || "default"],
              line: line.number,
            }
          })

        const newIndex: FileIndex = {
          filePath,
          lines: indexedLines,
          symbols,
          imports,
          metadata: {
            language: "javascript",
            totalLines: lines.length,
            codeLines: indexedLines.filter((l) => l.type === "code").length,
            commentLines: indexedLines.filter((l) => l.type === "comment").length,
            emptyLines: indexedLines.filter((l) => l.type === "empty").length,
            lastModified: new Date(),
            encoding: "utf-8",
          },
        }

        setFileIndex(newIndex)
        setIsIndexing(false)
        setIndexingProgress(0)
        addToConsole(`✅ File indexed: ${newIndex.metadata.totalLines} lines, ${symbols.length} symbols`)

        // Trigger MCP analysis
        analyzeMCP(newIndex)
      }, 1000)
    },
    [addToConsole],
  )

  // MCP Analysis Functions
  const analyzeMCP = useCallback(
    (index: FileIndex) => {
      addToConsole("🌐 MCP analyzing indexed content...")

      // Check for incomplete Bengali content
      const bengaliLines = index.lines.filter((line) => /[\u0980-\u09FF]/.test(line.content))

      bengaliLines.forEach((line) => {
        if (line.content.includes("আমার সোনার বাংলা") && !line.content.includes("আমি তোমায় ভালবাসি")) {
          const action: AgentAction = {
            id: `mcp-${Date.now()}`,
            type: "complete",
            line: line.number,
            column: line.content.length,
            original: line.content,
            suggested: line.content + "\n// আমি তোমায় ভালবাসি - National anthem completion",
            confidence: 95,
            reasoning: "Detected incomplete Bengali national anthem, suggesting completion",
            bengaliExplanation: "জাতীয় সংগীতের অসম্পূর্ণ অংশ সনাক্ত করা হয়েছে",
            mode: agentMode,
          }
          setAgentActions((prev) => [action, ...prev.slice(0, 9)])
          addToConsole(`🎯 Agent detected incomplete Bengali content at line ${line.number}`)
        }
      })

      // Check for code improvements
      index.lines.forEach((line) => {
        if (line.content.includes('console.log("Hello " + ')) {
          const action: AgentAction = {
            id: `mcp-${Date.now()}-${line.number}`,
            type: "refactor",
            line: line.number,
            column: 0,
            original: line.content,
            suggested: line.content.replace('console.log("Hello " + name)', "console.log(`Hello, ${name}`)"),
            confidence: 88,
            reasoning: "Template literal is more modern and readable",
            bengaliExplanation: "Template literal ব্যবহার করলে কোড আরো পরিষ্কার হবে",
            mode: agentMode,
          }
          setAgentActions((prev) => [action, ...prev.slice(0, 9)])
        }
      })
    },
    [agentMode, addToConsole],
  )

  // Model Detection Functions
  const detectLocalModels = useCallback(() => {
    addToConsole("🔍 Scanning for local models...")

    // Simulate model detection
    setTimeout(() => {
      const foundModels = [
        "ollama:llama3.2:3b",
        "ollama:codellama:7b",
        "lmstudio:bengali-code-assistant",
        "local:whisper-bengali",
      ]

      setDetectedModels(foundModels)
      addToConsole(`📦 Found ${foundModels.length} local models`)

      // Update MCP provider status
      setMcpProviders((prev) =>
        prev.map((provider) => {
          if (provider.type === "local" && foundModels.some((model) => model.includes(provider.name.toLowerCase()))) {
            return { ...provider, status: "connected", latency: Math.random() * 100 + 50 }
          }
          return provider
        }),
      )

      // Set active MCP to first available local provider
      const localProvider = mcpProviders.find((p) => p.type === "local" && p.status === "connected")
      if (localProvider) {
        setActiveMCP(localProvider.id)
        addToConsole(`🎯 Active MCP: ${localProvider.name}`)
      }
    }, 2000)
  }, [mcpProviders, addToConsole])

  // Agent Execution Functions
  const executeAgentAction = useCallback(
    (action: AgentAction) => {
      if (action.mode === "strict") {
        // Direct code injection
        const lines = code.split("\n")
        lines[action.line - 1] = action.suggested.split("\n")[0]
        setCode(lines.join("\n"))
        addToConsole(`⚡ Agent executed strict action at line ${action.line}`)
      } else {
        // Soft suggestion mode - just highlight
        addToConsole(`💡 Agent suggests change at line ${action.line}: ${action.bengaliExplanation}`)
      }

      // Remove executed action
      setAgentActions((prev) => prev.filter((a) => a.id !== action.id))
    },
    [code, addToConsole],
  )

  // Initialize on mount
  useEffect(() => {
    detectLocalModels()
    if (settings.autoIndex) {
      indexFile(code)
    }
  }, [])

  // Auto-index on code change
  useEffect(() => {
    if (settings.autoIndex && code.length > 50) {
      const debounceTimer = setTimeout(() => {
        indexFile(code)
      }, 2000)
      return () => clearTimeout(debounceTimer)
    }
  }, [code, settings.autoIndex, indexFile])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg">
                <Code className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">Bengali Copilot Extension</h1>
                <p className="text-sm text-gray-300">File Indexing • MCP Fallback • Agent Execution • Privacy-First</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="bg-green-900 text-green-100">
                <Database className="h-3 w-3 mr-1" />
                {detectedModels.length} Models
              </Badge>
              <Badge variant="secondary" className="bg-blue-900 text-blue-100">
                <Server className="h-3 w-3 mr-1" />
                MCP Active
              </Badge>
              <Badge variant="secondary" className="bg-purple-900 text-purple-100">
                <Shield className="h-3 w-3 mr-1" />
                Privacy Mode
              </Badge>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <Tabs defaultValue="index" className="w-full">
              <TabsList className="grid w-full grid-cols-4 bg-slate-800">
                <TabsTrigger value="index" className="text-xs">
                  Index
                </TabsTrigger>
                <TabsTrigger value="mcp" className="text-xs">
                  MCP
                </TabsTrigger>
                <TabsTrigger value="agents" className="text-xs">
                  Agents
                </TabsTrigger>
                <TabsTrigger value="models" className="text-xs">
                  Models
                </TabsTrigger>
              </TabsList>

              <TabsContent value="index" className="space-y-4">
                <Card className="bg-slate-800 border-slate-700">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-sm flex items-center gap-2 text-white">
                      <Scan className="h-4 w-4" />
                      File Index
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {isIndexing ? (
                      <div className="space-y-2">
                        <div className="text-xs text-gray-300">Indexing file...</div>
                        <Progress value={indexingProgress} className="h-2" />
                      </div>
                    ) : fileIndex ? (
                      <div className="space-y-2 text-xs">
                        <div className="grid grid-cols-2 gap-2">
                          <div className="text-gray-300">Total Lines:</div>
                          <div className="text-white">{fileIndex.metadata.totalLines}</div>
                          <div className="text-gray-300">Code Lines:</div>
                          <div className="text-white">{fileIndex.metadata.codeLines}</div>
                          <div className="text-gray-300">Symbols:</div>
                          <div className="text-white">{fileIndex.symbols.length}</div>
                          <div className="text-gray-300">Imports:</div>
                          <div className="text-white">{fileIndex.imports.length}</div>
                        </div>
                        <Separator className="bg-slate-600" />
                        <div>
                          <div className="text-gray-300 mb-1">Symbols:</div>
                          {fileIndex.symbols.slice(0, 5).map((symbol) => (
                            <div key={symbol.name} className="flex items-center gap-1 text-xs">
                              <Badge variant="outline" className="text-xs border-slate-600 text-gray-300">
                                {symbol.type}
                              </Badge>
                              <span className="text-white">{symbol.name}</span>
                              <span className="text-gray-400">:{symbol.line}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    ) : (
                      <div className="text-xs text-gray-400">No file indexed</div>
                    )}

                    <Button
                      size="sm"
                      onClick={() => indexFile(code)}
                      disabled={isIndexing}
                      className="w-full bg-blue-600 hover:bg-blue-700"
                    >
                      <Eye className="h-3 w-3 mr-1" />
                      Re-index File
                    </Button>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="mcp" className="space-y-4">
                <Card className="bg-slate-800 border-slate-700">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-sm flex items-center gap-2 text-white">
                      <Server className="h-4 w-4" />
                      MCP Providers
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {mcpProviders.map((provider) => (
                      <div
                        key={provider.id}
                        className={`p-2 rounded border cursor-pointer ${
                          activeMCP === provider.id
                            ? "border-blue-500 bg-blue-900/20"
                            : "border-slate-600 hover:border-slate-500"
                        }`}
                        onClick={() => setActiveMCP(provider.id)}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            {provider.status === "connected" ? (
                              <Wifi className="h-3 w-3 text-green-400" />
                            ) : (
                              <WifiOff className="h-3 w-3 text-red-400" />
                            )}
                            <span className="text-sm text-white">{provider.name}</span>
                          </div>
                          <Badge variant={provider.type === "local" ? "default" : "secondary"} className="text-xs">
                            {provider.type}
                          </Badge>
                        </div>
                        {provider.status === "connected" && (
                          <div className="text-xs text-gray-400 mt-1">Latency: {Math.round(provider.latency)}ms</div>
                        )}
                      </div>
                    ))}

                    <Alert className="bg-slate-700 border-slate-600">
                      <Shield className="h-4 w-4" />
                      <AlertDescription className="text-xs text-gray-300">
                        {activeMCP
                          ? `Active: ${mcpProviders.find((p) => p.id === activeMCP)?.name}`
                          : "No provider available - Input will show 'No Provider, No Model Available'"}
                      </AlertDescription>
                    </Alert>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="agents" className="space-y-4">
                <Card className="bg-slate-800 border-slate-700">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-sm flex items-center gap-2 text-white">
                      <Activity className="h-4 w-4" />
                      Agent Actions ({agentActions.length})
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex items-center justify-between">
                      <Label className="text-sm text-gray-300">Mode:</Label>
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-gray-400">Soft</span>
                        <Switch
                          checked={agentMode === "strict"}
                          onCheckedChange={(checked) => setAgentMode(checked ? "strict" : "soft")}
                        />
                        <span className="text-xs text-gray-400">Strict</span>
                      </div>
                    </div>

                    <ScrollArea className="h-48">
                      <div className="space-y-2">
                        {agentActions.map((action) => (
                          <div key={action.id} className="border border-slate-600 rounded p-2 space-y-2">
                            <div className="flex items-center justify-between">
                              <Badge variant="outline" className="text-xs border-slate-500 text-gray-300">
                                {action.type}
                              </Badge>
                              <Badge variant="secondary" className="text-xs">
                                {action.confidence}%
                              </Badge>
                            </div>
                            <div className="text-xs text-gray-300">Line {action.line}</div>
                            <div className="text-xs text-blue-300">{action.bengaliExplanation}</div>
                            <div className="flex gap-1">
                              <Button
                                size="sm"
                                onClick={() => executeAgentAction(action)}
                                className="h-6 text-xs bg-green-600 hover:bg-green-700"
                              >
                                Apply
                              </Button>
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() => setAgentActions((prev) => prev.filter((a) => a.id !== action.id))}
                                className="h-6 text-xs border-slate-600"
                              >
                                Dismiss
                              </Button>
                            </div>
                          </div>
                        ))}
                        {agentActions.length === 0 && (
                          <div className="text-xs text-gray-400 text-center py-4">No agent actions</div>
                        )}
                      </div>
                    </ScrollArea>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="models" className="space-y-4">
                <Card className="bg-slate-800 border-slate-700">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-sm flex items-center gap-2 text-white">
                      <Database className="h-4 w-4" />
                      Local Models ({detectedModels.length})
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {detectedModels.length > 0 ? (
                      detectedModels.map((model) => (
                        <div key={model} className="flex items-center gap-2 p-2 bg-slate-700 rounded">
                          <CheckCircle className="h-3 w-3 text-green-400" />
                          <span className="text-xs text-white font-mono">{model}</span>
                        </div>
                      ))
                    ) : (
                      <div className="text-center py-4">
                        <Database className="h-8 w-8 mx-auto mb-2 text-gray-500" />
                        <div className="text-xs text-gray-400">No models detected</div>
                        <Button size="sm" onClick={detectLocalModels} className="mt-2 bg-blue-600 hover:bg-blue-700">
                          Scan Again
                        </Button>
                      </div>
                    )}

                    <Alert className="bg-slate-700 border-slate-600">
                      <AlertDescription className="text-xs text-gray-300">
                        Models are automatically scanned on startup. Install Ollama or LM Studio for local AI support.
                      </AlertDescription>
                    </Alert>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>

          {/* Main Editor Area */}
          <div className="lg:col-span-3 space-y-4">
            {/* Code Editor */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-sm flex items-center gap-2 text-white">
                    <Code className="h-4 w-4" />
                    Bengali Copilot Editor
                  </CardTitle>
                  <div className="flex items-center gap-2">
                    {!activeMCP && (
                      <Badge variant="destructive" className="text-xs">
                        No Provider, No Model Available
                      </Badge>
                    )}
                    {isIndexing && (
                      <Badge variant="secondary" className="text-xs">
                        <Scan className="h-3 w-3 mr-1 animate-spin" />
                        Indexing...
                      </Badge>
                    )}
                    <Button size="sm" variant="outline" onClick={() => indexFile(code)}>
                      <Brain className="h-3 w-3 mr-1" />
                      Analyze
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <Textarea
                  ref={textareaRef}
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  className="min-h-[500px] font-mono text-sm bg-slate-900 border-slate-600 text-white"
                  placeholder={
                    activeMCP
                      ? "// Start typing... File will be auto-indexed\n// Bengali content will be detected and completed\n// MCP will provide intelligent suggestions"
                      : "// No Provider, No Model Available\n// Please install Ollama or LM Studio\n// Or configure cloud fallback"
                  }
                />

                {/* Inline Suggestions */}
                {agentActions.length > 0 && (
                  <div className="mt-4 space-y-2">
                    <div className="text-sm font-medium text-white">Active Suggestions:</div>
                    {agentActions.slice(0, 2).map((action) => (
                      <Alert key={action.id} className="bg-slate-700 border-slate-600">
                        <Lightbulb className="h-4 w-4 text-yellow-400" />
                        <AlertDescription>
                          <div className="space-y-2">
                            <div className="text-sm text-white">
                              Line {action.line}: {action.bengaliExplanation}
                            </div>
                            <div className="text-xs text-gray-300">{action.reasoning}</div>
                            <div className="flex gap-2">
                              <Button
                                size="sm"
                                onClick={() => executeAgentAction(action)}
                                className="h-7 bg-green-600 hover:bg-green-700"
                              >
                                <CheckCircle className="h-3 w-3 mr-1" />
                                Apply
                              </Button>
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() => setAgentActions((prev) => prev.filter((a) => a.id !== action.id))}
                                className="h-7 border-slate-600"
                              >
                                <XCircle className="h-3 w-3 mr-1" />
                                Dismiss
                              </Button>
                            </div>
                          </div>
                        </AlertDescription>
                      </Alert>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Console & Status */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center gap-2 text-white">
                  <Terminal className="h-4 w-4" />
                  System Console
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-32 w-full border border-slate-600 rounded p-3 bg-slate-900">
                  {consoleOutput.map((output, index) => (
                    <div key={index} className="text-xs text-gray-300 mb-1 font-mono">
                      {output}
                    </div>
                  ))}
                </ScrollArea>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
