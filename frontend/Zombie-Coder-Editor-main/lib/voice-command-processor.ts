"use client"

import voiceCommands from "@/config/voice-commands.json"
import ttsResponses from "@/config/tts-responses.json"
import { aiMemory } from "./ai-memory"

interface CommandResult {
  action: string
  success: boolean
  message: string
  data?: any
}

class VoiceCommandProcessor {
  private currentLanguage: "bengali" | "english" = "bengali"
  private ttsEnabled = true

  setLanguage(language: "bengali" | "english") {
    this.currentLanguage = language
  }

  setTTSEnabled(enabled: boolean) {
    this.ttsEnabled = enabled
  }

  async processCommand(transcript: string, editorRef?: any): Promise<CommandResult> {
    const normalizedTranscript = transcript.toLowerCase().trim()

    // Find matching command
    const commands = voiceCommands[this.currentLanguage]
    let matchedAction: string | null = null
    let matchedCategory: string | null = null

    // Search through all command categories
    for (const [category, categoryCommands] of Object.entries(commands)) {
      for (const [phrase, action] of Object.entries(categoryCommands as Record<string, string>)) {
        if (normalizedTranscript.includes(phrase.toLowerCase())) {
          matchedAction = action
          matchedCategory = category
          break
        }
      }
      if (matchedAction) break
    }

    if (!matchedAction) {
      // If no direct match, send to AI for processing
      return this.processWithAI(transcript)
    }

    // Execute the matched command
    const result = await this.executeCommand(matchedAction, matchedCategory!, editorRef)

    // Add to memory
    aiMemory.addMemory("conversation", `Voice command: ${transcript} -> ${matchedAction}`, {
      language: this.currentLanguage,
      category: matchedCategory,
    })

    // Provide TTS feedback
    if (this.ttsEnabled && result.success) {
      this.speakResponse(result.message)
    }

    return result
  }

  private async executeCommand(action: string, category: string, editorRef?: any): Promise<CommandResult> {
    try {
      switch (category) {
        case "file_operations":
          return this.executeFileOperation(action, editorRef)
        case "editing":
          return this.executeEditingCommand(action, editorRef)
        case "code_actions":
          return this.executeCodeAction(action, editorRef)
        case "navigation":
          return this.executeNavigationCommand(action, editorRef)
        case "ai_commands":
          return this.executeAICommand(action, editorRef)
        case "debug":
          return this.executeDebugCommand(action, editorRef)
        default:
          return {
            action,
            success: false,
            message: this.getResponse("command_not_understood"),
          }
      }
    } catch (error) {
      return {
        action,
        success: false,
        message: `Error executing command: ${error}`,
      }
    }
  }

  private async executeFileOperation(action: string, editorRef?: any): Promise<CommandResult> {
    switch (action) {
      case "create_file":
        // Trigger file creation dialog
        return {
          action,
          success: true,
          message: this.getResponse("file_created"),
          data: { triggerDialog: "createFile" },
        }
      case "save_file":
        // Trigger save
        if (editorRef?.current) {
          // Simulate Ctrl+S
          document.dispatchEvent(new KeyboardEvent("keydown", { key: "s", ctrlKey: true }))
        }
        return {
          action,
          success: true,
          message: this.getResponse("file_saved"),
        }
      default:
        return {
          action,
          success: false,
          message: this.getResponse("command_not_understood"),
        }
    }
  }

  private async executeEditingCommand(action: string, editorRef?: any): Promise<CommandResult> {
    if (!editorRef?.current) {
      return {
        action,
        success: false,
        message: "No active editor",
      }
    }

    const editor = editorRef.current
    switch (action) {
      case "copy":
        editor.trigger("keyboard", "editor.action.clipboardCopyAction")
        break
      case "paste":
        editor.trigger("keyboard", "editor.action.clipboardPasteAction")
        break
      case "cut":
        editor.trigger("keyboard", "editor.action.clipboardCutAction")
        break
      case "undo":
        editor.trigger("keyboard", "undo")
        break
      case "redo":
        editor.trigger("keyboard", "redo")
        break
      case "select_all":
        editor.trigger("keyboard", "editor.action.selectAll")
        break
      case "delete_line":
        editor.trigger("keyboard", "editor.action.deleteLines")
        break
      case "copy_line":
        editor.trigger("keyboard", "editor.action.copyLinesDownAction")
        break
    }

    return {
      action,
      success: true,
      message: "Command executed successfully",
    }
  }

  private async executeCodeAction(action: string, editorRef?: any): Promise<CommandResult> {
    if (!editorRef?.current) {
      return {
        action,
        success: false,
        message: "No active editor",
      }
    }

    const editor = editorRef.current
    switch (action) {
      case "add_comment":
        editor.trigger("keyboard", "editor.action.commentLine")
        return {
          action,
          success: true,
          message: this.getResponse("comment_added"),
        }
      case "format_code":
        editor.trigger("keyboard", "editor.action.formatDocument")
        return {
          action,
          success: true,
          message: this.getResponse("code_formatted"),
        }
      case "rename_variable":
        editor.trigger("keyboard", "editor.action.rename")
        return {
          action,
          success: true,
          message: this.getResponse("variable_renamed"),
        }
      default:
        return {
          action,
          success: false,
          message: this.getResponse("command_not_understood"),
        }
    }
  }

  private async executeNavigationCommand(action: string, editorRef?: any): Promise<CommandResult> {
    // Implementation for navigation commands
    return {
      action,
      success: true,
      message: "Navigation command executed",
    }
  }

  private async executeAICommand(action: string, editorRef?: any): Promise<CommandResult> {
    return {
      action,
      success: true,
      message: this.getResponse("ai_processing"),
      data: { triggerAI: action },
    }
  }

  private async executeDebugCommand(action: string, editorRef?: any): Promise<CommandResult> {
    switch (action) {
      case "add_breakpoint":
        return {
          action,
          success: true,
          message: this.getResponse("breakpoint_added"),
          data: { debugAction: "addBreakpoint" },
        }
      case "start_debug":
        return {
          action,
          success: true,
          message: this.getResponse("debug_started"),
          data: { debugAction: "startDebugging" },
        }
      default:
        return {
          action,
          success: false,
          message: this.getResponse("command_not_understood"),
        }
    }
  }

  private async processWithAI(transcript: string): Promise<CommandResult> {
    // Send to AI for processing when no direct command match
    return {
      action: "ai_process",
      success: true,
      message: this.getResponse("ai_processing"),
      data: { aiQuery: transcript },
    }
  }

  private getResponse(key: string): string {
    const responses = ttsResponses[this.currentLanguage] as Record<string, string>
    return responses[key] || "Command processed"
  }

  private speakResponse(text: string) {
    if ("speechSynthesis" in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = this.currentLanguage === "bengali" ? "bn-BD" : "en-US"
      utterance.rate = 0.9
      utterance.pitch = 1
      speechSynthesis.speak(utterance)
    }
  }
}

export const voiceProcessor = new VoiceCommandProcessor()
export type { CommandResult }
