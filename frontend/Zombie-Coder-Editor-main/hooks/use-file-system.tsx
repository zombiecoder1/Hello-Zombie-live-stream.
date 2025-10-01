"use client"

import { useState, useCallback } from "react"

export interface FileNode {
  name: string
  path: string
  type: "file" | "folder"
  children?: FileNode[]
  content?: string
}

const initialFiles: FileNode[] = [
  {
    name: "src",
    path: "/src",
    type: "folder",
    children: [
      {
        name: "components",
        path: "/src/components",
        type: "folder",
        children: [
          {
            name: "Button.tsx",
            path: "/src/components/Button.tsx",
            type: "file",
            content: `import React from 'react'

interface ButtonProps {
  children: React.ReactNode
  onClick?: () => void
  variant?: 'primary' | 'secondary'
}

export function Button({ children, onClick, variant = 'primary' }: ButtonProps) {
  return (
    <button
      onClick={onClick}
      className={\`px-4 py-2 rounded \${
        variant === 'primary' 
          ? 'bg-blue-500 text-white hover:bg-blue-600' 
          : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
      }\`}
    >
      {children}
    </button>
  )
}`,
          },
        ],
      },
      {
        name: "App.tsx",
        path: "/src/App.tsx",
        type: "file",
        content: `import React from 'react'
import { Button } from './components/Button'

function App() {
  const handleClick = () => {
    console.log('Button clicked!')
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">
          Welcome to Cursor AI Editor
        </h1>
        <Button onClick={handleClick}>
          Get Started
        </Button>
      </div>
    </div>
  )
}

export default App`,
      },
    ],
  },
  {
    name: "package.json",
    path: "/package.json",
    type: "file",
    content: `{
  "name": "cursor-ai-project",
  "version": "1.0.0",
  "description": "A project created with Cursor AI Editor",
  "main": "src/App.tsx",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "vite": "^4.4.0"
  }
}`,
  },
  {
    name: "README.md",
    path: "/README.md",
    type: "file",
    content: `# Cursor AI Project

This project was created using the Cursor AI Editor.

## Getting Started

1. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

2. Start the development server:
   \`\`\`bash
   npm run dev
   \`\`\`

3. Open your browser and navigate to \`http://localhost:3000\`

## Features

- Modern React with TypeScript
- Hot module replacement
- AI-powered code assistance
- Professional development environment

## Contributing

Feel free to contribute to this project by submitting pull requests or opening issues.
`,
  },
]

export function useFileSystem() {
  const [files, setFiles] = useState<FileNode[]>(initialFiles)
  const [activeFile, setActiveFile] = useState<FileNode | null>(null)

  const findFileByPath = useCallback(
    (path: string, nodes: FileNode[] = files): FileNode | null => {
      for (const node of nodes) {
        if (node.path === path) return node
        if (node.children) {
          const found = findFileByPath(path, node.children)
          if (found) return found
        }
      }
      return null
    },
    [files],
  )

  const openFile = useCallback((file: FileNode) => {
    if (file.type === "file") {
      setActiveFile(file)
    }
  }, [])

  const createFile = useCallback((path: string, type: "file" | "folder") => {
    const pathParts = path.split("/")
    const name = pathParts[pathParts.length - 1]
    const parentPath = pathParts.slice(0, -1).join("/") || "/"

    const newNode: FileNode = {
      name,
      path,
      type,
      children: type === "folder" ? [] : undefined,
      content: type === "file" ? "" : undefined,
    }

    const updateFiles = (nodes: FileNode[]): FileNode[] => {
      return nodes.map((node) => {
        if (node.path === parentPath && node.type === "folder") {
          return {
            ...node,
            children: [...(node.children || []), newNode],
          }
        }
        if (node.children) {
          return {
            ...node,
            children: updateFiles(node.children),
          }
        }
        return node
      })
    }

    if (parentPath === "/") {
      setFiles((prev) => [...prev, newNode])
    } else {
      setFiles(updateFiles)
    }
  }, [])

  const deleteFile = useCallback(
    (path: string) => {
      const removeFile = (nodes: FileNode[]): FileNode[] => {
        return nodes.filter((node) => {
          if (node.path === path) return false
          if (node.children) {
            node.children = removeFile(node.children)
          }
          return true
        })
      }

      setFiles(removeFile)
      if (activeFile?.path === path) {
        setActiveFile(null)
      }
    },
    [activeFile],
  )

  const updateFileContent = useCallback(
    (path: string, content: string) => {
      const updateContent = (nodes: FileNode[]): FileNode[] => {
        return nodes.map((node) => {
          if (node.path === path && node.type === "file") {
            return { ...node, content }
          }
          if (node.children) {
            return { ...node, children: updateContent(node.children) }
          }
          return node
        })
      }

      setFiles(updateContent)
      if (activeFile?.path === path) {
        setActiveFile((prev) => (prev ? { ...prev, content } : null))
      }
    },
    [activeFile],
  )

  return {
    files,
    activeFile,
    openFile,
    createFile,
    deleteFile,
    updateFileContent,
    findFileByPath,
  }
}
