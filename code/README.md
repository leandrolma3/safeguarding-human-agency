# Code

This directory ships the prompt templates and the evaluation helpers used
to produce the results reported in the paper.

| File | Purpose |
|---|---|
| `prompt_templates.py` | Prompt templates for Baseline, Self-Help, Skill/RAG, and Combo. Self-contained, no external imports. |
| `strategies.py` | Reference implementations of the four strategies. Relative imports (`from .config import ...`, `from .llm_provider import ...`, `from .response_parser import ...`) reflect the layout of the authors' internal experiment package and should be resolved against a compatible package when reusing the code. The logic itself is standalone. |
| `analise_resultados.py` | Accuracy-focused result aggregator. Reads evaluation CSVs and produces Markdown tables. Same import caveat as `strategies.py`. |
| `metrics.py` | Standalone extension that computes precision, recall, and F1 per bias type from the same evaluation CSVs. Runs without the internal package. |

## Strategies

The paper evaluates four strategies on the PIX-Br dataset:

- **Baseline**: control condition with no mitigation.
- **Self-Help**: prompt rewriting that preserves the factual core while removing framing and other adversarial cues.
- **Skill/RAG**: deterministic injection of the full product FAQ into the prompt.
- **Combo**: Self-Help chained into Skill/RAG, so the rewritten question is the one that is factually grounded.

All evaluation runs reported in the paper used **Mistral Small** as the underlying model.

## Expected CSV schema

The evaluation pipeline emits one row per (`id`, `tom`, `estado`) triple,
where `tom` is the formality level (`formal`, `informal`, `muito_informal`)
and `estado` is `neutra` or `viesada`. Column names are kept in Portuguese
because they mirror the dataset schema in `../data/`:

- `id`, `tom`, `estado`, `vies_aplicado`, `resposta_esperada`.
- `resposta_<strategy>`: predicted label for each strategy.
- `acerto_<strategy>`: 0/1 correctness flag for each strategy.

## Running the F1 extension

```
python metrics.py --input path/to/results_pix_*.csv \
                  --output metrics_summary.md
```

`metrics.py` produces precision, recall, and F1 both overall and per
bias type, for each of the four strategies listed above.
