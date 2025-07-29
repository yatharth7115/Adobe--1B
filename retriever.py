import fitz  # PyMuPDF
from typing import List, Dict

def extract_all_sections(pdf_paths: List[str]) -> List[Dict]:
    sections = []
    for path in pdf_paths:
        doc = fitz.open(path)
        title = None
        # First pass: get title and outline
        for pnum in range(len(doc)):
            page = doc[pnum]
            data = page.get_text("dict")
            prev_bottom = 0
            for block in data["blocks"]:
                if "lines" not in block: continue
                for line in block["lines"]:
                    spans = line["spans"]
                    text = "".join(s["text"] for s in spans).strip()
                    if not text: continue
                    # treat any line starting with H1 numbering or all caps as section
                    if text.isupper() or text.startswith("1."):
                        sections.append({
                            "document": path,
                            "section_title": text,
                            "start_page": pnum + 1,
                            "chunks": []
                        })
        # Second pass: for each section, collect its text chunks until next section
        for sec in sections:
            doc = fitz.open(sec["document"])
            collecting = False
            for pnum in range(len(doc)):
                page = doc[pnum]
                data = page.get_text("dict")
                for block in data["blocks"]:
                    if "lines" not in block: continue
                    for line in block["lines"]:
                        text = "".join(s["text"] for s in line["spans"]).strip()
                        if not text: continue
                        if pnum + 1 == sec["start_page"] and text == sec["section_title"]:
                            collecting = True
                            continue
                        if collecting:
                            # stop if another section title pattern
                            if text.isupper() or text.startswith("1."):
                                collecting = False
                                break
                            sec["chunks"].append({"text": text, "page": pnum + 1})
                    if not collecting and sec["chunks"]:
                        break
                if not collecting and sec["chunks"]:
                    break
    return sections
