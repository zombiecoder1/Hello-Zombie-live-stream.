"use client"

import { useState, useCallback, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Server, Wifi, WifiOff, Cloud, HardDrive, Zap, AlertTriangle, CheckCircle } from "lucide-react"

interface MCPProvider {
  id: string
  name: string
  type: "local" | "cloud" | "hybrid"
  status: "connected" | "disconnected" | "error" | "fallback"
  latency: number
  capabilities: string[]
  modelPath?: string
  apiEndpoint?: string
  priority: number
  lastUsed?: Date
  errorCount: number
  successRate: number
}

interface MCPRequest {
  id: string
  timestamp: Date
  type: "completion" | "analysis" | "translation" | "suggestion"
  content: string
  provider: string
  status: "pending" | "success" | "failed" | "fallback"
  latency?: number
  response?: string
}

interface MCPManagerProps {
  onProviderChange: (provider: MCPProvider | null) => void
  onRequestComplete: (request: MCPRequest) => void
}

export function MCPManager({ onProviderChange, onRequestComplete }: MCPManagerProps) {
  const [providers, setProviders] = useState<MCPProvider[]>([
    {
      id: "local-ollama",
      name: "Ollama Local",
      type: "local",
      status: "disconnected",
      latency: 0,
      capabilities: ["code-completion", "bengali-translation", "error-detection"],
      modelPath: "/usr/local/bin/ollama",
      priority: 1,
      errorCount: 0,
      successRate: 0,
    },
    {
      id: "local-lmstudio",
      name: "LM Studio",
      type: "local",
      status: "disconnected",
      latency: 0,
      capabilities: ["code-generation", "refactoring", "documentation"],
      modelPath: "/Applications/LM Studio.app",
      priority: 2,
      errorCount: 0,
      successRate: 0,
    },
    {
      id: "hybrid-local-server",
      name: "Local Server",
      type: "hybrid",
      status: "disconnected",
      latency: 0,
      capabilities: ["full-context", "bengali-nlp", "code-analysis"],
      apiEndpoint: "http://localhost:8080/api/v1",
      priority: 3,
      errorCount: 0,
      successRate: 0,
    },
    {
      id: "cloud-fallback",
      name: "Cloud Fallback",
      type: "cloud",
      status: "disconnected",
      latency: 0,
      capabilities: ["full-context", "bengali-nlp", "advanced-reasoning"],
      apiEndpoint: "https://api.example.com/v1",
      priority: 4,
      errorCount: 0,
      successRate: 0,
    },
  ])

  const [activeProvider, setActiveProvider] = useState<string | null>(null)
  const [recentRequests, setRecentRequests] = useState<MCPRequest[]>([])
  const [isScanning, setIsScanning] = useState(false)
  const [fallbackChain, setFallbackChain] = useState<string[]>([])

  // Scan for available providers
  const scanProviders = useCallback(async () => {
    setIsScanning(true)

    for (const provider of providers) {
      // Simulate provider detection
      await new Promise((resolve) => setTimeout(resolve, 500))

      let status: MCPProvider["status"] = "disconnected"
      let latency = 0

      if (provider.type === "local") {
        // Simulate local model detection
        const hasModel = Math.random() > 0.3 // 70% chance of having local model
        if (hasModel) {
          status = "connected"
          latency = Math.random() * 100 + 20 // 20-120ms
        }
      } else if (provider.type === "hybrid") {
        // Simulate local server check
        const serverRunning = Math.random() > 0.5 // 50% chance
        if (serverRunning) {
          status = "connected"
          latency = Math.random() * 50 + 10 // 10-60ms
        }
      } else if (provider.type === "cloud") {
        // Cloud is usually available but with higher latency
        status = "connected"
        latency = Math.random() * 200 + 100 // 100-300ms
      }

      setProviders((prev) =>
        prev.map((p) =>
          p.id === provider.id
            ? {
                ...p,
                status,
                latency,
                successRate: status === "connected" ? Math.random() * 30 + 70 : 0, // 70-100%
              }
            : p,
        ),
      )
    }

    setIsScanning(false)

    // Set active provider to the first available one with highest priority
    const availableProviders = providers.filter((p) => p.status === "connected").sort((a, b) => a.priority - b.priority)

    if (availableProviders.length > 0) {
      setActiveProvider(availableProviders[0].id)
      onProviderChange(availableProviders[0])

      // Create fallback chain
      setFallbackChain(availableProviders.map((p) => p.id))
    } else {
      setActiveProvider(null)
      onProviderChange(null)
      setFallbackChain([])
    }
  }, [providers, onProviderChange])

  // Make MCP request with fallback
  const makeRequest = useCallback(
    async (type: MCPRequest["type"], content: string): Promise<MCPRequest> => {
      const requestId = Date.now().toString()
      const request: MCPRequest = {
        id: requestId,
        timestamp: new Date(),
        type,
        content,
        provider: activeProvider || "none",
        status: "pending",
      }

      setRecentRequests((prev) => [request, ...prev.slice(0, 9)])

      if (!activeProvider) {
        const failedRequest = { ...request, status: "failed" as const, response: "No provider available" }
        setRecentRequests((prev) => prev.map((r) => (r.id === requestId ? failedRequest : r)))
        onRequestComplete(failedRequest)
        return failedRequest
      }

      // Try primary provider
      let currentProviderIndex = 0
      let finalRequest = request

      while (currentProviderIndex < fallbackChain.length) {
        const providerId = fallbackChain[currentProviderIndex]
        const provider = providers.find((p) => p.id === providerId)

        if (!provider || provider.status !== "connected") {
          currentProviderIndex++
          continue
        }

        try {
          // Simulate request
          const startTime = Date.now()
          await new Promise((resolve) => setTimeout(resolve, provider.latency + Math.random() * 100))

          // Simulate success/failure based on provider reliability
          const success = Math.random() < provider.successRate / 100

          if (success) {
            const latency = Date.now() - startTime
            let response = ""

            // Generate contextual response based on request type
            switch (type) {
              case "completion":
                if (content.includes("আমার সোনার বাংলা")) {
                  response = "আমি তোমায় ভালবাসি // National anthem completion detected"
                } else {
                  response = `// Code completion suggestion for: ${content.slice(0, 30)}...`
                }
                break
              case "analysis":
                response = `Code analysis complete. Found ${Math.floor(Math.random() * 5) + 1} suggestions.`
                break
              case "translation":
                response = `Bengali to English translation: "${content}" -> "English equivalent"`
                break
              case "suggestion":
                response = `Suggestion: Consider using template literals instead of string concatenation`
                break
            }

            finalRequest = {
              ...request,
              status: currentProviderIndex > 0 ? "fallback" : "success",
              provider: providerId,
              latency,
              response,
            }

            // Update provider stats
            setProviders((prev) =>
              prev.map((p) =>
                p.id === providerId
                  ? {
                      ...p,
                      lastUsed: new Date(),
                      successRate: Math.min(100, p.successRate + 1),
                    }
                  : p,
              ),
            )

            break
          } else {
            throw new Error("Provider request failed")
          }
        } catch (error) {
          // Update error count
          setProviders((prev) =>
            prev.map((p) =>
              p.id === providerId
                ? {
                    ...p,
                    errorCount: p.errorCount + 1,
                    successRate: Math.max(0, p.successRate - 2),
                  }
                : p,
            ),
          )

          currentProviderIndex++
        }
      }

      // If all providers failed
      if (finalRequest.status === "pending") {
        finalRequest = {
          ...request,
          status: "failed",
          response: "All providers failed. Check your local models or internet connection.",
        }
      }

      setRecentRequests((prev) => prev.map((r) => (r.id === requestId ? finalRequest : r)))
      onRequestComplete(finalRequest)
      return finalRequest
    },
    [activeProvider, fallbackChain, providers, onRequestComplete],
  )

  // Auto-scan on mount
  useEffect(() => {
    scanProviders()
  }, [])

  const getStatusIcon = (status: MCPProvider["status"]) => {
    switch (status) {
      case "connected":
        return <CheckCircle className="h-3 w-3 text-green-500" />
      case "disconnected":
        return <WifiOff className="h-3 w-3 text-gray-500" />
      case "error":
        return <AlertTriangle className="h-3 w-3 text-red-500" />
      case "fallback":
        return <Zap className="h-3 w-3 text-yellow-500" />
      default:
        return <WifiOff className="h-3 w-3 text-gray-500" />
    }
  }

  const getTypeIcon = (type: MCPProvider["type"]) => {
    switch (type) {
      case "local":
        return <HardDrive className="h-3 w-3" />
      case "cloud":
        return <Cloud className="h-3 w-3" />
      case "hybrid":
        return <Server className="h-3 w-3" />
      default:
        return <Server className="h-3 w-3" />
    }
  }

  return (
    <div className="space-y-4">
      {/* Provider Status */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm flex items-center gap-2">
              <Server className="h-4 w-4" />
              MCP Providers
            </CardTitle>
            <Button size="sm" onClick={scanProviders} disabled={isScanning}>
              {isScanning ? <Wifi className="h-3 w-3 animate-pulse" /> : <Wifi className="h-3 w-3" />}
              {isScanning ? "Scanning..." : "Scan"}
            </Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-3">
          {providers.map((provider) => (
            <div
              key={provider.id}
              className={`p-3 rounded border cursor-pointer transition-colors ${
                activeProvider === provider.id
                  ? "border-blue-500 bg-blue-50"
                  : provider.status === "connected"
                    ? "border-green-200 hover:border-green-300"
                    : "border-gray-200 hover:border-gray-300"
              }`}
              onClick={() => {
                if (provider.status === "connected") {
                  setActiveProvider(provider.id)
                  onProviderChange(provider)
                }
              }}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  {getStatusIcon(provider.status)}
                  {getTypeIcon(provider.type)}
                  <span className="font-medium text-sm">{provider.name}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant={provider.type === "local" ? "default" : "secondary"} className="text-xs">
                    {provider.type}
                  </Badge>
                  {provider.status === "connected" && (
                    <Badge variant="outline" className="text-xs">
                      {Math.round(provider.latency)}ms
                    </Badge>
                  )}
                </div>
              </div>

              {provider.status === "connected" && (
                <div className="space-y-1">
                  <div className="flex justify-between text-xs text-gray-600">
                    <span>Success Rate:</span>
                    <span>{Math.round(provider.successRate)}%</span>
                  </div>
                  <Progress value={provider.successRate} className="h-1" />
                  <div className="flex flex-wrap gap-1 mt-2">
                    {provider.capabilities.slice(0, 3).map((cap) => (
                      <Badge key={cap} variant="outline" className="text-xs">
                        {cap}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}

              {provider.status === "disconnected" && (
                <div className="text-xs text-gray-500">
                  {provider.type === "local" ? "Model not found" : "Service unavailable"}
                </div>
              )}
            </div>
          ))}

          {/* Fallback Chain */}
          {fallbackChain.length > 1 && (
            <Alert>
              <Zap className="h-4 w-4" />
              <AlertDescription className="text-sm">
                <div className="font-medium mb-1">Fallback Chain:</div>
                <div className="flex items-center gap-2">
                  {fallbackChain.map((providerId, index) => (
                    <div key={providerId} className="flex items-center gap-1">
                      <span className="text-xs">{providers.find((p) => p.id === providerId)?.name}</span>
                      {index < fallbackChain.length - 1 && <span className="text-gray-400">→</span>}
                    </div>
                  ))}
                </div>
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Recent Requests */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-sm">Recent Requests ({recentRequests.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-48">
            <div className="space-y-2">
              {recentRequests.map((request) => (
                <div key={request.id} className="border rounded p-2 space-y-1">
                  <div className="flex items-center justify-between">
                    <Badge variant="outline" className="text-xs">
                      {request.type}
                    </Badge>
                    <div className="flex items-center gap-2">
                      <Badge
                        variant={
                          request.status === "success"
                            ? "default"
                            : request.status === "fallback"
                              ? "secondary"
                              : "destructive"
                        }
                        className="text-xs"
                      >
                        {request.status}
                      </Badge>
                      {request.latency && <span className="text-xs text-gray-500">{request.latency}ms</span>}
                    </div>
                  </div>
                  <div className="text-xs text-gray-600 truncate">{request.content}</div>
                  {request.response && (
                    <div className="text-xs bg-gray-50 p-1 rounded font-mono">{request.response}</div>
                  )}
                  <div className="text-xs text-gray-400">
                    {request.timestamp.toLocaleTimeString()} • {request.provider}
                  </div>
                </div>
              ))}
              {recentRequests.length === 0 && (
                <div className="text-center text-gray-500 text-sm py-4">No recent requests</div>
              )}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>

      {/* Test Request */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-sm">Test MCP</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <Button
            size="sm"
            onClick={() => makeRequest("completion", "আমার সোনার বাংলা")}
            disabled={!activeProvider}
            className="w-full"
          >
            Test Bengali Completion
          </Button>
          <Button
            size="sm"
            onClick={() => makeRequest("analysis", "function test() { console.log('hello'); }")}
            disabled={!activeProvider}
            className="w-full"
            variant="outline"
          >
            Test Code Analysis
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
