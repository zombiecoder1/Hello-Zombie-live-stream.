"use client"

import { Files, Search, GitBranch, Bug, Puzzle, Settings, User, MessageSquare } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { cn } from "@/lib/utils"

interface ActivityBarProps {
  activeView: string
  onViewChange: (view: string) => void
}

export function ActivityBar({ activeView, onViewChange }: ActivityBarProps) {
  const activities = [
    { id: "explorer", icon: Files, label: "Explorer", shortcut: "Ctrl+Shift+E" },
    { id: "search", icon: Search, label: "Search", shortcut: "Ctrl+Shift+F" },
    { id: "git", icon: GitBranch, label: "Source Control", shortcut: "Ctrl+Shift+G" },
    { id: "debug", icon: Bug, label: "Run and Debug", shortcut: "Ctrl+Shift+D" },
    { id: "extensions", icon: Puzzle, label: "Extensions", shortcut: "Ctrl+Shift+X" },
    { id: "ai", icon: MessageSquare, label: "ZombieCoder AI", shortcut: "Ctrl+Shift+A" },
  ]

  return (
    <div className="w-12 bg-[#333333] flex flex-col items-center border-r border-[#3c3c3c]">
      <TooltipProvider delayDuration={300}>
        <div className="flex-1 flex flex-col items-center py-2 gap-1">
          {activities.map((activity) => (
            <Tooltip key={activity.id}>
              <TooltipTrigger asChild>
                <Button
                  variant="ghost"
                  size="sm"
                  className={cn(
                    "w-10 h-10 p-0 hover:bg-[#464647] relative",
                    activeView === activity.id && "bg-[#464647]",
                  )}
                  onClick={() => onViewChange(activity.id)}
                >
                  <activity.icon className="h-5 w-5 text-gray-300" />
                  {activeView === activity.id && <div className="absolute left-0 top-0 bottom-0 w-0.5 bg-green-400" />}
                </Button>
              </TooltipTrigger>
              <TooltipContent side="right" className="bg-[#1e1e1e] border-[#3c3c3c] text-white text-xs">
                <p>{activity.label}</p>
                <p className="text-gray-400 mt-1">{activity.shortcut}</p>
              </TooltipContent>
            </Tooltip>
          ))}
        </div>

        <div className="flex flex-col items-center py-2 gap-1 border-t border-[#3c3c3c]">
          <Tooltip>
            <TooltipTrigger asChild>
              <Button variant="ghost" size="sm" className="w-10 h-10 p-0 hover:bg-[#464647]">
                <User className="h-5 w-5 text-gray-300" />
              </Button>
            </TooltipTrigger>
            <TooltipContent side="right" className="bg-[#1e1e1e] border-[#3c3c3c] text-white text-xs">
              <p>Account</p>
            </TooltipContent>
          </Tooltip>

          <Tooltip>
            <TooltipTrigger asChild>
              <Button variant="ghost" size="sm" className="w-10 h-10 p-0 hover:bg-[#464647]">
                <Settings className="h-5 w-5 text-gray-300" />
              </Button>
            </TooltipTrigger>
            <TooltipContent side="right" className="bg-[#1e1e1e] border-[#3c3c3c] text-white text-xs">
              <p>Settings</p>
              <p className="text-gray-400 mt-1">Ctrl+,</p>
            </TooltipContent>
          </Tooltip>
        </div>
      </TooltipProvider>
    </div>
  )
}
