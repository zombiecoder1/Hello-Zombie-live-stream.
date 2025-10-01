#!/usr/bin/env python3
"""
Monitoring Alerts System
Pump/Automation - Real-time Alerts for Failures or Delays
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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MonitoringAlerts:
    def __init__(self):
        self.alerts_database = "monitoring_alerts.db"
        self.agents = ["programming", "bestpractices", "verifier", "conversational", "ops"]
        self.alert_interval = 10  # seconds
        self.alert_thresholds = {
            "cpu_usage": 85.0,
            "memory_usage": 90.0,
            "disk_usage": 95.0,
            "response_time": 5.0,
            "error_rate": 10.0,
            "uptime": 3600  # 1 hour in seconds
        }
        self.alert_channels = {
            "console": True,
            "log": True,
            "email": False,  # Disabled by default
            "webhook": False  # Disabled by default
        }
        self.setup_database()
        
    def setup_database(self):
        """Setup monitoring alerts database"""
        conn = sqlite3.connect(self.alerts_database)
        cursor = conn.cursor()
        
        # Create alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                alert_id TEXT UNIQUE NOT NULL,
                agent_id TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                alert_level TEXT NOT NULL,
                alert_message TEXT NOT NULL,
                alert_data TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                acknowledged BOOLEAN DEFAULT FALSE,
                resolved_at TEXT
            )
        ''')
        
        # Create alert history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                alert_id TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                user TEXT DEFAULT 'system'
            )
        ''')
        
        # Create notification log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notification_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                alert_id TEXT NOT NULL,
                channel TEXT NOT NULL,
                status TEXT NOT NULL,
                message TEXT,
                error_message TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Monitoring alerts database created successfully")
    
    def check_system_health(self, agent_id):
        """Check system health and generate alerts"""
        alerts = []
        
        try:
            # Check CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage > self.alert_thresholds["cpu_usage"]:
                alerts.append({
                    "alert_type": "high_cpu_usage",
                    "alert_level": "warning" if cpu_usage < 95 else "critical",
                    "alert_message": f"High CPU usage detected: {cpu_usage:.1f}%",
                    "alert_data": {"cpu_usage": cpu_usage, "threshold": self.alert_thresholds["cpu_usage"]}
                })
            
            # Check memory usage
            memory = psutil.virtual_memory()
            if memory.percent > self.alert_thresholds["memory_usage"]:
                alerts.append({
                    "alert_type": "high_memory_usage",
                    "alert_level": "warning" if memory.percent < 95 else "critical",
                    "alert_message": f"High memory usage detected: {memory.percent:.1f}%",
                    "alert_data": {"memory_usage": memory.percent, "threshold": self.alert_thresholds["memory_usage"]}
                })
            
            # Check disk usage
            disk = psutil.disk_usage('/')
            if disk.percent > self.alert_thresholds["disk_usage"]:
                alerts.append({
                    "alert_type": "high_disk_usage",
                    "alert_level": "warning" if disk.percent < 98 else "critical",
                    "alert_message": f"High disk usage detected: {disk.percent:.1f}%",
                    "alert_data": {"disk_usage": disk.percent, "threshold": self.alert_thresholds["disk_usage"]}
                })
            
            # Check system uptime
            uptime = time.time() - psutil.boot_time()
            if uptime < self.alert_thresholds["uptime"]:
                alerts.append({
                    "alert_type": "low_uptime",
                    "alert_level": "info",
                    "alert_message": f"System recently restarted: {uptime/3600:.1f} hours ago",
                    "alert_data": {"uptime": uptime, "threshold": self.alert_thresholds["uptime"]}
                })
            
        except Exception as e:
            alerts.append({
                "alert_type": "system_check_error",
                "alert_level": "error",
                "alert_message": f"Error checking system health: {str(e)}",
                "alert_data": {"error": str(e)}
            })
        
        return alerts
    
    def check_agent_status(self, agent_id):
        """Check agent status and generate alerts"""
        alerts = []
        
        try:
            # Check if agent log files exist and are recent
            log_files = [
                f"logs/agent_work.log",
                f"logs/agent_error.log",
                f"logs/agent_report.log"
            ]
            
            for log_file in log_files:
                if os.path.exists(log_file):
                    # Check if log file is recent (within last hour)
                    file_age = time.time() - os.path.getmtime(log_file)
                    if file_age > 3600:  # 1 hour
                        alerts.append({
                            "alert_type": "stale_log_file",
                            "alert_level": "warning",
                            "alert_message": f"Log file {log_file} is stale: {file_age/3600:.1f} hours old",
                            "alert_data": {"log_file": log_file, "age_hours": file_age/3600}
                        })
                else:
                    alerts.append({
                        "alert_type": "missing_log_file",
                        "alert_level": "error",
                        "alert_message": f"Log file {log_file} is missing",
                        "alert_data": {"log_file": log_file}
                    })
            
            # Check agent-specific processes
            agent_processes = self.check_agent_processes(agent_id)
            if not agent_processes:
                alerts.append({
                    "alert_type": "no_agent_processes",
                    "alert_level": "critical",
                    "alert_message": f"No processes found for agent {agent_id}",
                    "alert_data": {"agent_id": agent_id}
                })
            
        except Exception as e:
            alerts.append({
                "alert_type": "agent_check_error",
                "alert_level": "error",
                "alert_message": f"Error checking agent {agent_id}: {str(e)}",
                "alert_data": {"agent_id": agent_id, "error": str(e)}
            })
        
        return alerts
    
    def check_agent_processes(self, agent_id):
        """Check if agent processes are running"""
        try:
            # Look for Python processes related to the agent
            processes = list(psutil.process_iter(['pid', 'name', 'cmdline']))
            agent_processes = []
            
            for proc in processes:
                try:
                    if proc.info['name'] == 'python3':
                        cmdline = ' '.join(proc.info['cmdline'])
                        if agent_id in cmdline or 'zombiecoder' in cmdline:
                            agent_processes.append(proc.info)
                except:
                    continue
            
            return agent_processes
            
        except Exception as e:
            print(f"Error checking processes for agent {agent_id}: {str(e)}")
            return []
    
    def check_service_health(self, agent_id):
        """Check service health and generate alerts"""
        alerts = []
        
        try:
            # Check key services
            services_to_check = [
                "ollama",
                "systemd-resolved",
                "networking"
            ]
            
            for service in services_to_check:
                try:
                    result = subprocess.run([
                        "systemctl", "is-active", service
                    ], capture_output=True, text=True, timeout=5)
                    
                    if result.returncode != 0:
                        alerts.append({
                            "alert_type": "service_down",
                            "alert_level": "critical",
                            "alert_message": f"Service {service} is not active",
                            "alert_data": {"service": service, "status": result.stdout.strip()}
                        })
                
                except subprocess.TimeoutExpired:
                    alerts.append({
                        "alert_type": "service_check_timeout",
                        "alert_level": "warning",
                        "alert_message": f"Service {service} check timed out",
                        "alert_data": {"service": service}
                    })
                except:
                    # Service might not be managed by systemd
                    pass
            
        except Exception as e:
            alerts.append({
                "alert_type": "service_check_error",
                "alert_level": "error",
                "alert_message": f"Error checking services: {str(e)}",
                "alert_data": {"error": str(e)}
            })
        
        return alerts
    
    def create_alert(self, agent_id, alert_type, alert_level, alert_message, alert_data):
        """Create a new alert"""
        alert_id = f"{agent_id}_{alert_type}_{int(time.time())}"
        
        conn = sqlite3.connect(self.alerts_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO alerts 
            (timestamp, alert_id, agent_id, alert_type, alert_level, alert_message, alert_data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(), alert_id, agent_id, alert_type,
            alert_level, alert_message, json.dumps(alert_data)
        ))
        
        conn.commit()
        conn.close()
        
        # Send notifications
        self.send_notifications(alert_id, agent_id, alert_type, alert_level, alert_message)
        
        print(f"🚨 Alert created: {alert_type} for agent {agent_id} - {alert_message}")
    
    def send_notifications(self, alert_id, agent_id, alert_type, alert_level, alert_message):
        """Send notifications through configured channels"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Console notification
        if self.alert_channels["console"]:
            self.send_console_notification(alert_id, agent_id, alert_type, alert_level, alert_message, timestamp)
        
        # Log notification
        if self.alert_channels["log"]:
            self.send_log_notification(alert_id, agent_id, alert_type, alert_level, alert_message, timestamp)
        
        # Email notification
        if self.alert_channels["email"]:
            self.send_email_notification(alert_id, agent_id, alert_type, alert_level, alert_message, timestamp)
        
        # Webhook notification
        if self.alert_channels["webhook"]:
            self.send_webhook_notification(alert_id, agent_id, alert_type, alert_level, alert_message, timestamp)
    
    def send_console_notification(self, alert_id, agent_id, alert_type, alert_level, alert_message, timestamp):
        """Send console notification"""
        try:
            level_emoji = {
                "info": "ℹ️",
                "warning": "⚠️",
                "error": "❌",
                "critical": "🚨"
            }
            
            emoji = level_emoji.get(alert_level, "📢")
            
            print(f"\n{emoji} ALERT {emoji}")
            print(f"Time: {timestamp}")
            print(f"Agent: {agent_id}")
            print(f"Type: {alert_type}")
            print(f"Level: {alert_level.upper()}")
            print(f"Message: {alert_message}")
            print(f"Alert ID: {alert_id}")
            print("=" * 50)
            
            self.log_notification(alert_id, "console", "success", f"Console notification sent")
            
        except Exception as e:
            self.log_notification(alert_id, "console", "failed", f"Console notification failed: {str(e)}")
    
    def send_log_notification(self, alert_id, agent_id, alert_type, alert_level, alert_message, timestamp):
        """Send log notification"""
        try:
            log_entry = f"[{timestamp}] ALERT - Agent: {agent_id}, Type: {alert_type}, Level: {alert_level}, Message: {alert_message}, ID: {alert_id}\n"
            
            with open("logs/monitoring_alerts.log", "a") as f:
                f.write(log_entry)
            
            self.log_notification(alert_id, "log", "success", f"Log notification sent")
            
        except Exception as e:
            self.log_notification(alert_id, "log", "failed", f"Log notification failed: {str(e)}")
    
    def send_email_notification(self, alert_id, agent_id, alert_type, alert_level, alert_message, timestamp):
        """Send email notification (placeholder)"""
        try:
            # Email configuration would go here
            # For now, just log the attempt
            self.log_notification(alert_id, "email", "skipped", "Email notifications disabled")
            
        except Exception as e:
            self.log_notification(alert_id, "email", "failed", f"Email notification failed: {str(e)}")
    
    def send_webhook_notification(self, alert_id, agent_id, alert_type, alert_level, alert_message, timestamp):
        """Send webhook notification (placeholder)"""
        try:
            # Webhook configuration would go here
            # For now, just log the attempt
            self.log_notification(alert_id, "webhook", "skipped", "Webhook notifications disabled")
            
        except Exception as e:
            self.log_notification(alert_id, "webhook", "failed", f"Webhook notification failed: {str(e)}")
    
    def log_notification(self, alert_id, channel, status, message):
        """Log notification attempt"""
        conn = sqlite3.connect(self.alerts_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO notification_log 
            (timestamp, alert_id, channel, status, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), alert_id, channel, status, message))
        
        conn.commit()
        conn.close()
    
    def acknowledge_alert(self, alert_id, user="admin"):
        """Acknowledge an alert"""
        conn = sqlite3.connect(self.alerts_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE alerts SET acknowledged = TRUE WHERE alert_id = ?
        ''', (alert_id,))
        
        cursor.execute('''
            INSERT INTO alert_history 
            (timestamp, alert_id, action, details, user)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), alert_id, "acknowledged", f"Acknowledged by {user}", user))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Alert {alert_id} acknowledged by {user}")
    
    def resolve_alert(self, alert_id, user="admin"):
        """Resolve an alert"""
        conn = sqlite3.connect(self.alerts_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE alerts SET status = 'resolved', resolved_at = ? WHERE alert_id = ?
        ''', (datetime.now().isoformat(), alert_id))
        
        cursor.execute('''
            INSERT INTO alert_history 
            (timestamp, alert_id, action, details, user)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), alert_id, "resolved", f"Resolved by {user}", user))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Alert {alert_id} resolved by {user}")
    
    def start_monitoring_alerts(self):
        """Start the monitoring alerts system"""
        print("🧟 Monitoring Alerts - Starting Alert System")
        print("=" * 50)
        
        # Start monitoring in background thread
        monitoring_thread = threading.Thread(target=self.monitoring_loop)
        monitoring_thread.daemon = True
        monitoring_thread.start()
        
        print("✅ Monitoring alerts system started successfully")
        return True
    
    def monitoring_loop(self):
        """Main monitoring loop"""
        while True:
            try:
                print(f"🔍 Running monitoring cycle... {datetime.now().strftime('%H:%M:%S')}")
                
                for agent_id in self.agents:
                    # Check system health
                    system_alerts = self.check_system_health(agent_id)
                    for alert in system_alerts:
                        self.create_alert(agent_id, alert["alert_type"], alert["alert_level"], 
                                        alert["alert_message"], alert["alert_data"])
                    
                    # Check agent status
                    agent_alerts = self.check_agent_status(agent_id)
                    for alert in agent_alerts:
                        self.create_alert(agent_id, alert["alert_type"], alert["alert_level"], 
                                        alert["alert_message"], alert["alert_data"])
                    
                    # Check service health
                    service_alerts = self.check_service_health(agent_id)
                    for alert in service_alerts:
                        self.create_alert(agent_id, alert["alert_type"], alert["alert_level"], 
                                        alert["alert_message"], alert["alert_data"])
                
                # Wait for next cycle
                time.sleep(self.alert_interval)
                
            except Exception as e:
                print(f"Monitoring loop error: {str(e)}")
                time.sleep(10)
    
    def get_alerts_status(self):
        """Get current alerts status"""
        conn = sqlite3.connect(self.alerts_database)
        cursor = conn.cursor()
        
        # Get active alerts count
        cursor.execute('''
            SELECT alert_level, COUNT(*) FROM alerts
            WHERE status = 'active'
            GROUP BY alert_level
        ''')
        active_alerts = dict(cursor.fetchall())
        
        # Get recent alerts
        cursor.execute('''
            SELECT alert_id, agent_id, alert_type, alert_level, alert_message, timestamp
            FROM alerts
            ORDER BY timestamp DESC
            LIMIT 10
        ''')
        recent_alerts = cursor.fetchall()
        
        # Get notification stats
        cursor.execute('''
            SELECT channel, status, COUNT(*) FROM notification_log
            WHERE timestamp > datetime('now', '-1 hour')
            GROUP BY channel, status
        ''')
        notification_stats = cursor.fetchall()
        
        conn.close()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "active_alerts": active_alerts,
            "recent_alerts": recent_alerts,
            "notification_stats": notification_stats,
            "monitoring_active": True
        }
    
    def generate_alerts_report(self):
        """Generate monitoring alerts report"""
        status = self.get_alerts_status()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "alerts_database": self.alerts_database,
            "agents": self.agents,
            "alert_interval": self.alert_interval,
            "alert_thresholds": self.alert_thresholds,
            "alert_channels": self.alert_channels,
            "alerts_status": status,
            "system_status": "active"
        }
        
        with open("projects/pump_automation/alerts_report.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        print("✅ Monitoring alerts report generated")

def main():
    """Main function"""
    alerts = MonitoringAlerts()
    
    # Start monitoring alerts
    success = alerts.start_monitoring_alerts()
    
    if success:
        # Generate report
        alerts.generate_alerts_report()
        
        # Update work log
        with open("logs/agent_work.log", "a") as f:
            f.write(f"{datetime.now()}: Agent: Monitoring Alerts - Task: Monitoring Alerts - Status: Completed - Notes: Monitoring alerts system active\n")
        
        print("\n🎉 Monitoring alerts system setup completed successfully!")
        
        # Keep running
        try:
            while True:
                time.sleep(60)
                status = alerts.get_alerts_status()
                active_count = sum(status['active_alerts'].values())
                print(f"🚨 Monitoring alerts running... Active alerts: {active_count}")
        except KeyboardInterrupt:
            print("\n👋 Monitoring alerts system stopped by user")
    else:
        print("\n❌ Monitoring alerts system setup failed!")

if __name__ == "__main__":
    main()
