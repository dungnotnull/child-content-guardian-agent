# CLAUDE.md — child-content-guardian

## Project Identity
- **Name**: child-content-guardian
- **Tagline**: AI-powered real-time content filter protecting children from harmful, age-inappropriate, and psychologically damaging digital content
- **Status**: Phase 0 — Research & Environment Setup
- **Folder**: `D:\Dungchan\10\`

---

## Core Problem
Children in the digital/AI era are exposed to an overwhelming, algorithmically-amplified flood of content — much of it harmful: explicit material, online scams targeting minors, radicalization pipelines, and "brain rot" short-form content designed to hijack dopamine reward systems. No existing consumer-grade filter uses a full ML/DL stack with age-adaptive thresholds and multimodal analysis (text + image + video frames + audio). This project closes that gap.

---

## Architecture Summary
```
[Browser Extension / System Proxy]
        |
[Multimodal Ingestion Layer]  ← text, image, video frame, audio
        |
[Age Profile Manager]  ← active child profile (0-5 / 6-9 / 10-12 / 13+)
        |
[ML/DL Classifier Pipeline]
  ├─ Text Safety Classifier    (toxic-bert / fine-tuned RoBERTa)
  ├─ NSFW Image Detector       (Falconsai/nsfw_image_detection)
  ├─ Violence Detector         (dima806/violent_action_image_detection)
  ├─ Scam/Phishing Classifier  (fine-tuned DistilBERT)
  ├─ Brain-Rot Engagement Scorer (custom LSTM/Transformer)
  └─ Audio Harm Detector       (wav2vec2 + custom head)
        |
[Decision Engine]  ← per-age threshold matrix + ensemble vote
        |
  [BLOCK] → redirect to safe page + parental log
  [WARN]  → overlay warning + 5-second delay
  [ALLOW] → transparent pass-through
        |
[Parental Dashboard]  ← SQLite log, weekly report, override controls
        |
[Self-Improving Loop]  ← SECOND-KNOWLEDGE-BRAIN crawl4ai pipeline
```

**Platform**: Python 3.11 backend + FastAPI proxy server, React dashboard, Chrome/Firefox extension
**Local SLM**: Ollama (Mistral-7B-Instruct) for borderline-content explanations and parental reports
**Storage**: SQLite (local, AES-256 encrypted) — no data ever leaves the device

---

## Key Technical Decisions
1. **Ensemble vote, not single model**: Final block/warn/allow decision requires majority vote across at least 3 specialized classifiers — reduces both false positives and false negatives.
2. **Age-adaptive thresholds**: Each child profile carries an age band; threshold matrices differ significantly between age groups. A 5-year-old and a 13-year-old see different rules for the same content score.
3. **Multimodal at frame level**: Video is never processed as a whole — sampled at 1 fps and each frame independently scored. First frame to exceed threshold triggers block.
4. **Brain-rot scoring**: Beyond binary safe/unsafe, content receives an "addictive engagement" score (high variance reward signals, rapid scene changes, dopamine-bait patterns). Parents can set a daily brain-rot budget.
5. **Local-first privacy**: All inference runs on-device (CPU/GPU). Only domain reputation lookup hits an external API (optional, toggleable).
6. **Pluggable LLM backend**: Borderline-content explanations use configurable LLM (`LLM_PROVIDER` env var); defaults to local Ollama, falls back to Claude API.
7. **Graduated response**: observe → warn → block. First offense gets a parental notification; repeated patterns trigger escalating intervention.
8. **Scam pattern library**: Maintains a local, auto-updated library of scam/phishing patterns specifically targeting children (gift card scams, fake gaming rewards, grooming openers).

---

## External LLM API Integrations

| Provider | Use Case | Config Key | Model |
|---|---|---|---|
| Anthropic Claude | Parental report generation, borderline content explanation | `CLAUDE_API_KEY` | claude-sonnet-4-6 |
| OpenAI GPT-4o | Alternative explanation backend | `OPENAI_API_KEY` | gpt-4o |
| Ollama (local) | Default offline explanation engine | `OLLAMA_BASE_URL` | mistral:7b-instruct |

---

## HuggingFace Models in Use

| Model ID | Purpose | Link |
|---|---|---|
| `unitary/unbiased-toxic-roberta` | Text toxicity & hate speech detection | https://huggingface.co/unitary/unbiased-toxic-roberta |
| `Falconsai/nsfw_image_detection` | NSFW image classification | https://huggingface.co/Falconsai/nsfw_image_detection |
| `dima806/violent_action_image_detection` | Violence in images/video frames | https://huggingface.co/dima806/violent_action_image_detection |
| `cardiffnlp/twitter-roberta-base-hate` | Hate speech & radicalization signals | https://huggingface.co/cardiffnlp/twitter-roberta-base-hate |
| `facebook/bart-large-mnli` | Zero-shot content category classification | https://huggingface.co/facebook/bart-large-mnli |
| `openai/clip-vit-large-patch14` | Multimodal text-image alignment scoring | https://huggingface.co/openai/clip-vit-large-patch14 |
| `facebook/wav2vec2-base-960h` | Audio transcription for spoken harm detection | https://huggingface.co/facebook/wav2vec2-base-960h |
| `distilbert-base-uncased` | Base for fine-tuned scam/phishing classifier | https://huggingface.co/distilbert-base-uncased |

---

## Current Active Development Tasks
- [ ] Survey existing child safety datasets (Common Crawl filtered, JigSaw Toxic, LAION-5B audit)
- [ ] Set up local inference pipeline with ONNX-optimized models for CPU efficiency
- [ ] Design age-band threshold matrix (0–5, 6–9, 10–12, 13+)
- [ ] Build browser extension scaffold (MV3 / WebExtension API)
- [ ] Design SQLite schema for content log + parental dashboard
- [ ] Prototype brain-rot engagement scorer (temporal pattern analysis)
- [ ] Collect scam/phishing patterns targeting children for training data

---

## Related Files
- `PROJECT-detail.md` — full technical specification and architecture
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — phase roadmap with milestones
- `SECOND-KNOWLEDGE-BRAIN.md` — research papers, SOTA models, self-update protocol
