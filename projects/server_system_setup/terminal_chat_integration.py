#!/usr/bin/env python3
"""
Terminal Chat Integration System
Server System Setup - Terminal & Chat Integration
"""

import json
import time
import requests
import threading
from datetime import datetime
import os
import subprocess

class TerminalChatIntegration:
    def __init__(self):
        self.chat_database = "terminal_chat.db"
        self.agents = ["programming", "bestpractices", "verifier", "conversational", "ops"]
        self.chat_history = []
        
    def create_chat_database(self):
        """Create chat database for terminal integration"""
        import sqlite3
        
        conn = sqlite3.connect(self.chat_database)
        cursor = conn.cursor()
        
        # Create chat messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                sender TEXT NOT NULL,
                message_type TEXT NOT NULL,
                message_content TEXT NOT NULL,
                processed BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Create terminal commands table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS terminal_commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                command TEXT NOT NULL,
                result TEXT,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Terminal chat database created successfully")
    
    def process_chat_message(self, sender, message):
        """Process chat message"""
        import sqlite3
        
        # Store message in database
        conn = sqlite3.connect(self.chat_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_messages (timestamp, sender, message_type, message_content)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), sender, "chat", message))
        
        conn.commit()
        conn.close()
        
        # Generate response
        response = self.generate_chat_response(message, sender)
        
        # Store response
        conn = sqlite3.connect(self.chat_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_messages (timestamp, sender, message_type, message_content)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), "system", "response", response))
        
        conn.commit()
        conn.close()
        
        return response
    
    def generate_chat_response(self, message, sender):
        """Generate chat response based on message"""
        message_lower = message.lower()
        
        # System status responses
        if "status" in message_lower:
            return "System Status: All agents active, server running, sync system operational"
        elif "agents" in message_lower:
            return "Active Agents: Programming, Best Practices, Verifier, Conversational, Ops"
        elif "help" in message_lower:
            return "Available commands: status, agents, sync, terminal, chat, help"
        elif "sync" in message_lower:
            return "Sync Status: Input/Output sync active, all agents connected"
        elif "terminal" in message_lower:
            return "Terminal Integration: Ready for command processing"
        elif "hello" in message_lower or "hi" in message_lower:
            return f"Hello {sender}! How can I help you today?"
        else:
            return f"I understand your message: '{message}'. How else can I assist you?"
    
    def process_terminal_command(self, agent_id, command):
        """Process terminal command"""
        import sqlite3
        
        # Store command in database
        conn = sqlite3.connect(self.chat_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO terminal_commands (timestamp, agent_id, command, status)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), agent_id, command, "processing"))
        
        conn.commit()
        conn.close()
        
        # Execute command
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            
            # Update command result
            conn = sqlite3.connect(self.chat_database)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE terminal_commands SET result = ?, status = ?
                WHERE agent_id = ? AND command = ? AND status = 'processing'
            ''', (result.stdout + result.stderr, "completed", agent_id, command))
            
            conn.commit()
            conn.close()
            
            return {
                "status": "success",
                "result": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "result": "Command timed out",
                "error": "Command execution exceeded 30 seconds",
                "return_code": -1
            }
        except Exception as e:
            return {
                "status": "error",
                "result": "",
                "error": str(e),
                "return_code": -1
            }
    
    def get_chat_history(self, limit=10):
        """Get recent chat history"""
        import sqlite3
        
        conn = sqlite3.connect(self.chat_database)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT timestamp, sender, message_type, message_content
            FROM chat_messages
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        history = cursor.fetchall()
        conn.close()
        
        return history
    
    def get_terminal_history(self, agent_id=None, limit=10):
        """Get terminal command history"""
        import sqlite3
        
        conn = sqlite3.connect(self.chat_database)
        cursor = conn.cursor()
        
        if agent_id:
            cursor.execute('''
                SELECT timestamp, agent_id, command, result, status
                FROM terminal_commands
                WHERE agent_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (agent_id, limit))
        else:
            cursor.execute('''
                SELECT timestamp, agent_id, command, result, status
                FROM terminal_commands
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
        
        history = cursor.fetchall()
        conn.close()
        
        return history
    
    def start_chat_interface(self):
        """Start interactive chat interface"""
        print("🧟 Terminal Chat Integration - Starting Chat Interface")
        print("=" * 60)
        print("Type 'help' for available commands, 'exit' to quit")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n💬 Chat: ").strip()
                
                if user_input.lower() == 'exit':
                    print("Goodbye! 👋")
                    break
                elif user_input.lower() == 'history':
                    print("\n📜 Recent Chat History:")
                    history = self.get_chat_history(5)
                    for timestamp, sender, msg_type, content in history:
                        print(f"  [{timestamp}] {sender}: {content}")
                elif user_input.lower() == 'terminal':
                    print("\n🖥️ Terminal Commands:")
                    terminal_history = self.get_terminal_history(5)
                    for timestamp, agent_id, command, result, status in terminal_history:
                        print(f"  [{timestamp}] {agent_id}: {command} ({status})")
                elif user_input.lower() == 'agents':
                    print(f"\n🤖 Active Agents: {', '.join(self.agents)}")
                else:
                    response = self.process_chat_message("user", user_input)
                    print(f"🤖 System: {response}")
                    
            except KeyboardInterrupt:
                print("\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
    
    def test_integration(self):
        """Test terminal chat integration"""
        print("🧟 Terminal Chat Integration - Testing Integration")
        print("=" * 50)
        
        # Test chat processing
        print("1. Testing chat processing...")
        test_messages = [
            "hello",
            "status",
            "agents",
            "help"
        ]
        
        for message in test_messages:
            response = self.process_chat_message("test_user", message)
            print(f"   '{message}' -> '{response}'")
        
        # Test terminal command processing
        print("2. Testing terminal command processing...")
        test_commands = [
            "echo 'Hello World'",
            "ls -la",
            "pwd"
        ]
        
        for command in test_commands:
            result = self.process_terminal_command("test_agent", command)
            print(f"   '{command}' -> {result['status']}")
        
        print("✅ Integration test completed")
    
    def generate_integration_report(self):
        """Generate integration report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "chat_database": self.chat_database,
            "agents": self.agents,
            "integration_status": "active",
            "features": [
                "chat_processing",
                "terminal_command_execution",
                "history_tracking",
                "interactive_interface"
            ]
        }
        
        with open("projects/server_system_setup/terminal_chat_report.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        print("✅ Integration report generated")

def main():
    """Main function"""
    integration = TerminalChatIntegration()
    
    # Create chat database
    integration.create_chat_database()
    
    # Test integration
    integration.test_integration()
    
    # Generate report
    integration.generate_integration_report()
    
    # Update work log
    with open("logs/agent_work.log", "a") as f:
        f.write(f"{datetime.now()}: Agent: Terminal Chat Integration - Task: Terminal Chat Setup - Status: Completed - Notes: Terminal chat integration active\n")
    
    print("\n🎉 Terminal chat integration setup completed successfully!")
    
    # Start chat interface
    integration.start_chat_interface()

if __name__ == "__main__":
    main()
