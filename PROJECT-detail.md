# PROJECT-detail.md — child-content-guardian

## Executive Summary
child-content-guardian is a privacy-first, on-device AI content filter that protects children from the full spectrum of harmful digital content: explicit/violent material, online scams targeting minors, radicalization pipelines, and algorithmically-amplified "brain rot" content. It deploys a multimodal ML/DL pipeline (text + image + video + audio) with age-adaptive filtering thresholds and a self-improving knowledge base. All inference runs locally; no child behavioral data leaves the device.

---

## Problem Statement

### The Scale of the Threat
- **3.8 billion** children and teens use the internet globally; the average age of first smartphone access is now 9–10 years old in developed countries (Common Sense Media, 2023).
- Social media algorithms optimize for engagement, not wellbeing — children's developing dopamine reward systems are particularly susceptible to feedback loops created by short-form video (TikTok, YouTube Shorts, Reels).
- The WHO classifies "gaming disorder" as an ICD-11 diagnosis (2022); emerging research links excessive algorithmic content consumption with ADHD-like attention fragmentation in children under 12.
- The FBI's 2023 IC3 report lists children as a fast-growing target segment for online scams (fake gaming rewards, virtual currency fraud, sextortion schemes).
- Radicalization researchers at ISD Global document pipelines from mainstream platforms (YouTube) to extremist content in under 6 recommendation hops.

### Why Existing Solutions Fall Short
| Existing Tool | Gap |
|---|---|
| Platform-native filters (YouTube Kids, SafeSearch) | Platform-specific, easily bypassed, no multimodal ML |
| DNS-based blocklists (CleanBrowsing, OpenDNS) | URL-based only, cannot analyze content within a page |
| Parental control apps (Circle, Bark) | Subscription SaaS, uploads content metadata to cloud, no ML |
| Browser extensions (uBlock, etc.) | Ad-blocking only, no content classification |

### The Root Gap
No consumer-grade solution applies full ML/DL multimodal analysis at the content level, with per-age-group adaptive thresholds, on-device privacy, and a self-improving model that tracks emerging threat patterns (new scam types, new brain-rot content formats, new radicalization memes).

---

## Target Users & Use Cases

### Primary Users
- **Parents** of children aged 4–16 who want proactive protection beyond manual supervision
- **Schools / Educational institutions** deploying shared devices in classrooms
- **Child psychologists** who need data on a child's exposure patterns for therapeutic context

### Use Cases
1. **Home browsing protection**: Browser extension intercepts all page content (text, images, video) before rendering, blocks or warns on harmful material
2. **Age-appropriate streaming**: YouTube/TikTok embedded video frame analysis blocks individual videos rather than entire platform
3. **Scam interception**: Real-time phishing/scam pattern detection in chat apps and email webclients
4. **Brain-rot monitoring**: Daily "healthy media diet" dashboard showing time spent on high-engagement-score vs educational content
5. **Parental reporting**: Weekly AI-generated report (via local Ollama or Claude API) summarizing what was blocked and why, with actionable recommendations

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│                  BROWSER / APPLICATION LAYER              │
│   Chrome Extension (MV3) │ Firefox Add-on │ System Proxy │
└──────────────┬───────────────────────────────────────────┘
               │ Raw content (HTML, images, video URLs, audio)
               ▼
┌──────────────────────────────────────────────────────────┐
│               INGESTION & PREPROCESSING LAYER             │
│  Text Extractor │ Image Downsampler │ Video Frame Sampler │
│  Audio Transcriber (wav2vec2)       │ URL Reputation Cache│
└──────────────┬───────────────────────────────────────────┘
               │ Normalized features per modality
               ▼
┌──────────────────────────────────────────────────────────┐
│                  AGE PROFILE MANAGER                      │
│  Active Profile: {age_band, custom_rules, brain_rot_budget}│
│  Threshold Matrix: per-category per-age-band cutoffs      │
└──────────────┬───────────────────────────────────────────┘
               │ Profile-aware threshold config
               ▼
┌──────────────────────────────────────────────────────────┐
│               ML/DL CLASSIFIER PIPELINE                   │
│                                                          │
│  ┌─────────────────┐  ┌─────────────────┐               │
│  │ Text Classifier  │  │ Image Classifier │               │
│  │ toxic-roberta    │  │ nsfw_image_det.  │               │
│  │ hate-roberta     │  │ violence_detect  │               │
│  │ scam-distilbert  │  │ CLIP alignment   │               │
│  └────────┬────────┘  └────────┬────────┘               │
│           │                    │                          │
│  ┌────────▼────────┐  ┌────────▼────────┐               │
│  │ Audio Classifier │  │ Brain-Rot Scorer │               │
│  │ wav2vec2 + head  │  │ Temporal LSTM    │               │
│  │ (spoken content) │  │ (engagement/dopamine│            │
│  └────────┬────────┘  └────────┬────────┘               │
│           └──────────┬─────────┘                          │
│                      ▼                                    │
│           ┌─────────────────────┐                         │
│           │   DECISION ENGINE   │                         │
│           │  Ensemble Voter +   │                         │
│           │  Age-Threshold Gate │                         │
│           └──────────┬──────────┘                         │
└──────────────────────┼───────────────────────────────────┘
                       │
           ┌───────────┼───────────┐
           ▼           ▼           ▼
        [BLOCK]     [WARN]     [ALLOW]
     Safe redirect  Overlay   Pass-through
           │           │
           └─────┬─────┘
                 ▼
┌──────────────────────────────────────────────────────────┐
│              LOCAL STORAGE & PARENTAL DASHBOARD           │
│  SQLite (AES-256) │ FastAPI server │ React UI             │
│  Weekly LLM Report │ Override Controls │ Child Profiles   │
└──────────────────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────┐
│           SELF-IMPROVING KNOWLEDGE LOOP                   │
│  crawl4ai pipeline → SECOND-KNOWLEDGE-BRAIN.md update     │
│  New scam patterns → scam classifier fine-tuning dataset  │
│  New research → threshold calibration review              │
└──────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Component | Technology | Source |
|---|---|---|
| Backend API | FastAPI 0.111 + Uvicorn | PyPI |
| Browser Extension | WebExtension API (MV3) + Vite | npm |
| Parental Dashboard UI | React 18 + TailwindCSS | npm |
| Text classification | Transformers 4.40 (HuggingFace) | PyPI |
| Image classification | Transformers + timm | PyPI |
| Audio processing | torchaudio + wav2vec2 | PyPI |
| Video frame sampling | OpenCV 4.9 | PyPI |
| Local inference optimization | ONNX Runtime 1.18 | PyPI |
| Local SLM | Ollama (Mistral-7B-Instruct) | ollama.ai |
| Local database | SQLite 3 + SQLCipher (AES-256) | system |
| Encryption | cryptography 42.x (Fernet) | PyPI |
| Content crawling | crawl4ai 0.3 | PyPI |
| Scam URL reputation | Google Safe Browsing API (optional) | Google |
| Dependency management | uv | astral.sh |

---

## ML/DL Models

### Deployed Models (HuggingFace)

| Model ID | Task | Input | Output | Fine-tune Plan |
|---|---|---|---|---|
| `unitary/unbiased-toxic-roberta` | Multi-label toxicity (toxic, obscene, threat, insult, identity_hate) | text | 6-class scores | Fine-tune on child-specific corpus |
| `cardiffnlp/twitter-roberta-base-hate` | Hate speech & radicalization signals | text | binary + confidence | No fine-tune needed (MVP) |
| `facebook/bart-large-mnli` | Zero-shot: age-appropriateness categories | text | category probabilities | No fine-tune (zero-shot) |
| `Falconsai/nsfw_image_detection` | NSFW image binary classification | image (224×224) | safe/unsafe probability | No fine-tune needed |
| `dima806/violent_action_image_detection` | Violence detection in images/frames | image | binary violence score | No fine-tune (MVP) |
| `openai/clip-vit-large-patch14` | Cross-modal text-image alignment scoring | image + text | similarity score | No fine-tune |
| `facebook/wav2vec2-base-960h` | Audio → text transcription | audio waveform | transcript text | No fine-tune (feeds text pipeline) |
| `distilbert-base-uncased` | Base for scam/phishing classifier | text | scam category | Fine-tune on child-scam dataset (Phase 2) |

### Custom Models (to Build)

| Model | Architecture | Training Data | Purpose |
|---|---|---|---|
| Brain-Rot Engagement Scorer | Bidirectional LSTM + attention | Video metadata: scene change rate, color saturation variance, audio BPM, duration, like/share ratio | Score 0–1 for dopamine-bait content patterns |
| Age-Appropriate Text Rater | RoBERTa fine-tuned | Common Sense Media ratings corpus + manual annotation | Predict age suitability (0-5 / 6-9 / 10-12 / 13+) |
| Child-Targeted Scam Detector | DistilBERT fine-tuned | Curated dataset of gift card scams, fake gaming rewards, grooming openers | Binary + category classification |

### Training Data Sources
- JigSaw Toxic Comment Classification (Kaggle — public)
- Common Sense Media ratings database (licensed)
- LAION-5B safety audit subset (HuggingFace)
- PhishTank / OpenPhish (scam URL patterns)
- Child Exploitation and Online Protection (CEOP) threat intelligence reports (public)
- Manually annotated "brain rot" YouTube Shorts dataset (to be collected via crawl4ai)

---

## External LLM API Integration

Pluggable backend — controlled via `LLM_PROVIDER` environment variable.

```python
# config.py
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")  # ollama | claude | openai

LLM_CONFIG = {
    "ollama":  {"base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"), "model": "mistral:7b-instruct"},
    "claude":  {"api_key": os.getenv("CLAUDE_API_KEY"), "model": "claude-sonnet-4-6"},
    "openai":  {"api_key": os.getenv("OPENAI_API_KEY"), "model": "gpt-4o"},
}
```

**LLM Use Cases:**
- Generating human-readable explanations for blocked content (why was this blocked?)
- Writing the weekly parental summary report
- Answering parent questions: "Is this game safe for my 7-year-old?"
- Providing child-appropriate redirect messages when content is blocked

---

## Feature Specification

### MVP Features
- [ ] Text toxicity filtering (toxic-roberta) with configurable sensitivity
- [ ] NSFW image blocking in browser pages
- [ ] Scam/phishing URL and text pattern detection
- [ ] Three age profiles: Young Child (0–5), Child (6–12), Teen (13+)
- [ ] Block / Warn / Allow decision with parent notification
- [ ] Local SQLite log of all blocked events
- [ ] Simple React parental dashboard (view log, override, adjust profile)
- [ ] Chrome extension (Manifest V3) integration

### Advanced Features
- [ ] Video frame-level analysis (OpenCV + image classifiers at 1 fps)
- [ ] Audio harm detection via wav2vec2 transcription pipeline
- [ ] Brain-rot engagement scorer with daily budget controls
- [ ] Fine-grained age bands (0-5, 6-9, 10-12, 13-15, 16+)
- [ ] Weekly AI-generated parental report (Ollama/Claude)
- [ ] Multi-child household profiles with separate controls per child
- [ ] Self-improving scam pattern library (crawl4ai weekly update)
- [ ] Firefox add-on support
- [ ] System-level proxy mode (covers all apps, not just browser)
- [ ] Offline mode (all inference on-device, no internet required)
- [ ] Content time-boxing: block category X after N minutes/day
- [ ] "Learning mode": flag but don't block — builds a detailed exposure report for parent review
- [ ] Parent override with PIN + timed unlock (e.g., allow category for 30 minutes)
- [ ] Cross-platform: Windows 10/11, macOS 13+, Ubuntu 22+

---

## Full E2E Data Flow

1. Child opens browser tab; Chrome extension intercepts page load request
2. Extension extracts text (DOM), image URLs, and video embed URLs from the page
3. Content sent via local HTTP to FastAPI backend (localhost:8765) — never to internet
4. Backend loads the active child's age profile and threshold matrix
5. Text content → tokenized → fed to toxic-roberta + hate-roberta + scam-distilbert in parallel
6. Image URLs → downloaded locally → resized to 224×224 → fed to nsfw_image_detection + violence_detector
7. Video embed URL → first 3 frames sampled via OpenCV → processed same as images; metadata extracted for brain-rot scorer
8. Audio (if stream) → 5-second chunks → wav2vec2 transcription → text fed to text classifiers
9. CLIP alignment score computed for any (image, surrounding text) pair
10. All classifier outputs → Decision Engine applies age-adaptive threshold matrix
11. Ensemble vote: if ≥ 3 of 5 modalities flag content → BLOCK; ≥ 2 → WARN; <2 → ALLOW
12. Extension receives decision; applies block overlay / warning overlay / transparent pass-through
13. Event logged to SQLite (encrypted): timestamp, URL, content hash, classifier scores, decision, child profile
14. Parent dashboard polls local API for new events; sends push notification if configured
15. Weekly cron job invokes LLM to generate parental summary from the week's log

---

## Privacy & Security

| Concern | Mitigation |
|---|---|
| Child browsing data privacy | All data stored in AES-256 encrypted SQLite on-device. Zero cloud upload. |
| Parent dashboard authentication | PIN-protected dashboard, bcrypt-hashed. Dashboard only accessible on localhost. |
| Model weights tampering | SHA-256 hash verification of all downloaded model weights at startup |
| Extension XSS risk | Content Security Policy headers on all extension pages; no remote script loading |
| Local API exposure | FastAPI bound to 127.0.0.1 only; authentication token required for all endpoints |
| False positive impact | All blocks logged with scores; parent can review and create allowlist entries |
| Data retention | Configurable retention period (default 30 days); auto-purge on schedule |

---

## Key Python/JS Dependencies

```
# Python (pyproject.toml)
transformers>=4.40.0
torch>=2.3.0
onnxruntime>=1.18.0
torchaudio>=2.3.0
opencv-python>=4.9.0
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
sqlalchemy>=2.0.0
cryptography>=42.0.0
crawl4ai>=0.3.0
httpx>=0.27.0
pydantic>=2.7.0
python-multipart>=0.0.9
anthropic>=0.28.0
openai>=1.30.0

# JavaScript (package.json)
react: ^18.3.0
vite: ^5.2.0
tailwindcss: ^3.4.0
webextension-polyfill: ^0.10.0
axios: ^1.7.0
recharts: ^2.12.0   # dashboard charts
```

---

## Improvement Suggestions

1. **Federated threat intelligence**: Allow opt-in sharing of scam pattern signatures (not content, just hashes/signatures) between instances — builds a community threat map without leaking any child data
2. **Developmental psychology integration**: Partner with child psychologists to calibrate thresholds based on peer-reviewed developmental stage research rather than arbitrary age cutoffs
3. **Positive content scoring**: Complement the harm filter with a "beneficial content" scorer (educational, creative, prosocial) — parents see both what was blocked AND what was enriching
4. **Gaze-tracking integration**: On devices with front camera, optionally detect if child is showing stress responses (rapid blinking, leaning in) to flag borderline-pass content for parental review
5. **School network mode**: Batch API mode for IT admins managing shared school devices — central dashboard, per-student profiles, compliance reporting
6. **Multilingual expansion**: Initial models are primarily English; add Vietnamese language support (Viet phoBERT) for local market relevance
7. **Longitudinal behavior analysis**: Track a child's exposure patterns over months — if a child's content consumption drifts toward increasingly edge content, alert parent even if individual items pass the filter
8. **Game-specific scanner**: Dedicated scanner for in-game chat (Roblox, Minecraft servers) where text-based grooming and scam solicitation is increasingly common
9. **Adversarial robustness**: Train against known filter bypass techniques (l33tspeak, image-embedded text, multilingual code-switching used by bad actors)
10. **Explainable AI dashboard**: Show parents exactly which words/image regions triggered a block using SHAP/Grad-CAM explanations — builds trust and teaches media literacy
