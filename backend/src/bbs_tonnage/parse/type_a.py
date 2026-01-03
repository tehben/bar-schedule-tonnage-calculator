from __future__ import annotations
from typing import List, Tuple
import pdfplumber
import re
from typing import Optional

def parse_type_a_weights(pdf_path: str) -> Tuple[List[float], str]:
    weights: List[float] = []
    text_parts: List[str] = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            if page_text:
                text_parts.append(page_text)

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

    pdf_text = "\n".join(text_parts)
    return weights, pdf_text
def extract_declared_total_kg(pdf_text: str) -> Optional[float]:
    text = pdf_text or ""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    patterns = [
        # 1) Total... (kg) or [kg] with explicit = or :
        r"(?i)\btotal\b.*?(?:weight|mass)?\s*.*?[\[\(]?\s*kg\s*[\]\)]?\s*[=:]\s*([0-9]+(?:[.,][0-9]+)?)\b",
        r"(?i)\b(total|grand total)\b.*?[\[\(]?\s*kg\s*[\]\)]?\s*[=:]\s*([0-9]+(?:[.,][0-9]+)?)\b",

        # 2) Total... number ... kg  (no equals)
        r"(?i)\b(total|grand total)\b.*?\b([0-9]+(?:[.,][0-9]+)?)\s*kg\b",
        r"(?i)\btotal\b.*?(?:weight|mass)\b.*?\b([0-9]+(?:[.,][0-9]+)?)\s*kg\b",
    ]

    def parse_num(s: str) -> Optional[float]:
        if not s:
            return None
        s = s.strip().replace(" ", "")
        # handle comma decimals
        if "," in s and "." not in s:
            s = s.replace(",", ".")
        # handle thousands separators like 1,234.56
        elif "," in s and "." in s:
            s = s.replace(",", "")
        try:
            v = float(s)
            return v if v > 0 else None
        except Exception:
            return None

    # Search line-by-line to avoid grabbing stray numbers elsewhere (like 8666:2020)
    for ln in lines:
        for pat in patterns:
            m = re.search(pat, ln)
            if not m:
                continue

            # number is last captured group in each pattern
            num = m.groups()[-1]
            val = parse_num(num)
            if val is not None:
                return val

    return None
