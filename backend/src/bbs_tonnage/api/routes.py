from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

@router.post("/v1/parse")
async def parse_schedule(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported.")
    return {
        "status": "not_implemented",
        "filename": file.filename,
        "content_type": file.content_type,
        "note": "Parsing pipeline not implemented yet.",
    }
