from fastapi import APIRouter, UploadFile, File, HTTPException
from bbs_tonnage.storage.local import save_upload
from bbs_tonnage.parse.type_a import parse_type_a_weights

router = APIRouter()

@router.post("/v1/parse")
async def parse_schedule(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported.")

    pdf_path = await save_upload(file)
    weights = parse_type_a_weights(pdf_path)

    if not weights:
        return {
            "status": "no_weights_found",
            "note": "No weight column detected. Likely not a Type A schedule.",
        }

    total_kg = round(sum(weights), 3)

    return {
        "status": "ok",
        "rows_detected": len(weights),
        "total_weight_kg": total_kg,
        "total_weight_t": round(total_kg / 1000, 6),
        "source": "declared_weights",
    }
