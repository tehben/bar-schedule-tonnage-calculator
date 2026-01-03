from __future__ import annotations
import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "/tmp/bbs_uploads"

async def save_upload(file: UploadFile) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}_{file.filename}")
    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)
    return path
