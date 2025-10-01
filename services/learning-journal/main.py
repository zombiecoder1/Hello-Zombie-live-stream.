from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any, List

app = FastAPI(title="Learning Journal Service", version="1.0.0")

class JournalEntry(BaseModel):
    title: str
    content: str
    tags: List[str] = []
    category: str = "general"

class JournalResponse(BaseModel):
    entry_id: str
    status: str
    timestamp: str

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "learning-journal",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/api/status")
async def get_status():
    return {
        "message": "Learning Journal Service is running",
        "version": "1.0.0",
        "total_entries": 0,
        "categories": [
            "general",
            "programming",
            "ai",
            "devops",
            "learning"
        ],
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.post("/api/entries", response_model=JournalResponse)
async def create_entry(entry: JournalEntry):
    try:
        # Simulate journal entry creation
        entry_id = f"entry_{hash(entry.title)}_{hash(entry.content)}"
        
        return JournalResponse(
            entry_id=entry_id,
            status="created",
            timestamp="2024-01-01T00:00:00Z"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/entries")
async def get_entries(category: str = None, tag: str = None, limit: int = 10):
    try:
        # Simulate journal entries retrieval
        entries = [
            {
                "entry_id": "entry_1",
                "title": "Learning FastAPI",
                "content": "Today I learned about FastAPI and how to create REST APIs...",
                "tags": ["python", "fastapi", "api"],
                "category": "programming",
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "entry_id": "entry_2",
                "title": "Docker Best Practices",
                "content": "Docker containerization best practices for production...",
                "tags": ["docker", "devops", "containers"],
                "category": "devops",
                "created_at": "2024-01-01T00:00:00Z"
            }
        ]
        
        # Filter by category if specified
        if category:
            entries = [e for e in entries if e["category"] == category]
        
        # Filter by tag if specified
        if tag:
            entries = [e for e in entries if tag in e["tags"]]
        
        return {
            "entries": entries[:limit],
            "total_entries": len(entries),
            "status": "success",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/entries/{entry_id}")
async def get_entry(entry_id: str):
    try:
        # Simulate single entry retrieval
        entry = {
            "entry_id": entry_id,
            "title": "Sample Entry",
            "content": "This is a sample journal entry content...",
            "tags": ["sample", "test"],
            "category": "general",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        
        return {
            "entry": entry,
            "status": "success",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/entries/{entry_id}")
async def update_entry(entry_id: str, entry: JournalEntry):
    try:
        return {
            "entry_id": entry_id,
            "status": "updated",
            "message": "Journal entry updated successfully",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/entries/{entry_id}")
async def delete_entry(entry_id: str):
    try:
        return {
            "entry_id": entry_id,
            "status": "deleted",
            "message": "Journal entry deleted successfully",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics")
async def get_analytics():
    try:
        analytics = {
            "total_entries": 25,
            "entries_by_category": {
                "programming": 10,
                "ai": 8,
                "devops": 5,
                "general": 2
            },
            "entries_by_month": {
                "2024-01": 15,
                "2024-02": 10
            },
            "most_used_tags": [
                {"tag": "python", "count": 12},
                {"tag": "ai", "count": 8},
                {"tag": "docker", "count": 6}
            ]
        }
        
        return {
            "analytics": analytics,
            "status": "success",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8011)
