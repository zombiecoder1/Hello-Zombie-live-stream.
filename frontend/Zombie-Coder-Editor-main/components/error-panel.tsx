"use client"

import { AlertTriangle, AlertCircle, Info, X } from "lucide-react"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

interface ErrorItem {
  id: string
  file: string
  line: number
  column: number
  message: string
  severity: "error" | "warning" | "info"
  source: string
}

interface ErrorPanelProps {
  errors: ErrorItem[]
  warnings: ErrorItem[]
  onErrorClick: (error: ErrorItem) => void
}

export function ErrorPanel({ errors, warnings, onErrorClick }: ErrorPanelProps) {
  const allIssues = [...errors, ...warnings].sort((a, b) => {
    if (a.severity === "error" && b.severity !== "error") return -1
    if (a.severity !== "error" && b.severity === "error") return 1
    return a.line - b.line
  })

  const getIcon = (severity: string) => {
    switch (severity) {
      case "error":
        return <AlertCircle className="h-4 w-4 text-red-400" />
      case "warning":
        return <AlertTriangle className="h-4 w-4 text-yellow-400" />
      case "info":
        return <Info className="h-4 w-4 text-blue-400" />
      default:
        return <Info className="h-4 w-4 text-gray-400" />
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "error":
        return "border-l-red-400"
      case "warning":
        return "border-l-yellow-400"
      case "info":
        return "border-l-blue-400"
      default:
        return "border-l-gray-400"
    }
  }

  return (
    <div className="h-full bg-[#1e1e1e] border-t border-[#3c3c3c] flex flex-col">
      <div className="flex items-center justify-between p-2 border-b border-[#3c3c3c]">
        <div className="flex items-center gap-2 text-sm text-gray-300">
          <AlertTriangle className="h-4 w-4" />
          Problems
          <div className="flex gap-2">
            {errors.length > 0 && (
              <Badge variant="destructive" className="h-5 text-xs">
                {errors.length} errors
              </Badge>
            )}
            {warnings.length > 0 && (
              <Badge variant="secondary" className="h-5 text-xs bg-yellow-600">
                {warnings.length} warnings
              </Badge>
            )}
          </div>
        </div>
        <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
          <X className="h-3 w-3" />
        </Button>
      </div>

      <ScrollArea className="flex-1">
        {allIssues.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-400">
            <div className="text-center">
              <AlertTriangle className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p>No problems detected</p>
            </div>
          </div>
        ) : (
          <div className="p-2 space-y-1">
            {allIssues.map((issue) => (
              <div
                key={issue.id}
                className={`p-3 bg-[#2d2d30] border-l-2 ${getSeverityColor(issue.severity)} cursor-pointer hover:bg-[#37373d] transition-colors`}
                onClick={() => onErrorClick(issue)}
              >
                <div className="flex items-start gap-2">
                  {getIcon(issue.severity)}
                  <div className="flex-1 min-w-0">
                    <div className="text-sm text-white mb-1">{issue.message}</div>
                    <div className="text-xs text-gray-400 flex items-center gap-2">
                      <span>{issue.file.split("/").pop()}</span>
                      <span>
                        Line {issue.line}, Column {issue.column}
                      </span>
                      <Badge variant="outline" className="text-xs">
                        {issue.source}
                      </Badge>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </ScrollArea>
    </div>
  )
}
