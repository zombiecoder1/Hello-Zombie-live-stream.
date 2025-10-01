"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Search, ArrowRight } from "lucide-react"
import { Dialog, DialogContent } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { cn } from "@/lib/utils"

interface Command {
  id: string
  label: string
  category: string
  shortcut?: string
  action: () => void
}

interface CommandPaletteProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  commands: Command[]
}

export function CommandPalette({ open, onOpenChange, commands }: CommandPaletteProps) {
  const [search, setSearch] = useState("")
  const [selectedIndex, setSelectedIndex] = useState(0)

  const filteredCommands = commands.filter(
    (cmd) =>
      cmd.label.toLowerCase().includes(search.toLowerCase()) ||
      cmd.category.toLowerCase().includes(search.toLowerCase()),
  )

  useEffect(() => {
    if (open) {
      setSearch("")
      setSelectedIndex(0)
    }
  }, [open])

  useEffect(() => {
    setSelectedIndex(0)
  }, [search])

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") {
      e.preventDefault()
      setSelectedIndex((prev) => Math.min(prev + 1, filteredCommands.length - 1))
    } else if (e.key === "ArrowUp") {
      e.preventDefault()
      setSelectedIndex((prev) => Math.max(prev - 1, 0))
    } else if (e.key === "Enter" && filteredCommands[selectedIndex]) {
      e.preventDefault()
      filteredCommands[selectedIndex].action()
      onOpenChange(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="p-0 bg-[#252526] border-[#3c3c3c] max-w-2xl top-[20%] translate-y-0">
        <div className="flex items-center border-b border-[#3c3c3c] px-3 py-2">
          <Search className="h-4 w-4 text-gray-400 mr-2" />
          <Input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type a command or search..."
            className="border-0 bg-transparent text-white placeholder-gray-500 focus-visible:ring-0 focus-visible:ring-offset-0"
            autoFocus
          />
        </div>

        <ScrollArea className="max-h-[400px]">
          <div className="py-2">
            {filteredCommands.length === 0 ? (
              <div className="text-center text-gray-500 py-8 text-sm">No commands found</div>
            ) : (
              filteredCommands.map((command, index) => (
                <div
                  key={command.id}
                  className={cn(
                    "flex items-center justify-between px-3 py-2 cursor-pointer",
                    index === selectedIndex ? "bg-[#464647]" : "hover:bg-[#3c3c3c]",
                  )}
                  onClick={() => {
                    command.action()
                    onOpenChange(false)
                  }}
                  onMouseEnter={() => setSelectedIndex(index)}
                >
                  <div className="flex items-center gap-2">
                    <ArrowRight className="h-3 w-3 text-gray-500" />
                    <div>
                      <div className="text-sm text-white">{command.label}</div>
                      <div className="text-xs text-gray-500">{command.category}</div>
                    </div>
                  </div>
                  {command.shortcut && <div className="text-xs text-gray-500">{command.shortcut}</div>}
                </div>
              ))
            )}
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  )
}
