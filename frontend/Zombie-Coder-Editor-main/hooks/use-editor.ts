"use client"

import { useState, useCallback } from "react"

interface Tab {
  id: string
  name: string
  path: string
  content: string
  isDirty?: boolean
}

export function useEditor() {
  const [tabs, setTabs] = useState<Tab[]>([])
  const [activeTab, setActiveTab] = useState<string | null>(null)

  const openTab = useCallback(
    (file: { name: string; path: string; content?: string }) => {
      const existingTab = tabs.find((tab) => tab.path === file.path)

      if (existingTab) {
        setActiveTab(existingTab.id)
        return
      }

      const newTab: Tab = {
        id: Date.now().toString(),
        name: file.name,
        path: file.path,
        content: file.content || "",
      }

      setTabs((prev) => [...prev, newTab])
      setActiveTab(newTab.id)
    },
    [tabs],
  )

  const closeTab = useCallback(
    (tabId: string) => {
      setTabs((prev) => {
        const newTabs = prev.filter((tab) => tab.id !== tabId)
        if (activeTab === tabId) {
          setActiveTab(newTabs.length > 0 ? newTabs[newTabs.length - 1].id : null)
        }
        return newTabs
      })
    },
    [activeTab],
  )

  const switchTab = useCallback((tabId: string) => {
    setActiveTab(tabId)
  }, [])

  const updateTabContent = useCallback((tabId: string, content: string) => {
    setTabs((prev) => prev.map((tab) => (tab.id === tabId ? { ...tab, content, isDirty: true } : tab)))
  }, [])

  return {
    tabs,
    activeTab,
    openTab,
    closeTab,
    switchTab,
    updateTabContent,
  }
}
