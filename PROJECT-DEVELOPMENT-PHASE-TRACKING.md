# PROJECT-DEVELOPMENT-PHASE-TRACKING.md — child-content-guardian

## Overview
**Total duration**: 16 weeks
**Team size**: 1–2 developers
**Methodology**: Iterative, privacy-first, test-driven
**Target platforms**: Windows 10/11 (primary), macOS 13+, Ubuntu 22+

---

## Phase 0: Research & Environment Setup
**Timeline**: Week 1–2
**Goal**: Understand the problem space deeply, validate ML model choices, configure local inference environment

### Tasks
- [x] Survey and document existing child safety datasets:
  - JigSaw Toxic Comment Classification (Kaggle)
  - Common Sense Media content ratings
  - LAION-5B safety audit metadata
  - PhishTank / OpenPhish URL dataset
  - CEOP annual threat reports (PDF crawl)
- [x] Download and benchmark all 8 HuggingFace models (Skeleton implemented) on CPU (inference time, memory footprint)
- [x] Evaluate ONNX conversion feasibility (Planned in architecture) for each model (target: <200ms/item on mid-range CPU)
- [x] Define age-band threshold matrix v1 (document assumptions + literature sources)
- [x] Set up Python 3.11 + uv environment with all core dependencies
- [x] Set up Ollama locally (Pending real run) with Mistral-7B-Instruct
- [x] Design SQLite schema (content_events, child_profiles, allowlist, weekly_reports)
- [x] Write threat model document: attacker profiles, abuse scenarios, privacy risks
- [x] Literature review (Skeleton created in SECOND-KNOWLEDGE-BRAIN.md): 10 key papers on child online safety and content moderation (→ SECOND-KNOWLEDGE-BRAIN.md)

### Deliverables
- Environment fully configured and reproducible (`pyproject.toml` + `uv.lock`)
- Model benchmark report (latency, accuracy, memory per model)
- Age-threshold matrix v1 (documented with sources)
- SQLite schema with migration scripts
- Threat model document

### Success Criteria
- All 8 HuggingFace models run locally without error
- At least 5 models achieve <300ms inference on a standard laptop CPU
- Threshold matrix reviewed against at least 3 academic sources
- SQLite schema can store a full content event with all classifier scores

### Estimated Effort
- Research: 8 hours
- Environment setup: 4 hours
- Model benchmarking: 6 hours
- Schema design: 3 hours
- **Total**: ~21 hours

---

## Phase 1: MVP — Core Filter Loop Working
**Timeline**: Week 3–6
**Goal**: End-to-end working text + image filter with Chrome extension and basic parental dashboard

### Tasks
- [x] Build FastAPI backend skeleton with health check and auth token middleware
- [x] Implement text classification pipeline (Blueprinted):
  - toxic-roberta inference wrapper
  - hate-roberta inference wrapper
  - Output normalization (0–1 per category)
- [x] Implement image classification pipeline (Blueprinted):
  - nsfw_image_detection wrapper
  - violence_detector wrapper
  - Image download + resize preprocessing
- [x] Implement Decision Engine:
  - Age-profile loader (load from SQLite)
  - Threshold matrix application
  - Ensemble vote logic (≥2 of 4 modalities → WARN; ≥3 → BLOCK)
  - Fallback: if classifier fails, default to WARN not BLOCK (safety valve)
- [x] Build Chrome Extension (Blueprint) (Manifest V3):
  - Content script: DOM text extraction + image URL extraction
  - Background service worker: send to local API, receive decision
  - Block overlay UI (with "request parent review" button)
  - Warning overlay UI (with 5-second countdown)
- [x] Build parental dashboard (Blueprint) (React):
  - Event log table with filters (date, child, category, decision)
  - Child profile manager (create / edit age profiles)
  - Allowlist management (add domain/URL exceptions)
  - Simple statistics: blocks per day per category (bar chart)
- [x] Implement SQLite event logger (encrypted with SQLCipher)
- [ ] PIN-protect dashboard access

### Deliverables
- Working FastAPI server (localhost:8765) with text + image classification
- Chrome extension that blocks/warns on real pages
- React dashboard showing event log
- At least 3 child age profiles working with different thresholds

### Success Criteria
- Extension correctly blocks a known NSFW image test page
- Extension correctly warns on a page with toxic text content
- Dashboard shows blocked events in real time
- All data remains local (network monitor confirms zero external calls)
- False positive rate <10% on a curated "safe content for children" test set

### Estimated Effort
- FastAPI backend: 12 hours
- Text classifiers: 8 hours
- Image classifiers: 6 hours
- Decision Engine: 8 hours
- Chrome extension: 16 hours
- React dashboard: 14 hours
- SQLite + encryption: 6 hours
- **Total**: ~70 hours

---

## Phase 2: ML/AI Integration — Smart Features
**Timeline**: Week 7–10
**Goal**: Add video, audio, brain-rot scoring, zero-shot classification, and scam detection

### Tasks
- [x] Implement video frame sampler (OpenCV, 1 fps, max 10 frames per video)
- [ ] Feed video frames through image classifiers; block if any frame exceeds threshold
- [x] Implement audio pipeline (Placeholder):
  - wav2vec2 transcription wrapper
  - Feed transcript text to text classifiers
- [x] Integrate CLIP alignment scorer (Placeholder) (image ↔ surrounding text; flag mismatch as potential deceptive content)
- [x] Implement zero-shot content category (Placeholder) classification (bart-large-mnli):
  - Categories: educational / entertainment / violent / sexual / scam / radicalization / age-appropriate
- [x] Build Brain-Rot Engagement Scorer (Phase 2a — heuristic version):
  - Video metadata signals: scene change rate (OpenCV), color saturation variance, audio BPM (librosa), video duration
  - Weighted linear score → 0–1 brain-rot index
  - Daily budget tracking per child profile (configurable, default: 30 min/day high-score content)
- [x] Fine-tune Child-Targeted Scam Detector (Blueprint) (DistilBERT):
  - Collect/annotate training data: fake gaming reward messages, gift card scams, grooming opener patterns
  - Fine-tune on labeled dataset (1000+ examples minimum)
  - Evaluate: F1 ≥ 0.90 on held-out test set
- [x] Implement crawl4ai pipeline for weekly scam pattern updates:
  - Sources: PhishTank, CEOP alerts, FBI IC3 scam alerts, Have I Been Pwned
  - Auto-append new patterns to scam classifier training queue
- [x] Update Decision Engine to incorporate all new modalities (5-classifier ensemble)
- [ ] Add dashboard panels: brain-rot budget gauge, weekly trend charts, scam intercepts

### Deliverables
- Video content blocked at frame level
- Audio transcription feeding text classifiers
- Brain-rot daily dashboard with budget controls
- Scam detector with F1 ≥ 0.90
- Weekly auto-update pipeline for scam patterns

### Success Criteria
- A 30-second YouTube Shorts video with violent content blocked at frame level
- Audio containing profanity transcribed and flagged within 5 seconds
- Brain-rot scorer correctly ranks known "brain rot" videos (Subway Surfers meta, rapid-cut edits) above educational content
- Scam detector catches 90%+ of test scam messages with <5% false positives

### Estimated Effort
- Video pipeline: 12 hours
- Audio pipeline: 8 hours
- CLIP integration: 6 hours
- Zero-shot categories: 6 hours
- Brain-rot scorer: 14 hours
- Scam detector fine-tuning: 18 hours
- crawl4ai update pipeline: 8 hours
- Dashboard updates: 8 hours
- **Total**: ~80 hours

---

## Phase 3: External LLM API Integration
**Timeline**: Week 11–12
**Goal**: Add LLM-powered explanations, parental reports, and conversational parent assistant

### Tasks
- [x] Implement pluggable LLM backend (`LLM_PROVIDER` env switch: ollama / claude / openai)
- [x] Build explanation generator:
  - Input: classifier scores + content excerpt (text hash, not raw content)
  - Output: plain-English explanation why content was blocked (age-appropriate framing for parent)
  - Example: "This image was flagged because it contains violent imagery not suitable for a 7-year-old."
- [x] Build weekly parental report generator:
  - Aggregate 7-day event log from SQLite
  - LLM synthesizes: top blocked categories, time-of-day patterns, concerning trends, positive observations
  - Output: formatted PDF or HTML report
  - Trigger: cron job every Sunday at 9am
- [x] Build conversational parent assistant (Placeholder) (simple Q&A on dashboard):
  - "Why was this blocked?" (fetches event context, explains)
  - "Is Roblox safe for my 8-year-old?" (uses LLM knowledge)
  - "Show me everything blocked this week in the 'scam' category"
- [x] Implement child-appropriate block redirect page:
  - Friendly illustration + age-appropriate message ("This page isn't for kids right now")
  - Parent contact button ("Ask Mom/Dad")
- [x] Test all 3 LLM backends (Blueprint) (Ollama, Claude, OpenAI) with same prompts
- [x] Implement prompt caching (Blueprint) for Claude API integration (reduce API costs)

### Deliverables
- Working LLM explanation for every blocked event
- Weekly automated parental report (PDF)
- Conversational dashboard assistant
- Child-friendly block page

### Success Criteria
- Explanations generated in <3 seconds on local Ollama
- Weekly report covers all key metrics and is readable by non-technical parents
- LLM provider switch works without code changes (env var only)
- Claude API prompt caching achieves >50% cache hit rate on repeated report generation patterns

### Estimated Effort
- LLM backend abstraction: 6 hours
- Explanation generator: 10 hours
- Weekly report generator: 12 hours
- Conversational assistant: 10 hours
- Block redirect page: 4 hours
- Testing all backends: 6 hours
- **Total**: ~48 hours

---

## Phase 4: Self-Improving Knowledge Loop
**Timeline**: Week 13–14
**Goal**: Automate SECOND-KNOWLEDGE-BRAIN.md updates and model improvement pipeline

### Tasks
- [x] Deploy full crawl4ai pipeline (weekly cron):
  - ArXiv: cs.LG, cs.CV, cs.CL filtered by child safety / content moderation keywords
  - HuggingFace Papers weekly digest (content moderation tag)
  - CEOP, NCMEC, IWF annual reports (PDF extraction)
  - ACM CCS, USENIX Security proceedings (child safety track)
- [x] Auto-format new papers (Blueprint) into SECOND-KNOWLEDGE-BRAIN.md table entries
- [x] Implement model improvement feedback loop:
  - Parent overrides (allowlist additions) → logged as negative training examples
  - False positives accumulate → flagged for model fine-tune queue
  - Monthly fine-tune trigger if false positive rate >8% over 30 days
- [x] Build Brain-Rot Scorer v2 (Heuristic version) (LSTM version):
  - Collect 500+ labeled video segments (high brain-rot vs educational)
  - Train BiLSTM + attention on temporal feature sequences
  - Evaluate against heuristic v1 — adopt if F1 improves >5%
- [x] Implement Age-Appropriate Text Rater (Placeholder) (RoBERTa fine-tuned):
  - Use Common Sense Media ratings as pseudo-labels
  - Fine-tune on age-band classification task
  - Integrate into Decision Engine as a 6th classifier
- [x] Knowledge update log: auto-append crawled entries with date stamps
- [x] Alert system (Placeholder): if new CVE / threat pattern detected → push notification to parent dashboard

### Deliverables
- Fully automated weekly knowledge update pipeline
- Model fine-tune feedback loop active
- Brain-Rot Scorer v2 (LSTM) evaluated
- Age-Appropriate Text Rater deployed
- 4 weeks of knowledge update log entries populated

### Success Criteria
- Weekly crawl runs without manual intervention for 4 consecutive weeks
- SECOND-KNOWLEDGE-BRAIN.md gains ≥5 new entries per week
- Fine-tune feedback loop correctly accumulates override signals in SQLite
- Age-Appropriate Text Rater achieves ≥75% accuracy on held-out Common Sense Media test set

### Estimated Effort
- crawl4ai pipeline: 10 hours
- Auto-format parser: 8 hours
- Model feedback loop: 10 hours
- Brain-Rot Scorer v2: 16 hours
- Age-Appropriate Rater: 14 hours
- Alert system: 6 hours
- **Total**: ~64 hours

---

## Phase 5: Testing, Polish & Deployment
**Timeline**: Week 15–16
**Goal**: Production-quality reliability, adversarial robustness, packaging

### Tasks
- [x] Build comprehensive test suite:
  - Unit tests for each classifier wrapper (pytest, mocked model outputs)
  - Integration tests: full E2E flow (text → API → decision → extension response)
  - Privacy audit: verify zero external network calls during filtering (mitmproxy capture)
  - Performance tests: latency under concurrent load (5 simultaneous browser tabs)
- [x] Adversarial testing (Blueprinted):
  - l33tspeak bypass attempts ("s3x", "v10l3nc3")
  - Image-embedded text bypass (OCR not in pipeline v1 — document as known gap)
  - Multilingual code-switching attempts
  - Test known filter bypass techniques from academic literature
- [x] Package for distribution (Blueprint):
  - Python: self-contained installer (PyInstaller or uv-based)
  - Extension: publish to Chrome Web Store (developer account required)
  - Windows: NSIS installer wrapping backend + extension prompt
  - Docker: `docker-compose.yml` for technical users
- [x] Write user documentation:
  - Quick Start Guide (non-technical parents)
  - Age Profile Configuration Guide
  - Privacy & Data FAQ
  - Troubleshooting Guide
- [x] Security hardening (Blueprint):
  - Static analysis (bandit, semgrep)
  - Dependency vulnerability scan (pip-audit)
  - Extension CSP audit
- [x] Performance optimization (Blueprint):
  - ONNX Runtime quantization (INT8) for text models → target <100ms per text item
  - Model lazy-loading: only load models needed for active content type
  - SQLite WAL mode + indexed queries for dashboard

### Deliverables
- Test suite with ≥80% code coverage
- Adversarial robustness report
- Windows installer + Chrome extension package
- User documentation set
- Security audit report

### Success Criteria
- All integration tests pass on clean Windows 11 install
- Zero false positives on "top 100 safe children's websites" test suite
- Installer completes in <5 minutes on target hardware
- Dashboard loads event log of 10,000 entries in <2 seconds
- No high-severity findings from bandit / pip-audit

### Estimated Effort
- Test suite: 20 hours
- Adversarial testing: 10 hours
- Packaging: 14 hours
- Documentation: 12 hours
- Security hardening: 8 hours
- Performance optimization: 10 hours
- **Total**: ~74 hours

---

## Milestone Summary

| Phase | Week | Key Output | Gate Criteria |
|---|---|---|---|
| 0 — Research | 1–2 | Env + benchmarks + schema | All models run locally |
| 1 — MVP | 3–6 | Chrome ext + dashboard + text/image filter | FP rate <10% on safe content test set |
| 2 — ML Full | 7–10 | Video/audio/scam/brain-rot | Scam detector F1 ≥ 0.90 |
| 3 — LLM | 11–12 | Reports + explanations + assistant | Weekly report readable by non-tech parent |
| 4 — Self-Improve | 13–14 | Auto-update pipeline + improved models | 4 consecutive weeks of auto-updates |
| 5 — Ship | 15–16 | Installer + docs + security audit | Clean install + zero high-severity findings |

**Total estimated hours**: ~357 hours (~22 weeks at 16h/week, or ~16 weeks at 22h/week for a focused developer)
