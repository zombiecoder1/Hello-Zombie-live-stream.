#!/usr/bin/env python3
"""
Bengali TTS Audio Documentation Generator
ZombieCoder System - Complete Bengali Documentation
"""

import os
import sys
from datetime import datetime
from gtts import gTTS
import subprocess

class BengaliTTSGenerator:
    def __init__(self):
        self.output_dir = "audio_documentation"
        self.audio_file = "zombiecoder_complete_documentation_bengali.mp3"
        self.text_file = "zombiecoder_complete_documentation_bengali.txt"
        
    def read_documentation_text(self):
        """Read the Bengali documentation text"""
        try:
            with open(f"{self.output_dir}/{self.text_file}", 'r', encoding='utf-8') as f:
                text = f.read()
            print(f"✅ Documentation text loaded: {self.text_file}")
            return text
        except Exception as e:
            print(f"❌ Error reading documentation text: {str(e)}")
            return None
    
    def generate_audio(self, text):
        """Generate audio from text using Google TTS with Bengali language"""
        try:
            print("🎧 Generating Bengali audio with Google TTS...")
            
            # Create TTS object with Bengali language
            tts = gTTS(text=text, lang='bn', slow=False)
            
            # Save audio file
            audio_path = f"{self.output_dir}/{self.audio_file}"
            tts.save(audio_path)
            
            print(f"✅ Bengali audio generated successfully: {self.audio_file}")
            return audio_path
            
        except Exception as e:
            print(f"❌ Error generating Bengali audio: {str(e)}")
            return None
    
    def get_audio_duration(self, audio_path):
        """Get audio duration using ffprobe"""
        try:
            result = subprocess.run([
                'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
                '-of', 'csv=p=0', audio_path
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                return duration
            else:
                return None
                
        except Exception as e:
            print(f"Error getting audio duration: {str(e)}")
            return None
    
    def create_audio_metadata(self, audio_path, duration):
        """Create metadata file for audio"""
        metadata = {
            "title": "জম্বিকোডার সিস্টেম - সম্পূর্ণ ডকুমেন্টেশন",
            "description": "বাংলা ভাষায় সম্পূর্ণ সিস্টেম ডকুমেন্টেশন",
            "duration_seconds": duration,
            "duration_formatted": f"{int(duration//60)}:{int(duration%60):02d}",
            "generated_at": datetime.now().isoformat(),
            "file_size_mb": round(os.path.getsize(audio_path) / (1024*1024), 2),
            "language": "bn",
            "tts_engine": "Google TTS",
            "chapters": 14,
            "total_words": len(self.read_documentation_text().split()) if self.read_documentation_text() else 0
        }
        
        import json
        with open(f"{self.output_dir}/bengali_audio_metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Bengali audio metadata created")
        return metadata
    
    def generate_completion_report(self, metadata):
        """Generate completion report in Bengali"""
        report = f"""
# জম্বিকোডার বাংলা TTS ডকুমেন্টেশন রিপোর্ট

## উৎপাদনের তারিখ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### অডিও বিবরণ:
- **ফাইল**: {self.audio_file}
- **সময়কাল**: {metadata['duration_formatted']}
- **আকার**: {metadata['file_size_mb']} MB
- **ভাষা**: {metadata['language']}
- **TTS ইঞ্জিন**: {metadata['tts_engine']}
- **অধ্যায় সংখ্যা**: {metadata['chapters']}
- **মোট শব্দ**: {metadata['total_words']}

### বিষয়বস্তু কভারেজ:
- সিস্টেম পরিচিতি
- এজেন্ট সিস্টেম
- সিস্টেম আর্কিটেকচার
- অটোমেশন সিস্টেম
- বাস্তব প্রয়োগ
- জিরো টলারেন্স রুল
- বর্তমান সিস্টেম স্ট্যাটাস
- প্রযুক্তিগত অর্জন
- ভবিষ্যতের উন্নতি
- ব্যবহারের নির্দেশনা
- সমস্যা সমাধান
- সফলতার মেট্রিক্স
- জম্বি টিম স্পিরিট
- উপসংহার

### ব্যবহারের নির্দেশনা:
1. অডিও ফাইল চালিয়ে সম্পূর্ণ সিস্টেম বুঝুন
2. নতুন টিম সদস্যদের প্রশিক্ষণ উপকরণ হিসেবে ব্যবহার করুন
3. সিস্টেম আর্কিটেকচার আলোচনার জন্য রেফারেন্স
4. স্টেকহোল্ডার এবং ক্লায়েন্টদের জন্য ডকুমেন্টেশন

### উৎপাদিত ফাইল:
- {self.audio_file} - মূল অডিও ডকুমেন্টেশন
- {self.text_file} - উৎস টেক্সট ফাইল
- bengali_audio_metadata.json - অডিও মেটাডেটা
- bengali_tts_report.md - এই রিপোর্ট

## স্ট্যাটাস: ✅ সম্পূর্ণ
        """
        
        with open(f"{self.output_dir}/bengali_tts_report.md", 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("✅ বাংলা সম্পূর্ণতা রিপোর্ট তৈরি হয়েছে")
    
    def generate_complete_documentation(self):
        """Generate complete Bengali audio documentation"""
        print("🧟 জম্বিকোডার বাংলা TTS অডিও ডকুমেন্টেশন জেনারেটর")
        print("=" * 60)
        
        # Step 1: Read documentation text
        print("1. ডকুমেন্টেশন টেক্সট পড়া হচ্ছে...")
        text = self.read_documentation_text()
        
        if not text:
            print("❌ ডকুমেন্টেশন টেক্সট পড়তে পারিনি")
            return False
        
        # Step 2: Generate audio
        print("2. Google TTS দিয়ে বাংলা অডিও তৈরি করা হচ্ছে...")
        audio_path = self.generate_audio(text)
        
        if audio_path:
            # Step 3: Get audio duration
            print("3. অডিও সময়কাল জানা হচ্ছে...")
            duration = self.get_audio_duration(audio_path)
            
            if duration:
                print(f"   📊 অডিও সময়কাল: {int(duration//60)}:{int(duration%60):02d}")
                
                # Step 4: Create metadata
                print("4. অডিও মেটাডেটা তৈরি করা হচ্ছে...")
                metadata = self.create_audio_metadata(audio_path, duration)
                
                # Step 5: Generate report
                print("5. সম্পূর্ণতা রিপোর্ট তৈরি করা হচ্ছে...")
                self.generate_completion_report(metadata)
                
                print(f"\n🎉 বাংলা অডিও ডকুমেন্টেশন সফলভাবে তৈরি হয়েছে!")
                print(f"📁 আউটপুট ডিরেক্টরি: {self.output_dir}")
                print(f"🎵 অডিও ফাইল: {self.audio_file}")
                print(f"⏱️ সময়কাল: {metadata['duration_formatted']}")
                print(f"📊 ফাইল আকার: {metadata['file_size_mb']} MB")
                print(f"📝 মোট শব্দ: {metadata['total_words']}")
                
                return True
            else:
                print("❌ অডিও সময়কাল নির্ধারণ করতে পারিনি")
                return False
        else:
            print("❌ অডিও তৈরি ব্যর্থ")
            return False

def main():
    """Main function"""
    generator = BengaliTTSGenerator()
    
    # Check if gTTS is installed
    try:
        import gtts
        print("✅ Google TTS লাইব্রেরি পাওয়া গেছে")
    except ImportError:
        print("❌ Google TTS লাইব্রেরি পাওয়া যায়নি। ইনস্টল করা হচ্ছে...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'gtts', '--break-system-packages'], check=True)
        print("✅ Google TTS লাইব্রেরি ইনস্টল হয়েছে")
    
    # Generate complete documentation
    success = generator.generate_complete_documentation()
    
    if success:
        print("\n🎉 বাংলা অডিও ডকুমেন্টেশন জেনারেশন সফলভাবে সম্পন্ন হয়েছে!")
        print("📁 'audio_documentation' ফোল্ডার চেক করুন সব উৎপাদিত ফাইলের জন্য।")
    else:
        print("\n❌ বাংলা অডিও ডকুমেন্টেশন জেনারেশন ব্যর্থ!")

if __name__ == "__main__":
    main()
