from fastapi import APIRouter, UploadFile, File, HTTPException

from bbs_tonnage.storage.local import save_upload
from bbs_tonnage.parse.type_a import parse_type_a_weights, extract_declared_total_kg

router = APIRouter()


@router.post("/v1/parse")
async def parse_schedule(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported.")

    pdf_path = await save_upload(file)

    weights, pdf_text = parse_type_a_weights(pdf_path)
    declared_total_kg = extract_declared_total_kg(pdf_text)

    if not weights:
        return {
            "status": "no_weights_found",
            "note": "No weight column detected. Likely not a Type A schedule.",
        }

    total_kg = round(sum(weights), 3)
    tolerance_percent = 0.5
    delta_percent = None
    verification_pass = None

    if declared_total_kg is not None and declared_total_kg > 0:
        delta_percent = round(((total_kg - declared_total_kg) / declared_total_kg) * 100, 4)
        verification_pass = abs(delta_percent) <= tolerance_percent

    return {
        "status": "ok",
        "rows_detected": len(weights),
        "total_weight_kg": total_kg,
        "total_weight_t": round(total_kg / 1000, 6),
        "source": "declared_weights",
        "declared_total_kg": declared_total_kg,
        "delta_percent": delta_percent,
        "verification_pass": verification_pass,
		"tolerance_percent": tolerance_percent,

    }
