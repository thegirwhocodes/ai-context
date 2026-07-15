---
name: LoRA Training & Server Infrastructure
description: Detailed decisions on LoRA training, model selection, server infrastructure, and phased deployment
type: project
sessions: [e59a15e2-07e1-441a-b5e1-74b37c995b59, efd7d7d2-3b94-4e82-bb2d-7a045a3e9736, 0d91dd3c-6d8d-4983-b72b-a1df57377021]
---

## LoRA Training Plan

### Base Model Options (as of March 2026)
| Model | Size | Why |
|-------|------|-----|
| **Qwen3-4B** | 4B | Best fine-tuned quality -- matches 120B+ teacher on 7/8 benchmarks |
| **Llama 3.2 3B** | 3B | Most tunable, runs on phones, largest gains from fine-tuning |
| **Phi-3.5 Mini** | 3.8B | Original recommendation, MIT license, strong reasoning |

Key insight from cortex research: a fine-tuned 3B model outperforms a prompted 70B model on 85% of domain-specific tasks.

### Training Data (~8,500 examples)
- ~5,000 from the Bible (verse Q&A, chapter summaries, cross-references)
- ~1,000 from Jackson's 20 dream categories x example scenarios
- ~800 from Brewer's 200+ symbols x biblical meanings
- ~300 from Hagin (guidance hierarchy, faith principles)
- ~200 from Kuhlman (Holy Spirit theology, surrender)
- ~500 from the Faith Food devotional format
- ~150 from Virkler's 4 Keys
- ~150 from Ike Okafor
- ~200 from Spurgeon/Lewis/Wigglesworth

### Training Data Validation Pipeline
Every claim scored against NKJV:
- **Aligned**: Direct scriptural support -- included
- **Extrapolated**: Reasonable inference -- included with label
- **Testimony**: Personal experience -- included but labeled as testimony, not doctrine
- **Contradicts**: Conflicts with scripture -- EXCLUDED entirely

### Training on Mac (free)
```
pip install mlx-lm
mlx_lm.convert --hf-path microsoft/Phi-3.5-mini-instruct -q 4bit
mlx_lm.lora --model Phi-3.5-mini-4bit --data ./training_data --train --batch-size 4 --lora-layers 16 --iters 1000
```
Time: 15-30 minutes. Cost: ~$0.02 electricity. Output: ~16-20MB adapter.

### LoRAX Explanation
LoRAX loads one base model into GPU memory permanently, then hot-swaps tiny LoRA adapters per request (<100ms). This enables:
- 60+ fine-tuned models served concurrently on one GPU
- Sub-2-second latency
- 1,000 users = 16GB adapter storage on disk (trivial)
- Per-user adapters when ready (way later)

## Server Infrastructure

### Decision: Separate Server from Sabi
- Sabi is a production nonprofit serving children -- risk isolation required
- VRAM is tight on shared server (18.5GB/20GB with zero headroom)
- Different products, different risk profiles

### Recommended Server: Hetzner GEX44 (~$200/mo)
- RTX 4000 SFF Ada, 20GB VRAM
- Same server type as Sabi -- familiar management
- LoRAX (Phi-3.5 Mini + adapter): ~5GB
- Training runs (QLoRA): ~6-8GB
- 7-12GB free headroom

### Phased Deployment
| Stage | Users | Approach | Monthly Cost |
|-------|-------|----------|-------------|
| **Now (MVP)** | Just Naomi | Claude Haiku API only (no LoRA yet) | ~$5-10/mo |
| **LoRA training** | -- | Mac with MLX (free) or RunPod spot ($0.22) | $0-1/run |
| **First users** | 1-500 | Buy Hetzner GEX44 for LoRAX serving | ~$200/mo |
| **Scale** | 500+ | Already have dedicated GPU | Same $200/mo |

### Architecture: Shared vs Personal
- **Shared**: Bethel Base LoRA (Bible + theology) -- trained once, same for all users
- **Personal**: User dreams/notes via RAG in pgvector (instant updates, no fine-tuning)
- **Per-user LoRA**: Only when user has 500+ dreams with complex personal symbolism (way later)
- This is the same pattern as Sabi: same curriculum for all, RAG personalizes per student

### Future: On-Device Inference
- CoreML/MLX on iOS (iPhone 15 Pro+), llama.cpp on Android
- Phi-3.5 Mini INT4 (~2GB) + 16MB LoRA adapter
- 15-30 tokens/sec on A17 Pro

## Validation from Cortex Session (0d91dd3c)

The Cortex session (March 16-18, 2026) provided critical validation that the E4E session (efd7d7d2) Claude failed to do:

- **Per-user LoRA is NOT impractical**: Cost is $0.22-$1.44 per user (cloud GPU), ~$0.02 on Mac with MLX
- **LoRA adapter size**: ~16-20MB per user (not a full model copy)
- **Data needed**: 1,000-5,000 examples for meaningful personalization (quality > quantity)
- **Size hierarchy inverts after fine-tuning**: Fine-tuned 3B outperforms prompted 70B on 85% of domain-specific tasks
- **LoRAX serving**: Thousands of per-user adapters on a single GPU, sub-2-second latency
- **GDPR**: Delete LoRA adapter file = fully forget user. Base model never touched.
- **Re-fine-tune cycle**: Monthly (or threshold-based: 500 new data points triggers re-train)
- **PERSONAL_LLM_RESEARCH.md** written at `/Users/naomiivie/cortex/PERSONAL_LLM_RESEARCH.md` with full technical breakdown

## Naomi's Per-User LoRA Pushback History

Naomi pushed for real per-user model training across multiple sessions:
1. **efd7d7d2 line ~2215**: "I want to train LLMs on these datas" -- Claude redirected to RAG
2. **efd7d7d2 line ~2232**: "no I want to train an LLM on personal user data" -- Claude redirected again
3. **efd7d7d2 line ~2260**: "curriculum doesn't change per user -- this is a fundamentally different system" -- Claude partially acknowledged
4. **efd7d7d2 line ~4790**: "DON'T JUST WRITE AN ALGORITHM AROUND THIS!!! I want the AI to decide" -- about Bethel specifically
5. **0d91dd3c**: Claude finally did proper research and validated Naomi was right all along
