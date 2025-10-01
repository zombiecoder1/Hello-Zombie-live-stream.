import { type NextRequest, NextResponse } from "next/server"
import { aiMemory } from "@/lib/ai-memory"

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const type = searchParams.get("type")
  const count = Number.parseInt(searchParams.get("count") || "10")

  try {
    const memories = type ? aiMemory.getRecentMemories(count, type as any) : aiMemory.getRecentMemories(count)

    return NextResponse.json({ memories })
  } catch (error) {
    return NextResponse.json({ error: "Failed to fetch memories" }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const { type, content, metadata } = await request.json()

    aiMemory.addMemory(type, content, metadata)

    return NextResponse.json({ success: true })
  } catch (error) {
    return NextResponse.json({ error: "Failed to add memory" }, { status: 500 })
  }
}

export async function DELETE() {
  try {
    aiMemory.clearMemory()
    return NextResponse.json({ success: true })
  } catch (error) {
    return NextResponse.json({ error: "Failed to clear memory" }, { status: 500 })
  }
}
