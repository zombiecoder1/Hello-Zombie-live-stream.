"use client"

import { Folder, GitBranch, FileText, Zap, Command } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"

interface WelcomeScreenEnhancedProps {
  onOpenFolder: () => void
  onCloneRepo: () => void
  onNewFile: () => void
  onOpenAI: () => void
}

export function WelcomeScreenEnhanced({ onOpenFolder, onCloneRepo, onNewFile, onOpenAI }: WelcomeScreenEnhancedProps) {
  const shortcuts = [
    { label: "Open Folder", keys: ["Ctrl", "K", "Ctrl", "O"] },
    { label: "New File", keys: ["Ctrl", "N"] },
    { label: "Save", keys: ["Ctrl", "S"] },
    { label: "Find", keys: ["Ctrl", "F"] },
    { label: "Command Palette", keys: ["Ctrl", "Shift", "P"] },
    { label: "Toggle Terminal", keys: ["Ctrl", "`"] },
    { label: "Toggle AI", keys: ["Ctrl", "Shift", "A"] },
  ]

  return (
    <div className="flex items-center justify-center h-full bg-[#1e1e1e]">
      <div className="w-full max-w-3xl px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-300 mb-2">The Next-Gen Bengali AI Code Editor</h1>
          <p className="text-lg text-green-400 font-bengali">"বাংলার কোডারদের অস্ত্র"</p>
        </div>

        {/* Action Cards */}
        <div className="grid grid-cols-2 gap-6 mb-12">
          <Card
            className="bg-[#252526] border-[#3c3c3c] hover:border-blue-500/50 transition-all cursor-pointer group"
            onClick={onOpenFolder}
          >
            <CardContent className="p-8 text-center">
              <div className="mb-4 flex justify-center">
                <div className="w-20 h-20 rounded-xl bg-blue-500/10 flex items-center justify-center group-hover:bg-blue-500/20 transition-all">
                  <Folder className="h-10 w-10 text-blue-400" />
                </div>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Open Folder</h3>
              <p className="text-sm text-gray-400">Start working on your project by opening a folder</p>
            </CardContent>
          </Card>

          <Card
            className="bg-[#252526] border-[#3c3c3c] hover:border-green-500/50 transition-all cursor-pointer group"
            onClick={onCloneRepo}
          >
            <CardContent className="p-8 text-center">
              <div className="mb-4 flex justify-center">
                <div className="w-20 h-20 rounded-xl bg-green-500/10 flex items-center justify-center group-hover:bg-green-500/20 transition-all">
                  <GitBranch className="h-10 w-10 text-green-400" />
                </div>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Clone Repository</h3>
              <p className="text-sm text-gray-400">Clone a repository from GitHub or other sources</p>
            </CardContent>
          </Card>

          <Card
            className="bg-[#252526] border-[#3c3c3c] hover:border-yellow-500/50 transition-all cursor-pointer group"
            onClick={onNewFile}
          >
            <CardContent className="p-8 text-center">
              <div className="mb-4 flex justify-center">
                <div className="w-20 h-20 rounded-xl bg-yellow-500/10 flex items-center justify-center group-hover:bg-yellow-500/20 transition-all">
                  <FileText className="h-10 w-10 text-yellow-400" />
                </div>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">New File</h3>
              <p className="text-sm text-gray-400">Create a new file and start coding immediately</p>
            </CardContent>
          </Card>

          <Card
            className="bg-[#252526] border-[#3c3c3c] hover:border-purple-500/50 transition-all cursor-pointer group"
            onClick={onOpenAI}
          >
            <CardContent className="p-8 text-center">
              <div className="mb-4 flex justify-center">
                <div className="w-20 h-20 rounded-xl bg-purple-500/10 flex items-center justify-center group-hover:bg-purple-500/20 transition-all">
                  <Zap className="h-10 w-10 text-purple-400" />
                </div>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">AI Assistant</h3>
              <p className="text-sm text-gray-400">Get help from ZombieCoder AI in Bengali or English</p>
            </CardContent>
          </Card>
        </div>

        {/* Keyboard Shortcuts */}
        <div className="bg-[#252526] border border-[#3c3c3c] rounded-lg p-6">
          <h3 className="text-sm font-semibold text-gray-300 mb-4 flex items-center gap-2">
            <Command className="h-4 w-4" />
            ⌨️ Keyboard Shortcuts
          </h3>
          <div className="grid grid-cols-2 gap-x-8 gap-y-3">
            {shortcuts.map((shortcut, index) => (
              <div key={index} className="flex items-center justify-between text-sm">
                <span className="text-gray-400">{shortcut.label}</span>
                <div className="flex items-center gap-1">
                  {shortcut.keys.map((key, keyIndex) => (
                    <span key={keyIndex}>
                      <kbd className="px-2 py-1 text-xs bg-[#3c3c3c] border border-[#464647] rounded font-mono">
                        {key}
                      </kbd>
                      {keyIndex < shortcut.keys.length - 1 && <span className="mx-1 text-gray-600">+</span>}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
