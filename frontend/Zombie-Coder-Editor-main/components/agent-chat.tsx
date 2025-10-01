"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Send, Sparkles, X, StopCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { ScrollArea } from "@/components/ui/scroll-area"
import { cn } from "@/lib/utils"

interface Message {
  role: "user" | "assistant"
  content: string
  streaming?: boolean
}

interface AgentChatProps {
  currentFile: { name: string; content: string; path: string } | null
  onClose: () => void
}

export function AgentChat({ currentFile, onClose }: AgentChatProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isStreaming, setIsStreaming] = useState(false)
  const scrollRef = useRef<HTMLDivElement>(null)
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
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsStreaming(true)

    // Create abort controller for stopping stream
    abortControllerRef.current = new AbortController()

    try {
      const response = await fetch("http://localhost:8002/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer test-token",
        },
        body: JSON.stringify({
          model: "gpt-3.5-turbo",
          messages: [...messages, userMessage].map((m) => ({
            role: m.role,
            content: m.content,
          })),
          stream: true,
        }),
        signal: abortControllerRef.current.signal,
      })

      if (!response.ok) {
        throw new Error("Stream failed")
      }

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

  return (
    <div className="h-full bg-[#1e1e1e] border-l border-[#3c3c3c] flex flex-col">
      {/* Header */}
      <div className="h-12 border-b border-[#3c3c3c] flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <Sparkles className="h-4 w-4 text-green-400" />
          <span className="text-sm font-medium">Agent Chat</span>
        </div>
        <Button variant="ghost" size="sm" className="h-6 w-6 p-0" onClick={onClose}>
          <X className="h-4 w-4" />
        </Button>
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
              <div
                key={index}
                className={cn(
                  "p-3 rounded-lg text-sm",
                  message.role === "user" ? "bg-blue-600/20 ml-8" : "bg-[#2d2d30] mr-8",
                )}
              >
                <div className="whitespace-pre-wrap">
                  {message.content}
                  {message.streaming && <span className="inline-block w-2 h-4 bg-green-400 ml-1 animate-pulse" />}
                </div>
              </div>
            ))}
          </div>
        )}
      </ScrollArea>

      {/* Input */}
      <div className="border-t border-[#3c3c3c] p-4">
        {currentFile && <div className="text-xs text-gray-500 mb-2">Context: {currentFile.name}</div>}

        <form onSubmit={handleSubmit} className="flex gap-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Add context (#), extensions (@), commands"
            className="flex-1 min-h-[80px] bg-[#3c3c3c] border-[#464647] text-white resize-none"
            disabled={isStreaming}
          />
          <div className="flex flex-col gap-2">
            {isStreaming ? (
              <Button type="button" size="sm" variant="destructive" onClick={handleStop} className="h-8">
                <StopCircle className="h-4 w-4" />
              </Button>
            ) : (
              <Button type="submit" size="sm" disabled={!input.trim()} className="h-8">
                <Send className="h-4 w-4" />
              </Button>
            )}
          </div>
        </form>

        <div className="mt-2 text-xs text-gray-500">
          Press <kbd className="px-1 bg-[#3c3c3c] rounded">Ctrl+Shift+A</kbd> to toggle
        </div>
      </div>
    </div>
  )
}
