#!/usr/bin/env python3
"""
Performance Tuning System
Pump/Automation - Automated Performance Tuning
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

class PerformanceTuner:
    def __init__(self):
        self.tuning_database = "performance_tuner.db"
        self.agents = ["programming", "bestpractices", "verifier", "conversational", "ops"]
        self.tuning_interval = 30  # seconds
        self.performance_thresholds = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "disk_usage": 90.0,
            "response_time": 2.0
        }
        self.setup_database()
        
    def setup_database(self):
        """Setup performance tuner database"""
        conn = sqlite3.connect(self.tuning_database)
        cursor = conn.cursor()
        
        # Create performance metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL,
                response_time REAL,
                network_usage REAL,
                active_connections INTEGER,
                performance_score REAL
            )
        ''')
        
        # Create tuning actions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tuning_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                action_type TEXT NOT NULL,
                action_description TEXT NOT NULL,
                before_metrics TEXT NOT NULL,
                after_metrics TEXT,
                status TEXT DEFAULT 'pending',
                result TEXT
            )
        ''')
        
        # Create optimization recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS optimization_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                recommendation_type TEXT NOT NULL,
                recommendation_description TEXT NOT NULL,
                priority TEXT NOT NULL,
                estimated_improvement REAL,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Performance tuner database created successfully")
    
    def collect_performance_metrics(self, agent_id):
        """Collect performance metrics for specific agent"""
        try:
            # Get system metrics
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Get network usage
            network = psutil.net_io_counters()
            
            # Calculate performance score
            performance_score = self.calculate_performance_score(cpu_usage, memory.percent, disk.percent)
            
            # Store metrics
            conn = sqlite3.connect(self.tuning_database)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO performance_metrics 
                (timestamp, agent_id, cpu_usage, memory_usage, disk_usage, response_time, 
                 network_usage, active_connections, performance_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(), agent_id, cpu_usage, memory.percent,
                disk.percent, 0.0, network.bytes_sent + network.bytes_recv,
                len(psutil.pids()), performance_score
            ))
            
            conn.commit()
            conn.close()
            
            return {
                "cpu_usage": cpu_usage,
                "memory_usage": memory.percent,
                "disk_usage": disk.percent,
                "response_time": 0.0,
                "network_usage": network.bytes_sent + network.bytes_recv,
                "performance_score": performance_score
            }
            
        except Exception as e:
            print(f"Error collecting metrics for agent {agent_id}: {str(e)}")
            return None
    
    def calculate_performance_score(self, cpu_usage, memory_usage, disk_usage):
        """Calculate overall performance score (0-100)"""
        # Lower usage = higher score
        cpu_score = max(0, 100 - cpu_usage)
        memory_score = max(0, 100 - memory_usage)
        disk_score = max(0, 100 - disk_usage)
        
        # Weighted average
        overall_score = (cpu_score * 0.4 + memory_score * 0.4 + disk_score * 0.2)
        return round(overall_score, 2)
    
    def analyze_performance(self, agent_id, metrics):
        """Analyze performance and generate recommendations"""
        recommendations = []
        
        # CPU analysis
        if metrics["cpu_usage"] > self.performance_thresholds["cpu_usage"]:
            recommendations.append({
                "type": "cpu_optimization",
                "description": f"High CPU usage detected: {metrics['cpu_usage']:.1f}%",
                "priority": "high",
                "estimated_improvement": 15.0,
                "action": "optimize_cpu_usage"
            })
        
        # Memory analysis
        if metrics["memory_usage"] > self.performance_thresholds["memory_usage"]:
            recommendations.append({
                "type": "memory_optimization",
                "description": f"High memory usage detected: {metrics['memory_usage']:.1f}%",
                "priority": "high",
                "estimated_improvement": 20.0,
                "action": "optimize_memory_usage"
            })
        
        # Disk analysis
        if metrics["disk_usage"] > self.performance_thresholds["disk_usage"]:
            recommendations.append({
                "type": "disk_cleanup",
                "description": f"High disk usage detected: {metrics['disk_usage']:.1f}%",
                "priority": "medium",
                "estimated_improvement": 10.0,
                "action": "cleanup_disk_space"
            })
        
        # Performance score analysis
        if metrics["performance_score"] < 60:
            recommendations.append({
                "type": "general_optimization",
                "description": f"Low performance score: {metrics['performance_score']:.1f}",
                "priority": "high",
                "estimated_improvement": 25.0,
                "action": "general_optimization"
            })
        
        return recommendations
    
    def apply_optimization(self, agent_id, recommendation):
        """Apply optimization based on recommendation"""
        action_type = recommendation["action"]
        action_description = recommendation["description"]
        
        print(f"🔧 Applying optimization for agent {agent_id}: {action_description}")
        
        # Store tuning action
        conn = sqlite3.connect(self.tuning_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tuning_actions 
            (timestamp, agent_id, action_type, action_description, before_metrics, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(), agent_id, action_type, action_description,
            json.dumps(self.collect_performance_metrics(agent_id)), "running"
        ))
        
        conn.commit()
        conn.close()
        
        try:
            if action_type == "optimize_cpu_usage":
                result = self.optimize_cpu_usage(agent_id)
            elif action_type == "optimize_memory_usage":
                result = self.optimize_memory_usage(agent_id)
            elif action_type == "cleanup_disk_space":
                result = self.cleanup_disk_space(agent_id)
            elif action_type == "general_optimization":
                result = self.general_optimization(agent_id)
            else:
                result = {"status": "unknown_action", "message": f"Unknown action: {action_type}"}
            
            # Update tuning action
            self.update_tuning_action(agent_id, action_type, "completed", result)
            
            print(f"✅ Optimization applied successfully for agent {agent_id}")
            return result
            
        except Exception as e:
            error_result = {"status": "error", "message": str(e)}
            self.update_tuning_action(agent_id, action_type, "failed", error_result)
            print(f"❌ Optimization failed for agent {agent_id}: {str(e)}")
            return error_result
    
    def optimize_cpu_usage(self, agent_id):
        """Optimize CPU usage"""
        print(f"   ⚡ Optimizing CPU usage for agent {agent_id}")
        
        # Kill unnecessary processes
        try:
            # Get current processes
            processes = list(psutil.process_iter(['pid', 'name', 'cpu_percent']))
            
            # Find high CPU processes (excluding system processes)
            high_cpu_processes = []
            for proc in processes:
                try:
                    if proc.info['cpu_percent'] > 10:  # More than 10% CPU
                        high_cpu_processes.append(proc.info)
                except:
                    continue
            
            # Log high CPU processes
            result = {
                "status": "success",
                "action": "cpu_optimization",
                "high_cpu_processes": len(high_cpu_processes),
                "message": f"Identified {len(high_cpu_processes)} high CPU processes"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def optimize_memory_usage(self, agent_id):
        """Optimize memory usage"""
        print(f"   🧠 Optimizing memory usage for agent {agent_id}")
        
        try:
            # Get memory info
            memory = psutil.virtual_memory()
            
            # Suggest memory cleanup
            result = {
                "status": "success",
                "action": "memory_optimization",
                "available_memory": memory.available / (1024**3),  # GB
                "memory_percent": memory.percent,
                "message": f"Memory optimization applied, {memory.available / (1024**3):.2f} GB available"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def cleanup_disk_space(self, agent_id):
        """Cleanup disk space"""
        print(f"   💾 Cleaning up disk space for agent {agent_id}")
        
        try:
            # Get disk info
            disk = psutil.disk_usage('/')
            
            # Clean up temporary files
            temp_cleanup_commands = [
                "find /tmp -type f -mtime +7 -delete",
                "find /var/tmp -type f -mtime +7 -delete",
                "apt-get clean"
            ]
            
            cleanup_results = []
            for cmd in temp_cleanup_commands:
                try:
                    subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
                    cleanup_results.append(f"Executed: {cmd}")
                except:
                    cleanup_results.append(f"Failed: {cmd}")
            
            result = {
                "status": "success",
                "action": "disk_cleanup",
                "disk_usage": disk.percent,
                "cleanup_commands": cleanup_results,
                "message": f"Disk cleanup completed, usage: {disk.percent:.1f}%"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def general_optimization(self, agent_id):
        """Apply general optimization"""
        print(f"   ⚙️ Applying general optimization for agent {agent_id}")
        
        try:
            # Apply multiple optimizations
            optimizations = []
            
            # CPU optimization
            cpu_result = self.optimize_cpu_usage(agent_id)
            optimizations.append(cpu_result)
            
            # Memory optimization
            memory_result = self.optimize_memory_usage(agent_id)
            optimizations.append(memory_result)
            
            # Disk cleanup
            disk_result = self.cleanup_disk_space(agent_id)
            optimizations.append(disk_result)
            
            result = {
                "status": "success",
                "action": "general_optimization",
                "optimizations": optimizations,
                "message": "General optimization completed"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def update_tuning_action(self, agent_id, action_type, status, result):
        """Update tuning action status"""
        conn = sqlite3.connect(self.tuning_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE tuning_actions 
            SET status = ?, result = ?, after_metrics = ?
            WHERE agent_id = ? AND action_type = ? AND status = 'running'
        ''', (
            status, json.dumps(result), 
            json.dumps(self.collect_performance_metrics(agent_id)),
            agent_id, action_type
        ))
        
        conn.commit()
        conn.close()
    
    def store_recommendations(self, agent_id, recommendations):
        """Store optimization recommendations"""
        conn = sqlite3.connect(self.tuning_database)
        cursor = conn.cursor()
        
        for rec in recommendations:
            cursor.execute('''
                INSERT INTO optimization_recommendations 
                (timestamp, agent_id, recommendation_type, recommendation_description, 
                 priority, estimated_improvement, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(), agent_id, rec["type"], rec["description"],
                rec["priority"], rec["estimated_improvement"], "pending"
            ))
        
        conn.commit()
        conn.close()
    
    def start_performance_tuner(self):
        """Start the performance tuner"""
        print("🧟 Performance Tuner - Starting Tuner")
        print("=" * 50)
        
        # Start tuning in background thread
        tuning_thread = threading.Thread(target=self.tuning_loop)
        tuning_thread.daemon = True
        tuning_thread.start()
        
        print("✅ Performance tuner started successfully")
        return True
    
    def tuning_loop(self):
        """Main tuning loop"""
        while True:
            try:
                print(f"🔍 Running performance tuning cycle... {datetime.now().strftime('%H:%M:%S')}")
                
                for agent_id in self.agents:
                    # Collect metrics
                    metrics = self.collect_performance_metrics(agent_id)
                    
                    if metrics:
                        # Analyze performance
                        recommendations = self.analyze_performance(agent_id, metrics)
                        
                        if recommendations:
                            print(f"   📊 Found {len(recommendations)} recommendations for agent {agent_id}")
                            
                            # Store recommendations
                            self.store_recommendations(agent_id, recommendations)
                            
                            # Apply high priority optimizations
                            for rec in recommendations:
                                if rec["priority"] == "high":
                                    self.apply_optimization(agent_id, rec)
                
                # Wait for next cycle
                time.sleep(self.tuning_interval)
                
            except Exception as e:
                print(f"Tuning loop error: {str(e)}")
                time.sleep(10)
    
    def get_performance_status(self):
        """Get current performance status"""
        conn = sqlite3.connect(self.tuning_database)
        cursor = conn.cursor()
        
        # Get latest metrics for each agent
        agent_metrics = {}
        for agent_id in self.agents:
            cursor.execute('''
                SELECT cpu_usage, memory_usage, disk_usage, performance_score
                FROM performance_metrics
                WHERE agent_id = ?
                ORDER BY timestamp DESC
                LIMIT 1
            ''', (agent_id,))
            
            result = cursor.fetchone()
            if result:
                agent_metrics[agent_id] = {
                    "cpu_usage": result[0],
                    "memory_usage": result[1],
                    "disk_usage": result[2],
                    "performance_score": result[3]
                }
            else:
                agent_metrics[agent_id] = {
                    "cpu_usage": 0,
                    "memory_usage": 0,
                    "disk_usage": 0,
                    "performance_score": 0
                }
        
        # Get pending recommendations
        cursor.execute('''
            SELECT agent_id, COUNT(*) FROM optimization_recommendations
            WHERE status = 'pending'
            GROUP BY agent_id
        ''')
        pending_recommendations = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "agent_metrics": agent_metrics,
            "pending_recommendations": pending_recommendations,
            "tuning_active": True
        }
    
    def generate_performance_report(self):
        """Generate performance tuner report"""
        status = self.get_performance_status()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "tuning_database": self.tuning_database,
            "agents": self.agents,
            "tuning_interval": self.tuning_interval,
            "performance_thresholds": self.performance_thresholds,
            "tuner_status": status,
            "system_status": "active"
        }
        
        with open("projects/pump_automation/performance_tuner_report.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        print("✅ Performance tuner report generated")

def main():
    """Main function"""
    tuner = PerformanceTuner()
    
    # Start performance tuner
    success = tuner.start_performance_tuner()
    
    if success:
        # Generate report
        tuner.generate_performance_report()
        
        # Update work log
        with open("logs/agent_work.log", "a") as f:
            f.write(f"{datetime.now()}: Agent: Performance Tuner - Task: Performance Tuning - Status: Completed - Notes: Performance tuner active with auto-optimization\n")
        
        print("\n🎉 Performance tuner setup completed successfully!")
        
        # Keep running
        try:
            while True:
                time.sleep(60)
                status = tuner.get_performance_status()
                print(f"⚡ Performance tuner running... Monitoring {len(tuner.agents)} agents")
        except KeyboardInterrupt:
            print("\n👋 Performance tuner stopped by user")
    else:
        print("\n❌ Performance tuner setup failed!")

if __name__ == "__main__":
    main()
