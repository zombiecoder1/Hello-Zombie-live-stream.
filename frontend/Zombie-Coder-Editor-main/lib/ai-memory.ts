"use client"

interface MemoryEntry {
  id: string
  timestamp: Date
  type: "conversation" | "code_context" | "user_preference" | "project_context"
  content: string
  metadata?: Record<string, any>
}

interface ProjectContext {
  name: string
  language: string
  framework?: string
  dependencies: string[]
  recentFiles: string[]
  codeStyle: {
    indentation: "spaces" | "tabs"
    indentSize: number
    quotes: "single" | "double"
    semicolons: boolean
  }
}

class AIMemorySystem {
  private memories: MemoryEntry[] = []
  private projectContext: ProjectContext | null = null
  private maxMemories = 1000

  constructor() {
    this.loadFromStorage()
  }

  addMemory(type: MemoryEntry["type"], content: string, metadata?: Record<string, any>) {
    const memory: MemoryEntry = {
      id: Date.now().toString(),
      timestamp: new Date(),
      type,
      content,
      metadata,
    }

    this.memories.unshift(memory)

    // Keep only the most recent memories
    if (this.memories.length > this.maxMemories) {
      this.memories = this.memories.slice(0, this.maxMemories)
    }

    this.saveToStorage()
  }

  getRecentMemories(count = 10, type?: MemoryEntry["type"]): MemoryEntry[] {
    let filtered = this.memories
    if (type) {
      filtered = this.memories.filter((m) => m.type === type)
    }
    return filtered.slice(0, count)
  }

  searchMemories(query: string): MemoryEntry[] {
    const lowercaseQuery = query.toLowerCase()
    return this.memories.filter((memory) => memory.content.toLowerCase().includes(lowercaseQuery))
  }

  updateProjectContext(context: Partial<ProjectContext>) {
    this.projectContext = {
      ...this.projectContext,
      ...context,
    } as ProjectContext

    this.addMemory("project_context", JSON.stringify(this.projectContext))
    this.saveToStorage()
  }

  getProjectContext(): ProjectContext | null {
    return this.projectContext
  }

  getContextForAI(): string {
    const recentConversations = this.getRecentMemories(5, "conversation")
    const recentCodeContext = this.getRecentMemories(3, "code_context")

    let context = "## ZombieCoder AI Memory Context\n\n"

    if (this.projectContext) {
      context += `### Current Project: ${this.projectContext.name}\n`
      context += `- Language: ${this.projectContext.language}\n`
      context += `- Framework: ${this.projectContext.framework || "None"}\n`
      context += `- Recent Files: ${this.projectContext.recentFiles.join(", ")}\n\n`
    }

    if (recentConversations.length > 0) {
      context += "### Recent Conversations:\n"
      recentConversations.forEach((memory) => {
        context += `- ${memory.content}\n`
      })
      context += "\n"
    }

    if (recentCodeContext.length > 0) {
      context += "### Recent Code Context:\n"
      recentCodeContext.forEach((memory) => {
        context += `- ${memory.content}\n`
      })
      context += "\n"
    }

    return context
  }

  private saveToStorage() {
    if (typeof window !== "undefined") {
      localStorage.setItem("zombiecoder-memory", JSON.stringify(this.memories))
      if (this.projectContext) {
        localStorage.setItem("zombiecoder-project", JSON.stringify(this.projectContext))
      }
    }
  }

  private loadFromStorage() {
    if (typeof window !== "undefined") {
      const savedMemories = localStorage.getItem("zombiecoder-memory")
      if (savedMemories) {
        this.memories = JSON.parse(savedMemories)
      }

      const savedProject = localStorage.getItem("zombiecoder-project")
      if (savedProject) {
        this.projectContext = JSON.parse(savedProject)
      }
    }
  }

  clearMemory() {
    this.memories = []
    this.projectContext = null
    if (typeof window !== "undefined") {
      localStorage.removeItem("zombiecoder-memory")
      localStorage.removeItem("zombiecoder-project")
    }
  }
}

export const aiMemory = new AIMemorySystem()
export type { MemoryEntry, ProjectContext }
