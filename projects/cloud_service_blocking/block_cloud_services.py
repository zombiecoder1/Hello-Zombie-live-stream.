#!/usr/bin/env python3
"""
Cloud Service Blocker
Best Practices Agent - Cloud Service Blocking Task
"""

import subprocess
import requests
import time
from datetime import datetime

class CloudServiceBlocker:
    def __init__(self):
        self.hosts_file = "/etc/hosts"
        self.services_to_block = [
            "api.openai.com",
            "api.anthropic.com", 
            "huggingface.co"
        ]
        self.blocking_entries = []
        
    def check_current_blocking(self):
        """Check current blocking status"""
        print("🔍 Checking current cloud service blocking status...")
        
        results = {}
        for service in self.services_to_block:
            try:
                response = requests.get(f"https://{service}", timeout=5)
                if response.status_code == 200:
                    results[service] = "ACCESSIBLE"
                else:
                    results[service] = f"BLOCKED (Status: {response.status_code})"
            except requests.exceptions.RequestException:
                results[service] = "BLOCKED"
            except Exception as e:
                results[service] = f"ERROR: {str(e)}"
                
        return results
    
    def create_blocking_entries(self):
        """Create blocking entries for hosts file"""
        entries = []
        for service in self.services_to_block:
            entries.append(f"127.0.0.1 {service}")
            entries.append(f"::1 {service}")
        return entries
    
    def backup_hosts_file(self):
        """Backup current hosts file"""
        try:
            subprocess.run(["sudo", "cp", self.hosts_file, f"{self.hosts_file}.backup"], check=True)
            return True, "Hosts file backed up successfully"
        except subprocess.CalledProcessError as e:
            return False, f"Failed to backup hosts file: {str(e)}"
    
    def add_blocking_entries(self):
        """Add blocking entries to hosts file"""
        try:
            # Read current hosts file
            with open(self.hosts_file, 'r') as f:
                content = f.read()
            
            # Check if entries already exist
            blocking_entries = self.create_blocking_entries()
            new_entries = []
            
            for entry in blocking_entries:
                if entry not in content:
                    new_entries.append(entry)
            
            if new_entries:
                # Add new entries
                with open(self.hosts_file, 'a') as f:
                    f.write("\n# ZombieCoder Cloud Service Blocking\n")
                    for entry in new_entries:
                        f.write(f"{entry}\n")
                    f.write("# End ZombieCoder Blocking\n")
                
                return True, f"Added {len(new_entries)} blocking entries"
            else:
                return True, "All blocking entries already exist"
                
        except Exception as e:
            return False, f"Failed to add blocking entries: {str(e)}"
    
    def verify_blocking(self):
        """Verify that blocking is working"""
        print("🔍 Verifying cloud service blocking...")
        
        results = {}
        for service in self.services_to_block:
            try:
                response = requests.get(f"https://{service}", timeout=5)
                if response.status_code == 200:
                    results[service] = "STILL_ACCESSIBLE"
                else:
                    results[service] = f"BLOCKED (Status: {response.status_code})"
            except requests.exceptions.RequestException:
                results[service] = "BLOCKED"
            except Exception as e:
                results[service] = f"ERROR: {str(e)}"
                
        return results
    
    def run_blocking(self):
        """Run complete cloud service blocking process"""
        print("🧟 Best Practices Agent - Cloud Service Blocking")
        print("=" * 50)
        
        # Check current status
        print("1. Checking current blocking status...")
        current_status = self.check_current_blocking()
        for service, status in current_status.items():
            print(f"   {service}: {'✅' if 'BLOCKED' in status else '❌'} {status}")
        
        # Backup hosts file
        print("2. Backing up hosts file...")
        backup_success, backup_message = self.backup_hosts_file()
        print(f"   Status: {'✅' if backup_success else '❌'} {backup_message}")
        
        if not backup_success:
            return False, backup_message
        
        # Add blocking entries
        print("3. Adding blocking entries...")
        add_success, add_message = self.add_blocking_entries()
        print(f"   Status: {'✅' if add_success else '❌'} {add_message}")
        
        if not add_success:
            return False, add_message
        
        # Wait a moment for changes to take effect
        print("4. Waiting for changes to take effect...")
        time.sleep(2)
        
        # Verify blocking
        print("5. Verifying blocking effectiveness...")
        verification_results = self.verify_blocking()
        for service, status in verification_results.items():
            print(f"   {service}: {'✅' if 'BLOCKED' in status else '❌'} {status}")
        
        # Count blocked services
        blocked_count = sum(1 for status in verification_results.values() if 'BLOCKED' in status)
        total_count = len(verification_results)
        
        print(f"6. Blocking Summary: {blocked_count}/{total_count} services blocked")
        
        if blocked_count == total_count:
            return True, f"Successfully blocked all {total_count} cloud services"
        else:
            return False, f"Only {blocked_count}/{total_count} services blocked"
    
    def save_results(self, filename="blocking_results.json"):
        """Save blocking results"""
        import json
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "services_blocked": self.services_to_block,
            "blocking_entries": self.create_blocking_entries(),
            "verification_results": self.verify_blocking()
        }
        
        try:
            with open(f"projects/cloud_service_blocking/{filename}", 'w') as f:
                json.dump(results, f, indent=2)
            return True, f"Results saved to {filename}"
        except Exception as e:
            return False, f"Error saving results: {str(e)}"

def main():
    """Main function"""
    blocker = CloudServiceBlocker()
    
    # Run blocking
    success, message = blocker.run_blocking()
    
    if success:
        # Save results
        save_success, save_message = blocker.save_results()
        print(f"\n💾 Save Results: {'✅' if save_success else '❌'} {save_message}")
        
        # Update work log
        with open("logs/agent_work.log", "a") as f:
            f.write(f"{datetime.now()}: Agent: Best Practices Agent - Task: Cloud Service Blocking - Status: Completed - Notes: {message}\n")
        
        print(f"\n🎉 {message}")
    else:
        print(f"\n❌ {message}")
        
        # Log error
        with open("logs/agent_error.log", "a") as f:
            f.write(f"{datetime.now()}: Agent: Best Practices Agent - Error: {message} - Severity: HIGH - Status: UNRESOLVED\n")

if __name__ == "__main__":
    main()
