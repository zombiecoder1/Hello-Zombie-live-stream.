"use client"

import { useState } from "react"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"

export function MenuBar() {
  const [activeMenu, setActiveMenu] = useState<string | null>(null)

  const menus = [
    {
      name: "File",
      items: [
        { label: "New File", shortcut: "Ctrl+N" },
        { label: "New Window", shortcut: "Ctrl+Shift+N" },
        { label: "Open File...", shortcut: "Ctrl+O" },
        { label: "Open Folder...", shortcut: "Ctrl+K Ctrl+O" },
        { label: "Open Recent", shortcut: "Ctrl+R" },
        { separator: true },
        { label: "Save", shortcut: "Ctrl+S" },
        { label: "Save As...", shortcut: "Ctrl+Shift+S" },
        { label: "Save All", shortcut: "Ctrl+K S" },
        { separator: true },
        { label: "Close Editor", shortcut: "Ctrl+W" },
        { label: "Close Folder", shortcut: "Ctrl+K F" },
      ],
    },
    {
      name: "Edit",
      items: [
        { label: "Undo", shortcut: "Ctrl+Z" },
        { label: "Redo", shortcut: "Ctrl+Y" },
        { separator: true },
        { label: "Cut", shortcut: "Ctrl+X" },
        { label: "Copy", shortcut: "Ctrl+C" },
        { label: "Paste", shortcut: "Ctrl+V" },
        { separator: true },
        { label: "Find", shortcut: "Ctrl+F" },
        { label: "Replace", shortcut: "Ctrl+H" },
        { label: "Find in Files", shortcut: "Ctrl+Shift+F" },
      ],
    },
    {
      name: "Selection",
      items: [
        { label: "Select All", shortcut: "Ctrl+A" },
        { label: "Expand Selection", shortcut: "Shift+Alt+→" },
        { label: "Shrink Selection", shortcut: "Shift+Alt+←" },
        { separator: true },
        { label: "Copy Line Up", shortcut: "Shift+Alt+↑" },
        { label: "Copy Line Down", shortcut: "Shift+Alt+↓" },
        { label: "Move Line Up", shortcut: "Alt+↑" },
        { label: "Move Line Down", shortcut: "Alt+↓" },
      ],
    },
    {
      name: "View",
      items: [
        { label: "Command Palette", shortcut: "Ctrl+Shift+P" },
        { label: "Open View", shortcut: "Ctrl+Q" },
        { separator: true },
        { label: "Explorer", shortcut: "Ctrl+Shift+E" },
        { label: "Search", shortcut: "Ctrl+Shift+F" },
        { label: "Git", shortcut: "Ctrl+Shift+G" },
        { label: "Debug", shortcut: "Ctrl+Shift+D" },
        { label: "Extensions", shortcut: "Ctrl+Shift+X" },
        { separator: true },
        { label: "Terminal", shortcut: "Ctrl+`" },
        { label: "Output", shortcut: "Ctrl+Shift+U" },
        { label: "Problems", shortcut: "Ctrl+Shift+M" },
      ],
    },
    {
      name: "Go",
      items: [
        { label: "Go to File...", shortcut: "Ctrl+P" },
        { label: "Go to Symbol...", shortcut: "Ctrl+Shift+O" },
        { label: "Go to Line...", shortcut: "Ctrl+G" },
        { separator: true },
        { label: "Go Back", shortcut: "Alt+←" },
        { label: "Go Forward", shortcut: "Alt+→" },
      ],
    },
    {
      name: "Run",
      items: [
        { label: "Start Debugging", shortcut: "F5" },
        { label: "Run Without Debugging", shortcut: "Ctrl+F5" },
        { label: "Stop Debugging", shortcut: "Shift+F5" },
        { separator: true },
        { label: "Toggle Breakpoint", shortcut: "F9" },
      ],
    },
    {
      name: "Terminal",
      items: [
        { label: "New Terminal", shortcut: "Ctrl+Shift+`" },
        { label: "Split Terminal", shortcut: "Ctrl+Shift+5" },
        { label: "Kill Terminal", shortcut: "" },
        { separator: true },
        { label: "Clear Terminal", shortcut: "Ctrl+K" },
      ],
    },
    {
      name: "Help",
      items: [
        { label: "Welcome", shortcut: "" },
        { label: "Documentation", shortcut: "" },
        { label: "Show All Commands", shortcut: "Ctrl+Shift+P" },
        { separator: true },
        { label: "About ZombieCoder", shortcut: "" },
      ],
    },
  ]

  return (
    <div className="h-9 bg-[#323233] border-b border-[#3c3c3c] flex items-center px-2 text-sm">
      <div className="flex items-center gap-1">
        <div className="text-green-400 text-lg mr-2">🧟‍♂️</div>

        {menus.map((menu) => (
          <DropdownMenu key={menu.name} onOpenChange={(open) => setActiveMenu(open ? menu.name : null)}>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                size="sm"
                className="h-7 px-2 text-xs text-gray-300 hover:bg-[#464647] data-[state=open]:bg-[#464647]"
              >
                {menu.name}
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start" className="w-56 bg-[#252526] border-[#3c3c3c] text-gray-300">
              {menu.items.map((item, index) =>
                item.separator ? (
                  <DropdownMenuSeparator key={index} className="bg-[#3c3c3c]" />
                ) : (
                  <DropdownMenuItem key={index} className="text-xs focus:bg-[#464647] focus:text-white">
                    {item.label}
                    {item.shortcut && (
                      <DropdownMenuShortcut className="text-gray-500">{item.shortcut}</DropdownMenuShortcut>
                    )}
                  </DropdownMenuItem>
                ),
              )}
            </DropdownMenuContent>
          </DropdownMenu>
        ))}
      </div>
    </div>
  )
}
