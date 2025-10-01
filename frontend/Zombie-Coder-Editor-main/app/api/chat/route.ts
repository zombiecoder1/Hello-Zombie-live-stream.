import { generateText } from "ai"
import { openai } from "@ai-sdk/openai"
import { NextResponse } from "next/server"

export const runtime = "edge"

export async function POST(req: Request) {
  try {
    const body = await req.json()
    const { messages, input, mode, language } = body

    const systemPrompt =
      language === "bengali"
        ? `আপনি একজন বিশেষজ্ঞ কোডিং সহায়ক যিনি বাংলা এবং ইংরেজি উভয় ভাষায় সাহায্য করতে পারেন। আপনি কোড ব্যাখ্যা, বাগ খুঁজে বের করা, অপ্টিমাইজেশন এবং টেস্ট কেস তৈরিতে সাহায্য করেন। সবসময় পরিষ্কার এবং সহজবোধ্য উত্তর দিন।`
        : `You are an expert coding assistant who can help in both Bengali and English. You help with code explanation, finding bugs, optimization, and creating test cases. Always provide clear and easy-to-understand answers.`

    const prompt =
      mode === "code"
        ? `${systemPrompt}\n\nPlease help with this code-related question:\n${input}`
        : `${systemPrompt}\n\n${input}`

    const { text } = await generateText({
      model: openai("gpt-4o-mini"),
      prompt: prompt,
      temperature: 0.7,
      maxTokens: 2000,
    })

    return NextResponse.json({ text })
  } catch (error) {
    console.error("Error in chat API:", error)
    return NextResponse.json(
      { error: "Failed to generate response", details: error instanceof Error ? error.message : "Unknown error" },
      { status: 500 },
    )
  }
}
