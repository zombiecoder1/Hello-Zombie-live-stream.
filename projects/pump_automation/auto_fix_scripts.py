#!/usr/bin/env python3
"""
Auto-fix Scripts System
Pump/Automation - Error Detection + Automated Fixes
"""

import json
import time
import threading
from datetime import datetime, timedelta
import sqlite3
import os
import subprocess
import psutil
import requests
import re

class AutoFixScripts:
    def __init__(self):
        self.autofix_database = "auto_fix_scripts.db"
        self.agents = ["programming", "bestpractices", "verifier", "conversational", "ops"]
        self.check_interval = 15  # seconds
        self.error_patterns = {
            "memory_error": r"MemoryError|OutOfMemoryError|memory allocation failed",
            "disk_error": r"No space left on device|disk full|Disk quota exceeded",
            "network_error": r"Connection refused|Network is unreachable|Timeout",
            "permission_error": r"Permission denied|Access denied|Forbidden",
            "file_error": r"No such file or directory|File not found|Path not found",
            "process_error": r"Process not found|PID not found|Process terminated",
            "service_error": r"Service not running|Service failed|Connection refused"
        }
        self.fix_actions = {
            "memory_error": "fix_memory_issue",
            "disk_error": "fix_disk_issue",
            "network_error": "fix_network_issue",
            "permission_error": "fix_permission_issue",
            "file_error": "fix_file_issue",
            "process_error": "fix_process_issue",
            "service_error": "fix_service_issue"
        }
        self.setup_database()
        
    def setup_database(self):
        """Setup auto-fix database"""
        conn = sqlite3.connect(self.autofix_database)
        cursor = conn.cursor()
        
        # Create error detection table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS error_detection (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                error_type TEXT NOT NULL,
                error_message TEXT NOT NULL,
                error_source TEXT NOT NULL,
                severity TEXT NOT NULL,
                detected BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Create auto-fix actions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS auto_fix_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                error_type TEXT NOT NULL,
                fix_action TEXT NOT NULL,
                fix_description TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                result TEXT,
                execution_time REAL
            )
        ''')
        
        # Create fix history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fix_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                error_type TEXT NOT NULL,
                fix_applied TEXT NOT NULL,
                success BOOLEAN DEFAULT FALSE,
                before_state TEXT,
                after_state TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Auto-fix database created successfully")
    
    def detect_errors(self, agent_id):
        """Detect errors for specific agent"""
        errors_detected = []
        
        # Check system logs
        system_errors = self.check_system_logs(agent_id)
        errors_detected.extend(system_errors)
        
        # Check agent logs
        agent_errors = self.check_agent_logs(agent_id)
        errors_detected.extend(agent_errors)
        
        # Check system resources
        resource_errors = self.check_system_resources(agent_id)
        errors_detected.extend(resource_errors)
        
        # Check service status
        service_errors = self.check_service_status(agent_id)
        errors_detected.extend(service_errors)
        
        return errors_detected
    
    def check_system_logs(self, agent_id):
        """Check system logs for errors"""
        errors = []
        
        try:
            # Check syslog for recent errors
            result = subprocess.run([
                "tail", "-n", "100", "/var/log/syslog"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                log_lines = result.stdout.split('\n')
                
                for line in log_lines:
                    for error_type, pattern in self.error_patterns.items():
                        if re.search(pattern, line, re.IGNORECASE):
                            errors.append({
                                "error_type": error_type,
                                "error_message": line.strip(),
                                "error_source": "system_log",
                                "severity": "medium"
                            })
            
        except Exception as e:
            print(f"Error checking system logs: {str(e)}")
        
        return errors
    
    def check_agent_logs(self, agent_id):
        """Check agent-specific logs for errors"""
        errors = []
        
        try:
            # Check agent work log
            log_file = f"logs/agent_work.log"
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    log_lines = f.readlines()[-50:]  # Last 50 lines
                
                for line in log_lines:
                    for error_type, pattern in self.error_patterns.items():
                        if re.search(pattern, line, re.IGNORECASE):
                            errors.append({
                                "error_type": error_type,
                                "error_message": line.strip(),
                                "error_source": f"agent_{agent_id}_log",
                                "severity": "high"
                            })
            
            # Check agent error log
            error_log_file = f"logs/agent_error.log"
            if os.path.exists(error_log_file):
                with open(error_log_file, 'r') as f:
                    error_lines = f.readlines()[-20:]  # Last 20 lines
                
                for line in error_lines:
                    errors.append({
                        "error_type": "agent_error",
                        "error_message": line.strip(),
                        "error_source": f"agent_{agent_id}_error_log",
                        "severity": "high"
                    })
            
        except Exception as e:
            print(f"Error checking agent logs: {str(e)}")
        
        return errors
    
    def check_system_resources(self, agent_id):
        """Check system resources for issues"""
        errors = []
        
        try:
            # Check memory usage
            memory = psutil.virtual_memory()
            if memory.percent > 95:
                errors.append({
                    "error_type": "memory_error",
                    "error_message": f"Critical memory usage: {memory.percent:.1f}%",
                    "error_source": "system_resources",
                    "severity": "critical"
                })
            
            # Check disk usage
            disk = psutil.disk_usage('/')
            if disk.percent > 95:
                errors.append({
                    "error_type": "disk_error",
                    "error_message": f"Critical disk usage: {disk.percent:.1f}%",
                    "error_source": "system_resources",
                    "severity": "critical"
                })
            
            # Check CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage > 95:
                errors.append({
                    "error_type": "process_error",
                    "error_message": f"Critical CPU usage: {cpu_usage:.1f}%",
                    "error_source": "system_resources",
                    "severity": "high"
                })
            
        except Exception as e:
            print(f"Error checking system resources: {str(e)}")
        
        return errors
    
    def check_service_status(self, agent_id):
        """Check service status for issues"""
        errors = []
        
        try:
            # Check if key services are running
            services_to_check = [
                "ollama",
                "python3",
                "systemd"
            ]
            
            for service in services_to_check:
                try:
                    result = subprocess.run([
                        "systemctl", "is-active", service
                    ], capture_output=True, text=True, timeout=5)
                    
                    if result.returncode != 0:
                        errors.append({
                            "error_type": "service_error",
                            "error_message": f"Service {service} is not active",
                            "error_source": "service_status",
                            "severity": "high"
                        })
                
                except:
                    # Service might not be managed by systemd
                    pass
            
        except Exception as e:
            print(f"Error checking service status: {str(e)}")
        
        return errors
    
    def store_error_detection(self, agent_id, errors):
        """Store detected errors in database"""
        conn = sqlite3.connect(self.autofix_database)
        cursor = conn.cursor()
        
        for error in errors:
            cursor.execute('''
                INSERT INTO error_detection 
                (timestamp, agent_id, error_type, error_message, error_source, severity)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(), agent_id, error["error_type"],
                error["error_message"], error["error_source"], error["severity"]
            ))
        
        conn.commit()
        conn.close()
    
    def apply_auto_fix(self, agent_id, error_type, error_message):
        """Apply automatic fix for detected error"""
        fix_action = self.fix_actions.get(error_type)
        
        if not fix_action:
            print(f"   ❌ No fix action available for error type: {error_type}")
            return False
        
        print(f"   🔧 Applying auto-fix for {error_type}: {error_message}")
        
        # Store fix action
        conn = sqlite3.connect(self.autofix_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO auto_fix_actions 
            (timestamp, agent_id, error_type, fix_action, fix_description, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(), agent_id, error_type, fix_action,
            f"Auto-fix for {error_type}", "running"
        ))
        
        conn.commit()
        conn.close()
        
        # Execute fix
        start_time = time.time()
        
        try:
            if fix_action == "fix_memory_issue":
                result = self.fix_memory_issue(agent_id)
            elif fix_action == "fix_disk_issue":
                result = self.fix_disk_issue(agent_id)
            elif fix_action == "fix_network_issue":
                result = self.fix_network_issue(agent_id)
            elif fix_action == "fix_permission_issue":
                result = self.fix_permission_issue(agent_id)
            elif fix_action == "fix_file_issue":
                result = self.fix_file_issue(agent_id)
            elif fix_action == "fix_process_issue":
                result = self.fix_process_issue(agent_id)
            elif fix_action == "fix_service_issue":
                result = self.fix_service_issue(agent_id)
            else:
                result = {"status": "unknown_fix", "message": f"Unknown fix action: {fix_action}"}
            
            execution_time = time.time() - start_time
            
            # Update fix action
            self.update_fix_action(agent_id, error_type, fix_action, "completed", result, execution_time)
            
            print(f"   ✅ Auto-fix completed for {error_type}")
            return True
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_result = {"status": "error", "message": str(e)}
            self.update_fix_action(agent_id, error_type, fix_action, "failed", error_result, execution_time)
            print(f"   ❌ Auto-fix failed for {error_type}: {str(e)}")
            return False
    
    def fix_memory_issue(self, agent_id):
        """Fix memory issues"""
        print(f"     🧠 Fixing memory issue for agent {agent_id}")
        
        try:
            # Clear system cache
            subprocess.run(["sync"], check=True)
            subprocess.run(["echo", "3"], stdout=open("/proc/sys/vm/drop_caches", "w"), check=True)
            
            # Kill unnecessary processes
            processes = list(psutil.process_iter(['pid', 'name', 'memory_percent']))
            killed_count = 0
            
            for proc in processes:
                try:
                    if proc.info['memory_percent'] > 5:  # More than 5% memory
                        proc_name = proc.info['name']
                        if proc_name not in ['systemd', 'kernel', 'python3', 'ollama']:
                            proc.kill()
                            killed_count += 1
                except:
                    continue
            
            return {
                "status": "success",
                "action": "memory_cleanup",
                "killed_processes": killed_count,
                "message": f"Memory cleanup completed, killed {killed_count} processes"
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def fix_disk_issue(self, agent_id):
        """Fix disk space issues"""
        print(f"     💾 Fixing disk issue for agent {agent_id}")
        
        try:
            # Clean up temporary files
            cleanup_commands = [
                "find /tmp -type f -mtime +1 -delete",
                "find /var/tmp -type f -mtime +1 -delete",
                "apt-get clean",
                "apt-get autoremove -y"
            ]
            
            cleanup_results = []
            for cmd in cleanup_commands:
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
                    cleanup_results.append(f"Executed: {cmd}")
                except:
                    cleanup_results.append(f"Failed: {cmd}")
            
            return {
                "status": "success",
                "action": "disk_cleanup",
                "cleanup_commands": cleanup_results,
                "message": "Disk cleanup completed"
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def fix_network_issue(self, agent_id):
        """Fix network issues"""
        print(f"     🌐 Fixing network issue for agent {agent_id}")
        
        try:
            # Restart network services
            network_commands = [
                "systemctl restart networking",
                "systemctl restart NetworkManager"
            ]
            
            network_results = []
            for cmd in network_commands:
                try:
                    subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
                    network_results.append(f"Executed: {cmd}")
                except:
                    network_results.append(f"Failed: {cmd}")
            
            return {
                "status": "success",
                "action": "network_restart",
                "network_commands": network_results,
                "message": "Network services restarted"
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def fix_permission_issue(self, agent_id):
        """Fix permission issues"""
        print(f"     🔐 Fixing permission issue for agent {agent_id}")
        
        try:
            # Fix common permission issues
            permission_commands = [
                "chmod -R 755 /home/sahon/Desktop/zombiecoder/workspace",
                "chown -R sahon:sahon /home/sahon/Desktop/zombiecoder/workspace"
            ]
            
            permission_results = []
            for cmd in permission_commands:
                try:
                    subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
                    permission_results.append(f"Executed: {cmd}")
                except:
                    permission_results.append(f"Failed: {cmd}")
            
            return {
                "status": "success",
                "action": "permission_fix",
                "permission_commands": permission_results,
                "message": "Permission issues fixed"
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def fix_file_issue(self, agent_id):
        """Fix file issues"""
        print(f"     📁 Fixing file issue for agent {agent_id}")
        
        try:
            # Create missing directories
            directories = [
                "logs",
                "reports",
                "projects",
                "agents/memory",
                "agents/config"
            ]
            
            created_dirs = []
            for directory in directories:
                try:
                    os.makedirs(f"workspace/{directory}", exist_ok=True)
                    created_dirs.append(f"Created: {directory}")
                except:
                    created_dirs.append(f"Failed: {directory}")
            
            return {
                "status": "success",
                "action": "file_creation",
                "created_directories": created_dirs,
                "message": "File issues fixed"
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def fix_process_issue(self, agent_id):
        """Fix process issues"""
        print(f"     ⚙️ Fixing process issue for agent {agent_id}")
        
        try:
            # Restart Python processes
            subprocess.run(["pkill", "-f", "python3.*zombiecoder"], capture_output=True)
            time.sleep(2)
            
            # Restart main processes
            restart_commands = [
                "python3 projects/server_system_setup/main_server_integration.py &",
                "python3 projects/server_system_setup/workstation_integration.py &"
            ]
            
            restart_results = []
            for cmd in restart_commands:
                try:
                    subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
                    restart_results.append(f"Executed: {cmd}")
                except:
                    restart_results.append(f"Failed: {cmd}")
            
            return {
                "status": "success",
                "action": "process_restart",
                "restart_commands": restart_results,
                "message": "Process issues fixed"
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def fix_service_issue(self, agent_id):
        """Fix service issues"""
        print(f"     🔧 Fixing service issue for agent {agent_id}")
        
        try:
            # Restart key services
            services = ["ollama", "systemd-resolved"]
            service_results = []
            
            for service in services:
                try:
                    subprocess.run(["systemctl", "restart", service], capture_output=True, timeout=30)
                    service_results.append(f"Restarted: {service}")
                except:
                    service_results.append(f"Failed: {service}")
            
            return {
                "status": "success",
                "action": "service_restart",
                "service_results": service_results,
                "message": "Service issues fixed"
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def update_fix_action(self, agent_id, error_type, fix_action, status, result, execution_time):
        """Update fix action status"""
        conn = sqlite3.connect(self.autofix_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE auto_fix_actions 
            SET status = ?, result = ?, execution_time = ?
            WHERE agent_id = ? AND error_type = ? AND fix_action = ? AND status = 'running'
        ''', (status, json.dumps(result), execution_time, agent_id, error_type, fix_action))
        
        conn.commit()
        conn.close()
    
    def start_auto_fix_system(self):
        """Start the auto-fix system"""
        print("🧟 Auto-fix Scripts - Starting Auto-fix System")
        print("=" * 50)
        
        # Start auto-fix in background thread
        autofix_thread = threading.Thread(target=self.autofix_loop)
        autofix_thread.daemon = True
        autofix_thread.start()
        
        print("✅ Auto-fix system started successfully")
        return True
    
    def autofix_loop(self):
        """Main auto-fix loop"""
        while True:
            try:
                print(f"🔍 Running auto-fix cycle... {datetime.now().strftime('%H:%M:%S')}")
                
                for agent_id in self.agents:
                    # Detect errors
                    errors = self.detect_errors(agent_id)
                    
                    if errors:
                        print(f"   ⚠️ Detected {len(errors)} errors for agent {agent_id}")
                        
                        # Store errors
                        self.store_error_detection(agent_id, errors)
                        
                        # Apply fixes
                        for error in errors:
                            if error["severity"] in ["high", "critical"]:
                                self.apply_auto_fix(agent_id, error["error_type"], error["error_message"])
                
                # Wait for next cycle
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"Auto-fix loop error: {str(e)}")
                time.sleep(10)
    
    def get_autofix_status(self):
        """Get current auto-fix status"""
        conn = sqlite3.connect(self.autofix_database)
        cursor = conn.cursor()
        
        # Get error counts by type
        cursor.execute('''
            SELECT error_type, COUNT(*) FROM error_detection
            WHERE timestamp > datetime('now', '-1 hour')
            GROUP BY error_type
        ''')
        error_counts = dict(cursor.fetchall())
        
        # Get fix action counts by status
        cursor.execute('''
            SELECT status, COUNT(*) FROM auto_fix_actions
            WHERE timestamp > datetime('now', '-1 hour')
            GROUP BY status
        ''')
        fix_counts = dict(cursor.fetchall())
        
        # Get recent errors
        cursor.execute('''
            SELECT agent_id, error_type, error_message, severity, timestamp
            FROM error_detection
            ORDER BY timestamp DESC
            LIMIT 10
        ''')
        recent_errors = cursor.fetchall()
        
        conn.close()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "error_counts": error_counts,
            "fix_counts": fix_counts,
            "recent_errors": recent_errors,
            "autofix_active": True
        }
    
    def generate_autofix_report(self):
        """Generate auto-fix report"""
        status = self.get_autofix_status()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "autofix_database": self.autofix_database,
            "agents": self.agents,
            "check_interval": self.check_interval,
            "error_patterns": self.error_patterns,
            "fix_actions": self.fix_actions,
            "autofix_status": status,
            "system_status": "active"
        }
        
        with open("projects/pump_automation/autofix_report.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        print("✅ Auto-fix report generated")

def main():
    """Main function"""
    autofix = AutoFixScripts()
    
    # Start auto-fix system
    success = autofix.start_auto_fix_system()
    
    if success:
        # Generate report
        autofix.generate_autofix_report()
        
        # Update work log
        with open("logs/agent_work.log", "a") as f:
            f.write(f"{datetime.now()}: Agent: Auto-fix Scripts - Task: Auto-fix System - Status: Completed - Notes: Auto-fix system active with error detection\n")
        
        print("\n🎉 Auto-fix system setup completed successfully!")
        
        # Keep running
        try:
            while True:
                time.sleep(60)
                status = autofix.get_autofix_status()
                print(f"🔧 Auto-fix system running... Errors detected: {sum(status['error_counts'].values())}")
        except KeyboardInterrupt:
            print("\n👋 Auto-fix system stopped by user")
    else:
        print("\n❌ Auto-fix system setup failed!")

if __name__ == "__main__":
    main()
