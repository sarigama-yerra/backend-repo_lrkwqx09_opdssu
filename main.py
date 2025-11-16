import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Any

from schemas import Lead, Project
from database import create_document, get_documents

app = FastAPI(title="OTIKA API", description="Backend for OTIKA Digital Agency site")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "OTIKA API is running", "endpoints": ["/api/hello", "/api/leads", "/api/projects", "/test"]}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the OTIKA backend API!"}


@app.post("/api/leads")
def create_lead(lead: Lead):
    try:
        lead_id = create_document("lead", lead)
        return {"status": "ok", "id": lead_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects")
def list_projects(limit: int | None = 20) -> List[Any]:
    try:
        items = get_documents("project", {}, limit or 0)
        # Convert ObjectId to string safely
        for it in items:
            if "_id" in it:
                it["id"] = str(it.pop("_id"))
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/projects")
def create_project(project: Project):
    try:
        proj_id = create_document("project", project)
        return {"status": "ok", "id": proj_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


class SchemaOut(BaseModel):
    name: str
    schema: dict


@app.get("/schema", response_model=List[SchemaOut])
def get_schema():
    """Expose schemas for the database viewer"""
    return [
        {"name": "lead", "schema": Lead.model_json_schema()},
        {"name": "project", "schema": Project.model_json_schema()},
    ]


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
