"use client"

import { useState, useCallback } from "react"

interface LintError {
  id: string
  file: string
  line: number
  column: number
  message: string
  severity: "error" | "warning" | "info"
  source: string
}

export function useLinting() {
  const [errors, setErrors] = useState<LintError[]>([])
  const [warnings, setWarnings] = useState<LintError[]>([])

  const lintFile = useCallback((filePath: string, content: string) => {
    // Simulate linting process
    const newErrors: LintError[] = []
    const newWarnings: LintError[] = []

    // Basic TypeScript/JavaScript linting simulation
    if (
      filePath.endsWith(".ts") ||
      filePath.endsWith(".tsx") ||
      filePath.endsWith(".js") ||
      filePath.endsWith(".jsx")
    ) {
      const lines = content.split("\n")

      lines.forEach((line, index) => {
        // Check for common issues
        if (line.includes("console.log")) {
          newWarnings.push({
            id: `${filePath}-${index}-console`,
            file: filePath,
            line: index + 1,
            column: line.indexOf("console.log") + 1,
            message: "Unexpected console statement",
            severity: "warning",
            source: "eslint",
          })
        }

        if (line.includes("var ")) {
          newWarnings.push({
            id: `${filePath}-${index}-var`,
            file: filePath,
            line: index + 1,
            column: line.indexOf("var ") + 1,
            message: "'var' is deprecated. Use 'let' or 'const' instead",
            severity: "warning",
            source: "eslint",
          })
        }

        // Check for syntax errors (simplified)
        const openBraces = (line.match(/\{/g) || []).length
        const closeBraces = (line.match(/\}/g) || []).length
        if (openBraces !== closeBraces && line.trim().endsWith("{")) {
          // This is normal for opening braces
        } else if (openBraces !== closeBraces) {
          newErrors.push({
            id: `${filePath}-${index}-brace`,
            file: filePath,
            line: index + 1,
            column: 1,
            message: "Mismatched braces",
            severity: "error",
            source: "typescript",
          })
        }

        // Check for missing semicolons (simplified)
        if (line.trim().match(/^(let|const|var|return|import|export).*[^;{}\s]$/)) {
          newWarnings.push({
            id: `${filePath}-${index}-semicolon`,
            file: filePath,
            line: index + 1,
            column: line.length,
            message: "Missing semicolon",
            severity: "warning",
            source: "eslint",
          })
        }
      })
    }

    // Update errors and warnings for this file
    setErrors((prev) => prev.filter((e) => e.file !== filePath).concat(newErrors))
    setWarnings((prev) => prev.filter((w) => w.file !== filePath).concat(newWarnings))
  }, [])

  const clearLinting = useCallback((filePath: string) => {
    setErrors((prev) => prev.filter((e) => e.file !== filePath))
    setWarnings((prev) => prev.filter((w) => w.file !== filePath))
  }, [])

  return {
    errors,
    warnings,
    lintFile,
    clearLinting,
  }
}
