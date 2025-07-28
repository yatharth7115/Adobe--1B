# Challenge 1B: Persona‑Driven Document Intelligence

## Overview

In *Round 1B* of the Adobe “Connecting the Dots” hackathon, our task is to build an offline, CPU‑only document analysis engine that:

1. *Parses a collection* of PDF documents into structured sections.
2. *Ranks and extracts* the most relevant sections for a given *Persona* and *Job‑to‑be‑Done (JTBD)*.
3. *Outputs* a JSON containing metadata, top‑ranked sections, and refined sub‑section texts.

This README explains the end‑to‑end approach, key design decisions, and instructions for running the solution.

---

## Architecture

### 1. Section Extraction (Retriever)

- *Library*: [PyMuPDF (Fitz)](https://pymupdf.readthedocs.io/)  
- *Method*:  
  - For each PDF, call page.get_text("dict") to obtain low‑level text, font, bbox, and style metadata.  
  - Build visual and lexical features per line: relative font size, bold/italic flags, indentation, centering, ALL‑CAPS, numbering, space before, etc.  
  - *Heuristic + ML Hybrid*:  
    - *Layer 1 (Heuristics)*: Quickly classify obvious headings (large relative size, bold, centered, etc.).  
    - *Layer 2 (ML Classifier)*: A pre‑trained Logistic Regression model refines ambiguous cases using the full feature vector.  
  - Output: A list of {"document", "section_title", "start_page", "chunks": [{"text","page"}...]}.

### 2. Persona‑Aware Ranking (Ranker)

- *Library: [Sentence‑Transformers](https://www.sbert.net/) with the **all‑MiniLM‑L6‑v2* model (≈90 MB).  
- *Embedding*:  
  - Encode the *Persona* string (e.g., “HR professional”) and the *JTBD* string (e.g., “Create and manage fillable forms…”).  
  - For each section, encode all its text *chunks* (paragraphs) in one batch.  
- *Scoring*:  
  - Compute *cosine similarities* between each chunk and:  
    - JTBD (weight 0.7)  
    - Persona (weight 0.3)  
  - Select the chunk with the highest *weighted* score to represent that section.  
  - Assign section.score = max_weighted_similarity.  
- *Selection*: Sort all sections by descending score and take the *top‑5*.  
- *Output*:  
  - extracted_sections: array of {document, section_title, importance_rank, page_number}  
  - refined_sections: array of {document, refined_text, page_number}

---

## Installation & Usage

### Requirements

- Python 3.8+  
- Dependencies in requirements.txt:
  ```text
  numpy
  torch
  sentence-transformers
  PyMuPDF
