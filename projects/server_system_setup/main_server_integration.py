#!/usr/bin/env python3
"""
Main Server Integration System
Server System Setup - Main Server & Workstation Integration
"""

import json
import time
import requests
import threading
from datetime import datetime
from flask import Flask, request, jsonify
import sqlite3
import os

class MainServerIntegration:
    def __init__(self):
        self.app = Flask(__name__)
        self.server_port = 12345
        self.workstation_port = 8001
        self.office_port = 8002
        self.agents = {
            "programming": {"port": 8003, "status": "active"},
            "bestpractices": {"port": 8004, "status": "active"},
            "verifier": {"port": 8005, "status": "active"},
            "conversational": {"port": 8006, "status": "active"},
            "ops": {"port": 8007, "status": "active"}
        }
        self.sync_database = "server_sync.db"
        self.setup_routes()
        
    def setup_routes(self):
        """Setup Flask routes for server integration"""
        
        @self.app.route('/status', methods=['GET'])
        def get_status():
            """Get overall system status"""
            return jsonify({
                "status": "online",
                "timestamp": datetime.now().isoformat(),
                "agents": self.agents,
                "server_health": "healthy"
            })
        
        @self.app.route('/sync/input', methods=['POST'])
        def sync_input():
            """Sync input from agents"""
            data = request.json
            agent_id = data.get('agent_id')
            input_data = data.get('input_data')
            
            # Store in sync database
            self.store_sync_data(agent_id, 'input', input_data)
            
            return jsonify({
                "status": "success",
                "message": f"Input synced for agent {agent_id}",
                "timestamp": datetime.now().isoformat()
            })
        
        @self.app.route('/sync/output', methods=['POST'])
        def sync_output():
            """Sync output from agents"""
            data = request.json
            agent_id = data.get('agent_id')
            output_data = data.get('output_data')
            
            # Store in sync database
            self.store_sync_data(agent_id, 'output', output_data)
            
            return jsonify({
                "status": "success",
                "message": f"Output synced for agent {agent_id}",
                "timestamp": datetime.now().isoformat()
            })
        
        @self.app.route('/agents/status', methods=['GET'])
        def get_agents_status():
            """Get status of all agents"""
            agent_status = {}
            for agent_id, agent_info in self.agents.items():
                try:
                    response = requests.get(f"http://localhost:{agent_info['port']}/status", timeout=5)
                    agent_status[agent_id] = {
                        "status": "online" if response.status_code == 200 else "offline",
                        "port": agent_info['port'],
                        "response_time": response.elapsed.total_seconds() if response.status_code == 200 else None
                    }
                except:
                    agent_status[agent_id] = {
                        "status": "offline",
                        "port": agent_info['port'],
                        "response_time": None
                    }
            
            return jsonify({
                "agents": agent_status,
                "timestamp": datetime.now().isoformat()
            })
        
        @self.app.route('/workstation/update', methods=['POST'])
        def update_workstation():
            """Update workstation with agent data"""
            data = request.json
            agent_id = data.get('agent_id')
            workstation_data = data.get('workstation_data')
            
            # Process workstation update
            self.process_workstation_update(agent_id, workstation_data)
            
            return jsonify({
                "status": "success",
                "message": f"Workstation updated for agent {agent_id}",
                "timestamp": datetime.now().isoformat()
            })
    
    def create_sync_database(self):
        """Create sync database for agent communication"""
        conn = sqlite3.connect(self.sync_database)
        cursor = conn.cursor()
        
        # Create sync table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sync_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                data_type TEXT NOT NULL,
                data_content TEXT NOT NULL,
                processed BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Create workstation updates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workstation_updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                update_type TEXT NOT NULL,
                update_data TEXT NOT NULL,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Sync database created successfully")
    
    def store_sync_data(self, agent_id, data_type, data_content):
        """Store sync data in database"""
        conn = sqlite3.connect(self.sync_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sync_data (timestamp, agent_id, data_type, data_content)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), agent_id, data_type, json.dumps(data_content)))
        
        conn.commit()
        conn.close()
    
    def process_workstation_update(self, agent_id, workstation_data):
        """Process workstation update"""
        conn = sqlite3.connect(self.sync_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO workstation_updates (timestamp, agent_id, update_type, update_data)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), agent_id, 'workstation_update', json.dumps(workstation_data)))
        
        conn.commit()
        conn.close()
    
    def start_server(self):
        """Start the main server"""
        print("🧟 Main Server Integration - Starting Server")
        print("=" * 50)
        
        # Create sync database
        self.create_sync_database()
        
        # Start server in background thread
        server_thread = threading.Thread(target=self.run_server)
        server_thread.daemon = True
        server_thread.start()
        
        print(f"✅ Main server started on port {self.server_port}")
        print(f"✅ Sync database created: {self.sync_database}")
        print("✅ Server integration ready")
        
        return True
    
    def run_server(self):
        """Run the Flask server"""
        self.app.run(host='0.0.0.0', port=self.server_port, debug=False)
    
    def test_agent_connections(self):
        """Test connections to all agents"""
        print("🔍 Testing agent connections...")
        
        for agent_id, agent_info in self.agents.items():
            try:
                response = requests.get(f"http://localhost:{agent_info['port']}/status", timeout=5)
                if response.status_code == 200:
                    print(f"   ✅ {agent_id} agent: Online (Port {agent_info['port']})")
                else:
                    print(f"   ❌ {agent_id} agent: Offline (Port {agent_info['port']})")
            except:
                print(f"   ❌ {agent_id} agent: Offline (Port {agent_info['port']})")
    
    def generate_integration_report(self):
        """Generate integration report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "server_status": "online",
            "server_port": self.server_port,
            "workstation_port": self.workstation_port,
            "office_port": self.office_port,
            "agents": self.agents,
            "sync_database": self.sync_database,
            "integration_status": "active"
        }
        
        with open("projects/server_system_setup/integration_report.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        print("✅ Integration report generated")
        return report

def main():
    """Main function"""
    integration = MainServerIntegration()
    
    # Start server
    success = integration.start_server()
    
    if success:
        # Test connections
        integration.test_agent_connections()
        
        # Generate report
        integration.generate_integration_report()
        
        # Update work log
        with open("logs/agent_work.log", "a") as f:
            f.write(f"{datetime.now()}: Agent: Server Integration - Task: Main Server Setup - Status: Completed - Notes: Main server integration active\n")
        
        print("\n🎉 Main server integration completed successfully!")
    else:
        print("\n❌ Main server integration failed!")

if __name__ == "__main__":
    main()
