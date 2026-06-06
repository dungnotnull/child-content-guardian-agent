# SECOND-KNOWLEDGE-BRAIN.md — Child Content Guardian

## Knowledge Repository
This document serves as the long-term memory for the project, storing research, paper summaries, and architectural decisions.

## 1. Child Online Safety Literature
| Paper/Source | Key Insight | Application to Project | Status |
|---|---|---|---|
| Common Sense Media | Age-appropriate content ratings based on cognitive development | Used to define initial 	hresholds.json | Reviewed |
| CEOP Annual Report | Common grooming patterns and scam triggers | Informs the DistilBERT scam detector training | Pending |
| JigSaw Toxic Comments | Dataset for identifying hate speech and toxicity | Base for text classifier selection | Reviewed |

## 2. Model Selection Logic
- **Text**: RoBERTa was chosen over BERT for better performance on short-form toxic comments.
- **Images**: Use a multi-stage approach: NSFW detector $\rightarrow$ Violence detector.
- **Inference**: ONNX Runtime is the target for CPU acceleration to keep latency $<300\text{ms}$.

## 3. Decision Matrix Assumptions
- **Strict Mode (3-6y)**: Block anything with toxicity $> 0.3$.
- **Relaxed Mode (13-17y)**: Allow educational content with mild complexity, only block high-certainty NSFW/Violence.
