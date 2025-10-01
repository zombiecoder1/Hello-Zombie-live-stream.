"use client"

import { useState } from "react"
import { ChevronDown, ChevronRight, File, Folder, FolderOpen, Plus, Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"

interface FileNode {
  name: string
  path: string
  type: "file" | "folder"
  children?: FileNode[]
  content?: string
}

interface SidebarProps {
  files: FileNode[]
  onFileSelect: (file: FileNode) => void
  onFileCreate: (path: string, type: "file" | "folder") => void
  onFileDelete: (path: string) => void
  activeFile: FileNode | null
}

export function Sidebar({ files, onFileSelect, onFileCreate, onFileDelete, activeFile }: SidebarProps) {
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set(["/"]))
  const [creatingFile, setCreatingFile] = useState<{ path: string; type: "file" | "folder" } | null>(null)
  const [newFileName, setNewFileName] = useState("")

  const toggleFolder = (path: string) => {
    const newExpanded = new Set(expandedFolders)
    if (newExpanded.has(path)) {
      newExpanded.delete(path)
    } else {
      newExpanded.add(path)
    }
    setExpandedFolders(newExpanded)
  }

  const handleCreateFile = (parentPath: string, type: "file" | "folder") => {
    setCreatingFile({ path: parentPath, type })
    setNewFileName("")
  }

  const handleConfirmCreate = () => {
    if (creatingFile && newFileName.trim()) {
      const fullPath = creatingFile.path === "/" ? `/${newFileName}` : `${creatingFile.path}/${newFileName}`
      onFileCreate(fullPath, creatingFile.type)
      setCreatingFile(null)
      setNewFileName("")
    }
  }

  const handleCancelCreate = () => {
    setCreatingFile(null)
    setNewFileName("")
  }

  const renderFileTree = (nodes: FileNode[], level = 0) => {
    return nodes.map((node) => (
      <div key={node.path}>
        <div
          className={cn(
            "flex items-center gap-1 px-2 py-1 hover:bg-[#2a2a2a] cursor-pointer text-sm group",
            activeFile?.path === node.path && "bg-[#37373d]",
          )}
          style={{ paddingLeft: `${8 + level * 16}px` }}
        >
          {node.type === "folder" ? (
            <>
              <Button
                variant="ghost"
                size="sm"
                className="h-4 w-4 p-0 hover:bg-transparent"
                onClick={() => toggleFolder(node.path)}
              >
                {expandedFolders.has(node.path) ? (
                  <ChevronDown className="h-3 w-3" />
                ) : (
                  <ChevronRight className="h-3 w-3" />
                )}
              </Button>
              {expandedFolders.has(node.path) ? (
                <FolderOpen className="h-4 w-4 text-blue-400" />
              ) : (
                <Folder className="h-4 w-4 text-blue-400" />
              )}
              <span className="flex-1" onClick={() => toggleFolder(node.path)}>
                {node.name}
              </span>
              <div className="opacity-0 group-hover:opacity-100 flex gap-1">
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-4 w-4 p-0"
                  onClick={(e) => {
                    e.stopPropagation()
                    handleCreateFile(node.path, "file")
                  }}
                >
                  <Plus className="h-3 w-3" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-4 w-4 p-0"
                  onClick={(e) => {
                    e.stopPropagation()
                    onFileDelete(node.path)
                  }}
                >
                  <Trash2 className="h-3 w-3" />
                </Button>
              </div>
            </>
          ) : (
            <>
              <div className="w-4" />
              <File className="h-4 w-4 text-gray-400" />
              <span className="flex-1" onClick={() => onFileSelect(node)}>
                {node.name}
              </span>
              <Button
                variant="ghost"
                size="sm"
                className="h-4 w-4 p-0 opacity-0 group-hover:opacity-100"
                onClick={(e) => {
                  e.stopPropagation()
                  onFileDelete(node.path)
                }}
              >
                <Trash2 className="h-3 w-3" />
              </Button>
            </>
          )}
        </div>

        {creatingFile?.path === node.path && (
          <div className="flex items-center gap-1 px-2 py-1" style={{ paddingLeft: `${24 + level * 16}px` }}>
            {creatingFile.type === "file" ? (
              <File className="h-4 w-4 text-gray-400" />
            ) : (
              <Folder className="h-4 w-4 text-blue-400" />
            )}
            <Input
              value={newFileName}
              onChange={(e) => setNewFileName(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") handleConfirmCreate()
                if (e.key === "Escape") handleCancelCreate()
              }}
              onBlur={handleConfirmCreate}
              className="h-6 text-xs bg-[#3c3c3c] border-[#464647]"
              placeholder={creatingFile.type === "file" ? "filename.ext" : "folder name"}
              autoFocus
            />
          </div>
        )}

        {node.type === "folder" &&
          expandedFolders.has(node.path) &&
          node.children &&
          renderFileTree(node.children, level + 1)}
      </div>
    ))
  }

  return (
    <div className="h-full bg-[#252526] border-r border-[#3c3c3c]">
      <div className="p-3 border-b border-[#3c3c3c]">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-medium text-gray-300">EXPLORER</h2>
          <div className="flex gap-1">
            <Button variant="ghost" size="sm" className="h-6 w-6 p-0" onClick={() => handleCreateFile("/", "file")}>
              <Plus className="h-3 w-3" />
            </Button>
          </div>
        </div>
      </div>
      <div className="overflow-auto">{renderFileTree(files)}</div>
    </div>
  )
}
