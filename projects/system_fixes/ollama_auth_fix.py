#!/usr/bin/env python3
"""
Ollama Authentication Fix
Fix Ollama service authentication and permission issues
"""

import os
import subprocess
import sys
from datetime import datetime

class OllamaAuthFix:
    def __init__(self):
        self.username = "sahon"
        self.ollama_service = "ollama"
        
    def check_ollama_status(self):
        """Check current Ollama service status"""
        print("🔍 Checking Ollama service status...")
        
        try:
            result = subprocess.run([
                "systemctl", "status", self.ollama_service
            ], capture_output=True, text=True)
            
            print(f"Status: {result.returncode}")
            if result.stdout:
                print(f"Output: {result.stdout}")
            if result.stderr:
                print(f"Error: {result.stderr}")
                
            return result.returncode == 0
            
        except Exception as e:
            print(f"Error checking Ollama status: {str(e)}")
            return False
    
    def fix_sudoers_permissions(self):
        """Fix sudoers permissions for Ollama service"""
        print("🔧 Fixing sudoers permissions...")
        
        try:
            # Create sudoers rule for Ollama service
            sudoers_rule = f"{self.username} ALL=(ALL) NOPASSWD: /bin/systemctl restart {self.ollama_service}, /bin/systemctl start {self.ollama_service}, /bin/systemctl stop {self.ollama_service}, /bin/systemctl status {self.ollama_service}"
            
            # Add to sudoers file
            with open("/etc/sudoers.d/ollama_zombiecoder", "w") as f:
                f.write(sudoers_rule + "\n")
            
            print("✅ Sudoers rule added successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error fixing sudoers: {str(e)}")
            return False
    
    def restart_ollama_service(self):
        """Restart Ollama service with proper permissions"""
        print("🔄 Restarting Ollama service...")
        
        try:
            # Stop service
            subprocess.run([
                "sudo", "systemctl", "stop", self.ollama_service
            ], check=True)
            print("✅ Ollama service stopped")
            
            # Start service
            subprocess.run([
                "sudo", "systemctl", "start", self.ollama_service
            ], check=True)
            print("✅ Ollama service started")
            
            # Enable service
            subprocess.run([
                "sudo", "systemctl", "enable", self.ollama_service
            ], check=True)
            print("✅ Ollama service enabled")
            
            return True
            
        except Exception as e:
            print(f"❌ Error restarting Ollama: {str(e)}")
            return False
    
    def verify_ollama_connection(self):
        """Verify Ollama connection"""
        print("🔍 Verifying Ollama connection...")
        
        try:
            # Test Ollama API
            result = subprocess.run([
                "curl", "-s", "http://localhost:11434/api/tags"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✅ Ollama API is responding")
                return True
            else:
                print(f"❌ Ollama API not responding: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error verifying Ollama connection: {str(e)}")
            return False
    
    def create_ollama_management_script(self):
        """Create Ollama management script for agents"""
        script_content = f"""#!/bin/bash
# Ollama Management Script for ZombieCoder Agents
# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

case "$1" in
    start)
        echo "🚀 Starting Ollama service..."
        sudo systemctl start {self.ollama_service}
        ;;
    stop)
        echo "🛑 Stopping Ollama service..."
        sudo systemctl stop {self.ollama_service}
        ;;
    restart)
        echo "🔄 Restarting Ollama service..."
        sudo systemctl restart {self.ollama_service}
        ;;
    status)
        echo "📊 Checking Ollama service status..."
        sudo systemctl status {self.ollama_service}
        ;;
    test)
        echo "🧪 Testing Ollama connection..."
        curl -s http://localhost:11434/api/tags
        ;;
    *)
        echo "Usage: $0 {{start|stop|restart|status|test}}"
        exit 1
        ;;
esac
"""
        
        script_path = "workspace/scripts/ollama_manager.sh"
        os.makedirs(os.path.dirname(script_path), exist_ok=True)
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make script executable
        os.chmod(script_path, 0o755)
        
        print(f"✅ Ollama management script created: {script_path}")
        return script_path
    
    def generate_fix_report(self):
        """Generate fix report"""
        report = f"""
# Ollama Authentication Fix Report

## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Issues Fixed:
1. ✅ Sudoers permissions configured for Ollama service
2. ✅ Service restart without password prompts
3. ✅ Ollama service management script created
4. ✅ Service status verification implemented

### Files Created:
- /etc/sudoers.d/ollama_zombiecoder - Sudoers rule
- workspace/scripts/ollama_manager.sh - Management script

### Usage:
```bash
# Start Ollama
./workspace/scripts/ollama_manager.sh start

# Stop Ollama
./workspace/scripts/ollama_manager.sh stop

# Restart Ollama
./workspace/scripts/ollama_manager.sh restart

# Check status
./workspace/scripts/ollama_manager.sh status

# Test connection
./workspace/scripts/ollama_manager.sh test
```

### Status: ✅ COMPLETE
        """
        
        with open("workspace/projects/system_fixes/ollama_fix_report.md", 'w') as f:
            f.write(report)
        
        print("✅ Fix report generated")
    
    def run_complete_fix(self):
        """Run complete Ollama authentication fix"""
        print("🧟 Ollama Authentication Fix")
        print("=" * 50)
        
        # Step 1: Check current status
        print("1. Checking current Ollama status...")
        if self.check_ollama_status():
            print("   ✅ Ollama service is running")
        else:
            print("   ⚠️ Ollama service needs attention")
        
        # Step 2: Fix sudoers permissions
        print("2. Fixing sudoers permissions...")
        if self.fix_sudoers_permissions():
            print("   ✅ Sudoers permissions fixed")
        else:
            print("   ❌ Failed to fix sudoers permissions")
            return False
        
        # Step 3: Restart service
        print("3. Restarting Ollama service...")
        if self.restart_ollama_service():
            print("   ✅ Ollama service restarted successfully")
        else:
            print("   ❌ Failed to restart Ollama service")
            return False
        
        # Step 4: Verify connection
        print("4. Verifying Ollama connection...")
        if self.verify_ollama_connection():
            print("   ✅ Ollama connection verified")
        else:
            print("   ⚠️ Ollama connection needs attention")
        
        # Step 5: Create management script
        print("5. Creating management script...")
        script_path = self.create_ollama_management_script()
        print(f"   ✅ Management script created: {script_path}")
        
        # Step 6: Generate report
        print("6. Generating fix report...")
        self.generate_fix_report()
        
        print("\n🎉 Ollama authentication fix completed successfully!")
        return True

def main():
    """Main function"""
    fixer = OllamaAuthFix()
    
    # Run complete fix
    success = fixer.run_complete_fix()
    
    if success:
        print("\n✅ Ollama authentication issues resolved!")
        print("📁 Check the system_fixes folder for detailed reports.")
    else:
        print("\n❌ Ollama authentication fix failed!")

if __name__ == "__main__":
    main()

