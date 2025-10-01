from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any, List

app = FastAPI(title="File Indexer Service", version="1.0.0")

class IndexRequest(BaseModel):
    file_path: str
    file_type: str = "text"
    content: str = ""

class IndexResponse(BaseModel):
    index_id: str
    status: str
    timestamp: str

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "file-indexer",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/api/status")
async def get_status():
    return {
        "message": "File Indexer Service is running",
        "version": "1.0.0",
        "supported_file_types": [
            "text",
            "python",
            "javascript",
            "markdown",
            "json",
            "yaml"
        ],
        "indexed_files": 0,
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.post("/api/index", response_model=IndexResponse)
async def index_file(request: IndexRequest):
    try:
        # Simulate file indexing
        index_id = f"index_{hash(request.file_path)}_{hash(request.content)}"
        
        # Simulate indexing process
        indexed_data = {
            "file_path": request.file_path,
            "file_type": request.file_type,
            "content_length": len(request.content),
            "word_count": len(request.content.split()),
            "line_count": len(request.content.split('\n')),
            "indexed_at": "2024-01-01T00:00:00Z"
        }
        
        return IndexResponse(
            index_id=index_id,
            status="indexed",
            timestamp="2024-01-01T00:00:00Z"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search")
async def search_files(query: str, file_type: str = None):
    try:
        # Simulate file search
        results = [
            {
                "file_path": "/example/file1.py",
                "file_type": "python",
                "relevance_score": 0.95,
                "matches": [
                    {"line": 10, "content": f"Found: {query}"},
                    {"line": 25, "content": f"Another match: {query}"}
                ]
            },
            {
                "file_path": "/example/file2.js",
                "file_type": "javascript",
                "relevance_score": 0.87,
                "matches": [
                    {"line": 5, "content": f"JavaScript match: {query}"}
                ]
            }
        ]
        
        return {
            "query": query,
            "results": results,
            "total_matches": len(results),
            "status": "success",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files")
async def list_indexed_files():
    try:
        files = [
            {
                "file_path": "/example/file1.py",
                "file_type": "python",
                "indexed_at": "2024-01-01T00:00:00Z",
                "size": 1024
            },
            {
                "file_path": "/example/file2.js",
                "file_type": "javascript",
                "indexed_at": "2024-01-01T00:00:00Z",
                "size": 512
            }
        ]
        
        return {
            "files": files,
            "total_files": len(files),
            "status": "success",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/index/{index_id}")
async def remove_from_index(index_id: str):
    try:
        return {
            "index_id": index_id,
            "status": "removed",
            "message": "File removed from index successfully",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
