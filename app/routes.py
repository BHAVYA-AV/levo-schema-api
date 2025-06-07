import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from datetime import datetime
import yaml
import json
from app.validators import validate_openapi
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import SchemaVersion

router = APIRouter()

UPLOAD_DIR = "schemas"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload_schema(
    file: UploadFile = File(...),
    application: str = Form(...),
    service: str = Form(None),
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".json", ".yaml", ".yml"]:
        raise HTTPException(status_code=400, detail="Only .json or .yaml files are allowed.")

    contents = await file.read()

    try:
        data = yaml.safe_load(contents) if ext in [".yaml", ".yml"] else json.loads(contents)
        validate_openapi(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid OpenAPI file: {str(e)}")

    db: Session = next(get_db())

  
    latest = (
        db.query(SchemaVersion)
        .filter(SchemaVersion.application == application, SchemaVersion.service == service)
        .order_by(SchemaVersion.version.desc())
        .first()
    )
    next_version = 1 if latest is None else latest.version + 1

    # Save file
    folder_path = os.path.join(UPLOAD_DIR, application, service or "default")
    os.makedirs(folder_path, exist_ok=True)
    filename = f"schema_v{next_version}{ext}"
    full_path = os.path.join(folder_path, filename)
    with open(full_path, "wb") as f:
        f.write(contents)

    # Save to DB
    schema = SchemaVersion(
        application=application,
        service=service,
        version=next_version,
        filepath=full_path.replace("\\", "/"),
    )
    db.add(schema)
    db.commit()

    return {
        "message": f"Schema v{next_version} uploaded successfully!",
        "version": next_version,
        "filepath": schema.filepath
    }

@router.get("/get-latest")
def get_latest_schema(application: str, service: str = None):
    folder = os.path.join(UPLOAD_DIR, application, service or "default")

    if not os.path.exists(folder):
        raise HTTPException(status_code=404, detail="No schemas found for given app/service.")

    files = sorted(os.listdir(folder), reverse=True)
    if not files:
        raise HTTPException(status_code=404, detail="No schema versions available.")

    latest_file = os.path.join(folder, files[0])
    return FileResponse(latest_file, media_type="application/octet-stream", filename=files[0])


@router.get("/get-schema")
def get_schema_by_version(application: str, service: str = None, version: int = None):
    db: Session = next(get_db())

    query = db.query(SchemaVersion).filter(SchemaVersion.application == application)

    if service:
        query = query.filter(SchemaVersion.service == service)

    if version:
        query = query.filter(SchemaVersion.version == version)
    else:
        query = query.order_by(SchemaVersion.version.desc()).limit(1)

    record = query.first()

    if not record:
        raise HTTPException(status_code=404, detail="Schema not found.")

    return FileResponse(record.filepath, media_type="application/octet-stream", filename=os.path.basename(record.filepath))
