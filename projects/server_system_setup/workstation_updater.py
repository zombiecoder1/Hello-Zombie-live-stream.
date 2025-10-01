#!/usr/bin/env python3
"""
Workstation Updater System
Server System Setup - Workstation Updates
"""

import json
import time
import requests
from datetime import datetime
import os
import sqlite3

class WorkstationUpdater:
    def __init__(self):
        self.workstation_database = "workstation_updates.db"
        self.agents = ["programming", "bestpractices", "verifier", "conversational", "ops"]
        self.update_interval = 10  # seconds
        
    def create_workstation_database(self):
        """Create workstation database for updates"""
        conn = sqlite3.connect(self.workstation_database)
        cursor = conn.cursor()
        
        # Create workstation updates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workstation_updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                update_type TEXT NOT NULL,
                update_data TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                processed_timestamp TEXT
            )
        ''')
        
        # Create agent status table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                status TEXT NOT NULL,
                last_activity TEXT,
                performance_metrics TEXT
            )
        ''')
        
        # Create workstation metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workstation_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL,
                network_usage REAL,
                active_agents INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Workstation database created successfully")
    
    def update_agent_status(self, agent_id, status, performance_metrics=None):
        """Update agent status in workstation"""
        conn = sqlite3.connect(self.workstation_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO agent_status (timestamp, agent_id, status, last_activity, performance_metrics)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            agent_id,
            status,
            datetime.now().isoformat(),
            json.dumps(performance_metrics) if performance_metrics else None
        ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Agent {agent_id} status updated: {status}")
    
    def process_workstation_update(self, agent_id, update_type, update_data):
        """Process workstation update from agent"""
        conn = sqlite3.connect(self.workstation_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO workstation_updates (timestamp, agent_id, update_type, update_data)
            VALUES (?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            agent_id,
            update_type,
            json.dumps(update_data)
        ))
        
        conn.commit()
        conn.close()
        
        # Process update based on type
        if update_type == "task_completion":
            self.handle_task_completion(agent_id, update_data)
        elif update_type == "error_report":
            self.handle_error_report(agent_id, update_data)
        elif update_type == "performance_update":
            self.handle_performance_update(agent_id, update_data)
        elif update_type == "status_change":
            self.handle_status_change(agent_id, update_data)
        
        print(f"✅ Workstation update processed for agent {agent_id}: {update_type}")
    
    def handle_task_completion(self, agent_id, update_data):
        """Handle task completion update"""
        print(f"🎉 Task completed by agent {agent_id}: {update_data.get('task_name', 'Unknown')}")
        
        # Update agent status
        self.update_agent_status(agent_id, "task_completed", {
            "task_name": update_data.get('task_name'),
            "completion_time": update_data.get('completion_time'),
            "result": update_data.get('result')
        })
    
    def handle_error_report(self, agent_id, update_data):
        """Handle error report update"""
        print(f"⚠️ Error reported by agent {agent_id}: {update_data.get('error_message', 'Unknown error')}")
        
        # Update agent status
        self.update_agent_status(agent_id, "error", {
            "error_message": update_data.get('error_message'),
            "error_type": update_data.get('error_type'),
            "severity": update_data.get('severity')
        })
    
    def handle_performance_update(self, agent_id, update_data):
        """Handle performance update"""
        print(f"📊 Performance update from agent {agent_id}")
        
        # Update agent status
        self.update_agent_status(agent_id, "performance_updated", update_data)
    
    def handle_status_change(self, agent_id, update_data):
        """Handle status change update"""
        new_status = update_data.get('new_status', 'unknown')
        print(f"🔄 Status change for agent {agent_id}: {new_status}")
        
        # Update agent status
        self.update_agent_status(agent_id, new_status, update_data)
    
    def get_workstation_status(self):
        """Get current workstation status"""
        conn = sqlite3.connect(self.workstation_database)
        cursor = conn.cursor()
        
        # Get latest agent statuses
        agent_statuses = {}
        for agent_id in self.agents:
            cursor.execute('''
                SELECT status, last_activity, performance_metrics
                FROM agent_status
                WHERE agent_id = ?
                ORDER BY timestamp DESC
                LIMIT 1
            ''', (agent_id,))
            
            result = cursor.fetchone()
            if result:
                agent_statuses[agent_id] = {
                    "status": result[0],
                    "last_activity": result[1],
                    "performance_metrics": json.loads(result[2]) if result[2] else None
                }
            else:
                agent_statuses[agent_id] = {
                    "status": "unknown",
                    "last_activity": None,
                    "performance_metrics": None
                }
        
        # Get latest workstation metrics
        cursor.execute('''
            SELECT cpu_usage, memory_usage, disk_usage, network_usage, active_agents
            FROM workstation_metrics
            ORDER BY timestamp DESC
            LIMIT 1
        ''')
        
        metrics_result = cursor.fetchone()
        if metrics_result:
            workstation_metrics = {
                "cpu_usage": metrics_result[0],
                "memory_usage": metrics_result[1],
                "disk_usage": metrics_result[2],
                "network_usage": metrics_result[3],
                "active_agents": metrics_result[4]
            }
        else:
            workstation_metrics = {
                "cpu_usage": 0,
                "memory_usage": 0,
                "disk_usage": 0,
                "network_usage": 0,
                "active_agents": 0
            }
        
        conn.close()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "agent_statuses": agent_statuses,
            "workstation_metrics": workstation_metrics,
            "total_agents": len(self.agents),
            "active_agents": sum(1 for status in agent_statuses.values() if status["status"] != "unknown")
        }
    
    def collect_system_metrics(self):
        """Collect system performance metrics"""
        import psutil
        
        try:
            cpu_usage = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Count active agents
            active_agents = 0
            for agent_id in self.agents:
                status = self.get_agent_status(agent_id)
                if status and status != "unknown":
                    active_agents += 1
            
            metrics = {
                "cpu_usage": cpu_usage,
                "memory_usage": memory.percent,
                "disk_usage": disk.percent,
                "network_usage": 0,  # Placeholder
                "active_agents": active_agents
            }
            
            # Store metrics
            conn = sqlite3.connect(self.workstation_database)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO workstation_metrics (timestamp, cpu_usage, memory_usage, disk_usage, network_usage, active_agents)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                metrics["cpu_usage"],
                metrics["memory_usage"],
                metrics["disk_usage"],
                metrics["network_usage"],
                metrics["active_agents"]
            ))
            
            conn.commit()
            conn.close()
            
            return metrics
            
        except Exception as e:
            print(f"Error collecting system metrics: {str(e)}")
            return None
    
    def get_agent_status(self, agent_id):
        """Get current status of specific agent"""
        conn = sqlite3.connect(self.workstation_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT status FROM agent_status
            WHERE agent_id = ?
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (agent_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else "unknown"
    
    def test_workstation_updates(self):
        """Test workstation update system"""
        print("🧟 Workstation Updater - Testing Update System")
        print("=" * 50)
        
        # Test agent status updates
        print("1. Testing agent status updates...")
        for agent_id in self.agents:
            self.update_agent_status(agent_id, "active", {
                "cpu_usage": 25.5,
                "memory_usage": 512,
                "last_task": "test_task"
            })
        
        # Test workstation updates
        print("2. Testing workstation updates...")
        test_updates = [
            ("programming", "task_completion", {
                "task_name": "model_optimization",
                "completion_time": datetime.now().isoformat(),
                "result": "success"
            }),
            ("bestpractices", "error_report", {
                "error_message": "Test error",
                "error_type": "warning",
                "severity": "low"
            }),
            ("verifier", "performance_update", {
                "cpu_usage": 30.0,
                "memory_usage": 256,
                "response_time": 0.5
            })
        ]
        
        for agent_id, update_type, update_data in test_updates:
            self.process_workstation_update(agent_id, update_type, update_data)
        
        # Test system metrics collection
        print("3. Testing system metrics collection...")
        metrics = self.collect_system_metrics()
        if metrics:
            print(f"   CPU: {metrics['cpu_usage']}%")
            print(f"   Memory: {metrics['memory_usage']}%")
            print(f"   Disk: {metrics['disk_usage']}%")
            print(f"   Active Agents: {metrics['active_agents']}")
        
        # Get workstation status
        print("4. Getting workstation status...")
        status = self.get_workstation_status()
        print(f"   Total Agents: {status['total_agents']}")
        print(f"   Active Agents: {status['active_agents']}")
        
        print("✅ Workstation update test completed")
    
    def generate_workstation_report(self):
        """Generate workstation report"""
        status = self.get_workstation_status()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "workstation_database": self.workstation_database,
            "agents": self.agents,
            "workstation_status": status,
            "update_interval": self.update_interval,
            "system_status": "active"
        }
        
        with open("projects/server_system_setup/workstation_update_report.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        print("✅ Workstation report generated")

def main():
    """Main function"""
    updater = WorkstationUpdater()
    
    # Create workstation database
    updater.create_workstation_database()
    
    # Test workstation updates
    updater.test_workstation_updates()
    
    # Generate report
    updater.generate_workstation_report()
    
    # Update work log
    with open("logs/agent_work.log", "a") as f:
        f.write(f"{datetime.now()}: Agent: Workstation Updater - Task: Workstation Updates - Status: Completed - Notes: Workstation update system active\n")
    
    print("\n🎉 Workstation update system setup completed successfully!")

if __name__ == "__main__":
    main()
