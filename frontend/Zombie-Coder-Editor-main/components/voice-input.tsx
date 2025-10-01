"use client"

import { useState, useEffect } from "react"
import { Mic, MicOff, Send, X, Volume2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface VoiceInputProps {
  isListening: boolean
  transcript: string
  onClose: () => void
  onStartListening: () => void
  onStopListening: () => void
  currentFile: { name: string; content: string; path: string } | null
}

export function VoiceInput({
  isListening,
  transcript,
  onClose,
  onStartListening,
  onStopListening,
  currentFile,
}: VoiceInputProps) {
  const [language, setLanguage] = useState("bn-BD") // Bengali Bangladesh
  const [command, setCommand] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)

  const languages = [
    { code: "bn-BD", name: "বাংলা (Bangladesh)", flag: "🇧🇩" },
    { code: "en-US", name: "English (US)", flag: "🇺🇸" },
    { code: "hi-IN", name: "हिन्दी (India)", flag: "🇮🇳" },
    { code: "ur-PK", name: "اردو (Pakistan)", flag: "🇵🇰" },
  ]

  useEffect(() => {
    if (transcript) {
      setCommand(transcript)
    }
  }, [transcript])

  const handleProcessCommand = async () => {
    if (!command.trim()) return

    setIsProcessing(true)
    try {
      // Process voice command with AI
      const response = await fetch("/api/voice-command", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          command,
          language,
          currentFile: currentFile?.path,
          fileContent: currentFile?.content,
        }),
      })

      const result = await response.json()

      // Handle the AI response (code generation, file operations, etc.)
      console.log("Voice command result:", result)
    } catch (error) {
      console.error("Voice command processing failed:", error)
    } finally {
      setIsProcessing(false)
    }
  }

  const speakText = (text: string) => {
    if ("speechSynthesis" in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = language
      speechSynthesis.speak(utterance)
    }
  }

  return (
    <div className="absolute inset-0 bg-black/50 flex items-center justify-center z-50">
      <Card className="w-[500px] bg-[#2d2d30] border-[#3c3c3c] text-white">
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Mic className="h-5 w-5 text-green-400" />
            Voice Input - ZombieCoder AI
          </CardTitle>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </CardHeader>

        <CardContent className="space-y-4">
          <div className="flex items-center gap-2">
            <Select value={language} onValueChange={setLanguage}>
              <SelectTrigger className="w-[200px] bg-[#3c3c3c] border-[#464647]">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-[#3c3c3c] border-[#464647]">
                {languages.map((lang) => (
                  <SelectItem key={lang.code} value={lang.code}>
                    <span className="flex items-center gap-2">
                      <span>{lang.flag}</span>
                      <span>{lang.name}</span>
                    </span>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Badge variant={isListening ? "destructive" : "secondary"}>{isListening ? "Listening..." : "Ready"}</Badge>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium">Voice Command:</label>
              <Button variant="ghost" size="sm" onClick={() => speakText(command)} disabled={!command}>
                <Volume2 className="h-4 w-4" />
              </Button>
            </div>

            <Textarea
              value={command}
              onChange={(e) => setCommand(e.target.value)}
              placeholder={language === "bn-BD" ? "এখানে আপনার কমান্ড লিখুন বা বলুন..." : "Type or speak your command here..."}
              className="bg-[#3c3c3c] border-[#464647] min-h-[100px]"
            />
          </div>

          <div className="flex items-center justify-between">
            <div className="flex gap-2">
              <Button
                variant={isListening ? "destructive" : "default"}
                size="sm"
                onClick={isListening ? onStopListening : onStartListening}
              >
                {isListening ? <MicOff className="h-4 w-4 mr-2" /> : <Mic className="h-4 w-4 mr-2" />}
                {isListening ? "Stop" : "Start"} Recording
              </Button>

              <Button
                variant="secondary"
                size="sm"
                onClick={handleProcessCommand}
                disabled={!command.trim() || isProcessing}
              >
                <Send className="h-4 w-4 mr-2" />
                {isProcessing ? "Processing..." : "Execute"}
              </Button>
            </div>
          </div>

          {currentFile && (
            <div className="text-xs text-gray-400 bg-[#3c3c3c] p-2 rounded">
              <strong>Context:</strong> {currentFile.name}
            </div>
          )}

          <div className="text-xs text-gray-500 space-y-1">
            <p>
              <strong>Example Commands (বাংলা):</strong>
            </p>
            <ul className="list-disc list-inside space-y-1 ml-2">
              <li>"একটি রিয়েক্ট কম্পোনেন্ট বানাও"</li>
              <li>"এই ফাংশনটি ডিবাগ করো"</li>
              <li>"কোডে কমেন্ট যোগ করো"</li>
              <li>"নতুন ফাইল তৈরি করো"</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
