"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { Send, Code, MessageSquare, Brain } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { aiMemory } from "@/lib/ai-memory"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
}

interface AIPanelProps {
  currentFile: { name: string; content: string; path: string } | null
}

export function AIPanel({ currentFile }: AIPanelProps) {
  const [mode, setMode] = useState<"chat" | "code">("chat")
  const [language, setLanguage] = useState<"bengali" | "english">("bengali")
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content:
        "নমস্কার! আমি ZombieCoder AI Assistant। আমি আপনাকে কোডিং, ডিবাগিং এবং কোড ব্যাখ্যায় সাহায্য করতে পারি। আপনি কী নিয়ে কাজ করতে চান?",
    },
  ])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    // Update welcome message based on language
    setMessages([
      {
        id: "1",
        role: "assistant",
        content:
          language === "bengali"
            ? "নমস্কার! আমি ZombieCoder AI Assistant। আমি আপনাকে কোডিং, ডিবাগিং এবং কোড ব্যাখ্যায় সাহায্য করতে পারি। আপনি কী নিয়ে কাজ করতে চান?"
            : "Hello! I'm ZombieCoder AI Assistant. I can help you with coding, debugging, and code explanations. What would you like to work on?",
      },
    ])
  }, [language])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      let contextualInput = input
      if (currentFile && mode === "code") {
        const fileLanguage = getFileLanguage(currentFile.name)
        contextualInput = `Current file: ${currentFile.name}\n\`\`\`${fileLanguage}\n${currentFile.content}\n\`\`\`\n\nQuestion: ${input}`
      }

      // Add context from AI memory
      const memoryContext = aiMemory.getContextForAI()
      if (memoryContext) {
        contextualInput = `${memoryContext}\n\n${contextualInput}`
      }

      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          messages: [...messages, userMessage].map((m) => ({
            role: m.role,
            content: m.content,
          })),
          input: contextualInput,
          mode,
          language,
        }),
      })

      if (!response.ok) {
        throw new Error("Failed to get response")
      }

      const data = await response.json()
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.text || "Sorry, I couldn't generate a response.",
      }

      setMessages((prev) => [...prev, assistantMessage])

      // Add to memory
      aiMemory.addMemory("conversation", input, {
        mode,
        language,
        currentFile: currentFile?.path,
        response: assistantMessage.content,
      })
    } catch (error) {
      console.error("Error sending message:", error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content:
          language === "bengali"
            ? "দুঃখিত, একটি ত্রুটি হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।"
            : "Sorry, an error occurred. Please try again.",
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value)
  }

  const getFileLanguage = (filename: string) => {
    const ext = filename.split(".").pop()?.toLowerCase()
    const langMap: Record<string, string> = {
      ts: "typescript",
      tsx: "typescript",
      js: "javascript",
      jsx: "javascript",
      py: "python",
      html: "html",
      css: "css",
    }
    return langMap[ext || ""] || "text"
  }

  const quickPrompts = {
    bengali: ["এই কোডটি ব্যাখ্যা করো", "বাগ খুঁজে বের করো", "কোড অপ্টিমাইজ করো", "টেস্ট কেস লিখো", "ডকুমেন্টেশন যোগ করো"],
    english: ["Explain this code", "Find bugs", "Optimize code", "Write test cases", "Add documentation"],
  }

  return (
    <div className="h-full bg-[#252526] border-l border-[#3c3c3c] flex flex-col">
      <div className="p-3 border-b border-[#3c3c3c]">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-medium text-gray-300 flex items-center gap-2">
            <Brain className="h-4 w-4 text-zombie-400" />
            🧟‍♂️ ZombieCoder AI
          </h2>
          <Badge variant="outline" className="text-xs bg-zombie-900/20 text-zombie-400">
            {language === "bengali" ? "বাংলা" : "English"}
          </Badge>
        </div>

        <div className="flex gap-1 mb-2">
          <Button
            variant={mode === "chat" ? "default" : "ghost"}
            size="sm"
            className="h-7 px-2 text-xs"
            onClick={() => setMode("chat")}
          >
            <MessageSquare className="h-3 w-3 mr-1" />
            Chat
          </Button>
          <Button
            variant={mode === "code" ? "default" : "ghost"}
            size="sm"
            className="h-7 px-2 text-xs"
            onClick={() => setMode("code")}
          >
            <Code className="h-3 w-3 mr-1" />
            Code
          </Button>
        </div>

        <div className="flex gap-1">
          <Button
            variant={language === "bengali" ? "secondary" : "ghost"}
            size="sm"
            className="h-6 px-2 text-xs"
            onClick={() => setLanguage("bengali")}
          >
            🇧🇩 বাংলা
          </Button>
          <Button
            variant={language === "english" ? "secondary" : "ghost"}
            size="sm"
            className="h-6 px-2 text-xs"
            onClick={() => setLanguage("english")}
          >
            🇺🇸 English
          </Button>
        </div>
      </div>

      <ScrollArea className="flex-1 p-3">
        <div className="space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`p-3 rounded-lg text-sm ${
                message.role === "user"
                  ? "bg-zombie-900/20 text-white ml-4 border border-zombie-700/30"
                  : "bg-[#3c3c3c] text-gray-200 mr-4"
              }`}
            >
              <div className="whitespace-pre-wrap font-bengali">{message.content}</div>
            </div>
          ))}

          {isLoading && (
            <div className="bg-[#3c3c3c] text-gray-200 mr-4 p-3 rounded-lg text-sm">
              <div className="flex items-center gap-2">
                <div className="animate-spin h-3 w-3 border border-zombie-400 border-t-transparent rounded-full" />
                <span className="font-bengali">{language === "bengali" ? "চিন্তা করছি..." : "Thinking..."}</span>
              </div>
            </div>
          )}
        </div>
      </ScrollArea>

      {/* Quick Prompts */}
      <div className="p-2 border-t border-[#3c3c3c]">
        <div className="text-xs text-gray-400 mb-2">Quick Prompts:</div>
        <div className="flex flex-wrap gap-1">
          {quickPrompts[language].map((prompt, index) => (
            <Button
              key={index}
              variant="ghost"
              size="sm"
              className="h-6 px-2 text-xs text-gray-400 hover:text-white hover:bg-[#464647]"
              onClick={() => setInput(prompt)}
            >
              {prompt}
            </Button>
          ))}
        </div>
      </div>

      <div className="p-3 border-t border-[#3c3c3c]">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input
            value={input}
            onChange={handleInputChange}
            placeholder={
              mode === "code" && currentFile
                ? language === "bengali"
                  ? `${currentFile.name} সম্পর্কে জিজ্ঞাসা করুন...`
                  : `Ask about ${currentFile.name}...`
                : language === "bengali"
                  ? "কোড সম্পর্কে কিছু জিজ্ঞাসা করুন..."
                  : "Ask me anything about code..."
            }
            className="flex-1 bg-[#3c3c3c] border-[#464647] text-white placeholder-gray-400 font-bengali"
            disabled={isLoading}
          />
          <Button type="submit" size="sm" disabled={isLoading || !input.trim()} className="px-3">
            <Send className="h-4 w-4" />
          </Button>
        </form>

        {currentFile && mode === "code" && (
          <div className="mt-2 text-xs text-gray-400 font-bengali">
            {language === "bengali" ? "প্রসঙ্গ:" : "Context:"} {currentFile.name}
          </div>
        )}
      </div>
    </div>
  )
}
