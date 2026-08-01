#!/usr/bin/env python3
"""Convert the roofing pipeline Google Sheet CSV export into JSON for the dashboard."""
import csv, json, re, sys, io

SRC = r"C:\Users\WORKSP~1\AppData\Local\Temp\sheet.csv"

COLS = [
    "onLedgers", "projectManager", "projectNumber", "customer", "note", "address",
    "state", "entered", "sow", "roofTeam", "roofQuoteRequested", "roofQuoteReceived",
    "quoteTotal", "subhubAdder", "sq", "shingleColor", "financing", "installRequest",
    "installDate", "completed", "extraAdders", "updatedQuote", "hoCash",
    "totalRoofCost", "lastUpdate", "notes", "stage", "rtcEndNote",
]

def clean(v):
    if v is None:
        return ""
    v = v.strip()
    return v

def main():
    with open(SRC, "r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))

    out = []
    dropped = 0
    for i, row in enumerate(rows):
        # Pad short rows
        row = row + [""] * (len(COLS) - len(row))
        rec = {c: clean(row[j]) for j, c in enumerate(COLS)}
        # Drop fully-empty rows
        if not any(rec.values()):
            continue
        # Drop legend / non-job rows (no project number + no customer)
        has_proj = bool(rec["projectNumber"])
        has_cust = bool(rec["customer"])
        if not has_proj and not has_cust:
            dropped += 1
            continue
        # Drop stray duplicate header rows (they echo the column titles)
        if rec["projectManager"] == "PROJECT MANAGER" or rec["customer"] == "Customer" \
           or rec["projectNumber"] == "Project #":
            dropped += 1
            continue
        # Fix Windows line endings inside notes, collapse runaway whitespace
        for k, v in rec.items():
            if "\n" in v:
                v = v.replace("\r", "")
                v = re.sub(r"\n{2,}", "\n", v)
                rec[k] = v
        out.append(rec)

    print(f"Rows exported: {len(out)}  (dropped {dropped} legend/blank rows)")
    with open(r"C:\Users\workspace\Desktop\Pipeline\pipeline_data.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    # Quick stats for the dashboard config sanity check
    from collections import Counter
    print("Stages:", dict(Counter(r["stage"] for r in out).most_common()))
    print("PMs:", dict(Counter(r["projectManager"] for r in out).most_common()))

if __name__ == "__main__":
    main()
