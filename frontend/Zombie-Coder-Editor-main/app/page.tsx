"use client"

import { useState, useEffect, useRef } from "react"
import { Editor } from "@monaco-editor/react"
import { Sidebar } from "@/components/sidebar"
import { TabBar } from "@/components/tab-bar"
import { StatusBar } from "@/components/status-bar"
import { AgentChatEnhanced } from "@/components/agent-chat-enhanced"
import { TerminalEnhanced } from "@/components/terminal-enhanced"
import { MenuBar } from "@/components/menu-bar"
import { ActivityBar } from "@/components/activity-bar"
import { CommandPalette } from "@/components/command-palette"
import { WelcomeScreenEnhanced } from "@/components/welcome-screen-enhanced"
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from "@/components/ui/resizable"
import { useFileSystem } from "@/hooks/use-file-system"
import { useEditor } from "@/hooks/use-editor"
import { setupMonacoLanguageSupport } from "@/lib/monaco-setup"
import { toast } from "sonner"

export default function ZombieCoderEditor() {
  const [activeView, setActiveView] = useState<string>("explorer")
  const [showWelcomeScreen, setShowWelcomeScreen] = useState(true)
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false)
  const [terminalOpen, setTerminalOpen] = useState(false)
  const [agentChatOpen, setAgentChatOpen] = useState(false)
  const [cursorPosition, setCursorPosition] = useState({ line: 1, column: 1 })
  const [autoSaveEnabled, setAutoSaveEnabled] = useState(true)
  const [lastSaveTime, setLastSaveTime] = useState<Date | null>(null)

  const editorRef = useRef<any>(null)
  const autoSaveTimerRef = useRef<NodeJS.Timeout | null>(null)

  const { files, activeFile, openFile, createFile, deleteFile, updateFileContent } = useFileSystem()
  const { tabs, activeTab, openTab, closeTab, switchTab, updateTabContent } = useEditor()

  useEffect(() => {
    setupMonacoLanguageSupport()

    // Keyboard shortcuts
    const handleKeyboard = (e: KeyboardEvent) => {
      const ctrl = e.ctrlKey || e.metaKey

      // Ctrl+Shift+P - Command Palette
      if (ctrl && e.shiftKey && e.key === "P") {
        e.preventDefault()
        setCommandPaletteOpen(true)
        return
      }

      // Ctrl+` - Toggle Terminal
      if (ctrl && e.key === "`") {
        e.preventDefault()
        setTerminalOpen(!terminalOpen)
        return
      }

      // Ctrl+Shift+A - Toggle Agent Chat
      if (ctrl && e.shiftKey && e.key === "A") {
        e.preventDefault()
        setAgentChatOpen(!agentChatOpen)
        return
      }

      // Ctrl+S - Save
      if (ctrl && e.key === "s") {
        e.preventDefault()
        handleSave()
        return
      }

      // Ctrl+N - New File
      if (ctrl && e.key === "n") {
        e.preventDefault()
        handleNewFile()
        return
      }

      // Ctrl+W - Close Tab
      if (ctrl && e.key === "w") {
        e.preventDefault()
        if (activeTab) closeTab(activeTab)
        return
      }

      // Ctrl+F - Find
      if (ctrl && e.key === "f") {
        e.preventDefault()
        if (editorRef.current) {
          editorRef.current.trigger("keyboard", "actions.find")
        }
        return
      }

      // Ctrl+H - Replace
      if (ctrl && e.key === "h") {
        e.preventDefault()
        if (editorRef.current) {
          editorRef.current.trigger("keyboard", "editor.action.startFindReplaceAction")
        }
        return
      }

      // Ctrl+P - Quick Open
      if (ctrl && e.key === "p") {
        e.preventDefault()
        setCommandPaletteOpen(true)
        return
      }

      // Ctrl+V - Paste
      if (ctrl && e.key === "v") {
        // Let browser handle paste
        return
      }
    }

    window.addEventListener("keydown", handleKeyboard)
    return () => window.removeEventListener("keydown", handleKeyboard)
  }, [terminalOpen, agentChatOpen, activeTab])

  // Auto-save functionality
  useEffect(() => {
    if (!autoSaveEnabled || !activeFile) return

    // Clear existing timer
    if (autoSaveTimerRef.current) {
      clearTimeout(autoSaveTimerRef.current)
    }

    // Set new timer for 2 seconds after last edit
    autoSaveTimerRef.current = setTimeout(() => {
      handleSave(true)
    }, 2000)

    return () => {
      if (autoSaveTimerRef.current) {
        clearTimeout(autoSaveTimerRef.current)
      }
    }
  }, [activeFile, autoSaveEnabled])

  const handleSave = (isAutoSave = false) => {
    if (activeFile) {
      setLastSaveTime(new Date())
      if (!isAutoSave) {
        toast.success(`Saved ${activeFile.name}`)
      }
      // In a real app, this would save to file system
      console.log("Saving file:", activeFile.path)
    }
  }

  const handleNewFile = () => {
    const fileName = `/untitled-${Date.now()}.txt`
    createFile(fileName, "file")
    setShowWelcomeScreen(false)
  }

  const handleEditorChange = (value: string | undefined) => {
    if (activeFile && value !== undefined) {
      updateFileContent(activeFile.path, value)

      // Update tab content
      const currentTab = tabs.find((tab) => tab.path === activeFile.path)
      if (currentTab) {
        updateTabContent(currentTab.id, value)
      }
    }
  }

  const handleEditorMount = (editor: any, monaco: any) => {
    editorRef.current = editor

    // Track cursor position
    editor.onDidChangeCursorPosition((e: any) => {
      setCursorPosition({
        line: e.position.lineNumber,
        column: e.position.column,
      })
    })

    // Setup TypeScript
    monaco.languages.typescript.typescriptDefaults.setCompilerOptions({
      target: monaco.languages.typescript.ScriptTarget.Latest,
      allowNonTsExtensions: true,
      moduleResolution: monaco.languages.typescript.ModuleResolutionKind.NodeJs,
      module: monaco.languages.typescript.ModuleKind.CommonJS,
      noEmit: true,
      esModuleInterop: true,
      jsx: monaco.languages.typescript.JsxEmit.React,
      reactNamespace: "React",
      allowJs: true,
      strict: true,
    })

    // Custom key bindings
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
      handleSave()
    })
  }

  const handleFileSelect = (file: any) => {
    openFile(file)
    openTab(file)
    setShowWelcomeScreen(false)
  }

  const currentFile = activeFile || tabs.find((tab) => tab.id === activeTab)

  const commands = [
    {
      id: "open-folder",
      label: "Open Folder",
      category: "File",
      shortcut: "Ctrl+K Ctrl+O",
      action: () => {
        setShowWelcomeScreen(false)
        toast.success("Open folder feature coming soon!")
      },
    },
    {
      id: "new-file",
      label: "New File",
      category: "File",
      shortcut: "Ctrl+N",
      action: handleNewFile,
    },
    {
      id: "save",
      label: "Save",
      category: "File",
      shortcut: "Ctrl+S",
      action: () => handleSave(),
    },
    {
      id: "save-all",
      label: "Save All",
      category: "File",
      shortcut: "Ctrl+K S",
      action: () => toast.success("All files saved!"),
    },
    {
      id: "close-editor",
      label: "Close Editor",
      category: "File",
      shortcut: "Ctrl+W",
      action: () => {
        if (activeTab) closeTab(activeTab)
      },
    },
    {
      id: "toggle-terminal",
      label: "Toggle Terminal",
      category: "View",
      shortcut: "Ctrl+`",
      action: () => setTerminalOpen(!terminalOpen),
    },
    {
      id: "toggle-agent",
      label: "Toggle Agent Chat",
      category: "View",
      shortcut: "Ctrl+Shift+A",
      action: () => setAgentChatOpen(!agentChatOpen),
    },
    {
      id: "find",
      label: "Find",
      category: "Edit",
      shortcut: "Ctrl+F",
      action: () => {
        if (editorRef.current) {
          editorRef.current.trigger("keyboard", "actions.find")
        }
      },
    },
    {
      id: "replace",
      label: "Replace",
      category: "Edit",
      shortcut: "Ctrl+H",
      action: () => {
        if (editorRef.current) {
          editorRef.current.trigger("keyboard", "editor.action.startFindReplaceAction")
        }
      },
    },
    {
      id: "format",
      label: "Format Document",
      category: "Edit",
      shortcut: "Shift+Alt+F",
      action: () => {
        if (editorRef.current) {
          editorRef.current.trigger("keyboard", "editor.action.formatDocument")
        }
      },
    },
    {
      id: "toggle-auto-save",
      label: `Auto Save: ${autoSaveEnabled ? "On" : "Off"}`,
      category: "Settings",
      action: () => {
        setAutoSaveEnabled(!autoSaveEnabled)
        toast.success(`Auto Save ${!autoSaveEnabled ? "Enabled" : "Disabled"}`)
      },
    },
  ]

  return (
    <div className="h-screen bg-[#1e1e1e] text-white flex flex-col overflow-hidden">
      <MenuBar />

      <div className="flex-1 flex overflow-hidden">
        <ActivityBar
          activeView={activeView}
          onViewChange={(view) => {
            setActiveView(view)
            if (view === "ai") {
              setAgentChatOpen(true)
            }
          }}
        />

        {showWelcomeScreen ? (
          <WelcomeScreenEnhanced
            onOpenFolder={() => {
              setShowWelcomeScreen(false)
              toast.info("Open Folder feature coming soon!")
            }}
            onCloneRepo={() => {
              setShowWelcomeScreen(false)
              toast.info("Clone Repository feature coming soon!")
            }}
            onNewFile={handleNewFile}
            onOpenAI={() => {
              setShowWelcomeScreen(false)
              setAgentChatOpen(true)
            }}
          />
        ) : (
          <ResizablePanelGroup direction="horizontal" className="flex-1">
            {/* Left Sidebar */}
            <ResizablePanel defaultSize={20} minSize={15} maxSize={40}>
              <Sidebar
                files={files}
                onFileSelect={handleFileSelect}
                onFileCreate={createFile}
                onFileDelete={deleteFile}
                activeFile={activeFile}
              />
            </ResizablePanel>

            <ResizableHandle />

            {/* Main Editor Area */}
            <ResizablePanel defaultSize={agentChatOpen ? 60 : 80}>
              <ResizablePanelGroup direction="vertical">
                {/* Editor */}
                <ResizablePanel defaultSize={terminalOpen ? 70 : 100}>
                  <div className="h-full flex flex-col bg-[#1e1e1e]">
                    <TabBar tabs={tabs} activeTab={activeTab} onTabSelect={switchTab} onTabClose={closeTab} />

                    <div className="flex-1">
                      {currentFile ? (
                        <Editor
                          height="100%"
                          language={getLanguageFromExtension(currentFile.name)}
                          value={currentFile.content || ""}
                          onChange={handleEditorChange}
                          onMount={handleEditorMount}
                          theme="vs-dark"
                          options={{
                            fontSize: 14,
                            fontFamily: "JetBrains Mono, Fira Code, Consolas, monospace",
                            fontLigatures: true,
                            minimap: { enabled: true },
                            scrollBeyondLastLine: false,
                            automaticLayout: true,
                            tabSize: 2,
                            insertSpaces: true,
                            wordWrap: "on",
                            lineNumbers: "on",
                            renderWhitespace: "selection",
                            bracketPairColorization: { enabled: true },
                            suggestOnTriggerCharacters: true,
                            quickSuggestions: true,
                            formatOnPaste: true,
                            formatOnType: true,
                          }}
                        />
                      ) : (
                        <div className="h-full flex items-center justify-center">
                          <div className="text-center">
                            <div className="text-6xl mb-4">🧟‍♂️</div>
                            <p className="text-gray-400 mb-2">Welcome to ZombieCoder</p>
                            <p className="text-sm text-gray-500">Open a file to start editing</p>
                            <div className="mt-4 text-xs text-gray-600">
                              <p>
                                Auto-save: <span className="text-green-400">{autoSaveEnabled ? "ON" : "OFF"}</span>
                              </p>
                              {lastSaveTime && <p>Last saved: {lastSaveTime.toLocaleTimeString()}</p>}
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </ResizablePanel>

                {/* Terminal at Bottom */}
                {terminalOpen && (
                  <>
                    <ResizableHandle />
                    <ResizablePanel defaultSize={30} minSize={20} maxSize={50}>
                      <TerminalEnhanced onClose={() => setTerminalOpen(false)} />
                    </ResizablePanel>
                  </>
                )}
              </ResizablePanelGroup>
            </ResizablePanel>

            {/* Agent Chat on Right */}
            {agentChatOpen && (
              <>
                <ResizableHandle />
                <ResizablePanel defaultSize={20} minSize={15} maxSize={40}>
                  <AgentChatEnhanced currentFile={currentFile} onClose={() => setAgentChatOpen(false)} />
                </ResizablePanel>
              </>
            )}
          </ResizablePanelGroup>
        )}
      </div>

      <StatusBar currentFile={currentFile} cursorPosition={cursorPosition} />

      <CommandPalette open={commandPaletteOpen} onOpenChange={setCommandPaletteOpen} commands={commands} />
    </div>
  )
}

function getLanguageFromExtension(filename: string): string {
  const ext = filename.split(".").pop()?.toLowerCase()
  const languageMap: Record<string, string> = {
    js: "javascript",
    jsx: "javascript",
    ts: "typescript",
    tsx: "typescript",
    py: "python",
    html: "html",
    css: "css",
    json: "json",
    md: "markdown",
    txt: "plaintext",
  }
  return languageMap[ext || ""] || "plaintext"
}
