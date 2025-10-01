"use client"

import { useState, useCallback } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Button } from "@/components/ui/button"
import { Scan, Eye, FileText, Code, Hash, GitBranch, Search } from "lucide-react"

interface LineAnalysis {
  number: number
  content: string
  type: "code" | "comment" | "import" | "function" | "variable" | "class" | "empty" | "bengali"
  entities: string[]
  references: string[]
  bengaliContent?: string[]
  indentation: number
  complexity: number
}

interface FileIndexerProps {
  content: string
  onIndexComplete: (index: any) => void
}

export function FileIndexer({ content, onIndexComplete }: FileIndexerProps) {
  const [isIndexing, setIsIndexing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [analysis, setAnalysis] = useState<LineAnalysis[]>([])
  const [stats, setStats] = useState({
    totalLines: 0,
    codeLines: 0,
    commentLines: 0,
    bengaliLines: 0,
    functions: 0,
    variables: 0,
    imports: 0,
    complexity: 0,
  })

  const analyzeCode = useCallback(async () => {
    setIsIndexing(true)
    setProgress(0)

    const lines = content.split("\n")
    const analyzedLines: LineAnalysis[] = []
    const stats = {
      totalLines: lines.length,
      codeLines: 0,
      commentLines: 0,
      bengaliLines: 0,
      functions: 0,
      variables: 0,
      imports: 0,
      complexity: 0,
    }

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]
      const trimmed = line.trim()

      // Simulate processing delay
      await new Promise((resolve) => setTimeout(resolve, 10))
      setProgress(((i + 1) / lines.length) * 100)

      let type: LineAnalysis["type"] = "code"
      const entities: string[] = []
      const references: string[] = []
      const bengaliContent: string[] = []
      let complexity = 0

      // Determine line type
      if (trimmed === "") {
        type = "empty"
      } else if (trimmed.startsWith("//") || trimmed.startsWith("/*") || trimmed.includes("*/")) {
        type = "comment"
        stats.commentLines++
      } else if (trimmed.startsWith("import") || trimmed.startsWith("require") || trimmed.includes("from ")) {
        type = "import"
        stats.imports++
      } else if (
        trimmed.includes("function") ||
        trimmed.includes("=>") ||
        trimmed.includes("async") ||
        (trimmed.includes("const") && trimmed.includes("="))
      ) {
        if (trimmed.includes("function") || trimmed.includes("=>")) {
          type = "function"
          stats.functions++
          complexity += 2
        } else {
          type = "variable"
          stats.variables++
          complexity += 1
        }
        stats.codeLines++
      } else if (trimmed.includes("class") || trimmed.includes("interface") || trimmed.includes("type")) {
        type = "class"
        stats.codeLines++
        complexity += 3
      } else {
        stats.codeLines++
        complexity += 1
      }

      // Extract Bengali content
      const bengaliMatches = line.match(/[\u0980-\u09FF\s]+/g)
      if (bengaliMatches) {
        bengaliContent.push(...bengaliMatches.map((m) => m.trim()).filter(Boolean))
        if (bengaliContent.length > 0) {
          type = "bengali"
          stats.bengaliLines++
        }
      }

      // Extract entities (identifiers, function names, etc.)
      const identifierMatches = line.match(/\b[a-zA-Z_$][a-zA-Z0-9_$]*\b/g)
      if (identifierMatches) {
        entities.push(...identifierMatches)
      }

      // Extract string literals as potential references
      const stringMatches = line.match(/["'`]([^"'`]*)["'`]/g)
      if (stringMatches) {
        references.push(...stringMatches)
      }

      // Calculate complexity based on control structures
      if (trimmed.includes("if") || trimmed.includes("else") || trimmed.includes("switch")) complexity += 1
      if (trimmed.includes("for") || trimmed.includes("while") || trimmed.includes("forEach")) complexity += 2
      if (trimmed.includes("try") || trimmed.includes("catch") || trimmed.includes("finally")) complexity += 1

      stats.complexity += complexity

      analyzedLines.push({
        number: i + 1,
        content: line,
        type,
        entities: [...new Set(entities)], // Remove duplicates
        references: [...new Set(references)],
        bengaliContent,
        indentation: line.length - line.trimStart().length,
        complexity,
      })
    }

    setAnalysis(analyzedLines)
    setStats(stats)
    setIsIndexing(false)
    setProgress(0)

    // Create comprehensive index
    const index = {
      lines: analyzedLines,
      stats,
      symbols: analyzedLines
        .filter((l) => l.type === "function" || l.type === "variable" || l.type === "class")
        .map((l) => ({
          name: l.entities[0] || "unknown",
          type: l.type,
          line: l.number,
          complexity: l.complexity,
        })),
      bengaliContent: analyzedLines
        .filter((l) => l.bengaliContent && l.bengaliContent.length > 0)
        .map((l) => ({
          line: l.number,
          content: l.bengaliContent,
          context: l.content,
        })),
      imports: analyzedLines
        .filter((l) => l.type === "import")
        .map((l) => ({
          line: l.number,
          content: l.content,
          module: l.content.match(/from\s+['"]([^'"]+)['"]/)?.[1] || "unknown",
        })),
    }

    onIndexComplete(index)
  }, [content, onIndexComplete])

  const getTypeColor = (type: LineAnalysis["type"]) => {
    switch (type) {
      case "function":
        return "bg-blue-100 text-blue-800"
      case "variable":
        return "bg-green-100 text-green-800"
      case "class":
        return "bg-purple-100 text-purple-800"
      case "import":
        return "bg-yellow-100 text-yellow-800"
      case "comment":
        return "bg-gray-100 text-gray-800"
      case "bengali":
        return "bg-orange-100 text-orange-800"
      default:
        return "bg-slate-100 text-slate-800"
    }
  }

  const getTypeIcon = (type: LineAnalysis["type"]) => {
    switch (type) {
      case "function":
        return <Code className="h-3 w-3" />
      case "variable":
        return <Hash className="h-3 w-3" />
      case "class":
        return <GitBranch className="h-3 w-3" />
      case "import":
        return <FileText className="h-3 w-3" />
      case "bengali":
        return <Search className="h-3 w-3" />
      default:
        return <Eye className="h-3 w-3" />
    }
  }

  return (
    <div className="space-y-4">
      {/* Indexing Controls */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-sm flex items-center gap-2">
            <Scan className="h-4 w-4" />
            File Indexer
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Button onClick={analyzeCode} disabled={isIndexing} className="w-full">
            {isIndexing ? (
              <>
                <Scan className="h-3 w-3 mr-1 animate-spin" />
                Indexing... {Math.round(progress)}%
              </>
            ) : (
              <>
                <Eye className="h-3 w-3 mr-1" />
                Start Deep Index
              </>
            )}
          </Button>

          {isIndexing && <Progress value={progress} className="h-2" />}
        </CardContent>
      </Card>

      {/* Statistics */}
      {analysis.length > 0 && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm">Index Statistics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Total Lines:</span>
                  <span className="font-medium">{stats.totalLines}</span>
                </div>
                <div className="flex justify-between">
                  <span>Code Lines:</span>
                  <span className="font-medium">{stats.codeLines}</span>
                </div>
                <div className="flex justify-between">
                  <span>Comments:</span>
                  <span className="font-medium">{stats.commentLines}</span>
                </div>
                <div className="flex justify-between">
                  <span>Bengali Lines:</span>
                  <span className="font-medium">{stats.bengaliLines}</span>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Functions:</span>
                  <span className="font-medium">{stats.functions}</span>
                </div>
                <div className="flex justify-between">
                  <span>Variables:</span>
                  <span className="font-medium">{stats.variables}</span>
                </div>
                <div className="flex justify-between">
                  <span>Imports:</span>
                  <span className="font-medium">{stats.imports}</span>
                </div>
                <div className="flex justify-between">
                  <span>Complexity:</span>
                  <span className="font-medium">{stats.complexity}</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Line Analysis */}
      {analysis.length > 0 && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm">Line-by-Line Analysis</CardTitle>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-64">
              <div className="space-y-1">
                {analysis.slice(0, 50).map((line) => (
                  <div key={line.number} className="flex items-center gap-2 p-1 hover:bg-gray-50 rounded text-xs">
                    <div className="w-8 text-gray-500 text-right">{line.number}</div>
                    <Badge variant="outline" className={`text-xs ${getTypeColor(line.type)}`}>
                      {getTypeIcon(line.type)}
                      {line.type}
                    </Badge>
                    <div className="flex-1 font-mono truncate">{line.content || "(empty)"}</div>
                    {line.complexity > 0 && (
                      <Badge variant="secondary" className="text-xs">
                        C:{line.complexity}
                      </Badge>
                    )}
                  </div>
                ))}
                {analysis.length > 50 && (
                  <div className="text-center text-gray-500 text-xs py-2">
                    ... and {analysis.length - 50} more lines
                  </div>
                )}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
