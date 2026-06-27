# Sprint 2 — AI Pipeline

**Date:** 2026-06-27
**Status:** Complete

## What We Built

- **4-agent AI pipeline** that takes a job application and user's master profile and produces a tailored resume document with an ATS score
- **Extractor** (`claude-haiku-4-5`) — parses a raw job description into structured requirements: required/preferred skills, responsibilities, and experience level
- **Matcher** (`claude-haiku-4-5`) — compares extracted requirements against the user's `MasterProfile`, returning matched skills, missing skills, and a match percentage
- **Generator** (`claude-sonnet-4-6`) — rewrites resume bullet points and crafts a professional summary that emphasizes matched skills using only real experience from the user's profile
- **Scorer** (`claude-haiku-4-5`) — returns a 0–100 ATS score with a breakdown across skills (50%), experience (35%), and education (15%)
- **`POST /pipeline/tailor`** — orchestrates all four agents in sequence, persists the result as a `TailoredDocument`, and returns the full pipeline output
- **`GET /pipeline/documents/{application_id}`** — retrieves all tailored documents generated for a given application

## Architecture Decisions & Why

**JSON prefilling for structured output** — Each agent uses a system prompt instructing the model to respond in JSON only, and seeds the assistant turn with `{` to force the response to begin as a JSON object. This is more reliable than parsing freeform text and avoids tool-use overhead for simple extraction tasks.

**Model split: Haiku for extraction/scoring, Sonnet for generation** — Extraction, matching, and scoring are structured classification tasks where Haiku is fast and sufficient. Resume generation requires creative rewriting quality, so Sonnet is used there. This balances cost against output quality per stage.

**ATS score weighting (50/35/15)** — Skills are the primary signal modern ATS systems use, followed by experience relevance, with education weighted least for software roles. These weights are applied in the scorer and can be tuned in a later sprint.

**Pipeline errors surface as 502** — If the Anthropic API fails or returns unparseable JSON, the endpoint raises a `502 Bad Gateway` with the error detail. This keeps the failure mode transparent to callers without leaking internal state.

**`TailoredDocument.content` stores the full pipeline state** — The JSONB `content` column persists the complete pipeline result (extraction, match, generated, score breakdown), not just the final resume. This enables future UI features like showing skill gap analysis and re-running individual stages without rerunning the full pipeline.

## AI Pipeline Notes

- All four agents are pure functions that accept an `anthropic.Anthropic` client as a parameter, making them trivially mockable in tests without patching internals
- The orchestrator (`orchestrator.py`) creates one shared client per request using the user's decrypted BYOK key — the key is never stored in memory beyond the request lifecycle
- Tests mock `run_pipeline` at the router level to validate error handling and storage logic independently of the Anthropic API

## Challenges & How We Solved Them

**Reliable JSON from LLMs** — Models occasionally prepend explanatory text before JSON. Solved by combining a strict system prompt ("Respond only with valid JSON") with assistant-turn prefilling (`{"role": "assistant", "content": "{"}`). The raw response is then prepended with `{` before parsing.

**Test isolation from real API calls** — Pipeline tests use `unittest.mock.patch` to replace `run_pipeline` with a fixed `PipelineContent` fixture. This keeps tests fast, deterministic, and free of API key requirements while still exercising the full router logic (auth, DB writes, error branches).

## Sprint 3 Preview — Frontend

Next sprint builds the React frontend:
1. **Auth screens** — register/login wired to JWT
2. **Kanban board** — drag-and-drop application tracker across `saved → applied → interviewing → rejected → offer`
3. **Profile editor** — form to manage master work history, education, and skills
4. **Tailor modal** — trigger the AI pipeline from an application card, display ATS score and generated content
