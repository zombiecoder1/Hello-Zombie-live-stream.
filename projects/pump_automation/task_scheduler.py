#!/usr/bin/env python3
"""
Task Scheduler System
Pump/Automation - Automated Task Scheduling for All Agents
"""

import json
import time
import threading
import schedule
from datetime import datetime, timedelta
import sqlite3
import os
import subprocess
import requests

class TaskScheduler:
    def __init__(self):
        self.scheduler_database = "task_scheduler.db"
        self.agents = ["programming", "bestpractices", "verifier", "conversational", "ops"]
        self.scheduled_tasks = {}
        self.running_tasks = {}
        self.setup_database()
        
    def setup_database(self):
        """Setup task scheduler database"""
        conn = sqlite3.connect(self.scheduler_database)
        cursor = conn.cursor()
        
        # Create scheduled tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT UNIQUE NOT NULL,
                agent_id TEXT NOT NULL,
                task_name TEXT NOT NULL,
                task_type TEXT NOT NULL,
                schedule_time TEXT NOT NULL,
                schedule_frequency TEXT,
                task_data TEXT NOT NULL,
                status TEXT DEFAULT 'scheduled',
                created_at TEXT NOT NULL,
                last_run TEXT,
                next_run TEXT
            )
        ''')
        
        # Create task execution log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_execution_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                execution_time TEXT NOT NULL,
                status TEXT NOT NULL,
                result TEXT,
                error_message TEXT,
                duration REAL
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Task scheduler database created successfully")
    
    def schedule_task(self, task_id, agent_id, task_name, task_type, schedule_time, task_data, frequency=None):
        """Schedule a new task"""
        conn = sqlite3.connect(self.scheduler_database)
        cursor = conn.cursor()
        
        # Calculate next run time
        if frequency:
            next_run = self.calculate_next_run(schedule_time, frequency)
        else:
            next_run = schedule_time
        
        cursor.execute('''
            INSERT OR REPLACE INTO scheduled_tasks 
            (task_id, agent_id, task_name, task_type, schedule_time, schedule_frequency, task_data, created_at, next_run)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            task_id, agent_id, task_name, task_type, schedule_time, frequency,
            json.dumps(task_data), datetime.now().isoformat(), next_run
        ))
        
        conn.commit()
        conn.close()
        
        # Add to scheduler
        self.add_to_scheduler(task_id, agent_id, task_name, task_type, task_data, frequency)
        
        print(f"✅ Task scheduled: {task_name} for agent {agent_id}")
    
    def add_to_scheduler(self, task_id, agent_id, task_name, task_type, task_data, frequency):
        """Add task to Python scheduler"""
        if frequency == "daily":
            schedule.every().day.at(task_data.get('time', '09:00')).do(
                self.execute_task, task_id, agent_id, task_name, task_type, task_data
            )
        elif frequency == "hourly":
            schedule.every().hour.do(
                self.execute_task, task_id, agent_id, task_name, task_type, task_data
            )
        elif frequency == "every_5_minutes":
            schedule.every(5).minutes.do(
                self.execute_task, task_id, agent_id, task_name, task_type, task_data
            )
        elif frequency == "every_10_minutes":
            schedule.every(10).minutes.do(
                self.execute_task, task_id, agent_id, task_name, task_type, task_data
            )
        else:
            # One-time task
            schedule_time = datetime.fromisoformat(task_data.get('schedule_time', datetime.now().isoformat()))
            if schedule_time <= datetime.now():
                # Execute immediately
                self.execute_task(task_id, agent_id, task_name, task_type, task_data)
            else:
                # Schedule for later
                schedule.every().day.at(schedule_time.strftime('%H:%M')).do(
                    self.execute_task, task_id, agent_id, task_name, task_type, task_data
                )
    
    def calculate_next_run(self, schedule_time, frequency):
        """Calculate next run time based on frequency"""
        base_time = datetime.fromisoformat(schedule_time)
        
        if frequency == "daily":
            return (base_time + timedelta(days=1)).isoformat()
        elif frequency == "hourly":
            return (base_time + timedelta(hours=1)).isoformat()
        elif frequency == "every_5_minutes":
            return (base_time + timedelta(minutes=5)).isoformat()
        elif frequency == "every_10_minutes":
            return (base_time + timedelta(minutes=10)).isoformat()
        else:
            return schedule_time
    
    def execute_task(self, task_id, agent_id, task_name, task_type, task_data):
        """Execute a scheduled task"""
        start_time = time.time()
        execution_time = datetime.now().isoformat()
        
        print(f"🚀 Executing task: {task_name} for agent {agent_id}")
        
        try:
            # Mark task as running
            self.update_task_status(task_id, "running")
            
            # Execute based on task type
            if task_type == "model_optimization":
                result = self.execute_model_optimization(agent_id, task_data)
            elif task_type == "cloud_service_check":
                result = self.execute_cloud_service_check(agent_id, task_data)
            elif task_type == "memory_cleanup":
                result = self.execute_memory_cleanup(agent_id, task_data)
            elif task_type == "performance_check":
                result = self.execute_performance_check(agent_id, task_data)
            elif task_type == "system_health_check":
                result = self.execute_system_health_check(agent_id, task_data)
            else:
                result = self.execute_generic_task(agent_id, task_data)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log successful execution
            self.log_task_execution(task_id, execution_time, "completed", result, None, duration)
            
            # Update task status
            self.update_task_status(task_id, "completed")
            
            print(f"✅ Task completed: {task_name} (Duration: {duration:.2f}s)")
            
            # Schedule next run if recurring
            self.schedule_next_run(task_id)
            
        except Exception as e:
            duration = time.time() - start_time
            error_message = str(e)
            
            # Log failed execution
            self.log_task_execution(task_id, execution_time, "failed", None, error_message, duration)
            
            # Update task status
            self.update_task_status(task_id, "failed")
            
            print(f"❌ Task failed: {task_name} - {error_message}")
    
    def execute_model_optimization(self, agent_id, task_data):
        """Execute model optimization task"""
        print(f"   🔧 Running model optimization for agent {agent_id}")
        
        # Run model optimizer script
        try:
            result = subprocess.run([
                "python3", "projects/local_model_optimization/model_optimizer.py"
            ], capture_output=True, text=True, timeout=60)
            
            return {
                "status": "success",
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "output": "",
                "error": "Model optimization timed out",
                "return_code": -1
            }
        except Exception as e:
            return {
                "status": "error",
                "output": "",
                "error": str(e),
                "return_code": -1
            }
    
    def execute_cloud_service_check(self, agent_id, task_data):
        """Execute cloud service check task"""
        print(f"   🌐 Running cloud service check for agent {agent_id}")
        
        # Run cloud service blocking script
        try:
            result = subprocess.run([
                "python3", "projects/cloud_service_blocking/block_cloud_services.py"
            ], capture_output=True, text=True, timeout=30)
            
            return {
                "status": "success",
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {
                "status": "error",
                "output": "",
                "error": str(e),
                "return_code": -1
            }
    
    def execute_memory_cleanup(self, agent_id, task_data):
        """Execute memory cleanup task"""
        print(f"   🧹 Running memory cleanup for agent {agent_id}")
        
        # Run memory isolation script
        try:
            result = subprocess.run([
                "python3", "projects/agent_memory_isolation/memory_isolation.py"
            ], capture_output=True, text=True, timeout=30)
            
            return {
                "status": "success",
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {
                "status": "error",
                "output": "",
                "error": str(e),
                "return_code": -1
            }
    
    def execute_performance_check(self, agent_id, task_data):
        """Execute performance check task"""
        print(f"   📊 Running performance check for agent {agent_id}")
        
        # Check system performance
        import psutil
        
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "status": "success",
            "cpu_usage": cpu_usage,
            "memory_usage": memory.percent,
            "disk_usage": disk.percent,
            "memory_available": memory.available / (1024**3)  # GB
        }
    
    def execute_system_health_check(self, agent_id, task_data):
        """Execute system health check task"""
        print(f"   🏥 Running system health check for agent {agent_id}")
        
        # Check system health
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "system_status": "healthy",
            "checks": []
        }
        
        # Check disk space
        import psutil
        disk = psutil.disk_usage('/')
        if disk.percent > 90:
            health_status["checks"].append({"check": "disk_space", "status": "warning", "value": disk.percent})
        else:
            health_status["checks"].append({"check": "disk_space", "status": "ok", "value": disk.percent})
        
        # Check memory
        memory = psutil.virtual_memory()
        if memory.percent > 90:
            health_status["checks"].append({"check": "memory", "status": "warning", "value": memory.percent})
        else:
            health_status["checks"].append({"check": "memory", "status": "ok", "value": memory.percent})
        
        # Check CPU
        cpu_usage = psutil.cpu_percent()
        if cpu_usage > 90:
            health_status["checks"].append({"check": "cpu", "status": "warning", "value": cpu_usage})
        else:
            health_status["checks"].append({"check": "cpu", "status": "ok", "value": cpu_usage})
        
        return health_status
    
    def execute_generic_task(self, agent_id, task_data):
        """Execute generic task"""
        print(f"   ⚙️ Running generic task for agent {agent_id}")
        
        # Generic task execution
        command = task_data.get('command', 'echo "No command specified"')
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            return {
                "status": "success",
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {
                "status": "error",
                "output": "",
                "error": str(e),
                "return_code": -1
            }
    
    def update_task_status(self, task_id, status):
        """Update task status in database"""
        conn = sqlite3.connect(self.scheduler_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE scheduled_tasks SET status = ?, last_run = ?
            WHERE task_id = ?
        ''', (status, datetime.now().isoformat(), task_id))
        
        conn.commit()
        conn.close()
    
    def log_task_execution(self, task_id, execution_time, status, result, error_message, duration):
        """Log task execution"""
        conn = sqlite3.connect(self.scheduler_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO task_execution_log 
            (task_id, execution_time, status, result, error_message, duration)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            task_id, execution_time, status, json.dumps(result) if result else None,
            error_message, duration
        ))
        
        conn.commit()
        conn.close()
    
    def schedule_next_run(self, task_id):
        """Schedule next run for recurring tasks"""
        conn = sqlite3.connect(self.scheduler_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT schedule_frequency, schedule_time FROM scheduled_tasks
            WHERE task_id = ?
        ''', (task_id,))
        
        result = cursor.fetchone()
        if result and result[0]:  # If it's a recurring task
            frequency = result[0]
            schedule_time = result[1]
            next_run = self.calculate_next_run(schedule_time, frequency)
            
            cursor.execute('''
                UPDATE scheduled_tasks SET next_run = ?, status = 'scheduled'
                WHERE task_id = ?
            ''', (next_run, task_id))
            
            conn.commit()
        
        conn.close()
    
    def start_scheduler(self):
        """Start the task scheduler"""
        print("🧟 Task Scheduler - Starting Scheduler")
        print("=" * 50)
        
        # Load existing tasks from database
        self.load_scheduled_tasks()
        
        # Start scheduler in background thread
        scheduler_thread = threading.Thread(target=self.run_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()
        
        print("✅ Task scheduler started successfully")
        return True
    
    def load_scheduled_tasks(self):
        """Load scheduled tasks from database"""
        conn = sqlite3.connect(self.scheduler_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT task_id, agent_id, task_name, task_type, schedule_time, 
                   schedule_frequency, task_data, status
            FROM scheduled_tasks
            WHERE status IN ('scheduled', 'running')
        ''')
        
        tasks = cursor.fetchall()
        for task in tasks:
            task_id, agent_id, task_name, task_type, schedule_time, frequency, task_data, status = task
            task_data = json.loads(task_data)
            
            # Add to scheduler
            self.add_to_scheduler(task_id, agent_id, task_name, task_type, task_data, frequency)
            
            print(f"   📅 Loaded task: {task_name} for agent {agent_id}")
        
        conn.close()
        print(f"✅ Loaded {len(tasks)} scheduled tasks")
    
    def run_scheduler(self):
        """Run the scheduler loop"""
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                print(f"Scheduler error: {str(e)}")
                time.sleep(5)
    
    def create_default_tasks(self):
        """Create default scheduled tasks"""
        print("📅 Creating default scheduled tasks...")
        
        # Model optimization - every 6 hours
        self.schedule_task(
            "model_opt_6h", "programming", "Model Optimization", "model_optimization",
            datetime.now().isoformat(), {"time": "00:00"}, "every_6_hours"
        )
        
        # Cloud service check - every hour
        self.schedule_task(
            "cloud_check_1h", "bestpractices", "Cloud Service Check", "cloud_service_check",
            datetime.now().isoformat(), {"time": "00:00"}, "hourly"
        )
        
        # Memory cleanup - every 12 hours
        self.schedule_task(
            "memory_cleanup_12h", "verifier", "Memory Cleanup", "memory_cleanup",
            datetime.now().isoformat(), {"time": "02:00"}, "every_12_hours"
        )
        
        # Performance check - every 10 minutes
        self.schedule_task(
            "perf_check_10m", "ops", "Performance Check", "performance_check",
            datetime.now().isoformat(), {"time": "00:00"}, "every_10_minutes"
        )
        
        # System health check - every 30 minutes
        self.schedule_task(
            "health_check_30m", "conversational", "System Health Check", "system_health_check",
            datetime.now().isoformat(), {"time": "00:00"}, "every_30_minutes"
        )
        
        print("✅ Default tasks created successfully")
    
    def get_scheduler_status(self):
        """Get current scheduler status"""
        conn = sqlite3.connect(self.scheduler_database)
        cursor = conn.cursor()
        
        # Get task counts by status
        cursor.execute('''
            SELECT status, COUNT(*) FROM scheduled_tasks GROUP BY status
        ''')
        status_counts = dict(cursor.fetchall())
        
        # Get recent executions
        cursor.execute('''
            SELECT task_id, execution_time, status, duration
            FROM task_execution_log
            ORDER BY execution_time DESC
            LIMIT 10
        ''')
        recent_executions = cursor.fetchall()
        
        conn.close()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "status_counts": status_counts,
            "recent_executions": recent_executions,
            "scheduler_active": True
        }
    
    def generate_scheduler_report(self):
        """Generate scheduler report"""
        status = self.get_scheduler_status()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "scheduler_database": self.scheduler_database,
            "agents": self.agents,
            "scheduler_status": status,
            "system_status": "active"
        }
        
        with open("projects/pump_automation/scheduler_report.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        print("✅ Scheduler report generated")

def main():
    """Main function"""
    scheduler = TaskScheduler()
    
    # Create default tasks
    scheduler.create_default_tasks()
    
    # Start scheduler
    success = scheduler.start_scheduler()
    
    if success:
        # Generate report
        scheduler.generate_scheduler_report()
        
        # Update work log
        with open("logs/agent_work.log", "a") as f:
            f.write(f"{datetime.now()}: Agent: Task Scheduler - Task: Task Scheduling - Status: Completed - Notes: Task scheduler active with default tasks\n")
        
        print("\n🎉 Task scheduler setup completed successfully!")
        
        # Keep running
        try:
            while True:
                time.sleep(60)
                print(f"⏰ Scheduler running... {datetime.now().strftime('%H:%M:%S')}")
        except KeyboardInterrupt:
            print("\n👋 Scheduler stopped by user")
    else:
        print("\n❌ Task scheduler setup failed!")

if __name__ == "__main__":
    main()
