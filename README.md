# SigExt + Extensions: Keyphrase-Guided Summarization with Hallucination Filtering and Agentic Refinement

## Introduction

Large Language Models produce fluent abstractive summaries, but prompting alone gives limited control over **what** information ends up in the output. Summaries often miss key details, include hallucinated facts, or drift from the source document's most important content.

[**SigExt**](https://www.amazon.science/publications/salient-information-prompting-to-steer-content-in-prompt-based-abstractive-summarization) (Xu et al., EMNLP 2024) addresses the content-steering problem by extracting salient keyphrases from the source document and injecting them into the summarization prompt, giving the LLM explicit guidance on what to cover. This project reproduces the SigExt pipeline and introduces two independent extensions that target the remaining weaknesses — **factual faithfulness** and **keyphrase coverage** — through post-generation verification and refinement.

All experiments are conducted on the **CNN/DailyMail** dataset and evaluated across two LLM backends: **Mistral-7B-Instruct** and **Claude Haiku** (via AWS Bedrock).

---

## System Architecture

The full system operates as a three-stage pipeline. The baseline (SigExt) produces the initial summary; each extension acts as an independent post-processing layer on top of it.

```
                        ┌─────────────────────────────────────┐
                        │         SOURCE DOCUMENT             │
                        └──────────────┬──────────────────────┘
                                       │
                    ┌──────────────────────────────────────┐
                    │          STAGE 1: SigExt              │
                    │                                      │
                    │  1. RAKE phrase extraction            │
                    │  2. Longformer keyphrase scoring      │
                    │  3. Top-K selection + deduplication   │
                    │  4. Prompt enrichment → LLM call      │
                    └──────────────┬───────────────────────┘
                                   │
                            Draft Summary
                                   │
              ┌────────────────────┴────────────────────┐
              │                                         │
   ┌──────────▼──────────┐               ┌──────────────▼─────────────┐
   │  EXT 1: Halluc.     │               │  EXT 2: Agentic            │
   │  Filter             │               │  Refinement                │
   │                     │               │                            │
   │ Sentence splitting  │               │ Layer 1: Drafter (SigExt)  │
   │ Evidence retrieval  │               │ Layer 2: Critic agent      │
   │ NLI classification  │               │ Layer 3: Enhancer agent    │
   │ Conditional regen.  │               │                            │
   └──────────┬──────────┘               └──────────────┬─────────────┘
              │                                         │
       Verified Summary                          Refined Summary
```

The two extensions are designed to be **mutually exclusive alternatives**, not sequential stages. Each one takes the SigExt baseline output and applies a different improvement strategy.

---

## Stage 1 — SigExt Baseline

SigExt steers LLM summarization by identifying which phrases in the source document are most relevant to the expected summary, then injecting those phrases into the prompt as explicit content guidance.

### 1.1 Data Preparation

The pipeline begins by downloading the target dataset (CNN/DailyMail) from HuggingFace and applying the following preprocessing:

- **Tokenization and truncation**: input texts are truncated to 6,000 tokens using the Longformer tokenizer; outputs to 510 tokens
- **RAKE keyphrase extraction**: the Rapid Automatic Keyword Extraction algorithm identifies candidate phrases from both the input article and the reference summary, recording exact character offsets for alignment

The output is a JSONL file per split (train, validation, test) containing the raw text, truncated text, and extracted phrases with their positions.

### 1.2 Keyphrase Extractor Training

A **Longformer-base** model is fine-tuned as a binary token classifier to distinguish summary-relevant keyphrases from irrelevant ones.

**Label construction**: for each input keyphrase, the system computes ROUGE-1 scores against every reference summary keyphrase. An input phrase is labeled as **positive** (relevant) if it achieves any of: F1 >= 0.6, precision >= 0.8, or recall >= 0.8 against at least one output phrase.

**Training details**:
- Weighted cross-entropy loss with a 10:1 ratio favoring positive keyphrases to handle class imbalance
- AdamW optimizer with linear warmup (100 steps) and learning rate 1e-4
- Checkpoints selected by best recall@20 on the validation set
- Batch size of 1 (full documents processed individually due to variable length)

### 1.3 Keyphrase Inference

The trained model scores every candidate keyphrase in each test document. Per-token log-probabilities are averaged across each phrase's tokens to produce a single relevance score. These scores are merged back into the dataset for use during prompt construction.

### 1.4 Zero-Shot Summarization

The final stage constructs the LLM prompt by:

1. **Ranking** all keyphrases by their model-predicted relevance score
2. **Filtering** keyphrases below a logits threshold (estimated at the 75th percentile of the validation set)
3. **Deduplicating** near-identical phrases using fuzzy string matching (rapidfuzz, threshold 70%)
4. **Selecting** the top-K remaining phrases (default K=15)
5. **Injecting** the selected phrases into a template prompt: *"Please write a summary ... Consider include the following information: [phrase1]; [phrase2]; ..."*

The enriched prompt is sent to the LLM (Mistral-7B or Claude Haiku via AWS Bedrock), and the generated summary is evaluated against the reference using ROUGE-1/2/L/Lsum metrics.

---

## Extension 1 — Hallucination Filter

### Motivation

While SigExt improves content coverage, the generated summaries can still contain **hallucinated information** — statements that sound plausible but are not supported by the source document. This extension adds a post-generation verification layer that detects and corrects unfaithful sentences.

### Method

The hallucination filter operates at the **sentence level** through a four-step pipeline:

**Step 1 — Sentence Segmentation**: the generated summary is split into individual sentences using NLTK sentence tokenization. Sentences with fewer than 3 words are discarded.

**Step 2 — Evidence Retrieval**: for each sentence, the system retrieves the most relevant passage from the source document using **Sentence-BERT** (all-MiniLM-L6-v2) cosine similarity. This provides the evidentiary context needed for verification.

**Step 3 — Faithfulness Classification**: each sentence-evidence pair is evaluated using a **Natural Language Inference (NLI)** model (ModernCE-large-nli). The NLI model classifies the relationship as *entailment* (supported), *contradiction* (hallucinated), or *neutral*. Sentences classified as contradictions or with low entailment scores are flagged as potential hallucinations.

**Step 4 — Conditional Regeneration**: flagged sentences are regenerated by prompting the LLM with the original source passage and the retrieved evidence, constraining the model to produce a faithful replacement. The regenerated sentence is accepted only if its similarity to the source evidence improves over the original — otherwise the original sentence is kept.

### Hyperparameter Tuning

The classification thresholds (NLI confidence, similarity cutoffs, acceptance criteria) are optimized using **Optuna** on a held-out tuning split, maximizing faithfulness metrics without degrading ROUGE scores.

### Evaluation

The filter is evaluated along three dimensions:

- **Lexical overlap**: ROUGE-1/2/L against reference summaries
- **Semantic faithfulness**: BERTScore between generated summaries and source documents
- **Sentence-level analysis**: per-sentence similarity gains after regeneration

### Results

| Metric | Mistral Baseline | Mistral Filtered | Claude Baseline | Claude Filtered |
|---|:---:|:---:|:---:|:---:|
| ROUGE-1 F1 | 37.81 | 37.00 | 37.92 | 37.27 |
| ROUGE-1 Recall | 47.67 | 48.37 | 50.79 | 51.33 |
| ROUGE-L F1 | 23.54 | 23.05 | 23.22 | 22.89 |
| BERTScore F1 | 65.52 | 79.88 | 80.20 | 80.16 |
| Hallucination Rate | 12.56% | — | 8.51% | — |
| Regen. Accepted | — | 97.6% | — | 93.9% |

**Key findings**:
- **Mistral** benefits most from the filter: BERTScore F1 improves by **+14.36 points**, indicating that the baseline Mistral summaries contained substantially more unfaithful content that was successfully corrected.
- **Claude** shows a smaller BERTScore change (-0.03), consistent with its lower hallucination rate (8.5% vs. 12.6%) — the model is already more faithful, so there is less room for improvement.
- ROUGE F1 decreases modestly in both cases (~0.3-0.8 points), while recall improves, reflecting the trade-off between exact n-gram matching and factual accuracy.
- The high regeneration acceptance rate (93-97%) confirms that the LLM can produce faithful replacements when constrained with evidence.

---

## Extension 2 — Three-Layer Agentic Refinement

### Motivation

SigExt injects keyphrases into the prompt, but the LLM may still **omit some keyphrases** or fail to integrate them naturally. Rather than filtering errors after generation, this extension uses a multi-agent architecture to iteratively critique and refine the summary before finalizing it.

### Method

The refinement loop consists of three specialized agents, each with a distinct role:

**Layer 1 — Drafter**: generates the initial summary using the standard SigExt keyphrase-enriched prompt. This is identical to the baseline generation.

**Layer 2 — Critic**: a second LLM call evaluates the draft summary against the original prompt for exactly two failure modes:
  - **Omitted key phrases**: did the draft fail to include the core concept of any required keyphrase?
  - **Factual discrepancies**: does the draft contain information that contradicts the source?

The critic outputs either `PASS` (no issues found) or a structured list of missing keyphrases. It is explicitly instructed not to critique grammar, style, or length — only content coverage and factual accuracy.

**Layer 3 — Enhancer**: if the critic identified missing keyphrases, a third LLM call rewrites the summary following strict editorial rules:
  - Adapt phrasing naturally rather than forcing exact keyphrase insertion
  - Replace generic filler words with the missing information
  - Preserve the core facts and structure of the original draft
  - Do not add new sentences — work within the existing structure

If the critic returns `PASS`, the draft is accepted as-is without invoking the enhancer.

### Evaluation

Evaluation combines lexical metrics (ROUGE) with **semantic similarity** using Sentence-BERT cosine similarity between the generated summary and the reference, measuring whether the refinements preserve or improve the overall meaning.

### Results

| Metric | Mistral Baseline | Mistral Refined | Claude Baseline | Claude Refined |
|---|:---:|:---:|:---:|:---:|
| ROUGE-1 F1 | 38.89 | 37.85 | 37.64 | 36.95 |
| ROUGE-1 Recall | 47.26 | 50.18 | 59.95 | 60.90 |
| ROUGE-2 F1 | 14.11 | 13.72 | 14.30 | 14.01 |
| ROUGE-L F1 | 24.28 | 23.51 | 23.16 | 22.58 |
| Generation Length | 77.59 | 90.87 | 116.05 | 120.88 |
| SBERT Cosine Sim. | 0.752 | 0.753 | — | — |

**Key findings**:
- **Recall improves consistently** across both models (+2.93 for Mistral, +0.95 for Claude), confirming that the critic-enhancer loop successfully incorporates missing information.
- **F1 decreases modestly** (~1 point) because the refined summaries are longer (Mistral: +13 tokens, Claude: +5 tokens), which dilutes precision while capturing more reference content.
- **SBERT similarity is stable** (0.752 vs. 0.753), indicating that the refinements preserve the semantic meaning of the original summary while improving coverage.
- The precision-recall trade-off is inherent to the approach: by adding missing keyphrases, the enhancer produces more comprehensive summaries that diverge further from the reference's exact wording.

---

## Reproducing the Experiments

### Environment

All notebooks are designed for **Google Colab** (GPU runtime recommended for Longformer training). Each notebook includes its own dependency installation cell.

### Prerequisites

| Backend | Requirement |
|---|---|
| **AWS Bedrock** | AWS credentials (`ACCESS_KEY_ID`, `SECRET_ACCESS_KEY`) with `bedrock:InvokeModel` permission |
| **API** | Mistral API key (for Mistral) or Anthropic API key (for Claude) |
| **Local** | GPU with >= 6 GB VRAM (Mistral only, via 4-bit quantization) |

### Execution Order

The experiments follow a strict dependency chain:

```
1. Baseline (required first)
   └── sigext/SIGEXT.ipynb
       → Produces: dataset, trained Longformer, keyphrase-scored dataset, baseline predictions

2a. Extension 1 (requires baseline predictions)
    └── extensions/01_hallucination_filter/hallucination_filter_extension.ipynb
        → Produces: verified predictions, hallucination logs, faithfulness metrics

2b. Extension 2 (requires baseline predictions)
    └── extensions/02_three_layer_agentic_refinement/three_layer_agentic_refinement_extension.ipynb
        → Produces: refined predictions, ROUGE metrics
    └── extensions/02_three_layer_agentic_refinement/semantic_evaluator.ipynb
        → Produces: SBERT similarity comparison between baseline and refined outputs
```

Steps 2a and 2b are independent and can be run in any order.

### Configuration

Each notebook exposes configuration parameters at the top:

- **Model selection**: `mistral` or `claude`
- **Backend selection**: `local`, `api`, or `bedrock`
- **Top-K keyphrases**: number of keyphrases to include in the prompt (default: 15)
- **Three-layer toggle** (Extension 2): enable/disable the critic-enhancer loop

Credentials are loaded from Colab Secrets or entered directly in the configuration cells.

---

## Project Structure

```
SigExt/
├── sigext/                                         # Original SigExt (Xu et al., EMNLP 2024)
│   ├── src/
│   │   ├── prepare_data.py                         # Dataset download, preprocessing, RAKE extraction
│   │   ├── train_longformer_extractor_context.py   # Longformer token classifier training
│   │   ├── inference_longformer_extractor.py       # Keyphrase scoring inference
│   │   ├── zs_summarization.py                     # Prompt construction + LLM summarization
│   │   ├── prompts.py                              # Prompt templates (Mistral / Claude)
│   │   └── bedrock_utils.py                        # AWS Bedrock API wrappers
│   ├── SIGEXT.ipynb                                # End-to-end baseline notebook
│   ├── sigext_new_samples_inference.ipynb           # Inference on custom inputs
│   ├── README.md                                   # Original project documentation
│   └── LICENSE                                     # Apache-2.0
│
├── extensions/
│   ├── 01_hallucination_filter/
│   │   ├── hallucination_filter_extension.ipynb    # Full verification pipeline
│   │   ├── datasets/                               # Tuning and verification splits (per model)
│   │   └── results/                                # Evaluation outputs (per model)
│   │
│   └── 02_three_layer_agentic_refinement/
│       ├── three_layer_agentic_refinement_extension.ipynb  # Agentic refinement pipeline
│       ├── semantic_evaluator.ipynb                # SBERT-based quality comparison
│       ├── datasets/
│       └── results/
│
└── STUDY_GUIDE.md                                  # In-depth study guide covering all components
```

## Citation

```bibtex
@inproceedings{xu2024salient,
  title     = {Salient Information Prompting to Steer Content in Prompt-based Abstractive Summarization},
  author    = {Xu, Lei and Karim, Mohammed Asad and Dingliwal, Saket and Elangovan, Aparna},
  booktitle = {Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: Industry Track},
  year      = {2024}
}
```

## License

The original SigExt code is licensed under the [Apache-2.0 License](sigext/LICENSE).
