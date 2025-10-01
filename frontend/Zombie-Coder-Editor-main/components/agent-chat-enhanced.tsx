"use client"

import type React from "react"
import { useState, useRef, useEffect } from "react"
import { Send, Sparkles, X, StopCircle, Settings, ImageIcon, Mic, Paperclip, Code2, Zap } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"

interface Message {
  role: "user" | "assistant"
  content: string
  streaming?: boolean
  images?: string[]
  files?: { name: string; path: string }[]
}

interface AgentChatEnhancedProps {
  currentFile: { name: string; content: string; path: string } | null
  onClose: () => void
}

export function AgentChatEnhanced({ currentFile, onClose }: AgentChatEnhancedProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isStreaming, setIsStreaming] = useState(false)
  const [selectedProvider, setSelectedProvider] = useState("local")
  const [selectedAgent, setSelectedAgent] = useState("bengali-nlp")
  const [attachedImages, setAttachedImages] = useState<string[]>([])
  const [attachedFiles, setAttachedFiles] = useState<{ name: string; path: string }[]>([])
  const [isRecording, setIsRecording] = useState(false)

  const scrollRef = useRef<HTMLDivElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const imageInputRef = useRef<HTMLInputElement>(null)
  const abortControllerRef = useRef<AbortController | null>(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isStreaming) return

    const userMessage: Message = {
      role: "user",
      content: input,
      images: attachedImages.length > 0 ? [...attachedImages] : undefined,
      files: attachedFiles.length > 0 ? [...attachedFiles] : undefined,
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setAttachedImages([])
    setAttachedFiles([])
    setIsStreaming(true)

    abortControllerRef.current = new AbortController()

    try {
      const apiUrl = selectedProvider === "local" ? "http://localhost:8002" : "https://api.openai.com"

      const response = await fetch(`${apiUrl}/v1/chat/completions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${selectedProvider === "local" ? "test-token" : process.env.OPENAI_API_KEY || ""}`,
        },
        body: JSON.stringify({
          model: selectedProvider === "local" ? "gpt-3.5-turbo" : "gpt-4",
          messages: [...messages, userMessage].map((m) => ({
            role: m.role,
            content: m.content,
          })),
          stream: true,
          agent: selectedAgent,
        }),
        signal: abortControllerRef.current.signal,
      })

      if (!response.ok) throw new Error("Stream failed")

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      const assistantMessage: Message = {
        role: "assistant",
        content: "",
        streaming: true,
      }

      setMessages((prev) => [...prev, assistantMessage])

      while (reader) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split("\n")

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6)
            if (data === "[DONE]") {
              setIsStreaming(false)
              setMessages((prev) => prev.map((m, i) => (i === prev.length - 1 ? { ...m, streaming: false } : m)))
              break
            }

            try {
              const parsed = JSON.parse(data)
              const content = parsed.choices?.[0]?.delta?.content || ""
              if (content) {
                setMessages((prev) => {
                  const newMessages = [...prev]
                  const lastMessage = newMessages[newMessages.length - 1]
                  if (lastMessage.role === "assistant") {
                    lastMessage.content += content
                  }
                  return newMessages
                })
              }
            } catch (e) {
              // Ignore parse errors
            }
          }
        }
      }
    } catch (error: any) {
      if (error.name === "AbortError") {
        console.log("Stream stopped by user")
      } else {
        console.error("Stream error:", error)
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: "Sorry, there was an error connecting to the AI agent.",
          },
        ])
      }
    } finally {
      setIsStreaming(false)
      abortControllerRef.current = null
    }
  }

  const handleStop = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
      setIsStreaming(false)
    }
  }

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files) {
      Array.from(files).forEach((file) => {
        const reader = new FileReader()
        reader.onload = (event) => {
          if (event.target?.result) {
            setAttachedImages((prev) => [...prev, event.target!.result as string])
          }
        }
        reader.readAsDataURL(file)
      })
    }
  }

  const handleFileAttach = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files) {
      const newFiles = Array.from(files).map((file) => ({
        name: file.name,
        path: file.webkitRelativePath || file.name,
      }))
      setAttachedFiles((prev) => [...prev, ...newFiles])
    }
  }

  const handleVoiceInput = () => {
    if (!isRecording) {
      // Start recording
      setIsRecording(true)
      // TODO: Implement actual voice recording
      setTimeout(() => {
        setIsRecording(false)
        setInput("Voice input feature coming soon...")
      }, 2000)
    } else {
      setIsRecording(false)
    }
  }

  const availableProviders = [
    { id: "local", name: "Local Model", icon: "💻" },
    { id: "openai", name: "OpenAI", icon: "🤖" },
    { id: "anthropic", name: "Anthropic", icon: "🧠" },
  ]

  const availableAgents = [
    { id: "bengali-nlp", name: "Bengali NLP", icon: "🇧🇩" },
    { id: "code-assistant", name: "Code Assistant", icon: "💻" },
    { id: "general", name: "General", icon: "💬" },
  ]

  return (
    <div className="h-full bg-[#1e1e1e] border-l border-[#3c3c3c] flex flex-col">
      {/* Header with Settings */}
      <div className="h-12 border-b border-[#3c3c3c] flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <Sparkles className="h-4 w-4 text-green-400" />
          <span className="text-sm font-medium">ZombieCoder AI</span>
          <Badge variant="outline" className="text-xs">
            {selectedProvider === "local" ? "Local" : "Cloud"}
          </Badge>
        </div>
        <div className="flex items-center gap-2">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm" className="h-7 px-2">
                <Settings className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56 bg-[#2d2d30] border-[#3c3c3c]">
              <DropdownMenuItem className="text-xs">
                <Code2 className="h-3 w-3 mr-2" />
                Model Settings
              </DropdownMenuItem>
              <DropdownMenuItem className="text-xs">
                <Zap className="h-3 w-3 mr-2" />
                Performance
              </DropdownMenuItem>
              <DropdownMenuSeparator className="bg-[#3c3c3c]" />
              <DropdownMenuItem className="text-xs">
                <Settings className="h-3 w-3 mr-2" />
                Preferences
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Provider and Agent Selection */}
      <div className="border-b border-[#3c3c3c] p-3 space-y-2">
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-400">Provider:</span>
          <Select value={selectedProvider} onValueChange={setSelectedProvider}>
            <SelectTrigger className="h-7 text-xs bg-[#3c3c3c] border-[#464647] flex-1">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="bg-[#2d2d30] border-[#3c3c3c]">
              {availableProviders.map((provider) => (
                <SelectItem key={provider.id} value={provider.id} className="text-xs">
                  <span className="flex items-center gap-2">
                    <span>{provider.icon}</span>
                    <span>{provider.name}</span>
                  </span>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-400">Agent:</span>
          <Select value={selectedAgent} onValueChange={setSelectedAgent}>
            <SelectTrigger className="h-7 text-xs bg-[#3c3c3c] border-[#464647] flex-1">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="bg-[#2d2d30] border-[#3c3c3c]">
              {availableAgents.map((agent) => (
                <SelectItem key={agent.id} value={agent.id} className="text-xs">
                  <span className="flex items-center gap-2">
                    <span>{agent.icon}</span>
                    <span>{agent.name}</span>
                  </span>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Messages */}
      <ScrollArea className="flex-1 p-4" ref={scrollRef}>
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <Sparkles className="h-12 w-12 text-gray-600 mb-4" />
            <h3 className="text-lg font-medium text-gray-400 mb-2">Build with agent mode.</h3>
            <p className="text-sm text-gray-500 mb-4">AI responses may be inaccurate.</p>
            <p className="text-xs text-blue-400 cursor-pointer hover:underline">
              Generate instructions to onboard AI onto your codebase.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((message, index) => (
              <div key={index}>
                <div
                  className={cn(
                    "p-3 rounded-lg text-sm",
                    message.role === "user" ? "bg-blue-600/20 ml-8" : "bg-[#2d2d30] mr-8",
                  )}
                >
                  {message.images && message.images.length > 0 && (
                    <div className="flex gap-2 mb-2 flex-wrap">
                      {message.images.map((img, i) => (
                        <img
                          key={i}
                          src={img || "/placeholder.svg"}
                          alt="Attached"
                          className="w-20 h-20 object-cover rounded"
                        />
                      ))}
                    </div>
                  )}
                  {message.files && message.files.length > 0 && (
                    <div className="flex gap-2 mb-2 flex-wrap">
                      {message.files.map((file, i) => (
                        <Badge key={i} variant="outline" className="text-xs">
                          📄 {file.name}
                        </Badge>
                      ))}
                    </div>
                  )}
                  <div className="whitespace-pre-wrap">
                    {message.content}
                    {message.streaming && <span className="inline-block w-2 h-4 bg-green-400 ml-1 animate-pulse" />}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </ScrollArea>

      {/* Input Area */}
      <div className="border-t border-[#3c3c3c] p-4">
        {/* Context Display */}
        {currentFile && (
          <div className="text-xs text-gray-500 mb-2 flex items-center gap-2">
            <Code2 className="h-3 w-3" />
            <span>Context: {currentFile.name}</span>
          </div>
        )}

        {/* Attached Items */}
        {(attachedImages.length > 0 || attachedFiles.length > 0) && (
          <div className="mb-2 flex gap-2 flex-wrap">
            {attachedImages.map((img, i) => (
              <div key={i} className="relative">
                <img src={img || "/placeholder.svg"} alt="Attached" className="w-16 h-16 object-cover rounded" />
                <Button
                  variant="ghost"
                  size="sm"
                  className="absolute -top-2 -right-2 h-5 w-5 p-0 bg-red-500 hover:bg-red-600 rounded-full"
                  onClick={() => setAttachedImages((prev) => prev.filter((_, index) => index !== i))}
                >
                  <X className="h-3 w-3" />
                </Button>
              </div>
            ))}
            {attachedFiles.map((file, i) => (
              <Badge key={i} variant="outline" className="text-xs">
                📄 {file.name}
                <X
                  className="h-3 w-3 ml-1 cursor-pointer"
                  onClick={() => setAttachedFiles((prev) => prev.filter((_, index) => index !== i))}
                />
              </Badge>
            ))}
          </div>
        )}

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="space-y-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Add context (#), extensions (@), commands"
            className="min-h-[80px] bg-[#3c3c3c] border-[#464647] text-white resize-none"
            disabled={isStreaming}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault()
                handleSubmit(e)
              }
            }}
          />

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1">
              <input
                type="file"
                ref={imageInputRef}
                onChange={handleImageUpload}
                accept="image/*"
                multiple
                className="hidden"
              />
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="h-8 px-2"
                onClick={() => imageInputRef.current?.click()}
              >
                <ImageIcon className="h-4 w-4" />
              </Button>

              <input type="file" ref={fileInputRef} onChange={handleFileAttach} multiple className="hidden" />
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="h-8 px-2"
                onClick={() => fileInputRef.current?.click()}
              >
                <Paperclip className="h-4 w-4" />
              </Button>

              <Button
                type="button"
                variant="ghost"
                size="sm"
                className={cn("h-8 px-2", isRecording && "text-red-400 animate-pulse")}
                onClick={handleVoiceInput}
              >
                <Mic className="h-4 w-4" />
              </Button>
            </div>

            <div className="flex items-center gap-2">
              {isStreaming ? (
                <Button type="button" size="sm" variant="destructive" onClick={handleStop} className="h-8">
                  <StopCircle className="h-4 w-4 mr-1" />
                  Stop
                </Button>
              ) : (
                <Button
                  type="submit"
                  size="sm"
                  disabled={!input.trim()}
                  className="h-8 bg-green-600 hover:bg-green-700"
                >
                  <Send className="h-4 w-4 mr-1" />
                  Send
                </Button>
              )}
            </div>
          </div>
        </form>

        <div className="mt-2 text-xs text-gray-500">
          <kbd className="px-1 bg-[#3c3c3c] rounded">Ctrl+Shift+A</kbd> to toggle •{" "}
          <kbd className="px-1 bg-[#3c3c3c] rounded">Enter</kbd> to send •{" "}
          <kbd className="px-1 bg-[#3c3c3c] rounded">Shift+Enter</kbd> for new line
        </div>
      </div>
    </div>
  )
}
