"use client"

import { useState, useCallback, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Database, HardDrive, Download, CheckCircle, XCircle, Search, Zap } from "lucide-react"

interface DetectedModel {
  id: string
  name: string
  path: string
  size: string
  type: "ollama" | "lmstudio" | "huggingface" | "custom"
  capabilities: string[]
  language: string[]
  status: "available" | "loading" | "error" | "downloading"
  performance: {
    speed: number // tokens/sec
    memory: number // GB
    accuracy: number // percentage
  }
  lastUsed?: Date
  downloadProgress?: number
}

interface ModelDetectorProps {
  onModelSelected: (model: DetectedModel) => void
  onModelsDetected: (models: DetectedModel[]) => void
}

export function ModelDetector({ onModelSelected, onModelsDetected }: ModelDetectorProps) {
  const [models, setModels] = useState<DetectedModel[]>([])
  const [isScanning, setIsScanning] = useState(false)
  const [scanProgress, setScanProgress] = useState(0)
  const [selectedModel, setSelectedModel] = useState<string | null>(null)
  const [recommendedModels, setRecommendedModels] = useState<DetectedModel[]>([])

  // Simulate model detection
  const scanForModels = useCallback(async () => {
    setIsScanning(true)
    setScanProgress(0)

    const scanLocations = [
      "Scanning Ollama models...",
      "Checking LM Studio...",
      "Looking for HuggingFace cache...",
      "Searching custom locations...",
      "Validating model integrity...",
    ]

    for (let i = 0; i < scanLocations.length; i++) {
      await new Promise((resolve) => setTimeout(resolve, 800))
      setScanProgress(((i + 1) / scanLocations.length) * 100)
    }

    // Simulate found models
    const detectedModels: DetectedModel[] = [
      {
        id: "ollama-llama3.2-3b",
        name: "Llama 3.2 3B",
        path: "/usr/local/bin/ollama/models/llama3.2:3b",
        size: "2.1 GB",
        type: "ollama",
        capabilities: ["code-completion", "chat", "reasoning"],
        language: ["english", "bengali"],
        status: "available",
        performance: {
          speed: 45,
          memory: 4.2,
          accuracy: 87,
        },
        lastUsed: new Date(Date.now() - 86400000),
      },
      {
        id: "ollama-codellama-7b",
        name: "CodeLlama 7B",
        path: "/usr/local/bin/ollama/models/codellama:7b",
        size: "3.8 GB",
        type: "ollama",
        capabilities: ["code-generation", "debugging", "refactoring"],
        language: ["english"],
        status: "available",
        performance: {
          speed: 32,
          memory: 6.1,
          accuracy: 92,
        },
        lastUsed: new Date(Date.now() - 3600000),
      },
      {
        id: "lmstudio-bengali-assistant",
        name: "Bengali Code Assistant",
        path: "/Applications/LM Studio.app/models/bengali-assistant-7b",
        size: "4.2 GB",
        type: "lmstudio",
        capabilities: ["bengali-translation", "code-explanation", "documentation"],
        language: ["bengali", "english"],
        status: "available",
        performance: {
          speed: 28,
          memory: 7.3,
          accuracy: 89,
        },
      },
      {
        id: "huggingface-whisper-bengali",
        name: "Whisper Bengali",
        path: "~/.cache/huggingface/transformers/whisper-large-v3-bengali",
        size: "1.5 GB",
        type: "huggingface",
        capabilities: ["speech-to-text", "bengali-transcription"],
        language: ["bengali"],
        status: "available",
        performance: {
          speed: 15,
          memory: 2.8,
          accuracy: 94,
        },
      },
    ]

    // Simulate some models not being available
    if (Math.random() > 0.3) {
      detectedModels.push({
        id: "recommended-deepseek-coder",
        name: "DeepSeek Coder 6.7B",
        path: "Not installed",
        size: "3.5 GB",
        type: "ollama",
        capabilities: ["code-generation", "debugging", "optimization"],
        language: ["english", "bengali"],
        status: "error",
        performance: {
          speed: 38,
          memory: 5.9,
          accuracy: 91,
        },
      })
    }

    setModels(detectedModels.filter((m) => m.status === "available"))
    setRecommendedModels(detectedModels.filter((m) => m.status === "error"))
    setIsScanning(false)
    setScanProgress(0)

    onModelsDetected(detectedModels.filter((m) => m.status === "available"))

    // Auto-select best model
    const bestModel = detectedModels
      .filter((m) => m.status === "available")
      .sort((a, b) => b.performance.accuracy - a.performance.accuracy)[0]

    if (bestModel) {
      setSelectedModel(bestModel.id)
      onModelSelected(bestModel)
    }
  }, [onModelsDetected, onModelSelected])

  // Download/Install model
  const installModel = useCallback(async (model: DetectedModel) => {
    setModels((prev) => prev.map((m) => (m.id === model.id ? { ...m, status: "downloading", downloadProgress: 0 } : m)))

    // Simulate download progress
    for (let progress = 0; progress <= 100; progress += 5) {
      await new Promise((resolve) => setTimeout(resolve, 200))
      setModels((prev) => prev.map((m) => (m.id === model.id ? { ...m, downloadProgress: progress } : m)))
    }

    // Mark as available
    setModels((prev) =>
      prev.map((m) => (m.id === model.id ? { ...m, status: "available", downloadProgress: undefined } : m)),
    )

    // Move from recommended to available
    setRecommendedModels((prev) => prev.filter((m) => m.id !== model.id))
    setModels((prev) => [...prev, { ...model, status: "available" }])
  }, [])

  // Select model
  const selectModel = useCallback(
    (model: DetectedModel) => {
      setSelectedModel(model.id)
      onModelSelected(model)
    },
    [onModelSelected],
  )

  // Auto-scan on mount
  useEffect(() => {
    scanForModels()
  }, [scanForModels])

  const getModelIcon = (type: DetectedModel["type"]) => {
    switch (type) {
      case "ollama":
        return <Database className="h-4 w-4 text-blue-600" />
      case "lmstudio":
        return <HardDrive className="h-4 w-4 text-green-600" />
      case "huggingface":
        return <Download className="h-4 w-4 text-orange-600" />
      case "custom":
        return <Zap className="h-4 w-4 text-purple-600" />
      default:
        return <Database className="h-4 w-4 text-gray-600" />
    }
  }

  const getPerformanceColor = (score: number) => {
    if (score >= 90) return "text-green-600"
    if (score >= 80) return "text-yellow-600"
    if (score >= 70) return "text-orange-600"
    return "text-red-600"
  }

  return (
    <div className="space-y-4">
      {/* Scanner */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm flex items-center gap-2">
              <Search className="h-4 w-4" />
              Model Scanner
            </CardTitle>
            <Button size="sm" onClick={scanForModels} disabled={isScanning}>
              {isScanning ? (
                <>
                  <Search className="h-3 w-3 mr-1 animate-spin" />
                  Scanning...
                </>
              ) : (
                <>
                  <Search className="h-3 w-3 mr-1" />
                  Scan Again
                </>
              )}
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {isScanning && (
            <div className="space-y-2">
              <Progress value={scanProgress} className="h-2" />
              <div className="text-xs text-gray-500">Scanning local models... {Math.round(scanProgress)}%</div>
            </div>
          )}

          {!isScanning && (
            <div className="text-sm text-gray-600">
              Found {models.length} available models • {recommendedModels.length} recommended for download
            </div>
          )}
        </CardContent>
      </Card>

      {/* Available Models */}
      {models.length > 0 && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm">Available Models ({models.length})</CardTitle>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-64">
              <div className="space-y-3">
                {models.map((model) => (
                  <div
                    key={model.id}
                    className={`border rounded-lg p-3 cursor-pointer transition-colors ${
                      selectedModel === model.id
                        ? "border-blue-500 bg-blue-50"
                        : "border-gray-200 hover:border-gray-300"
                    }`}
                    onClick={() => selectModel(model)}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        {getModelIcon(model.type)}
                        <span className="font-medium text-sm">{model.name}</span>
                        {selectedModel === model.id && <CheckCircle className="h-4 w-4 text-blue-600" />}
                      </div>
                      <Badge variant="outline" className="text-xs">
                        {model.size}
                      </Badge>
                    </div>

                    <div className="space-y-2">
                      {/* Performance Metrics */}
                      <div className="grid grid-cols-3 gap-2 text-xs">
                        <div className="text-center">
                          <div className={`font-medium ${getPerformanceColor(model.performance.accuracy)}`}>
                            {model.performance.accuracy}%
                          </div>
                          <div className="text-gray-500">Accuracy</div>
                        </div>
                        <div className="text-center">
                          <div className="font-medium text-blue-600">{model.performance.speed}/s</div>
                          <div className="text-gray-500">Speed</div>
                        </div>
                        <div className="text-center">
                          <div className="font-medium text-purple-600">{model.performance.memory}GB</div>
                          <div className="text-gray-500">Memory</div>
                        </div>
                      </div>

                      {/* Capabilities */}
                      <div className="flex flex-wrap gap-1">
                        {model.capabilities.slice(0, 3).map((cap) => (
                          <Badge key={cap} variant="secondary" className="text-xs">
                            {cap}
                          </Badge>
                        ))}
                        {model.capabilities.length > 3 && (
                          <Badge variant="outline" className="text-xs">
                            +{model.capabilities.length - 3}
                          </Badge>
                        )}
                      </div>

                      {/* Languages */}
                      <div className="flex items-center gap-1">
                        <span className="text-xs text-gray-500">Languages:</span>
                        {model.language.map((lang) => (
                          <Badge key={lang} variant={lang === "bengali" ? "default" : "outline"} className="text-xs">
                            {lang}
                          </Badge>
                        ))}
                      </div>

                      {model.lastUsed && (
                        <div className="text-xs text-gray-500">Last used: {model.lastUsed.toLocaleDateString()}</div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>
      )}

      {/* Recommended Models */}
      {recommendedModels.length > 0 && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm">Recommended Models</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {recommendedModels.map((model) => (
                <div key={model.id} className="border border-dashed rounded-lg p-3">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      {getModelIcon(model.type)}
                      <span className="font-medium text-sm">{model.name}</span>
                      <XCircle className="h-4 w-4 text-red-500" />
                    </div>
                    <Badge variant="outline" className="text-xs">
                      {model.size}
                    </Badge>
                  </div>

                  <div className="space-y-2">
                    <div className="text-xs text-gray-600">High-performance model for Bengali code assistance</div>

                    <div className="flex flex-wrap gap-1">
                      {model.capabilities.map((cap) => (
                        <Badge key={cap} variant="outline" className="text-xs">
                          {cap}
                        </Badge>
                      ))}
                    </div>

                    <Button
                      size="sm"
                      onClick={() => installModel(model)}
                      disabled={model.status === "downloading"}
                      className="w-full"
                    >
                      {model.status === "downloading" ? (
                        <>
                          <Download className="h-3 w-3 mr-1 animate-bounce" />
                          Downloading... {model.downloadProgress}%
                        </>
                      ) : (
                        <>
                          <Download className="h-3 w-3 mr-1" />
                          Install Model
                        </>
                      )}
                    </Button>

                    {model.status === "downloading" && model.downloadProgress !== undefined && (
                      <Progress value={model.downloadProgress} className="h-1" />
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* No Models Found */}
      {!isScanning && models.length === 0 && recommendedModels.length === 0 && (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-8">
              <Database className="h-12 w-12 mx-auto mb-4 text-gray-400" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No Models Found</h3>
              <p className="text-gray-600 mb-4">
                Install Ollama, LM Studio, or download models to get started with Bengali code assistance.
              </p>
              <div className="space-y-2">
                <Button onClick={scanForModels} className="w-full">
                  <Search className="h-4 w-4 mr-2" />
                  Scan Again
                </Button>
                <Alert>
                  <AlertDescription className="text-xs">
                    <strong>Quick Setup:</strong>
                    <br />
                    1. Install Ollama: <code>curl -fsSL https://ollama.ai/install.sh | sh</code>
                    <br />
                    2. Download model: <code>ollama pull llama3.2:3b</code>
                    <br />
                    3. Restart the scanner
                  </AlertDescription>
                </Alert>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
