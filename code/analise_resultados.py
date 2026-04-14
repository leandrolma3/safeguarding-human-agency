"""Result analysis script: builds Markdown tables from the evaluation CSVs."""

import argparse
from glob import glob
from pathlib import Path

import pandas as pd

from .config import RESULTS_DIR


# Mapping from the CSV correctness columns to strategy display names
STRATEGIES = {
    "acerto_baseline": "Baseline",
    "acerto_self_help": "Self-Help",
    "acerto_skill": "Skill/RAG",
    "acerto_combo": "Combo",
}


def load_results(pattern: str) -> dict[str, pd.DataFrame]:
    """Load evaluation CSVs and group them by formality level.

    Args:
        pattern: glob pattern (for example 'resultados/pix_*.csv') or a
            comma-separated list of explicit paths.

    Returns:
        A dictionary whose keys are formality labels ('formal', 'informal',
        'muito_informal') and whose values are the loaded DataFrames.
    """
    if "," in pattern:
        files = [f.strip() for f in pattern.split(",")]
    else:
        files = sorted(glob(pattern))

    if not files:
        raise FileNotFoundError(f"No file matched: {pattern}")

    dfs_by_tone = {}
    for f in files:
        df = pd.read_csv(f)
        if "tom" not in df.columns:
            print(f"WARNING: {f} has no 'tom' column; skipping.")
            continue
        tom = df["tom"].iloc[0]
        dfs_by_tone[tom] = df

    return dfs_by_tone


def _acuracia(df: pd.DataFrame, col: str) -> float:
    """Return the accuracy (percentage) of a correctness column."""
    return df[col].fillna(0).mean() * 100


def gerar_tabela_resumo(dfs: dict[str, pd.DataFrame]) -> str:
    """Table 1: overall summary (accuracy by strategy, formality, and state)."""
    tone_order = ["formal", "informal", "muito_informal"]
    tone_labels = {"formal": "Formal", "informal": "Informal", "muito_informal": "Very Informal"}
    tones = [t for t in tone_order if t in dfs]

    # Header
    header_cols = []
    for t in tones:
        label = tone_labels.get(t, t)
        header_cols.extend([f"Neutral {label}", f"Biased {label}"])

    header = "| Strategy | " + " | ".join(header_cols) + " |"
    sep = "|---|" + "|".join(["---"] * len(header_cols)) + "|"

    rows = []
    for col, name in STRATEGIES.items():
        vals = []
        for t in tones:
            df = dfs[t]
            for estado in ["neutra", "viesada"]:
                subset = df[df["estado"] == estado]
                acc = _acuracia(subset, col)
                vals.append(f"{acc:.2f}%")
        rows.append(f"| {name} | " + " | ".join(vals) + " |")

    return "\n".join([header, sep] + rows)


def gerar_tabela_delta(dfs: dict[str, pd.DataFrame]) -> str:
    """Delta table (neutral minus biased) by strategy and formality level."""
    tone_order = ["formal", "informal", "muito_informal"]
    tone_labels = {"formal": "Formal", "informal": "Informal", "muito_informal": "Very Informal"}
    tones = [t for t in tone_order if t in dfs]

    header = "| Strategy | " + " | ".join(tone_labels.get(t, t) for t in tones) + " |"
    sep = "|---|" + "|".join(["---"] * len(tones)) + "|"

    rows = []
    for col, name in STRATEGIES.items():
        vals = []
        for t in tones:
            df = dfs[t]
            acc_n = _acuracia(df[df["estado"] == "neutra"], col)
            acc_v = _acuracia(df[df["estado"] == "viesada"], col)
            delta = acc_n - acc_v
            vals.append(f"{delta:+.2f} pp")
        rows.append(f"| {name} | " + " | ".join(vals) + " |")

    return "\n".join([header, sep] + rows)


def gerar_tabela_por_vies(df: pd.DataFrame, tom: str) -> str:
    """Accuracy by bias type for a specific formality level (biased split plus neutral reference)."""
    tone_labels = {"formal": "FORMAL", "informal": "INFORMAL", "muito_informal": "VERY INFORMAL"}
    label = tone_labels.get(tom, tom.upper())

    viesada = df[df["estado"] == "viesada"]
    neutra = df[df["estado"] == "neutra"]

    vieses = sorted(viesada["vies_aplicado"].unique())

    header = "| Bias | N | " + " | ".join(STRATEGIES.values()) + " |"
    sep = "|---|---|" + "|".join(["---"] * len(STRATEGIES)) + "|"

    rows = []
    for vies in vieses:
        sub = viesada[viesada["vies_aplicado"] == vies]
        n = len(sub)
        vals = []
        for col in STRATEGIES:
            acc = _acuracia(sub, col)
            vals.append(f"{acc:.2f}%")
        rows.append(f"| {vies} | {n} | " + " | ".join(vals) + " |")

    # Biased mean row
    n_total = len(viesada)
    vals_media = [f"{_acuracia(viesada, col):.2f}%" for col in STRATEGIES]
    rows.append(f"| **BIASED MEAN** | **{n_total}** | " + " | ".join(f"**{v}**" for v in vals_media) + " |")

    # Neutral reference row
    n_neutra = len(neutra)
    vals_neutra = [f"{_acuracia(neutra, col):.2f}%" for col in STRATEGIES]
    rows.append(f"| **NEUTRAL (ref)** | **{n_neutra}** | " + " | ".join(f"**{v}**" for v in vals_neutra) + " |")

    title = f"## Table: Analysis by Bias Type, Tone {label}"
    return title + "\n\n" + "\n".join([header, sep] + rows)


def gerar_observacoes(dfs: dict[str, pd.DataFrame]) -> str:
    """Automatic observations section derived from the loaded data."""
    lines = []
    lines.append("## Observations and Next Steps")
    lines.append("")
    lines.append("### Main findings")
    lines.append("")

    # Best overall strategy (average across tones, biased split)
    best_scores = {}
    for col, name in STRATEGIES.items():
        accs = []
        for tom, df in dfs.items():
            viesada = df[df["estado"] == "viesada"]
            accs.append(_acuracia(viesada, col))
        best_scores[name] = sum(accs) / len(accs)

    sorted_strategies = sorted(best_scores.items(), key=lambda x: x[1], reverse=True)
    best_name, best_acc = sorted_strategies[0]

    lines.append(f"1. **{best_name} is the best mitigation strategy** (biased mean: {best_acc:.1f}%)")

    # Per-tone breakdown
    for tom, df in sorted(dfs.items()):
        viesada = df[df["estado"] == "viesada"]
        neutra = df[df["estado"] == "neutra"]
        for col, name in STRATEGIES.items():
            if name == best_name:
                acc_v = _acuracia(viesada, col)
                acc_n = _acuracia(neutra, col)
                lines.append(f"   - {tom}: {acc_v:.0f}% biased ({acc_n:.0f}% neutral)")

    lines.append("")

    # Self-Help regressions on the neutral split
    sh_issues = []
    for tom, df in sorted(dfs.items()):
        neutra = df[df["estado"] == "neutra"]
        acc_sh = _acuracia(neutra, "acerto_self_help")
        acc_bl = _acuracia(neutra, "acerto_baseline")
        if acc_sh < acc_bl:
            sh_issues.append(f"{tom}: {acc_sh:.0f}% vs {acc_bl:.0f}% baseline")

    if sh_issues:
        lines.append("2. **Self-Help shows regressions on the neutral split:**")
        for issue in sh_issues:
            lines.append(f"   - Reduces neutral accuracy on {issue}")
        lines.append("")

    # Hardest biases (lowest accuracy in Skill/RAG biased split)
    vies_accs = {}
    for tom, df in dfs.items():
        viesada = df[df["estado"] == "viesada"]
        for vies in viesada["vies_aplicado"].unique():
            sub = viesada[viesada["vies_aplicado"] == vies]
            acc = _acuracia(sub, "acerto_skill")
            if vies not in vies_accs:
                vies_accs[vies] = []
            vies_accs[vies].append(acc)

    vies_medias = {v: sum(a) / len(a) for v, a in vies_accs.items()}
    sorted_vieses = sorted(vies_medias.items(), key=lambda x: x[1])

    n_obs = 3 if sh_issues else 2
    lines.append(f"{n_obs}. **Hardest biases (consistently lowest):**")
    for vies, acc in sorted_vieses[:3]:
        lines.append(f"   - `{vies}`: Skill/RAG mean {acc:.0f}%")
    lines.append("")

    n_obs += 1
    lines.append(f"{n_obs}. **Easiest biases:**")
    for vies, acc in sorted_vieses[-2:]:
        lines.append(f"   - `{vies}`: Skill/RAG mean {acc:.0f}%")

    # Metrics
    lines.append("")
    lines.append("### Experiment metrics")
    lines.append("")

    total_lines = sum(len(df) for df in dfs.values())
    n_tones = len(dfs)
    # Unique question count (unique ids in the first DataFrame)
    first_df = list(dfs.values())[0]
    n_perguntas = first_df["id"].nunique()
    lines_per_tone = len(first_df)

    lines.append(f"- **Volume:** {total_lines} rows processed ({lines_per_tone} per tone x {n_tones} tones)")
    lines.append(f"- **Questions:** {n_perguntas} unique questions (subset of the full base)")
    lines.append(f"- **Strategies:** {len(STRATEGIES)} ({', '.join(STRATEGIES.values())})")

    return "\n".join(lines)


def gerar_documento(dfs: dict[str, pd.DataFrame], model_name: str = None) -> str:
    """Build the full Markdown analysis document."""
    tone_order = ["formal", "informal", "muito_informal"]
    tones = [t for t in tone_order if t in dfs]

    # Detect model and product from the first CSV
    first_df = list(dfs.values())[0]
    product = first_df["id"].iloc[0].split("_")[0] if "id" in first_df.columns else "?"
    n_perguntas = first_df["id"].nunique()

    lines = []
    lines.append("# Evaluation Results")
    lines.append("")
    if model_name:
        lines.append(f"**Model:** {model_name}")
    lines.append(f"**Base:** {product.upper()} ({n_perguntas} questions, {len(first_df)} rows per tone)")
    lines.append(f"**Tones:** {', '.join(tones)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Table 1: summary
    lines.append("## Table 1: Overall Summary, Accuracy by Strategy and Tone")
    lines.append("")
    lines.append(gerar_tabela_resumo(dfs))
    lines.append("")

    # Delta
    lines.append("### Bias delta (neutral minus biased)")
    lines.append("")
    lines.append("Positive values indicate that the neutral variant outperformed the biased one (the model suffered from the bias).")
    lines.append("Negative values indicate that the biased variant outperformed the neutral one.")
    lines.append("")
    lines.append(gerar_tabela_delta(dfs))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Per-bias tables (one per tone)
    for i, tom in enumerate(tones, start=2):
        lines.append(gerar_tabela_por_vies(dfs[tom], tom))
        lines.append("")
        lines.append("---")
        lines.append("")

    # Observations
    lines.append(gerar_observacoes(dfs))

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyse evaluation results and generate Markdown tables.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m experiments.analise_resultados --input "resultados/pix_*.csv"
  python -m experiments.analise_resultados --input "resultados/pix_*.csv" --output docs/ANALYSIS_RESULTS.md
  python -m experiments.analise_resultados --input "resultados/pix_*.csv" --model "mistral-small"
        """,
    )
    parser.add_argument(
        "--input", required=True,
        help="Glob pattern for CSVs (e.g. 'resultados/pix_*.csv') or a comma-separated list",
    )
    parser.add_argument(
        "--output", default=None,
        help="Markdown output path (default: print to stdout)",
    )
    parser.add_argument(
        "--model", default=None,
        help="Model name used in the document header",
    )

    args = parser.parse_args()

    dfs = load_results(args.input)

    if not dfs:
        print("Error: no data loaded.")
        return

    doc = gerar_documento(dfs, model_name=args.model)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(doc, encoding="utf-8")
        print(f"Analysis written to: {args.output}")
    else:
        print(doc)


if __name__ == "__main__":
    main()
