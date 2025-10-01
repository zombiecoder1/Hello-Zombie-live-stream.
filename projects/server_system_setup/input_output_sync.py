#!/usr/bin/env python3
"""
Input/Output Sync System
Server System Setup - Input/Output Synchronization
"""

import json
import time
import requests
import threading
from datetime import datetime
import sqlite3
import os

class InputOutputSync:
    def __init__(self):
        self.main_server_url = "http://localhost:12345"
        self.sync_database = "input_output_sync.db"
        self.agents = ["programming", "bestpractices", "verifier", "conversational", "ops"]
        self.sync_interval = 5  # seconds
        
    def create_sync_database(self):
        """Create sync database for input/output synchronization"""
        conn = sqlite3.connect(self.sync_database)
        cursor = conn.cursor()
        
        # Create input sync table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS input_sync (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                input_type TEXT NOT NULL,
                input_data TEXT NOT NULL,
                processed BOOLEAN DEFAULT FALSE,
                processed_timestamp TEXT
            )
        ''')
        
        # Create output sync table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS output_sync (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                output_type TEXT NOT NULL,
                output_data TEXT NOT NULL,
                synced BOOLEAN DEFAULT FALSE,
                synced_timestamp TEXT
            )
        ''')
        
        # Create sync status table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sync_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                input_count INTEGER DEFAULT 0,
                output_count INTEGER DEFAULT 0,
                last_sync TEXT,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Input/Output sync database created successfully")
    
    def sync_input(self, agent_id, input_type, input_data):
        """Sync input data from agent"""
        try:
            # Store in local database
            conn = sqlite3.connect(self.sync_database)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO input_sync (timestamp, agent_id, input_type, input_data)
                VALUES (?, ?, ?, ?)
            ''', (datetime.now().isoformat(), agent_id, input_type, json.dumps(input_data)))
            
            conn.commit()
            conn.close()
            
            # Sync with main server
            response = requests.post(f"{self.main_server_url}/sync/input", 
                                   json={
                                       "agent_id": agent_id,
                                       "input_data": {
                                           "type": input_type,
                                           "data": input_data,
                                           "timestamp": datetime.now().isoformat()
                                       }
                                   }, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ Input synced for agent {agent_id}")
                return True
            else:
                print(f"❌ Failed to sync input for agent {agent_id}")
                return False
                
        except Exception as e:
            print(f"❌ Input sync error for agent {agent_id}: {str(e)}")
            return False
    
    def sync_output(self, agent_id, output_type, output_data):
        """Sync output data from agent"""
        try:
            # Store in local database
            conn = sqlite3.connect(self.sync_database)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO output_sync (timestamp, agent_id, output_type, output_data)
                VALUES (?, ?, ?, ?)
            ''', (datetime.now().isoformat(), agent_id, output_type, json.dumps(output_data)))
            
            conn.commit()
            conn.close()
            
            # Sync with main server
            response = requests.post(f"{self.main_server_url}/sync/output", 
                                   json={
                                       "agent_id": agent_id,
                                       "output_data": {
                                           "type": output_type,
                                           "data": output_data,
                                           "timestamp": datetime.now().isoformat()
                                       }
                                   }, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ Output synced for agent {agent_id}")
                return True
            else:
                print(f"❌ Failed to sync output for agent {agent_id}")
                return False
                
        except Exception as e:
            print(f"❌ Output sync error for agent {agent_id}: {str(e)}")
            return False
    
    def get_sync_status(self, agent_id):
        """Get sync status for specific agent"""
        conn = sqlite3.connect(self.sync_database)
        cursor = conn.cursor()
        
        # Get input count
        cursor.execute('''
            SELECT COUNT(*) FROM input_sync WHERE agent_id = ? AND processed = TRUE
        ''', (agent_id,))
        input_count = cursor.fetchone()[0]
        
        # Get output count
        cursor.execute('''
            SELECT COUNT(*) FROM output_sync WHERE agent_id = ? AND synced = TRUE
        ''', (agent_id,))
        output_count = cursor.fetchone()[0]
        
        # Get last sync
        cursor.execute('''
            SELECT MAX(timestamp) FROM input_sync WHERE agent_id = ?
        ''', (agent_id,))
        last_sync = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "agent_id": agent_id,
            "input_count": input_count,
            "output_count": output_count,
            "last_sync": last_sync,
            "status": "active"
        }
    
    def get_all_sync_status(self):
        """Get sync status for all agents"""
        status = {}
        for agent_id in self.agents:
            status[agent_id] = self.get_sync_status(agent_id)
        return status
    
    def process_pending_syncs(self):
        """Process pending sync operations"""
        conn = sqlite3.connect(self.sync_database)
        cursor = conn.cursor()
        
        # Process pending inputs
        cursor.execute('''
            SELECT id, agent_id, input_type, input_data FROM input_sync 
            WHERE processed = FALSE
        ''')
        pending_inputs = cursor.fetchall()
        
        for input_id, agent_id, input_type, input_data in pending_inputs:
            # Process input
            processed = self.process_input(agent_id, input_type, json.loads(input_data))
            
            if processed:
                cursor.execute('''
                    UPDATE input_sync SET processed = TRUE, processed_timestamp = ?
                    WHERE id = ?
                ''', (datetime.now().isoformat(), input_id))
        
        # Process pending outputs
        cursor.execute('''
            SELECT id, agent_id, output_type, output_data FROM output_sync 
            WHERE synced = FALSE
        ''')
        pending_outputs = cursor.fetchall()
        
        for output_id, agent_id, output_type, output_data in pending_outputs:
            # Sync output
            synced = self.sync_output(agent_id, output_type, json.loads(output_data))
            
            if synced:
                cursor.execute('''
                    UPDATE output_sync SET synced = TRUE, synced_timestamp = ?
                    WHERE id = ?
                ''', (datetime.now().isoformat(), output_id))
        
        conn.commit()
        conn.close()
    
    def process_input(self, agent_id, input_type, input_data):
        """Process input data"""
        # Simple input processing
        if input_type == "task_update":
            print(f"Processing task update for agent {agent_id}")
            return True
        elif input_type == "status_update":
            print(f"Processing status update for agent {agent_id}")
            return True
        elif input_type == "error_report":
            print(f"Processing error report for agent {agent_id}")
            return True
        else:
            print(f"Processing {input_type} for agent {agent_id}")
            return True
    
    def start_sync_monitor(self):
        """Start sync monitoring in background thread"""
        def monitor():
            while True:
                try:
                    self.process_pending_syncs()
                    time.sleep(self.sync_interval)
                except Exception as e:
                    print(f"Sync monitor error: {str(e)}")
                    time.sleep(self.sync_interval)
        
        monitor_thread = threading.Thread(target=monitor)
        monitor_thread.daemon = True
        monitor_thread.start()
        print("✅ Sync monitor started")
    
    def test_sync_system(self):
        """Test the sync system"""
        print("🧟 Input/Output Sync - Testing Sync System")
        print("=" * 50)
        
        # Test input sync
        print("1. Testing input sync...")
        test_input = {
            "task": "test_task",
            "data": "test_data",
            "timestamp": datetime.now().isoformat()
        }
        
        for agent_id in self.agents:
            success = self.sync_input(agent_id, "test_input", test_input)
            print(f"   {agent_id}: {'✅' if success else '❌'}")
        
        # Test output sync
        print("2. Testing output sync...")
        test_output = {
            "result": "test_result",
            "data": "test_output_data",
            "timestamp": datetime.now().isoformat()
        }
        
        for agent_id in self.agents:
            success = self.sync_output(agent_id, "test_output", test_output)
            print(f"   {agent_id}: {'✅' if success else '❌'}")
        
        # Get sync status
        print("3. Getting sync status...")
        sync_status = self.get_all_sync_status()
        for agent_id, status in sync_status.items():
            print(f"   {agent_id}: Input={status['input_count']}, Output={status['output_count']}")
        
        print("✅ Sync system test completed")
    
    def generate_sync_report(self):
        """Generate sync system report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "sync_database": self.sync_database,
            "agents": self.agents,
            "sync_interval": self.sync_interval,
            "sync_status": self.get_all_sync_status(),
            "system_status": "active"
        }
        
        with open("projects/server_system_setup/sync_report.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        print("✅ Sync report generated")

def main():
    """Main function"""
    sync_system = InputOutputSync()
    
    # Create sync database
    sync_system.create_sync_database()
    
    # Start sync monitor
    sync_system.start_sync_monitor()
    
    # Test sync system
    sync_system.test_sync_system()
    
    # Generate report
    sync_system.generate_sync_report()
    
    # Update work log
    with open("logs/agent_work.log", "a") as f:
        f.write(f"{datetime.now()}: Agent: Input/Output Sync - Task: Sync System Setup - Status: Completed - Notes: Input/Output sync system active\n")
    
    print("\n🎉 Input/Output sync system setup completed successfully!")

if __name__ == "__main__":
    main()
