"use client"

import { Folder, GitBranch, FileText, Command, Zap } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"

interface WelcomeScreenProps {
  onOpenFolder: () => void
  onCloneRepo: () => void
  onNewFile: () => void
}

export function WelcomeScreen({ onOpenFolder, onCloneRepo, onNewFile }: WelcomeScreenProps) {
  const shortcuts = [
    { label: "Show All Commands", keys: ["Ctrl", "Shift", "P"] },
    { label: "Open File", keys: ["Ctrl", "O"] },
    { label: "Open Folder", keys: ["Ctrl", "K", "Ctrl", "O"] },
    { label: "Open Recent", keys: ["Ctrl", "R"] },
    { label: "Open Chat", keys: ["Ctrl", "Shift", "A"] },
  ]

  return (
    <div className="flex items-center justify-center h-full bg-[#1e1e1e]">
      <div className="w-full max-w-4xl px-8">
        <div className="text-center mb-12">
          <div className="text-8xl mb-6 animate-pulse">🧟‍♂️</div>
          <h1 className="text-5xl font-bold mb-4 zombiecoder-brand">ZombieCoder</h1>
          <p className="text-xl text-gray-400 mb-2">The Next-Gen Bengali AI Code Editor</p>
          <p className="text-sm text-gray-500 font-bengali">"বাংলার কোডারদের অস্ত্র"</p>
        </div>

        <div className="grid grid-cols-2 gap-6 mb-12">
          <Card className="bg-[#252526] border-[#3c3c3c] hover:border-green-400/50 transition-colors cursor-pointer">
            <CardContent className="p-6" onClick={onOpenFolder}>
              <Folder className="h-12 w-12 text-blue-400 mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">Open Folder</h3>
              <p className="text-sm text-gray-400">Start working on your project by opening a folder</p>
            </CardContent>
          </Card>

          <Card className="bg-[#252526] border-[#3c3c3c] hover:border-green-400/50 transition-colors cursor-pointer">
            <CardContent className="p-6" onClick={onCloneRepo}>
              <GitBranch className="h-12 w-12 text-green-400 mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">Clone Repository</h3>
              <p className="text-sm text-gray-400">Clone a repository from GitHub or other sources</p>
            </CardContent>
          </Card>

          <Card className="bg-[#252526] border-[#3c3c3c] hover:border-green-400/50 transition-colors cursor-pointer">
            <CardContent className="p-6" onClick={onNewFile}>
              <FileText className="h-12 w-12 text-yellow-400 mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">New File</h3>
              <p className="text-sm text-gray-400">Create a new file and start coding immediately</p>
            </CardContent>
          </Card>

          <Card className="bg-[#252526] border-[#3c3c3c] hover:border-green-400/50 transition-colors cursor-pointer">
            <CardContent className="p-6">
              <Zap className="h-12 w-12 text-purple-400 mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">AI Assistant</h3>
              <p className="text-sm text-gray-400">Get help from ZombieCoder AI in Bengali or English</p>
            </CardContent>
          </Card>
        </div>

        <div className="bg-[#252526] border border-[#3c3c3c] rounded-lg p-6">
          <h3 className="text-sm font-semibold text-gray-300 mb-4 flex items-center gap-2">
            <Command className="h-4 w-4" />
            Keyboard Shortcuts
          </h3>
          <div className="space-y-3">
            {shortcuts.map((shortcut, index) => (
              <div key={index} className="flex items-center justify-between text-sm">
                <span className="text-gray-400">{shortcut.label}</span>
                <div className="flex items-center gap-1">
                  {shortcut.keys.map((key, keyIndex) => (
                    <span key={keyIndex}>
                      <kbd className="px-2 py-1 text-xs bg-[#3c3c3c] border border-[#464647] rounded">{key}</kbd>
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
