# 🧟‍♂️ ZombieCoder - Complete Documentation

**"বাংলার কোডারদের অস্ত্র"** - The Next-Gen Bengali AI Code Editor

---

## 📚 Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Features](#features)
4. [Keyboard Shortcuts](#keyboard-shortcuts)
5. [AI System Integration](#ai-system-integration)
6. [Architecture](#architecture)
7. [Development Guide](#development-guide)
8. [Optimization](#optimization)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Introduction

ZombieCoder is a professional-grade code editor built specifically for Bengali developers, with full support for:

- **Local AI Models** (Ollama, LM Studio)
- **Cloud AI Providers** (OpenAI, Anthropic)
- **Bengali Language Support** (Voice input, UI, Documentation)
- **VS Code Compatibility** (Same shortcuts, layout, features)
- **Copilot Features** (Streaming responses, completions, context injection)

---

## 💻 Installation

### Prerequisites

- **Node.js** 18+ and npm
- **Git**
- **VS Code** (optional, for comparison)
- **Ollama** or **LM Studio** (for local AI)

### Step 1: Clone Repository

\`\`\`bash
git clone https://github.com/your-username/zombiecoder.git
cd zombiecoder
\`\`\`

### Step 2: Install Dependencies

\`\`\`bash
npm install
\`\`\`

### Step 3: Configure Environment

Create a `.env.local` file:

\`\`\`env
# OpenAI (Optional)
OPENAI_API_KEY=your_openai_key_here

# Local AI Server (Default: http://localhost:8002)
LOCAL_AI_URL=http://localhost:8002
\`\`\`

### Step 4: Run Development Server

\`\`\`bash
npm run dev
\`\`\`

Open [http://localhost:3000](http://localhost:3000)

### Step 5: Build for Production

\`\`\`bash
npm run build
npm start
\`\`\`

---

## ✨ Features

### 🎨 Professional UI

- **VS Code-like Interface**
- **Responsive Design** (works on all screen sizes)
- **Dark Theme** with perfect color combinations
- **Custom Icons & Fonts** for readability
- **Activity Bar** with icons (Explorer, Search, Git, Debug, Extensions, AI)

### 🤖 AI Features

1. **Agent Chat**
   - Streaming responses (live typing effect)
   - Provider selection (Local, OpenAI, Anthropic)
   - Agent selection (Bengali NLP, Code Assistant, General)
   - Image upload support
   - Audio input support
   - File context awareness

2. **Code Completions**
   - Inline suggestions
   - Context-aware completions
   - Multi-language support

3. **Bengali Support**
   - Voice input in Bengali
   - Bengali UI elements
   - Bengali documentation

### 📁 File Management

- **Explorer Sidebar**
- **File Tree Navigation**
- **Create/Delete Files & Folders**
- **Multi-tab Support**
- **Auto-save** (configurable)

### 💻 Terminal

- **Multiple Terminal Types**
  - PowerShell (Default)
  - Command Prompt
  - Git Bash
  - Ubuntu (WSL)
  
- **Terminal Features**
  - Multiple terminal instances
  - Split terminal support
  - Custom commands
  - Output panel
  - Debug console

### 🎹 Editor Features

- **Monaco Editor** (same as VS Code)
- **Syntax Highlighting**
- **IntelliSense**
- **Code Formatting**
- **Find & Replace**
- **Multi-cursor Support**
- **Bracket Matching**
- **Code Folding**

---

## ⌨️ Keyboard Shortcuts

### File Operations

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New File |
| `Ctrl+O` | Open File |
| `Ctrl+S` | Save File |
| `Ctrl+Shift+S` | Save As |
| `Ctrl+K S` | Save All |
| `Ctrl+W` | Close Tab |

### Editing

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Copy |
| `Ctrl+X` | Cut |
| `Ctrl+V` | Paste |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Ctrl+F` | Find |
| `Ctrl+H` | Replace |
| `Ctrl+/` | Toggle Comment |
| `Shift+Alt+F` | Format Document |

### Navigation

| Shortcut | Action |
|----------|--------|
| `Ctrl+P` | Quick Open |
| `Ctrl+Shift+P` | Command Palette |
| `Ctrl+G` | Go to Line |
| `Ctrl+Tab` | Switch Tab |

### View

| Shortcut | Action |
|----------|--------|
| `Ctrl+` ` | Toggle Terminal |
| `Ctrl+Shift+A` | Toggle AI Chat |
| `Ctrl+Shift+E` | Explorer |
| `Ctrl+Shift+F` | Search |
| `Ctrl+Shift+G` | Git |
| `Ctrl+Shift+D` | Debug |
| `Ctrl+Shift+X` | Extensions |

---

## 🤖 AI System Integration

### Local AI Setup (Recommended for Beginners)

#### Option 1: Ollama

1. **Install Ollama**

\`\`\`bash
# Linux/Mac
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
\`\`\`

2. **Run AI Gateway**

\`\`\`bash
cd ai-gateway
python gateway.py
\`\`\`

3. **Pull Models**

\`\`\`bash
ollama pull llama2
ollama pull codellama
\`\`\`

#### Option 2: LM Studio

1. Download from [lmstudio.ai](https://lmstudio.ai)
2. Load a model (e.g., CodeLlama)
3. Start local server on port 8002

### Cloud AI Setup

#### OpenAI

1. Get API key from [platform.openai.com](https://platform.openai.com)
2. Add to `.env.local`:

\`\`\`env
OPENAI_API_KEY=sk-...
\`\`\`

#### Anthropic

1. Get API key from [console.anthropic.com](https://console.anthropic.com)
2. Configure in settings

---

## 🏗️ Architecture

### Project Structure

\`\`\`
zombiecoder/
├── app/
│   ├── api/
│   │   ├── chat/route.ts          # Chat API
│   │   └── voice-command/route.ts # Voice API
│   ├── globals.css
│   └── page.tsx                    # Main Editor
├── components/
│   ├── ui/                         # shadcn components
│   ├── activity-bar.tsx
│   ├── agent-chat-enhanced.tsx     # AI Chat
│   ├── command-palette.tsx
│   ├── menu-bar.tsx
│   ├── sidebar.tsx                 # File Explorer
│   ├── status-bar.tsx
│   ├── tab-bar.tsx
│   ├── terminal-enhanced.tsx       # Terminal
│   └── welcome-screen-enhanced.tsx
├── hooks/
│   ├── use-editor.ts
│   ├── use-file-system.ts
│   └── use-voice.ts
├── lib/
│   ├── ai-memory.ts
│   ├── monaco-setup.ts
│   └── voice-command-processor.ts
├── ai-gateway/
│   ├── gateway.py                  # AI Gateway Server
│   └── requirements.txt
└── DOCUMENTATION.md
\`\`\`

### Component Hierarchy

\`\`\`
App
├── MenuBar
├── ActivityBar
├── Content
│   ├── Sidebar (Explorer)
│   ├── Editor Area
│   │   ├── TabBar
│   │   ├── Monaco Editor
│   │   └── Terminal
│   └── AgentChat
└── StatusBar
\`\`\`

---

## 👨‍💻 Development Guide

### Adding a New Feature

1. **Plan the Feature**
   - Define requirements
   - Create component structure
   - Design UI/UX

2. **Create Component**

\`\`\`tsx
// components/my-feature.tsx
"use client"

import { useState } from "react"

export function MyFeature() {
  return <div>My Feature</div>
}
\`\`\`

3. **Add to Main App**

\`\`\`tsx
// app/page.tsx
import { MyFeature } from "@/components/my-feature"

// Add to render
<MyFeature />
\`\`\`

4. **Test Thoroughly**

\`\`\`bash
npm run dev
# Test all edge cases
\`\`\`

### Adding Keyboard Shortcuts

\`\`\`tsx
useEffect(() => {
  const handleKeyboard = (e: KeyboardEvent) => {
    if (e.ctrlKey && e.key === "k") {
      e.preventDefault()
      // Your action here
    }
  }
  
  window.addEventListener("keydown", handleKeyboard)
  return () => window.removeEventListener("keydown", handleKeyboard)
}, [])
\`\`\`

### Adding AI Providers

1. **Update Provider List**

\`\`\`tsx
const availableProviders = [
  { id: "local", name: "Local Model", icon: "💻" },
  { id: "my-provider", name: "My Provider", icon: "🤖" },
]
\`\`\`

2. **Add API Integration**

\`\`\`tsx
const apiUrl = selectedProvider === "my-provider" 
  ? "https://my-api.com" 
  : "http://localhost:8002"
\`\`\`

---

## ⚡ Optimization

### Performance Tips

1. **Code Splitting**

\`\`\`tsx
const HeavyComponent = dynamic(() => import("./heavy"), {
  loading: () => <div>Loading...</div>
})
\`\`\`

2. **Debounce Auto-save**

\`\`\`tsx
const debouncedSave = useMemo(
  () => debounce((content) => save(content), 2000),
  []
)
\`\`\`

3. **Lazy Load Monaco**

\`\`\`tsx
const Editor = dynamic(() => import("@monaco-editor/react"), {
  ssr: false
})
\`\`\`

### Build Optimization

\`\`\`bash
# Analyze bundle
npm run build -- --analyze

# Optimize images
npm install sharp

# Use production build
NODE_ENV=production npm run build
\`\`\`

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Terminal Not Working

**Solution:**
- Check terminal type compatibility
- Verify shell exists on system
- Restart editor

#### 2. AI Not Responding

**Solution:**
- Check AI server is running (port 8002)
- Verify API keys in `.env.local`
- Check console for errors

#### 3. Auto-save Not Working

**Solution:**
- Check auto-save is enabled in settings
- Verify file permissions
- Check console for errors

#### 4. Keyboard Shortcuts Not Working

**Solution:**
- Check for conflicting browser shortcuts
- Verify focus is in editor
- Restart application

### Debug Mode

Enable debug logging:

\`\`\`tsx
// Set in .env.local
DEBUG=true
\`\`\`

---

## 📞 Support

- **GitHub Issues**: [github.com/your-repo/issues](https://github.com/your-repo/issues)
- **Discord**: [discord.gg/zombiecoder](https://discord.gg/zombiecoder)
- **Email**: support@zombiecoder.dev

---

## 📜 License

MIT License - See LICENSE file

---

## 🙏 Credits

Built with ❤️ by Bengali developers for Bengali developers.

**Tech Stack:**
- Next.js 15
- React 19
- Monaco Editor
- Tailwind CSS
- shadcn/ui
- AI SDK (Vercel)

**Inspired by:**
- VS Code
- Cursor AI
- GitHub Copilot

---

**May Allah bless all developers! 🤲**

**"বাংলার কোডারদের অস্ত্র" 🧟‍♂️**
\`\`\`

Now creating the **Installation Guide**:
