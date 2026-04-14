# Supplementary Material: Index

This index lists the supplementary documents that complement the paper.
Each document provides additional detail on a specific topic and is
referenced from the corresponding section of the camera-ready PDF.

| Document | Topic |
|---|---|
| [BIAS_PRODUCT_MATRIX.md](BIAS_PRODUCT_MATRIX.md) | Bias-product applicability matrix for the PIX evaluation scope. |
| [RAG_PARAMETERS.md](RAG_PARAMETERS.md) | Retrieval mechanics, source documents, and knowledge-base composition of the Skill/RAG module. |
| [SURVEY_METHODOLOGY.md](SURVEY_METHODOLOGY.md) | Survey instrument, recruitment, sample characteristics, and known limitations. |
| [BASELINE_ERROR_ANALYSIS.md](BASELINE_ERROR_ANALYSIS.md) | Qualitative analysis of the residual baseline error on unbiased questions. |
| [INTER_RATER.md](INTER_RATER.md) | Annotation process, consensus protocol, and annotation instrument released with this repository. |
| [../code/README.md](../code/README.md) | Prompt templates (Self-Help, Skill/RAG, Combo) and evaluation scripts, including the precision, recall, and F1 extension. |
| [../data/README.md](../data/README.md) | Dataset schema, taxonomy, label balance, and formality convention. |

The multi-seed evaluation planned in follow-up work is described in
`BASELINE_ERROR_ANALYSIS.md`, with the corresponding evaluation scripts
in `../code/`.

## Reproducibility statement

All scripts and prompt templates released here are the exact artifacts
used in the paper's PIX evaluation, with the evaluation pipeline
(`strategies.py`) and templates (`prompt_templates.py`) preserved as
authored. Relative imports (for example, `from .config import ...`)
reflect the original experiment package layout and are documented in
`../code/README.md`.
