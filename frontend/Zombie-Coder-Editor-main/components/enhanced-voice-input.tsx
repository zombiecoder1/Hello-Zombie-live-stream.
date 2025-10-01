"use client"

import { useState, useEffect } from "react"
import { Mic, MicOff, Send, X, Volume2, Settings, Zap } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { voiceProcessor, type CommandResult } from "@/lib/voice-command-processor"

interface EnhancedVoiceInputProps {
  isListening: boolean
  transcript: string
  onClose: () => void
  onStartListening: () => void
  onStopListening: () => void
  currentFile: { name: string; content: string; path: string } | null
  editorRef?: any
}

export function EnhancedVoiceInput({
  isListening,
  transcript,
  onClose,
  onStartListening,
  onStopListening,
  currentFile,
  editorRef,
}: EnhancedVoiceInputProps) {
  const [language, setLanguage] = useState<"bengali" | "english">("bengali")
  const [command, setCommand] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)
  const [ttsEnabled, setTtsEnabled] = useState(true)
  const [commandHistory, setCommandHistory] = useState<CommandResult[]>([])
  const [showSettings, setShowSettings] = useState(false)

  const languages = [
    { code: "bengali", name: "বাংলা (Bangladesh)", flag: "🇧🇩", speechLang: "bn-BD" },
    { code: "english", name: "English (US)", flag: "🇺🇸", speechLang: "en-US" },
  ]

  useEffect(() => {
    if (transcript) {
      setCommand(transcript)
    }
  }, [transcript])

  useEffect(() => {
    voiceProcessor.setLanguage(language)
    voiceProcessor.setTTSEnabled(ttsEnabled)
  }, [language, ttsEnabled])

  const handleProcessCommand = async () => {
    if (!command.trim()) return

    setIsProcessing(true)
    try {
      const result = await voiceProcessor.processCommand(command, editorRef)
      setCommandHistory((prev) => [result, ...prev.slice(0, 9)]) // Keep last 10 commands

      // Handle special actions
      if (result.data?.triggerDialog) {
        // Trigger appropriate dialog
        console.log("Trigger dialog:", result.data.triggerDialog)
      }

      if (result.data?.triggerAI) {
        // Send to AI panel
        console.log("Trigger AI:", result.data.triggerAI)
      }

      if (result.data?.debugAction) {
        // Trigger debug action
        console.log("Debug action:", result.data.debugAction)
      }

      // Clear command after successful processing
      setCommand("")
    } catch (error) {
      console.error("Voice command processing failed:", error)
    } finally {
      setIsProcessing(false)
    }
  }

  const speakText = (text: string) => {
    if ("speechSynthesis" in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      const selectedLang = languages.find((l) => l.code === language)
      utterance.lang = selectedLang?.speechLang || "bn-BD"
      utterance.rate = 0.9
      speechSynthesis.speak(utterance)
    }
  }

  const getStatusColor = (success: boolean) => {
    return success ? "text-green-400" : "text-red-400"
  }

  return (
    <div className="absolute inset-0 bg-black/50 flex items-center justify-center z-50">
      <Card className="w-[600px] max-h-[80vh] bg-[#2d2d30] border-[#3c3c3c] text-white overflow-hidden">
        <CardHeader className="flex flex-row items-center justify-between pb-3">
          <CardTitle className="flex items-center gap-2">
            <div className="relative">
              <Mic className="h-5 w-5 text-green-400" />
              {isListening && <div className="absolute -inset-1 bg-green-400/20 rounded-full animate-ping" />}
            </div>
            🧟‍♂️ ZombieCoder Voice Assistant
          </CardTitle>
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" onClick={() => setShowSettings(!showSettings)}>
              <Settings className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Settings Panel */}
          {showSettings && (
            <div className="p-3 bg-[#3c3c3c] rounded-lg space-y-3">
              <div className="flex items-center justify-between">
                <Label htmlFor="tts-toggle">Text-to-Speech</Label>
                <Switch id="tts-toggle" checked={ttsEnabled} onCheckedChange={setTtsEnabled} />
              </div>
            </div>
          )}

          {/* Language Selection */}
          <div className="flex items-center gap-2">
            <Select value={language} onValueChange={(value: "bengali" | "english") => setLanguage(value)}>
              <SelectTrigger className="w-[250px] bg-[#3c3c3c] border-[#464647]">
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

            <Badge variant={isListening ? "destructive" : "secondary"} className="animate-pulse-green">
              {isListening ? "🎤 Listening..." : "⏸️ Ready"}
            </Badge>

            {isProcessing && (
              <Badge variant="outline" className="animate-pulse">
                <Zap className="h-3 w-3 mr-1" />
                Processing...
              </Badge>
            )}
          </div>

          {/* Voice Command Input */}
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
              placeholder={
                language === "bengali" ? "এখানে আপনার কমান্ড লিখুন বা বলুন..." : "Type or speak your command here..."
              }
              className="bg-[#3c3c3c] border-[#464647] min-h-[80px] font-bengali"
            />
          </div>

          {/* Control Buttons */}
          <div className="flex items-center justify-between">
            <div className="flex gap-2">
              <Button
                variant={isListening ? "destructive" : "default"}
                size="sm"
                onClick={isListening ? onStopListening : onStartListening}
                className="relative"
              >
                {isListening ? (
                  <>
                    <MicOff className="h-4 w-4 mr-2" />
                    Stop Recording
                  </>
                ) : (
                  <>
                    <Mic className="h-4 w-4 mr-2" />
                    Start Recording
                  </>
                )}
                {isListening && <div className="absolute -inset-1 bg-red-500/20 rounded animate-pulse" />}
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

          {/* Current File Context */}
          {currentFile && (
            <div className="text-xs text-gray-400 bg-[#3c3c3c] p-2 rounded">
              <strong>Context:</strong> {currentFile.name}
            </div>
          )}

          {/* Command History */}
          {commandHistory.length > 0 && (
            <div className="space-y-2">
              <div className="text-sm font-medium">Recent Commands:</div>
              <div className="max-h-[200px] overflow-y-auto space-y-1">
                {commandHistory.map((result, index) => (
                  <div key={index} className="text-xs p-2 bg-[#3c3c3c] rounded">
                    <div className="flex items-center justify-between">
                      <span className="font-mono">{result.action}</span>
                      <Badge variant={result.success ? "default" : "destructive"} className="text-xs">
                        {result.success ? "✓" : "✗"}
                      </Badge>
                    </div>
                    <div className={`mt-1 ${getStatusColor(result.success)}`}>{result.message}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Example Commands */}
          <div className="text-xs text-gray-500 space-y-1">
            <p>
              <strong>{language === "bengali" ? "উদাহরণ কমান্ড (বাংলা):" : "Example Commands (English):"}</strong>
            </p>
            <ul className="list-disc list-inside space-y-1 ml-2 font-bengali">
              {language === "bengali" ? (
                <>
                  <li>"নতুন ফাইল তৈরি করো"</li>
                  <li>"কোড ফরম্যাট করো"</li>
                  <li>"কমেন্ট যোগ করো"</li>
                  <li>"ব্রেকপয়েন্ট যোগ করো"</li>
                  <li>"এআই দিয়ে কোড লিখো"</li>
                </>
              ) : (
                <>
                  <li>"create new file"</li>
                  <li>"format code"</li>
                  <li>"add comment"</li>
                  <li>"add breakpoint"</li>
                  <li>"generate code with AI"</li>
                </>
              )}
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
