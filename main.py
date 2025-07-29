import os
import json
import argparse
from datetime import datetime
from retriever import extract_all_sections
from ranker import rank_sections

def main(input_json, output_json, pdf_dir):
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    persona = data.get("persona", {}).get("role", "")
    jtbd = data.get("job_to_be_done", {}).get("task", "")
    docs_meta = data.get("documents", [])

    pdf_paths = []
    input_docs = []
    for doc in docs_meta:
        fn = doc["filename"]
        input_docs.append(fn)
        path = os.path.join(pdf_dir, fn)
        if os.path.exists(path):
            pdf_paths.append(path)
        else:
            print(f"⚠️ Skipping missing PDF: {path}")

    if not pdf_paths:
        print("❌ No valid PDFs found. Exiting.")
        return

    sections = extract_all_sections(pdf_paths)
    if not sections:
        print("⚠️ No sections extracted. Exiting.")
        return

    extracted, refined = rank_sections(persona, jtbd, sections)

    result = {
        "metadata": {
            "input_documents": input_docs,
            "persona": persona,
            "job_to_be_done": jtbd,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": extracted,
        "subsection_analysis": refined
    }

    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"✅ Output written to {output_json}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("input_json", help="challenge1b_input.json")
    p.add_argument("output_json", help="Where to write the output")
    p.add_argument("--pdf_dir", required=True, help="Folder containing the PDFs")
    args = p.parse_args()
    main(args.input_json, args.output_json, args.pdf_dir)
