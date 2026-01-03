from __future__ import annotations
from typing import List
import pdfplumber

def parse_type_a_weights(pdf_path: str) -> List[float]:
    """
    Extract per-row weights (kg) from a Type A bar schedule PDF.
    Assumes a visible 'Weight' or 'kg' column exists.
    """
    weights: List[float] = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table or not table[0]:
                    continue

                header = [str(h or "").lower() for h in table[0]]
                weight_idx = None

                for i, col in enumerate(header):
                    if "weight" in col or col.strip() == "kg":
                        weight_idx = i
                        break

                if weight_idx is None:
                    continue

                for row in table[1:]:
                    try:
                        val = row[weight_idx]
                        if val is None:
                            continue
                        weight = float(str(val).replace(",", "").strip())
                        weights.append(weight)
                    except Exception:
                        continue

    return weights
