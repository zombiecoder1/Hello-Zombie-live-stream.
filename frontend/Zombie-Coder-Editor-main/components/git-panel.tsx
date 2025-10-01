"use client"

import { useState } from "react"
import { GitBranch, GitCommit, GitPullRequest, Plus, Minus, FileText, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"

interface GitChange {
  file: string
  status: "modified" | "added" | "deleted" | "untracked"
  changes: number
}

export function GitPanel() {
  const [currentBranch, setCurrentBranch] = useState("main")
  const [commitMessage, setCommitMessage] = useState("")
  const [changes] = useState<GitChange[]>([
    { file: "src/App.tsx", status: "modified", changes: 15 },
    { file: "components/Button.tsx", status: "added", changes: 25 },
    { file: "styles/globals.css", status: "modified", changes: 3 },
    { file: "README.md", status: "deleted", changes: 0 },
  ])

  const getStatusColor = (status: GitChange["status"]) => {
    switch (status) {
      case "modified":
        return "text-yellow-400"
      case "added":
        return "text-green-400"
      case "deleted":
        return "text-red-400"
      case "untracked":
        return "text-gray-400"
      default:
        return "text-gray-400"
    }
  }

  const getStatusIcon = (status: GitChange["status"]) => {
    switch (status) {
      case "modified":
        return "M"
      case "added":
        return "A"
      case "deleted":
        return "D"
      case "untracked":
        return "U"
      default:
        return "?"
    }
  }

  return (
    <div className="h-full bg-[#252526] border-l border-[#3c3c3c] flex flex-col">
      <div className="p-3 border-b border-[#3c3c3c]">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-medium text-gray-300 flex items-center gap-2">
            <GitBranch className="h-4 w-4" />
            Git Integration
          </h2>
          <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
            <RefreshCw className="h-3 w-3" />
          </Button>
        </div>

        <div className="flex items-center gap-2 mb-3">
          <Badge variant="outline" className="text-xs">
            <GitBranch className="h-3 w-3 mr-1" />
            {currentBranch}
          </Badge>
          <Badge variant="secondary" className="text-xs">
            {changes.length} changes
          </Badge>
        </div>
      </div>

      <ScrollArea className="flex-1">
        <div className="p-3 space-y-4">
          {/* Changes Section */}
          <div>
            <div className="text-xs text-gray-400 mb-2 flex items-center justify-between">
              <span>Changes ({changes.length})</span>
              <div className="flex gap-1">
                <Button variant="ghost" size="sm" className="h-5 w-5 p-0">
                  <Plus className="h-3 w-3" />
                </Button>
                <Button variant="ghost" size="sm" className="h-5 w-5 p-0">
                  <Minus className="h-3 w-3" />
                </Button>
              </div>
            </div>

            <div className="space-y-1">
              {changes.map((change, index) => (
                <div
                  key={index}
                  className="flex items-center gap-2 p-2 hover:bg-[#2a2a2a] rounded cursor-pointer text-xs"
                >
                  <span className={`font-mono w-4 text-center ${getStatusColor(change.status)}`}>
                    {getStatusIcon(change.status)}
                  </span>
                  <FileText className="h-3 w-3 text-gray-400" />
                  <span className="flex-1 text-gray-300">{change.file}</span>
                  {change.changes > 0 && (
                    <Badge variant="outline" className="text-xs">
                      +{change.changes}
                    </Badge>
                  )}
                </div>
              ))}
            </div>
          </div>

          <Separator className="bg-[#3c3c3c]" />

          {/* Commit Section */}
          <div>
            <div className="text-xs text-gray-400 mb-2">Commit Message</div>
            <Textarea
              value={commitMessage}
              onChange={(e) => setCommitMessage(e.target.value)}
              placeholder="Enter commit message..."
              className="bg-[#3c3c3c] border-[#464647] text-white text-xs min-h-[60px] mb-2"
            />

            <div className="flex gap-2">
              <Button size="sm" className="flex-1 h-7 text-xs" disabled={!commitMessage.trim()}>
                <GitCommit className="h-3 w-3 mr-1" />
                Commit
              </Button>
              <Button variant="outline" size="sm" className="h-7 text-xs bg-transparent">
                <GitCommit className="h-3 w-3 mr-1" />
                Commit & Push
              </Button>
            </div>
          </div>

          <Separator className="bg-[#3c3c3c]" />

          {/* Branch Operations */}
          <div>
            <div className="text-xs text-gray-400 mb-2">Branch Operations</div>
            <div className="space-y-2">
              <Input
                placeholder="New branch name..."
                className="bg-[#3c3c3c] border-[#464647] text-white text-xs h-7"
              />
              <div className="flex gap-2">
                <Button variant="outline" size="sm" className="flex-1 h-7 text-xs bg-transparent">
                  Create Branch
                </Button>
                <Button variant="outline" size="sm" className="flex-1 h-7 text-xs bg-transparent">
                  <GitPullRequest className="h-3 w-3 mr-1" />
                  Pull Request
                </Button>
              </div>
            </div>
          </div>

          <Separator className="bg-[#3c3c3c]" />

          {/* Recent Commits */}
          <div>
            <div className="text-xs text-gray-400 mb-2">Recent Commits</div>
            <div className="space-y-2">
              {[
                { hash: "a1b2c3d", message: "Add voice input feature", author: "ZombieCoder", time: "2 hours ago" },
                { hash: "e4f5g6h", message: "Fix debugger integration", author: "ZombieCoder", time: "1 day ago" },
                { hash: "i7j8k9l", message: "Initial commit", author: "ZombieCoder", time: "2 days ago" },
              ].map((commit, index) => (
                <div key={index} className="p-2 bg-[#3c3c3c] rounded text-xs">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-mono text-blue-400">{commit.hash}</span>
                    <span className="text-gray-400">{commit.time}</span>
                  </div>
                  <div className="text-white mb-1">{commit.message}</div>
                  <div className="text-gray-400">by {commit.author}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </ScrollArea>
    </div>
  )
}
