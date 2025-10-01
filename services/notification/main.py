from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any, List

app = FastAPI(title="Notification Service", version="1.0.0")

class NotificationRequest(BaseModel):
    title: str
    message: str
    recipient: str
    notification_type: str = "info"
    priority: str = "normal"

class NotificationResponse(BaseModel):
    notification_id: str
    status: str
    timestamp: str

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "notification",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/api/status")
async def get_status():
    return {
        "message": "Notification Service is running",
        "version": "1.0.0",
        "supported_types": [
            "info",
            "warning",
            "error",
            "success"
        ],
        "supported_priorities": [
            "low",
            "normal",
            "high",
            "urgent"
        ],
        "total_notifications": 0,
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.post("/api/send", response_model=NotificationResponse)
async def send_notification(request: NotificationRequest):
    try:
        # Simulate notification sending
        notification_id = f"notif_{hash(request.title)}_{hash(request.message)}"
        
        # Simulate sending process
        notification_data = {
            "notification_id": notification_id,
            "title": request.title,
            "message": request.message,
            "recipient": request.recipient,
            "type": request.notification_type,
            "priority": request.priority,
            "sent_at": "2024-01-01T00:00:00Z",
            "status": "sent"
        }
        
        return NotificationResponse(
            notification_id=notification_id,
            status="sent",
            timestamp="2024-01-01T00:00:00Z"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notifications")
async def get_notifications(recipient: str = None, status: str = None, limit: int = 10):
    try:
        # Simulate notifications retrieval
        notifications = [
            {
                "notification_id": "notif_1",
                "title": "System Update",
                "message": "System will be updated at 2 AM",
                "recipient": "admin@example.com",
                "type": "info",
                "priority": "normal",
                "status": "sent",
                "sent_at": "2024-01-01T00:00:00Z"
            },
            {
                "notification_id": "notif_2",
                "title": "Error Alert",
                "message": "Database connection failed",
                "recipient": "dev@example.com",
                "type": "error",
                "priority": "high",
                "status": "sent",
                "sent_at": "2024-01-01T00:00:00Z"
            }
        ]
        
        # Filter by recipient if specified
        if recipient:
            notifications = [n for n in notifications if n["recipient"] == recipient]
        
        # Filter by status if specified
        if status:
            notifications = [n for n in notifications if n["status"] == status]
        
        return {
            "notifications": notifications[:limit],
            "total_notifications": len(notifications),
            "status": "success",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notifications/{notification_id}")
async def get_notification(notification_id: str):
    try:
        # Simulate single notification retrieval
        notification = {
            "notification_id": notification_id,
            "title": "Sample Notification",
            "message": "This is a sample notification message...",
            "recipient": "user@example.com",
            "type": "info",
            "priority": "normal",
            "status": "sent",
            "sent_at": "2024-01-01T00:00:00Z",
            "read_at": None
        }
        
        return {
            "notification": notification,
            "status": "success",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/notifications/{notification_id}/read")
async def mark_as_read(notification_id: str):
    try:
        return {
            "notification_id": notification_id,
            "status": "read",
            "message": "Notification marked as read",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/notifications/{notification_id}")
async def delete_notification(notification_id: str):
    try:
        return {
            "notification_id": notification_id,
            "status": "deleted",
            "message": "Notification deleted successfully",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics")
async def get_analytics():
    try:
        analytics = {
            "total_notifications": 150,
            "notifications_by_type": {
                "info": 80,
                "warning": 30,
                "error": 25,
                "success": 15
            },
            "notifications_by_priority": {
                "low": 50,
                "normal": 70,
                "high": 25,
                "urgent": 5
            },
            "delivery_stats": {
                "sent": 150,
                "delivered": 145,
                "failed": 5,
                "read": 120
            }
        }
        
        return {
            "analytics": analytics,
            "status": "success",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8012)
