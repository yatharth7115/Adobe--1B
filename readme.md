# 📄 Challenge 1B – Connecting the Dots: Semantic Document Intelligence

## 🧠 Problem Statement Overview

Challenge 1B of the Adobe Hackathon tasks participants with building a document intelligence system capable of analyzing a set of unstructured PDF documents to extract the most relevant content based on two inputs:

- A **persona** (e.g., "HR professional")
- A **job-to-be-done (JTBD)** (e.g., "Create and manage fillable forms for onboarding and compliance")

The system must semantically understand the intent behind these inputs and intelligently extract the most useful sections from the documents.

---

## 🧩 Solution Architecture

Our pipeline is composed of two major modules:

### 1. 🕵️ Section Extraction (`retriever.py`)
- Parses PDFs using **PyMuPDF** to detect headings, font sizes, and spatial layout.
- Extracts titles and splits documents into **logical sections**.
- Uses a **fallback heuristic** (font size, center offset, word count) if headings are not clear.
- Produces a structured list of sections with:
  - `document` name
  - `section_title`
  - `chunks` (text blocks)
  - `start_page` number

---

### 2. 📊 Semantic Ranking (`ranker.py`)
- Embeds:
  - Persona string
  - JTBD string
  - Each content chunk
- Uses **`sentence-transformers/all-MiniLM-L6-v2`** to convert texts to vector embeddings.
- Calculates **cosine similarity** between:
  - Section ↔ Persona
  - Section ↔ JTBD
- Computes a weighted score:
  ```python
  final_score = 0.7 * JTBD_similarity + 0.3 * Persona_similarity
