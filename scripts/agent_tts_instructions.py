#!/usr/bin/env python3
"""
Agent TTS Instructions for ZombieCoder
Complete instructions for agents to generate Bengali TTS audio
"""

import os
from datetime import datetime

def create_agent_instructions():
    """Create comprehensive agent instructions"""
    
    instructions = f"""
# 🧟‍♂️ Agents জন্য Instruction – Bengali TTS Audio Documentation
## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1️⃣ Markdown/Text প্রস্তুত করা

### File: workspace/docs/project_doc.txt

### Content Requirements:
- প্রজেক্ট overview
- Local model + Smart routing logic
- MPC dispatcher & agent workflow
- Server system + library dependencies
- Current system status
- Real-life workflow explanation (কীভাবে user input থেকে output আসে, memory update হয়, cloud API fallback কবে লাগে)
- Zero tolerance rules & agent task flow

### Important: 
সব অপ্রয়োজনীয় আইকন, #, .., emojis বা symbol বাদ দিতে হবে।

### Example:
- # Programming Agent → Programming Agent
- ✅ Completed → Completed
- 🚀 Ready → Ready

## 2️⃣ Google TTS Python Script Adjustments

### Language: Bengali (lang='bn')
### Chunk processing: Google TTS limit (~5000 chars) এর জন্য টেক্সট ভাগ করা
### Audio merging: pydub ব্যবহার করে seamless final mp3
### Metadata: duration, size, language, chunks info

### Example Code:
```python
from gtts import gTTS
from pydub import AudioSegment
import os

doc_file = "workspace/docs/project_doc.txt"
audio_file = "workspace/docs/project_doc.mp3"

with open(doc_file, "r", encoding="utf-8") as f:
    text_content = f.read()

# Remove unwanted symbols
clean_text = text_content.replace("#", "").replace("..", "").replace("🧟‍♂️", "")

# Chunk processing
max_chars = 4000
chunks = [clean_text[i:i+max_chars] for i in range(0, len(clean_text), max_chars)]

audio_parts = []
for idx, chunk in enumerate(chunks):
    tts = gTTS(text=chunk, lang='bn')
    part_file = f"workspace/docs/part_{{idx+1}}.mp3"
    tts.save(part_file)
    audio_parts.append(part_file)

# Merge audio
combined = AudioSegment.empty()
for part in audio_parts:
    combined += AudioSegment.from_mp3(part)

combined.export(audio_file, format="mp3")
print(f"[SUCCESS] Final Bengali audio ready: {{audio_file}}")
```

## 3️⃣ Real-Life Workflow Explanation Integration

### Agents কে বলো Markdown এ বাস্তব জীবনের উদাহরণ সহ লিখতে:

#### Input: User voice/text → Local model via smart routing
#### Processing: MPC dispatcher, memory check, cloud API fallback
#### Output: Response sent to user
#### Logging: Dashboard & agent log update

### ব্যাখ্যা দিন যেন agents বোঝে কিভাবে system কাজ করে step-by-step

## 4️⃣ Git Commit & Reporting

```bash
git add workspace/docs/project_doc*.mp3
git commit -m "✅ Bengali TTS audio documentation updated – real-life workflow included"
git push
```

### Agents কে নিশ্চিত করতে হবে: 
- সব log, memory update, dashboard sync confirm
- Audio file quality check
- Metadata generation confirm
- Temporary files cleanup

## 5️⃣ Summary – Key Points

- **No symbols / emojis** – শুধু text
- **Full Bengali narration** – বাস্তব জীবনের context
- **Smart routing + Local model + Cloud fallback explain**
- **Chunk + Merge** – >10 min audio possible
- **Metadata** – duration, size, language
- **Agents ready** – direct run, auto cleanup

## 6️⃣ Execution Steps for Agents

### Step 1: Prepare Documentation
```bash
# Edit the documentation file
nano workspace/docs/project_doc.txt

# Ensure content includes:
# - Project overview
# - Real-life workflow explanation
# - No symbols or emojis
# - Bengali text only
```

### Step 2: Run TTS Generator
```bash
# Run the improved audio generator
python3 scripts/improved_audio_generator.py

# This will:
# - Clean text from symbols
# - Split into chunks
# - Generate Bengali TTS
# - Merge audio parts
# - Create metadata
# - Clean up temp files
```

### Step 3: Verify Output
```bash
# Check generated files
ls -la workspace/docs/

# Verify audio file
file workspace/docs/project_doc.mp3

# Check metadata
cat workspace/docs/audio_metadata.json
```

### Step 4: Commit Changes
```bash
# Add and commit all changes
git add workspace/docs/
git commit -m "✅ Bengali TTS audio documentation updated with real-life workflow"
git push
```

## 7️⃣ Quality Checklist

### Before Generation:
- [ ] Text file contains real-life workflow explanation
- [ ] No symbols, emojis, or special characters
- [ ] Bengali text only
- [ ] Content covers all required sections

### After Generation:
- [ ] Audio file generated successfully
- [ ] Duration is appropriate (7-10 minutes)
- [ ] File size is reasonable (< 5MB)
- [ ] Metadata file created
- [ ] Temporary files cleaned up
- [ ] Git commit completed

## 8️⃣ Troubleshooting

### Common Issues:
1. **gTTS connection error**: Check internet connection
2. **Audio merging failed**: Install pydub and ffmpeg
3. **File not found**: Ensure correct file paths
4. **Permission denied**: Check file permissions

### Solutions:
```bash
# Install dependencies
sudo apt install python3-gtts python3-pydub ffmpeg

# Fix permissions
chmod +x scripts/improved_audio_generator.py

# Check file paths
ls -la workspace/docs/
```

## 9️⃣ Expected Output

### Files Generated:
- `workspace/docs/project_doc.txt` - Clean Bengali text
- `workspace/docs/project_doc.mp3` - Final audio file
- `workspace/docs/audio_metadata.json` - Audio metadata

### Audio Specifications:
- **Duration**: 7-10 minutes
- **Language**: Bengali
- **Format**: MP3
- **Quality**: High (64 kbps, 24 kHz)
- **Size**: 1.5-3 MB

## 🔟 Final Message

> "Agents, এই instructions follow করে তোমরা professional-quality Bengali TTS audio documentation generate করতে পারবে। 
> 
> সব steps carefully follow করো, quality check করো, এবং final output verify করো।
> 
> ZombieCoder system এর জন্য high-quality audio documentation তৈরি করো।
> 
> - ZombieCoder Development Team"

---

**Instructions Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Status**: ✅ READY FOR AGENT EXECUTION  
**Priority**: 🔥 HIGH  
**Deadline**: Immediate
    """
    
    # Save instructions
    with open("agent_tts_instructions.md", 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ Agent TTS instructions created: agent_tts_instructions.md")
    return instructions

def create_quick_reference():
    """Create quick reference for agents"""
    
    quick_ref = f"""
# Quick Reference - Bengali TTS Generation

## Commands:
```bash
# 1. Edit documentation
nano workspace/docs/project_doc.txt

# 2. Generate audio
python3 scripts/improved_audio_generator.py

# 3. Check output
ls -la workspace/docs/

# 4. Commit changes
git add workspace/docs/ && git commit -m "TTS audio updated"
```

## File Locations:
- Documentation: `workspace/docs/project_doc.txt`
- Audio Output: `workspace/docs/project_doc.mp3`
- Metadata: `workspace/docs/audio_metadata.json`
- Script: `workspace/scripts/improved_audio_generator.py`

## Quality Check:
- Duration: 7-10 minutes
- Language: Bengali
- Format: MP3
- Size: 1.5-3 MB
- No symbols/emojis in text

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    with open("tts_quick_reference.md", 'w', encoding='utf-8') as f:
        f.write(quick_ref)
    
    print("✅ Quick reference created: tts_quick_reference.md")

def main():
    """Main function"""
    print("🧟 Agent TTS Instructions Generator")
    print("=" * 50)
    
    # Create instructions
    print("1. Creating agent instructions...")
    create_agent_instructions()
    
    # Create quick reference
    print("2. Creating quick reference...")
    create_quick_reference()
    
    print("\n🎉 Agent TTS instructions generated successfully!")
    print("📁 Files created:")
    print("   - agent_tts_instructions.md")
    print("   - tts_quick_reference.md")
    print("\n✅ Agents can now follow the instructions to generate Bengali TTS audio!")

if __name__ == "__main__":
    main()
