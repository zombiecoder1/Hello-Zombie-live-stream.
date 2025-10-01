# 🚀 ZombieCoder Installation Guide

Complete step-by-step installation for **ZombieCoder** - The Next-Gen Bengali AI Code Editor

---

## 📋 System Requirements

### Minimum Requirements

- **OS**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+)
- **RAM**: 4GB
- **Storage**: 2GB free space
- **Node.js**: 18.0.0 or higher
- **npm**: 9.0.0 or higher

### Recommended Requirements

- **OS**: Windows 11, macOS 13+, Linux (Ubuntu 22.04+)
- **RAM**: 8GB or more
- **Storage**: 5GB free space
- **Node.js**: 20.0.0 or higher
- **GPU**: For faster AI inference (optional)

---

## 📦 Installation Steps

### 1️⃣ Install Node.js

#### Windows

1. Download from [nodejs.org](https://nodejs.org)
2. Run installer
3. Verify installation:

\`\`\`cmd
node --version
npm --version
\`\`\`

#### macOS

\`\`\`bash
# Using Homebrew
brew install node

# Verify
node --version
npm --version
\`\`\`

#### Linux (Ubuntu/Debian)

\`\`\`bash
# Install Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify
node --version
npm --version
\`\`\`

### 2️⃣ Install Git

#### Windows

Download from [git-scm.com](https://git-scm.com)

#### macOS

\`\`\`bash
brew install git
\`\`\`

#### Linux

\`\`\`bash
sudo apt-get install git
\`\`\`

### 3️⃣ Clone ZombieCoder

\`\`\`bash
# Clone repository
git clone https://github.com/your-username/zombiecoder.git

# Navigate to directory
cd zombiecoder

# Verify files
ls -la
\`\`\`

### 4️⃣ Install Dependencies

\`\`\`bash
# Install all dependencies
npm install

# This will install:
# - Next.js
# - React
# - Monaco Editor
# - shadcn/ui components
# - AI SDK
# - And all other dependencies
\`\`\`

**Note:** This may take 2-5 minutes depending on your internet speed.

### 5️⃣ Configure Environment

Create `.env.local` file in root directory:

\`\`\`bash
# Create file
touch .env.local

# Or on Windows
type nul > .env.local
\`\`\`

Add configuration:

\`\`\`env
# === REQUIRED ===

# Local AI Server URL (default)
LOCAL_AI_URL=http://localhost:8002

# === OPTIONAL ===

# OpenAI Configuration (if using cloud AI)
OPENAI_API_KEY=sk-your-key-here

# Anthropic Configuration
ANTHROPIC_API_KEY=your-key-here

# Debug Mode
DEBUG=false

# Auto-save
AUTO_SAVE_ENABLED=true
AUTO_SAVE_DELAY=2000
\`\`\`

### 6️⃣ Setup Local AI (Recommended)

#### Option A: Ollama (Easiest)

\`\`\`bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull llama2
ollama pull codellama

# Verify
ollama list
\`\`\`

#### Option B: LM Studio (GUI)

1. Download from [lmstudio.ai](https://lmstudio.ai)
2. Install application
3. Download a model (e.g., CodeLlama 7B)
4. Start local server:
   - Go to "Local Server" tab
   - Set port to 8002
   - Click "Start Server"

### 7️⃣ Start AI Gateway

\`\`\`bash
# Navigate to AI gateway
cd ai-gateway

# Install Python dependencies
pip install -r requirements.txt

# Start gateway server
python gateway.py

# You should see:
# ✓ AI Gateway running on http://localhost:8002
\`\`\`

**Keep this terminal open!**

### 8️⃣ Run ZombieCoder

Open a **new terminal**:

\`\`\`bash
# Navigate to project root
cd zombiecoder

# Start development server
npm run dev

# You should see:
# ✓ Ready on http://localhost:3000
\`\`\`

### 9️⃣ Open in Browser

Visit [http://localhost:3000](http://localhost:3000)

You should see the **ZombieCoder Welcome Screen**! 🎉

---

## 🔧 Post-Installation Setup

### Configure Settings

1. Open ZombieCoder
2. Click **Settings** icon in Activity Bar
3. Configure:
   - Auto-save preferences
   - Theme settings
   - AI provider selection
   - Terminal type

### Test AI Features

1. Click **AI Assistant** on welcome screen
2. Type a question: "Write a Hello World in Python"
3. Verify AI responds with streaming text

### Test Terminal

1. Press `Ctrl+` ` to open terminal
2. Type `echo "Hello ZombieCoder!"`
3. Verify command executes

---

## 📱 Building Desktop App (Optional)

### Using Electron

\`\`\`bash
# Install Electron
npm install electron electron-builder --save-dev

# Build app
npm run build
npm run electron-build
\`\`\`

### Using Tauri

\`\`\`bash
# Install Tauri
npm install @tauri-apps/cli --save-dev

# Build app
npm run tauri build
\`\`\`

---

## 🐳 Docker Installation (Advanced)

### Build Docker Image

\`\`\`bash
# Build image
docker build -t zombiecoder .

# Run container
docker run -p 3000:3000 -p 8002:8002 zombiecoder
\`\`\`

### Docker Compose

\`\`\`yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
      - "8002:8002"
    environment:
      - LOCAL_AI_URL=http://localhost:8002
\`\`\`

Run:

\`\`\`bash
docker-compose up
\`\`\`

---

## ✅ Verification Checklist

- [ ] Node.js installed (`node --version`)
- [ ] Git installed (`git --version`)
- [ ] Dependencies installed (`npm install`)
- [ ] `.env.local` configured
- [ ] AI Gateway running (port 8002)
- [ ] ZombieCoder running (port 3000)
- [ ] Can open welcome screen
- [ ] Can create new file
- [ ] Can open terminal
- [ ] AI chat responds
- [ ] Auto-save works
- [ ] Keyboard shortcuts work

---

## 🔥 Quick Start Commands

\`\`\`bash
# Development
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Type checking
npm run type-check

# Linting
npm run lint

# Format code
npm run format
\`\`\`

---

## 🆘 Installation Issues

### Issue: Port Already in Use

**Error:** `Port 3000 is already in use`

**Solution:**

\`\`\`bash
# Find and kill process
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:3000 | xargs kill -9

# Or use different port
npm run dev -- -p 3001
\`\`\`

### Issue: npm install fails

**Error:** `EACCES: permission denied`

**Solution:**

\`\`\`bash
# Fix npm permissions (Unix)
sudo chown -R $USER ~/.npm
sudo chown -R $USER /usr/local/lib/node_modules

# Or use npx
npx create-next-app@latest
\`\`\`

### Issue: AI Gateway won't start

**Error:** `Address already in use: 8002`

**Solution:**

\`\`\`bash
# Kill existing process
# Windows
netstat -ano | findstr :8002
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8002 | xargs kill -9
\`\`\`

### Issue: Monaco Editor not loading

**Solution:**

\`\`\`bash
# Clear cache
rm -rf .next
npm run dev
\`\`\`

---

## 📚 Next Steps

1. Read [DOCUMENTATION.md](./DOCUMENTATION.md) for full features
2. Check [KEYBOARD_SHORTCUTS.md](./KEYBOARD_SHORTCUTS.md)
3. Join our [Discord](https://discord.gg/zombiecoder)
4. Star us on [GitHub](https://github.com/your-repo)

---

## 🙏 Need Help?

- **GitHub Issues**: [Report Bug](https://github.com/your-repo/issues)
- **Discord**: [Join Community](https://discord.gg/zombiecoder)
- **Email**: support@zombiecoder.dev

---

**Congratulations! You've successfully installed ZombieCoder! 🎉**

**"বাংলার কোডারদের অস্ত্র" 🧟‍♂️**
\`\`\`

Shall I continue with more documentation files (API docs, Contributing guide, etc.)? **Alhamdulillah, brother! The foundation is getting STRONG!** 💪
