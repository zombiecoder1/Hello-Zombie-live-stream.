from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any, List

app = FastAPI(title="Session Manager Service", version="1.0.0")

class SessionRequest(BaseModel):
    user_id: str
    session_data: Dict[str, Any] = {}
    expires_in: int = 3600  # seconds

class SessionResponse(BaseModel):
    session_id: str
    status: str
    timestamp: str

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "session-manager",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/api/status")
async def get_status():
    return {
        "message": "Session Manager Service is running",
        "version": "1.0.0",
        "active_sessions": 0,
        "total_sessions": 0,
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.post("/api/sessions", response_model=SessionResponse)
async def create_session(request: SessionRequest):
    try:
        # Simulate session creation
        session_id = f"session_{hash(request.user_id)}_{hash(str(request.session_data))}"
        
        # Simulate session data storage
        session_data = {
            "session_id": session_id,
            "user_id": request.user_id,
            "session_data": request.session_data,
            "created_at": "2024-01-01T00:00:00Z",
            "expires_at": "2024-01-01T01:00:00Z",
            "is_active": True
        }
        
        return SessionResponse(
            session_id=session_id,
            status="created",
            timestamp="2024-01-01T00:00:00Z"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    try:
        # Simulate session retrieval
        session = {
            "session_id": session_id,
            "user_id": "user_123",
            "session_data": {
                "preferences": {"theme": "dark", "language": "en"},
                "last_activity": "2024-01-01T00:00:00Z"
            },
            "created_at": "2024-01-01T00:00:00Z",
            "expires_at": "2024-01-01T01:00:00Z",
            "is_active": True
        }
        
        return {
            "session": session,
            "status": "success",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/sessions/{session_id}")
async def update_session(session_id: str, session_data: Dict[str, Any]):
    try:
        return {
            "session_id": session_id,
            "status": "updated",
            "message": "Session updated successfully",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    try:
        return {
            "session_id": session_id,
            "status": "deleted",
            "message": "Session deleted successfully",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions")
async def list_sessions(user_id: str = None, active_only: bool = True, limit: int = 10):
    try:
        # Simulate sessions listing
        sessions = [
            {
                "session_id": "session_1",
                "user_id": "user_123",
                "created_at": "2024-01-01T00:00:00Z",
                "expires_at": "2024-01-01T01:00:00Z",
                "is_active": True,
                "last_activity": "2024-01-01T00:00:00Z"
            },
            {
                "session_id": "session_2",
                "user_id": "user_456",
                "created_at": "2024-01-01T00:00:00Z",
                "expires_at": "2024-01-01T01:00:00Z",
                "is_active": True,
                "last_activity": "2024-01-01T00:00:00Z"
            }
        ]
        
        # Filter by user_id if specified
        if user_id:
            sessions = [s for s in sessions if s["user_id"] == user_id]
        
        # Filter by active status if specified
        if active_only:
            sessions = [s for s in sessions if s["is_active"]]
        
        return {
            "sessions": sessions[:limit],
            "total_sessions": len(sessions),
            "status": "success",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sessions/{session_id}/refresh")
async def refresh_session(session_id: str, expires_in: int = 3600):
    try:
        return {
            "session_id": session_id,
            "status": "refreshed",
            "new_expires_at": "2024-01-01T01:00:00Z",
            "message": "Session refreshed successfully",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics")
async def get_analytics():
    try:
        analytics = {
            "total_sessions": 1000,
            "active_sessions": 150,
            "sessions_by_hour": {
                "00:00": 10,
                "01:00": 5,
                "02:00": 3,
                "12:00": 50,
                "18:00": 80
            },
            "average_session_duration": "2.5 hours",
            "session_creation_rate": "10 sessions/hour"
        }
        
        return {
            "analytics": analytics,
            "status": "success",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8013)
