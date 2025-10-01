#!/usr/bin/env python3
"""
Simple Bengali TTS Generator
ZombieCoder System - Summary Documentation
"""

import os
from datetime import datetime
from gtts import gTTS

def generate_bengali_audio():
    """Generate Bengali audio from summary text"""
    
    # Read the summary text
    try:
        with open('zombiecoder_summary_bengali.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        print("✅ Summary text loaded successfully")
    except Exception as e:
        print(f"❌ Error reading text: {str(e)}")
        return False
    
    try:
        print("🎧 Generating Bengali audio with Google TTS...")
        
        # Create TTS object with Bengali language
        tts = gTTS(text=text, lang='bn', slow=False)
        
        # Save audio file
        audio_file = "zombiecoder_summary_bengali.mp3"
        tts.save(audio_file)
        
        print(f"✅ Bengali audio generated successfully: {audio_file}")
        
        # Get file size
        file_size = os.path.getsize(audio_file) / (1024*1024)
        print(f"📊 File size: {file_size:.2f} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating audio: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧟 জম্বিকোডার বাংলা TTS জেনারেটর")
    print("=" * 40)
    
    success = generate_bengali_audio()
    
    if success:
        print("\n🎉 বাংলা অডিও সফলভাবে তৈরি হয়েছে!")
        print("📁 বর্তমান ফোল্ডারে MP3 ফাইল দেখুন।")
    else:
        print("\n❌ অডিও তৈরি ব্যর্থ!")
