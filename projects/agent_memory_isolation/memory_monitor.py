#!/usr/bin/env python3
import sqlite3
import json
import os
from datetime import datetime

def check_memory_usage():
    agents = ["programming", "bestpractices", "verifier", "conversational", "ops"]
    results = {}
    
    for agent in agents:
        db_path = f"agents/memory/{agent}/memory.db"
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM memory")
            count = cursor.fetchone()[0]
            conn.close()
            results[agent] = {"entries": count, "status": "OK"}
        else:
            results[agent] = {"entries": 0, "status": "MISSING"}
    
    return results

if __name__ == "__main__":
    results = check_memory_usage()
    print(json.dumps(results, indent=2))
