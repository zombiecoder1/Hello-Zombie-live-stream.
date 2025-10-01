"use client"

import { X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface Tab {
  id: string
  name: string
  path: string
  isDirty?: boolean
}

interface TabBarProps {
  tabs: Tab[]
  activeTab: string | null
  onTabSelect: (tabId: string) => void
  onTabClose: (tabId: string) => void
}

export function TabBar({ tabs, activeTab, onTabSelect, onTabClose }: TabBarProps) {
  if (tabs.length === 0) return null

  return (
    <div className="flex bg-[#2d2d30] border-b border-[#3c3c3c] overflow-x-auto">
      {tabs.map((tab) => (
        <div
          key={tab.id}
          className={cn(
            "flex items-center gap-2 px-3 py-2 border-r border-[#3c3c3c] cursor-pointer group min-w-0 max-w-[200px]",
            activeTab === tab.id ? "bg-[#1e1e1e] text-white" : "bg-[#2d2d30] text-gray-300 hover:bg-[#37373d]",
          )}
          onClick={() => onTabSelect(tab.id)}
        >
          <span className="text-sm truncate flex-1">
            {tab.name}
            {tab.isDirty && <span className="ml-1 text-orange-400">●</span>}
          </span>
          <Button
            variant="ghost"
            size="sm"
            className="h-4 w-4 p-0 opacity-0 group-hover:opacity-100 hover:bg-[#464647]"
            onClick={(e) => {
              e.stopPropagation()
              onTabClose(tab.id)
            }}
          >
            <X className="h-3 w-3" />
          </Button>
        </div>
      ))}
    </div>
  )
}
