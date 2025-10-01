#!/usr/bin/env python3
"""
Improved Audio Documentation Generator for ZombieCoder
Bengali TTS with symbol cleaning and real-life workflow
"""

from gtts import gTTS
import time
import os
import re
from datetime import datetime

class ImprovedAudioGenerator:
    def __init__(self):
        self.doc_file = "workspace/docs/project_doc.txt"
        self.audio_file = "workspace/docs/project_doc.mp3"
        self.max_chars = 4000
        self.language = 'bn'  # Bengali
        
    def clean_text(self, text):
        """Clean text by removing symbols, emojis, and unwanted characters"""
        print("🧹 Cleaning text from symbols and emojis...")
        
        # Remove emojis and symbols
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        
        # Clean text
        clean_text = emoji_pattern.sub('', text)
        clean_text = clean_text.replace('#', '')
        clean_text = clean_text.replace('..', '')
        clean_text = clean_text.replace('🧟‍♂️', '')
        clean_text = clean_text.replace('🎯', '')
        clean_text = clean_text.replace('✅', '')
        clean_text = clean_text.replace('❌', '')
        clean_text = clean_text.replace('⚠️', '')
        clean_text = clean_text.replace('🔧', '')
        clean_text = clean_text.replace('📊', '')
        clean_text = clean_text.replace('🚀', '')
        clean_text = clean_text.replace('🎉', '')
        clean_text = clean_text.replace('🎵', '')
        clean_text = clean_text.replace('🧹', '')
        clean_text = clean_text.replace('🔍', '')
        clean_text = clean_text.replace('📁', '')
        clean_text = clean_text.replace('⏱️', '')
        clean_text = clean_text.replace('🌐', '')
        clean_text = clean_text.replace('📝', '')
        clean_text = clean_text.replace('🔗', '')
        clean_text = clean_text.replace('🎧', '')
        clean_text = clean_text.replace('📖', '')
        
        # Remove extra whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text)
        clean_text = clean_text.strip()
        
        print(f"✅ Text cleaned: {len(text)} -> {len(clean_text)} characters")
        return clean_text
    
    def load_and_clean_documentation(self):
        """Load and clean project documentation"""
        print(f"📖 Loading documentation from: {self.doc_file}")
        
        if not os.path.exists(self.doc_file):
            print(f"❌ Documentation file not found: {self.doc_file}")
            return None
        
        with open(self.doc_file, "r", encoding="utf-8") as f:
            text_content = f.read()
        
        # Clean the text
        clean_text = self.clean_text(text_content)
        
        print(f"✅ Documentation loaded and cleaned: {len(clean_text)} characters")
        return clean_text
    
    def split_text_into_chunks(self, text):
        """Split text into chunks for TTS processing"""
        print(f"📝 Splitting text into chunks (max {self.max_chars} chars per chunk)...")
        
        # Split by sentences first to avoid breaking words
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk + sentence) < self.max_chars:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        print(f"✅ Text split into {len(chunks)} chunks")
        return chunks
    
    def generate_tts_chunks(self, chunks):
        """Generate TTS audio for each chunk"""
        print(f"🎧 Generating Bengali TTS audio for {len(chunks)} chunks...")
        
        audio_parts = []
        
        for idx, chunk in enumerate(chunks):
            print(f"   Processing chunk {idx+1}/{len(chunks)}...")
            
            try:
                tts = gTTS(text=chunk, lang=self.language, slow=False)
                part_file = f"workspace/docs/part_{idx+1}.mp3"
                tts.save(part_file)
                audio_parts.append(part_file)
                print(f"   ✅ Chunk {idx+1} saved: {part_file}")
                
                # Small delay to avoid rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"   ❌ Error processing chunk {idx+1}: {str(e)}")
                continue
        
        print(f"✅ Generated {len(audio_parts)} audio parts")
        return audio_parts
    
    def merge_audio_parts(self, audio_parts):
        """Merge audio parts into final MP3"""
        print(f"🔗 Merging {len(audio_parts)} audio parts...")
        
        try:
            from pydub import AudioSegment
            
            combined = AudioSegment.empty()
            
            for part in audio_parts:
                if os.path.exists(part):
                    audio_segment = AudioSegment.from_mp3(part)
                    combined += audio_segment
                    print(f"   ✅ Added: {part}")
                else:
                    print(f"   ⚠️ Part not found: {part}")
            
            # Export final audio
            combined.export(self.audio_file, format="mp3")
            print(f"✅ Final audio saved: {self.audio_file}")
            
            # Get audio duration
            duration_seconds = len(combined) / 1000
            duration_minutes = duration_seconds / 60
            print(f"📊 Audio duration: {duration_minutes:.1f} minutes")
            
            return True, duration_minutes
            
        except Exception as e:
            print(f"❌ Error merging audio parts: {str(e)}")
            return False, 0
    
    def cleanup_temp_files(self, audio_parts):
        """Clean up temporary audio files"""
        print("🧹 Cleaning up temporary files...")
        
        for part in audio_parts:
            try:
                if os.path.exists(part):
                    os.remove(part)
                    print(f"   ✅ Removed: {part}")
            except Exception as e:
                print(f"   ⚠️ Could not remove {part}: {str(e)}")
    
    def generate_metadata(self, duration_minutes):
        """Generate metadata for the audio file"""
        metadata = {
            "title": "ZombieCoder System Documentation",
            "description": "Bengali TTS audio documentation with real-life workflow",
            "duration_minutes": round(duration_minutes, 1),
            "language": "Bengali",
            "generated_at": datetime.now().isoformat(),
            "file_size_mb": round(os.path.getsize(self.audio_file) / (1024*1024), 2),
            "tts_engine": "Google TTS",
            "text_cleaned": True,
            "chunks_processed": len([f for f in os.listdir("workspace/docs/") if f.startswith("part_") and f.endswith(".mp3")]) if os.path.exists("workspace/docs/") else 0
        }
        
        import json
        with open("workspace/docs/audio_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("✅ Audio metadata generated")
        return metadata
    
    def play_audio(self):
        """Play the generated audio file"""
        print("🎵 Playing generated audio...")
        
        try:
            if os.name == 'nt':  # Windows
                os.startfile(self.audio_file)
            elif os.name == 'posix':  # Linux / Mac
                # Try different audio players
                players = ['mpg123', 'mpv', 'vlc', 'play']
                for player in players:
                    if os.system(f"which {player} > /dev/null 2>&1") == 0:
                        os.system(f"{player} {self.audio_file} &")
                        print(f"✅ Playing with {player}")
                        return
                print("⚠️ No audio player found. Install mpg123, mpv, or vlc")
        except Exception as e:
            print(f"⚠️ Could not auto-play audio: {str(e)}")
    
    def generate_complete_audio(self):
        """Generate complete audio documentation"""
        print("🧟 ZombieCoder Improved Audio Documentation Generator")
        print("=" * 60)
        print(f"Language: Bengali")
        print(f"Max chars per chunk: {self.max_chars}")
        print(f"Text cleaning: Enabled")
        print("")
        
        # Step 1: Load and clean documentation
        clean_text = self.load_and_clean_documentation()
        if not clean_text:
            return False
        
        print("")
        
        # Step 2: Split into chunks
        chunks = self.split_text_into_chunks(clean_text)
        print("")
        
        # Step 3: Generate TTS for each chunk
        audio_parts = self.generate_tts_chunks(chunks)
        print("")
        
        # Step 4: Merge audio parts
        success, duration_minutes = self.merge_audio_parts(audio_parts)
        if success:
            print("")
            
            # Step 5: Generate metadata
            metadata = self.generate_metadata(duration_minutes)
            print("")
            
            # Step 6: Cleanup temp files
            self.cleanup_temp_files(audio_parts)
            print("")
            
            # Step 7: Play audio (optional)
            self.play_audio()
            print("")
            
            # Final report
            print("🎉 Bengali TTS audio documentation generation completed successfully!")
            print(f"📁 Output file: {self.audio_file}")
            print(f"⏱️ Duration: {metadata['duration_minutes']} minutes")
            print(f"📊 File size: {metadata['file_size_mb']} MB")
            print(f"🌐 Language: {metadata['language']}")
            print(f"🧹 Text cleaned: {metadata['text_cleaned']}")
            
            return True
        else:
            print("❌ Audio merging failed")
            return False

def main():
    """Main function"""
    generator = ImprovedAudioGenerator()
    
    # Generate complete audio documentation
    success = generator.generate_complete_audio()
    
    if success:
        print("\n✅ Bengali TTS audio documentation generation completed!")
        print("📁 Check the workspace/docs/ folder for generated files.")
        print("🎵 Audio ready for playback!")
    else:
        print("\n❌ Audio documentation generation failed!")

if __name__ == "__main__":
    main()
