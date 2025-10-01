#!/usr/bin/env python3
"""
Batch Processing System
Pump/Automation - Batch Job Processing for Repetitive Tasks
"""

import json
import time
import threading
from datetime import datetime, timedelta
import sqlite3
import os
import subprocess
import queue
import concurrent.futures

class BatchProcessor:
    def __init__(self):
        self.batch_database = "batch_processor.db"
        self.agents = ["programming", "bestpractices", "verifier", "conversational", "ops"]
        self.batch_queue = queue.Queue()
        self.processing_threads = []
        self.max_workers = 3
        self.setup_database()
        
    def setup_database(self):
        """Setup batch processor database"""
        conn = sqlite3.connect(self.batch_database)
        cursor = conn.cursor()
        
        # Create batch jobs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS batch_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT UNIQUE NOT NULL,
                job_name TEXT NOT NULL,
                job_type TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                job_data TEXT NOT NULL,
                priority INTEGER DEFAULT 5,
                status TEXT DEFAULT 'pending',
                created_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                result TEXT,
                error_message TEXT
            )
        ''')
        
        # Create batch job log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS batch_job_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT NOT NULL,
                log_level TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Batch processor database created successfully")
    
    def create_batch_job(self, job_id, job_name, job_type, agent_id, job_data, priority=5):
        """Create a new batch job"""
        conn = sqlite3.connect(self.batch_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO batch_jobs 
            (job_id, job_name, job_type, agent_id, job_data, priority, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            job_id, job_name, job_type, agent_id, json.dumps(job_data), priority,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        # Add to processing queue
        self.batch_queue.put((job_id, job_name, job_type, agent_id, job_data, priority))
        
        print(f"✅ Batch job created: {job_name} for agent {agent_id}")
    
    def create_batch_jobs_from_template(self, template_name, agent_ids, job_data_template):
        """Create multiple batch jobs from a template"""
        print(f"📦 Creating batch jobs from template: {template_name}")
        
        job_count = 0
        for agent_id in agent_ids:
            job_id = f"{template_name}_{agent_id}_{int(time.time())}"
            job_name = f"{template_name} - {agent_id}"
            
            # Customize job data for each agent
            customized_data = job_data_template.copy()
            customized_data['agent_id'] = agent_id
            customized_data['template'] = template_name
            
            self.create_batch_job(job_id, job_name, template_name, agent_id, customized_data)
            job_count += 1
        
        print(f"✅ Created {job_count} batch jobs from template {template_name}")
        return job_count
    
    def process_batch_job(self, job_id, job_name, job_type, agent_id, job_data, priority):
        """Process a single batch job"""
        start_time = time.time()
        
        # Update job status
        self.update_job_status(job_id, "running", started_at=datetime.now().isoformat())
        self.log_job_message(job_id, "INFO", f"Starting batch job: {job_name}")
        
        try:
            # Execute based on job type
            if job_type == "model_optimization_batch":
                result = self.execute_model_optimization_batch(agent_id, job_data)
            elif job_type == "cloud_service_batch":
                result = self.execute_cloud_service_batch(agent_id, job_data)
            elif job_type == "memory_cleanup_batch":
                result = self.execute_memory_cleanup_batch(agent_id, job_data)
            elif job_type == "performance_analysis_batch":
                result = self.execute_performance_analysis_batch(agent_id, job_data)
            elif job_type == "system_health_batch":
                result = self.execute_system_health_batch(agent_id, job_data)
            elif job_type == "data_processing_batch":
                result = self.execute_data_processing_batch(agent_id, job_data)
            else:
                result = self.execute_generic_batch(agent_id, job_data)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Update job status
            self.update_job_status(job_id, "completed", 
                                 completed_at=datetime.now().isoformat(),
                                 result=json.dumps(result))
            
            self.log_job_message(job_id, "INFO", f"Batch job completed successfully in {duration:.2f}s")
            
            print(f"✅ Batch job completed: {job_name} (Duration: {duration:.2f}s)")
            
        except Exception as e:
            duration = time.time() - start_time
            error_message = str(e)
            
            # Update job status
            self.update_job_status(job_id, "failed", 
                                 completed_at=datetime.now().isoformat(),
                                 error_message=error_message)
            
            self.log_job_message(job_id, "ERROR", f"Batch job failed: {error_message}")
            
            print(f"❌ Batch job failed: {job_name} - {error_message}")
    
    def execute_model_optimization_batch(self, agent_id, job_data):
        """Execute model optimization batch job"""
        print(f"   🔧 Running model optimization batch for agent {agent_id}")
        
        # Run model optimizer with batch parameters
        try:
            result = subprocess.run([
                "python3", "projects/local_model_optimization/model_optimizer.py"
            ], capture_output=True, text=True, timeout=120)
            
            return {
                "status": "success",
                "agent_id": agent_id,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode,
                "job_type": "model_optimization_batch"
            }
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "agent_id": agent_id,
                "output": "",
                "error": "Model optimization batch timed out",
                "return_code": -1,
                "job_type": "model_optimization_batch"
            }
        except Exception as e:
            return {
                "status": "error",
                "agent_id": agent_id,
                "output": "",
                "error": str(e),
                "return_code": -1,
                "job_type": "model_optimization_batch"
            }
    
    def execute_cloud_service_batch(self, agent_id, job_data):
        """Execute cloud service batch job"""
        print(f"   🌐 Running cloud service batch for agent {agent_id}")
        
        try:
            result = subprocess.run([
                "python3", "projects/cloud_service_blocking/block_cloud_services.py"
            ], capture_output=True, text=True, timeout=60)
            
            return {
                "status": "success",
                "agent_id": agent_id,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode,
                "job_type": "cloud_service_batch"
            }
        except Exception as e:
            return {
                "status": "error",
                "agent_id": agent_id,
                "output": "",
                "error": str(e),
                "return_code": -1,
                "job_type": "cloud_service_batch"
            }
    
    def execute_memory_cleanup_batch(self, agent_id, job_data):
        """Execute memory cleanup batch job"""
        print(f"   🧹 Running memory cleanup batch for agent {agent_id}")
        
        try:
            result = subprocess.run([
                "python3", "projects/agent_memory_isolation/memory_isolation.py"
            ], capture_output=True, text=True, timeout=60)
            
            return {
                "status": "success",
                "agent_id": agent_id,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode,
                "job_type": "memory_cleanup_batch"
            }
        except Exception as e:
            return {
                "status": "error",
                "agent_id": agent_id,
                "output": "",
                "error": str(e),
                "return_code": -1,
                "job_type": "memory_cleanup_batch"
            }
    
    def execute_performance_analysis_batch(self, agent_id, job_data):
        """Execute performance analysis batch job"""
        print(f"   📊 Running performance analysis batch for agent {agent_id}")
        
        import psutil
        
        # Collect performance metrics
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Analyze performance
        analysis = {
            "cpu_analysis": "good" if cpu_usage < 50 else "warning" if cpu_usage < 80 else "critical",
            "memory_analysis": "good" if memory.percent < 70 else "warning" if memory.percent < 90 else "critical",
            "disk_analysis": "good" if disk.percent < 80 else "warning" if disk.percent < 95 else "critical"
        }
        
        return {
            "status": "success",
            "agent_id": agent_id,
            "cpu_usage": cpu_usage,
            "memory_usage": memory.percent,
            "disk_usage": disk.percent,
            "analysis": analysis,
            "job_type": "performance_analysis_batch"
        }
    
    def execute_system_health_batch(self, agent_id, job_data):
        """Execute system health batch job"""
        print(f"   🏥 Running system health batch for agent {agent_id}")
        
        import psutil
        
        health_checks = []
        
        # Check disk space
        disk = psutil.disk_usage('/')
        health_checks.append({
            "check": "disk_space",
            "value": disk.percent,
            "status": "ok" if disk.percent < 90 else "warning" if disk.percent < 95 else "critical"
        })
        
        # Check memory
        memory = psutil.virtual_memory()
        health_checks.append({
            "check": "memory",
            "value": memory.percent,
            "status": "ok" if memory.percent < 80 else "warning" if memory.percent < 90 else "critical"
        })
        
        # Check CPU
        cpu_usage = psutil.cpu_percent(interval=1)
        health_checks.append({
            "check": "cpu",
            "value": cpu_usage,
            "status": "ok" if cpu_usage < 70 else "warning" if cpu_usage < 90 else "critical"
        })
        
        # Overall health status
        critical_checks = [check for check in health_checks if check["status"] == "critical"]
        warning_checks = [check for check in health_checks if check["status"] == "warning"]
        
        if critical_checks:
            overall_status = "critical"
        elif warning_checks:
            overall_status = "warning"
        else:
            overall_status = "healthy"
        
        return {
            "status": "success",
            "agent_id": agent_id,
            "overall_status": overall_status,
            "health_checks": health_checks,
            "critical_count": len(critical_checks),
            "warning_count": len(warning_checks),
            "job_type": "system_health_batch"
        }
    
    def execute_data_processing_batch(self, agent_id, job_data):
        """Execute data processing batch job"""
        print(f"   📊 Running data processing batch for agent {agent_id}")
        
        # Simulate data processing
        data_size = job_data.get('data_size', 1000)
        processing_time = data_size * 0.001  # Simulate processing time
        
        time.sleep(min(processing_time, 5))  # Cap at 5 seconds
        
        return {
            "status": "success",
            "agent_id": agent_id,
            "processed_records": data_size,
            "processing_time": processing_time,
            "job_type": "data_processing_batch"
        }
    
    def execute_generic_batch(self, agent_id, job_data):
        """Execute generic batch job"""
        print(f"   ⚙️ Running generic batch for agent {agent_id}")
        
        command = job_data.get('command', 'echo "No command specified"')
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
            return {
                "status": "success",
                "agent_id": agent_id,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode,
                "job_type": "generic_batch"
            }
        except Exception as e:
            return {
                "status": "error",
                "agent_id": agent_id,
                "output": "",
                "error": str(e),
                "return_code": -1,
                "job_type": "generic_batch"
            }
    
    def update_job_status(self, job_id, status, started_at=None, completed_at=None, result=None, error_message=None):
        """Update job status in database"""
        conn = sqlite3.connect(self.batch_database)
        cursor = conn.cursor()
        
        update_fields = ["status = ?"]
        values = [status]
        
        if started_at:
            update_fields.append("started_at = ?")
            values.append(started_at)
        
        if completed_at:
            update_fields.append("completed_at = ?")
            values.append(completed_at)
        
        if result:
            update_fields.append("result = ?")
            values.append(result)
        
        if error_message:
            update_fields.append("error_message = ?")
            values.append(error_message)
        
        values.append(job_id)
        
        cursor.execute(f'''
            UPDATE batch_jobs SET {', '.join(update_fields)}
            WHERE job_id = ?
        ''', values)
        
        conn.commit()
        conn.close()
    
    def log_job_message(self, job_id, log_level, message):
        """Log job message"""
        conn = sqlite3.connect(self.batch_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO batch_job_log (job_id, log_level, message, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (job_id, log_level, message, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def start_batch_processor(self):
        """Start the batch processor"""
        print("🧟 Batch Processor - Starting Processor")
        print("=" * 50)
        
        # Start worker threads
        for i in range(self.max_workers):
            worker_thread = threading.Thread(target=self.worker_thread, name=f"Worker-{i+1}")
            worker_thread.daemon = True
            worker_thread.start()
            self.processing_threads.append(worker_thread)
        
        print(f"✅ Batch processor started with {self.max_workers} workers")
        return True
    
    def worker_thread(self):
        """Worker thread for processing batch jobs"""
        while True:
            try:
                # Get job from queue
                job_data = self.batch_queue.get(timeout=1)
                job_id, job_name, job_type, agent_id, job_data_dict, priority = job_data
                
                # Process job
                self.process_batch_job(job_id, job_name, job_type, agent_id, job_data_dict, priority)
                
                # Mark task as done
                self.batch_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Worker thread error: {str(e)}")
                time.sleep(1)
    
    def create_sample_batch_jobs(self):
        """Create sample batch jobs for testing"""
        print("📦 Creating sample batch jobs...")
        
        # Model optimization batch for all agents
        self.create_batch_jobs_from_template(
            "model_optimization_batch",
            self.agents,
            {"optimization_level": "high", "timeout": 60}
        )
        
        # Performance analysis batch for all agents
        self.create_batch_jobs_from_template(
            "performance_analysis_batch",
            self.agents,
            {"analysis_depth": "detailed", "include_metrics": True}
        )
        
        # System health batch for all agents
        self.create_batch_jobs_from_template(
            "system_health_batch",
            self.agents,
            {"check_level": "comprehensive", "alert_threshold": 80}
        )
        
        print("✅ Sample batch jobs created successfully")
    
    def get_batch_processor_status(self):
        """Get current batch processor status"""
        conn = sqlite3.connect(self.batch_database)
        cursor = conn.cursor()
        
        # Get job counts by status
        cursor.execute('''
            SELECT status, COUNT(*) FROM batch_jobs GROUP BY status
        ''')
        status_counts = dict(cursor.fetchall())
        
        # Get queue size
        queue_size = self.batch_queue.qsize()
        
        # Get recent jobs
        cursor.execute('''
            SELECT job_id, job_name, agent_id, status, created_at
            FROM batch_jobs
            ORDER BY created_at DESC
            LIMIT 10
        ''')
        recent_jobs = cursor.fetchall()
        
        conn.close()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "status_counts": status_counts,
            "queue_size": queue_size,
            "active_workers": len(self.processing_threads),
            "recent_jobs": recent_jobs,
            "processor_active": True
        }
    
    def generate_batch_processor_report(self):
        """Generate batch processor report"""
        status = self.get_batch_processor_status()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "batch_database": self.batch_database,
            "agents": self.agents,
            "max_workers": self.max_workers,
            "processor_status": status,
            "system_status": "active"
        }
        
        with open("projects/pump_automation/batch_processor_report.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        print("✅ Batch processor report generated")

def main():
    """Main function"""
    processor = BatchProcessor()
    
    # Create sample batch jobs
    processor.create_sample_batch_jobs()
    
    # Start batch processor
    success = processor.start_batch_processor()
    
    if success:
        # Generate report
        processor.generate_batch_processor_report()
        
        # Update work log
        with open("logs/agent_work.log", "a") as f:
            f.write(f"{datetime.now()}: Agent: Batch Processor - Task: Batch Processing - Status: Completed - Notes: Batch processor active with sample jobs\n")
        
        print("\n🎉 Batch processor setup completed successfully!")
        
        # Keep running
        try:
            while True:
                time.sleep(60)
                status = processor.get_batch_processor_status()
                print(f"📦 Batch processor running... Queue: {status['queue_size']}, Workers: {status['active_workers']}")
        except KeyboardInterrupt:
            print("\n👋 Batch processor stopped by user")
    else:
        print("\n❌ Batch processor setup failed!")

if __name__ == "__main__":
    main()
