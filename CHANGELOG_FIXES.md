# Project Fixes & Optimizations Changelog

This document tracks fixes applied to the backend, complete with the rationale, code changes, and exact dates, allowing for easy reversion if necessary.

---
## [2026-07-23] Backend Performance Optimizations

### 1. RAG Context Filter & Table Limit (Level 1)
**File:** `backend/api/rag_engine.py`
**Rationale:** The addition of the `common` schema caused the RAG engine to pull thousands of audit columns into the LLM context window, increasing pre-fill latency to 51 seconds.
**Changes Applied:**
- Reduced the max returned tables from `8` to `4` in `retrieve_context`.
- Added an exclusion list in `_load_postgres_schema` to silently drop columns starting with `g_aud_`, `r_void_`, `l_hibernate_`, etc.

### 2. LLM Few-Shot Examples Caching (Level 2)
**File:** `backend/api/llm_agent.py`
**Rationale:** Reading `r_vv_tb_examples.txt` synchronously from the disk on every request blocks the FastAPI async event loop.
**Changes Applied:**
- Created a global variable `_cached_few_shot_examples`.
- Modified `generate_sql_from_intent` to read the file into memory exactly once and reuse it for all subsequent requests.

### 3. LLM Over-Prediction Cap (Level 3)
**File:** `backend/api/llm_agent.py`
**Rationale:** The `num_predict: 800` parameter allowed the model to spend up to 15s generating useless text if it got confused.
**Changes Applied:**
- Reduced `"num_predict"` in the Ollama JSON payload from `800` to `200`.

---
