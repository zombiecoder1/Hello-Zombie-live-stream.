import { streamText } from "ai"
import { openai } from "@ai-sdk/openai"
import { aiMemory } from "@/lib/ai-memory"

export async function POST(req: Request) {
  const { command, language, currentFile, fileContent } = await req.json()

  // Get AI memory context
  const memoryContext = aiMemory.getContextForAI()

  const result = await streamText({
    model: openai("gpt-4o"),
    system: `You are ZombieCoder Voice Command Processor - specialized in processing Bengali and English voice commands for code editing.

🧟‍♂️ Voice Command Processing:
- Understand Bengali (বাংলা) and English voice commands
- Generate appropriate code based on voice instructions
- Provide TTS-friendly responses
- Execute file operations and code transformations
- Support context-aware code generation

Current Context:
- Language: ${language}
- Current File: ${currentFile || "No file selected"}
- File Content Preview: ${fileContent ? fileContent.substring(0, 500) + "..." : "Empty file"}

${memoryContext}

Voice Command Guidelines:
1. If command is in Bengali, respond in Bengali with code examples
2. If command is in English, respond in English
3. Always provide executable code when requested
4. Include helpful comments in the appropriate language
5. Consider the current file context when generating responses
6. Provide step-by-step instructions for complex operations

Response Format:
- For code generation: Provide complete, runnable code
- For explanations: Use simple, clear language suitable for TTS
- For file operations: Confirm the action and provide next steps`,
    messages: [
      {
        role: "user",
        content: `Voice command (${language}): ${command}`,
      },
    ],
  })

  // Add voice command to memory
  aiMemory.addMemory("conversation", `Voice Command (${language}): ${command}`, {
    type: "voice_command",
    language,
    currentFile,
  })

  return result.toDataStreamResponse()
}
