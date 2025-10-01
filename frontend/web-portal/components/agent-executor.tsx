"use client"

import { useState, useCallback } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Progress } from "@/components/ui/progress"
import { Activity, Zap, CheckCircle, XCircle, AlertTriangle, Code, GitBranch, Lightbulb } from "lucide-react"

interface AgentAction {
  id: string
  type: "suggestion" | "fix" | "refactor" | "complete" | "explain" | "optimize"
  line: number
  column: number
  original: string
  suggested: string
  confidence: number
  reasoning: string
  bengaliExplanation: string
  mode: "strict" | "soft"
  priority: "low" | "medium" | "high" | "critical"
  category: "syntax" | "logic" | "performance" | "style" | "bengali" | "security"
  estimatedImpact: number
  dependencies: string[]
}

interface ExecutionResult {
  actionId: string
  success: boolean
  appliedChanges: string[]
  errors: string[]
  warnings: string[]
  executionTime: number
}

interface AgentExecutorProps {
  actions: AgentAction[]
  onActionExecuted: (result: ExecutionResult) => void
  onActionDismissed: (actionId: string) => void
  mode: "strict" | "soft"
  onModeChange: (mode: "strict" | "soft") => void
}

export function AgentExecutor({
  actions,
  onActionExecuted,
  onActionDismissed,
  mode,
  onModeChange,
}: AgentExecutorProps) {
  const [executingActions, setExecutingActions] = useState<Set<string>>(new Set())
  const [executionHistory, setExecutionHistory] = useState<ExecutionResult[]>([])
  const [autoExecute, setAutoExecute] = useState(false)
  const [batchMode, setBatchMode] = useState(false)
  const [selectedActions, setSelectedActions] = useState<Set<string>>(new Set())

  // Execute single action
  const executeAction = useCallback(
    async (action: AgentAction) => {
      setExecutingActions((prev) => new Set([...prev, action.id]))

      // Simulate execution time based on action complexity
      const executionTime = action.priority === "critical" ? 500 : action.priority === "high" ? 300 : 200

      await new Promise((resolve) => setTimeout(resolve, executionTime))

      const result: ExecutionResult = {
        actionId: action.id,
        success: Math.random() > 0.1, // 90% success rate
        appliedChanges: [],
        errors: [],
        warnings: [],
        executionTime,
      }

      if (result.success) {
        result.appliedChanges = [`Line ${action.line}: Applied ${action.type} suggestion`]

        // Add warnings for risky operations
        if (action.type === "refactor" && action.confidence < 80) {
          result.warnings.push("Low confidence refactoring - please review changes")
        }

        if (action.category === "security") {
          result.warnings.push("Security-related change applied - verify functionality")
        }
      } else {
        result.errors = ["Failed to apply changes", "Syntax conflict detected"]
      }

      setExecutionHistory((prev) => [result, ...prev.slice(0, 19)])
      setExecutingActions((prev) => {
        const newSet = new Set(prev)
        newSet.delete(action.id)
        return newSet
      })

      onActionExecuted(result)
    },
    [onActionExecuted],
  )

  // Execute batch of actions
  const executeBatch = useCallback(async () => {
    const actionsToExecute = actions.filter((action) => selectedActions.has(action.id))

    for (const action of actionsToExecute) {
      await executeAction(action)
      // Small delay between batch executions
      await new Promise((resolve) => setTimeout(resolve, 100))
    }

    setSelectedActions(new Set())
  }, [actions, selectedActions, executeAction])

  // Auto-execute high priority actions in strict mode
  const autoExecuteHighPriority = useCallback(() => {
    if (mode === "strict" && autoExecute) {
      const highPriorityActions = actions.filter(
        (action) => (action.priority === "critical" || action.priority === "high") && action.confidence > 90,
      )

      highPriorityActions.forEach((action) => {
        if (!executingActions.has(action.id)) {
          executeAction(action)
        }
      })
    }
  }, [mode, autoExecute, actions, executingActions, executeAction])

  // Toggle action selection for batch mode
  const toggleActionSelection = useCallback((actionId: string) => {
    setSelectedActions((prev) => {
      const newSet = new Set(prev)
      if (newSet.has(actionId)) {
        newSet.delete(actionId)
      } else {
        newSet.add(actionId)
      }
      return newSet
    })
  }, [])

  const getActionIcon = (type: AgentAction["type"]) => {
    switch (type) {
      case "fix":
        return <CheckCircle className="h-3 w-3 text-green-600" />
      case "refactor":
        return <GitBranch className="h-3 w-3 text-blue-600" />
      case "complete":
        return <Code className="h-3 w-3 text-purple-600" />
      case "optimize":
        return <Zap className="h-3 w-3 text-yellow-600" />
      case "explain":
        return <Lightbulb className="h-3 w-3 text-orange-600" />
      default:
        return <Activity className="h-3 w-3 text-gray-600" />
    }
  }

  const getPriorityColor = (priority: AgentAction["priority"]) => {
    switch (priority) {
      case "critical":
        return "bg-red-100 text-red-800"
      case "high":
        return "bg-orange-100 text-orange-800"
      case "medium":
        return "bg-yellow-100 text-yellow-800"
      case "low":
        return "bg-green-100 text-green-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getCategoryColor = (category: AgentAction["category"]) => {
    switch (category) {
      case "security":
        return "bg-red-100 text-red-800"
      case "performance":
        return "bg-blue-100 text-blue-800"
      case "bengali":
        return "bg-orange-100 text-orange-800"
      case "syntax":
        return "bg-purple-100 text-purple-800"
      case "logic":
        return "bg-green-100 text-green-800"
      case "style":
        return "bg-gray-100 text-gray-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  return (
    <div className="space-y-4">
      {/* Agent Controls */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-sm flex items-center gap-2">
            <Activity className="h-4 w-4" />
            Agent Executor
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Mode Controls */}
          <div className="flex items-center justify-between">
            <Label className="text-sm">Execution Mode:</Label>
            <div className="flex items-center gap-2">
              <span className="text-xs text-gray-500">Soft</span>
              <Switch
                checked={mode === "strict"}
                onCheckedChange={(checked) => onModeChange(checked ? "strict" : "soft")}
              />
              <span className="text-xs text-gray-500">Strict</span>
            </div>
          </div>

          {/* Auto Execute */}
          <div className="flex items-center justify-between">
            <Label className="text-sm">Auto Execute High Priority:</Label>
            <Switch checked={autoExecute} onCheckedChange={setAutoExecute} disabled={mode !== "strict"} />
          </div>

          {/* Batch Mode */}
          <div className="flex items-center justify-between">
            <Label className="text-sm">Batch Mode:</Label>
            <Switch checked={batchMode} onCheckedChange={setBatchMode} />
          </div>

          {/* Batch Controls */}
          {batchMode && (
            <div className="flex gap-2">
              <Button size="sm" onClick={executeBatch} disabled={selectedActions.size === 0} className="flex-1">
                Execute Selected ({selectedActions.size})
              </Button>
              <Button size="sm" variant="outline" onClick={() => setSelectedActions(new Set(actions.map((a) => a.id)))}>
                Select All
              </Button>
              <Button size="sm" variant="outline" onClick={() => setSelectedActions(new Set())}>
                Clear
              </Button>
            </div>
          )}

          {/* Mode Explanation */}
          <Alert>
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription className="text-xs">
              {mode === "strict" ? (
                <div>
                  <strong>Strict Mode:</strong> Actions are applied directly to code. High-confidence actions may
                  auto-execute.
                </div>
              ) : (
                <div>
                  <strong>Soft Mode:</strong> Actions are shown as suggestions. Manual approval required for all
                  changes.
                </div>
              )}
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>

      {/* Active Actions */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-sm">Pending Actions ({actions.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-64">
            <div className="space-y-3">
              {actions.map((action) => (
                <div key={action.id} className="border rounded-lg p-3 space-y-2">
                  {/* Action Header */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {batchMode && (
                        <input
                          type="checkbox"
                          checked={selectedActions.has(action.id)}
                          onChange={() => toggleActionSelection(action.id)}
                          className="rounded"
                        />
                      )}
                      {getActionIcon(action.type)}
                      <span className="font-medium text-sm">Line {action.line}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Badge variant="outline" className={`text-xs ${getPriorityColor(action.priority)}`}>
                        {action.priority}
                      </Badge>
                      <Badge variant="outline" className={`text-xs ${getCategoryColor(action.category)}`}>
                        {action.category}
                      </Badge>
                      <Badge variant="secondary" className="text-xs">
                        {action.confidence}%
                      </Badge>
                    </div>
                  </div>

                  {/* Bengali Explanation */}
                  <div className="text-sm text-blue-600 font-medium">{action.bengaliExplanation}</div>

                  {/* Technical Reasoning */}
                  <div className="text-xs text-gray-600">{action.reasoning}</div>

                  {/* Code Preview */}
                  <div className="bg-gray-50 p-2 rounded text-xs font-mono">
                    <div className="text-red-600 mb-1">- {action.original}</div>
                    <div className="text-green-600">+ {action.suggested.split("\n")[0]}...</div>
                  </div>

                  {/* Impact & Dependencies */}
                  {action.estimatedImpact > 0 && (
                    <div className="flex items-center gap-2 text-xs">
                      <span className="text-gray-500">Impact:</span>
                      <Progress value={action.estimatedImpact} className="h-1 flex-1" />
                      <span className="text-gray-500">{action.estimatedImpact}%</span>
                    </div>
                  )}

                  {action.dependencies.length > 0 && (
                    <div className="text-xs text-gray-500">Dependencies: {action.dependencies.join(", ")}</div>
                  )}

                  {/* Action Buttons */}
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      onClick={() => executeAction(action)}
                      disabled={executingActions.has(action.id)}
                      className="h-7"
                    >
                      {executingActions.has(action.id) ? (
                        <>
                          <Activity className="h-3 w-3 mr-1 animate-spin" />
                          Executing...
                        </>
                      ) : (
                        <>
                          <CheckCircle className="h-3 w-3 mr-1" />
                          {mode === "strict" ? "Execute" : "Apply"}
                        </>
                      )}
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => onActionDismissed(action.id)} className="h-7">
                      <XCircle className="h-3 w-3 mr-1" />
                      Dismiss
                    </Button>
                  </div>
                </div>
              ))}

              {actions.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  <Activity className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p>No pending actions</p>
                </div>
              )}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>

      {/* Execution History */}
      {executionHistory.length > 0 && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm">Execution History ({executionHistory.length})</CardTitle>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-48">
              <div className="space-y-2">
                {executionHistory.map((result, index) => (
                  <div key={`${result.actionId}-${index}`} className="border rounded p-2 space-y-1">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        {result.success ? (
                          <CheckCircle className="h-3 w-3 text-green-500" />
                        ) : (
                          <XCircle className="h-3 w-3 text-red-500" />
                        )}
                        <span className="text-sm font-medium">{result.success ? "Success" : "Failed"}</span>
                      </div>
                      <span className="text-xs text-gray-500">{result.executionTime}ms</span>
                    </div>

                    {result.appliedChanges.length > 0 && (
                      <div className="text-xs text-green-600">
                        {result.appliedChanges.map((change, i) => (
                          <div key={i}>✓ {change}</div>
                        ))}
                      </div>
                    )}

                    {result.warnings.length > 0 && (
                      <div className="text-xs text-yellow-600">
                        {result.warnings.map((warning, i) => (
                          <div key={i}>⚠ {warning}</div>
                        ))}
                      </div>
                    )}

                    {result.errors.length > 0 && (
                      <div className="text-xs text-red-600">
                        {result.errors.map((error, i) => (
                          <div key={i}>✗ {error}</div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
