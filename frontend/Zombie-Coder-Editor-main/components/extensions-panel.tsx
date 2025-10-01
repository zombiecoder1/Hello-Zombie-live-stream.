"use client"

import { useState } from "react"
import { Search, Download, Star, Settings, Puzzle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

interface Extension {
  id: string
  name: string
  description: string
  author: string
  version: string
  downloads: number
  rating: number
  installed: boolean
  category: string
  icon: string
}

export function ExtensionsPanel() {
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("all")

  const extensions: Extension[] = [
    {
      id: "prettier",
      name: "Prettier - Code formatter",
      description: "Code formatter using prettier",
      author: "Prettier",
      version: "9.10.4",
      downloads: 25000000,
      rating: 4.8,
      installed: true,
      category: "formatters",
      icon: "🎨",
    },
    {
      id: "eslint",
      name: "ESLint",
      description: "Integrates ESLint JavaScript into VS Code",
      author: "Microsoft",
      version: "2.4.2",
      downloads: 20000000,
      rating: 4.7,
      installed: true,
      category: "linters",
      icon: "🔍",
    },
    {
      id: "tailwind",
      name: "Tailwind CSS IntelliSense",
      description: "Intelligent Tailwind CSS tooling",
      author: "Tailwind Labs",
      version: "0.9.11",
      downloads: 5000000,
      rating: 4.9,
      installed: false,
      category: "snippets",
      icon: "🎨",
    },
    {
      id: "live-server",
      name: "Live Server",
      description: "Launch a development local Server with live reload",
      author: "Ritwick Dey",
      version: "5.7.9",
      downloads: 15000000,
      rating: 4.6,
      installed: false,
      category: "other",
      icon: "🌐",
    },
    {
      id: "bengali-support",
      name: "Bengali Language Support",
      description: "Bengali language support for ZombieCoder",
      author: "ZombieCoder Team",
      version: "1.0.0",
      downloads: 1000,
      rating: 5.0,
      installed: true,
      category: "language-packs",
      icon: "🇧🇩",
    },
    {
      id: "ai-assistant",
      name: "ZombieCoder AI Assistant",
      description: "Advanced AI coding assistant with Bengali support",
      author: "ZombieCoder Team",
      version: "2.1.0",
      downloads: 5000,
      rating: 4.9,
      installed: true,
      category: "ai",
      icon: "🧠",
    },
  ]

  const categories = [
    { id: "all", name: "All", count: extensions.length },
    { id: "ai", name: "AI Tools", count: extensions.filter((e) => e.category === "ai").length },
    { id: "formatters", name: "Formatters", count: extensions.filter((e) => e.category === "formatters").length },
    { id: "linters", name: "Linters", count: extensions.filter((e) => e.category === "linters").length },
    {
      id: "language-packs",
      name: "Language Packs",
      count: extensions.filter((e) => e.category === "language-packs").length,
    },
    { id: "snippets", name: "Snippets", count: extensions.filter((e) => e.category === "snippets").length },
    { id: "other", name: "Other", count: extensions.filter((e) => e.category === "other").length },
  ]

  const filteredExtensions = extensions.filter((ext) => {
    const matchesSearch =
      ext.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ext.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = selectedCategory === "all" || ext.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  const formatDownloads = (downloads: number) => {
    if (downloads >= 1000000) {
      return `${(downloads / 1000000).toFixed(1)}M`
    } else if (downloads >= 1000) {
      return `${(downloads / 1000).toFixed(1)}K`
    }
    return downloads.toString()
  }

  return (
    <div className="h-full bg-[#252526] border-l border-[#3c3c3c] flex flex-col">
      <div className="p-3 border-b border-[#3c3c3c]">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-medium text-gray-300 flex items-center gap-2">
            <Puzzle className="h-4 w-4" />
            Extensions
          </h2>
          <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
            <Settings className="h-3 w-3" />
          </Button>
        </div>

        <div className="relative mb-3">
          <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 h-3 w-3 text-gray-400" />
          <Input
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search extensions..."
            className="pl-7 bg-[#3c3c3c] border-[#464647] text-white text-xs h-7"
          />
        </div>

        <div className="flex flex-wrap gap-1">
          {categories.map((category) => (
            <Button
              key={category.id}
              variant={selectedCategory === category.id ? "secondary" : "ghost"}
              size="sm"
              className="h-6 px-2 text-xs"
              onClick={() => setSelectedCategory(category.id)}
            >
              {category.name} ({category.count})
            </Button>
          ))}
        </div>
      </div>

      <ScrollArea className="flex-1 p-3">
        <div className="space-y-3">
          {filteredExtensions.map((extension) => (
            <Card key={extension.id} className="bg-[#2d2d30] border-[#3c3c3c]">
              <CardHeader className="pb-2">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{extension.icon}</span>
                    <div>
                      <CardTitle className="text-sm text-white">{extension.name}</CardTitle>
                      <CardDescription className="text-xs text-gray-400">by {extension.author}</CardDescription>
                    </div>
                  </div>
                  <div className="flex items-center gap-1">
                    <Star className="h-3 w-3 text-yellow-400 fill-current" />
                    <span className="text-xs text-gray-400">{extension.rating}</span>
                  </div>
                </div>
              </CardHeader>

              <CardContent className="pt-0">
                <p className="text-xs text-gray-300 mb-2">{extension.description}</p>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-xs text-gray-400">
                    <Badge variant="outline" className="text-xs">
                      v{extension.version}
                    </Badge>
                    <span>{formatDownloads(extension.downloads)} downloads</span>
                  </div>

                  <Button
                    size="sm"
                    variant={extension.installed ? "secondary" : "default"}
                    className="h-6 px-2 text-xs"
                    disabled={extension.installed}
                  >
                    {extension.installed ? (
                      "Installed"
                    ) : (
                      <>
                        <Download className="h-3 w-3 mr-1" />
                        Install
                      </>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </ScrollArea>
    </div>
  )
}
