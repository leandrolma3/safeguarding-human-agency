# Baseline Error Analysis

The paper reports 86.88% accuracy on the unbiased questions of the
500-instance PIX evaluation, with a standard deviation of plus or minus
0.16 percentage points. This document discusses the sources of the
residual error and outlines the methodological directions planned for
extending seed and split coverage in subsequent releases.

## Categories of baseline error

1. **Regulatory drift after the model cutoff.** Several PIX rules were
   updated close to or after the training-data cutoff of Mistral Small.
   PIX Automático in particular was launched in June 2025 and is
   therefore outside the knowledge base of several model snapshots. The
   `novidades` category in the dataset is designed to probe exactly this
   kind of post-cutoff fact, and the model frequently answers "Não" to
   questions whose correct answer became "Sim" after the regulatory
   update.
2. **Ambiguous regulatory edge cases.** Some questions sit at the edge
   of the written rules: MED eligibility windows for borderline scam
   scenarios, nuanced fee exemptions for hybrid PJ/PF accounts,
   interaction between the nighttime transfer limit and scheduled
   transfers initiated earlier in the day. The ground-truth label
   reflects the BCB's published interpretation, but the model sometimes
   answers according to a reasonable alternative reading.
3. **Parsing residue.** The baseline requires the model to output exactly
   "Sim" or "Não". In a small fraction of cases the model produces a
   short qualifying sentence before the final token, which the output
   parser treats conservatively.
4. **Acronym and orthographic variation.** The `muito_informal` level is
   intentionally unaccented; some baseline failures correlate with
   rare orthographic forms the model is less confident about.

Examples of each category, drawn from the neutral evaluation, are
annotated in the internal evaluation logs and summarised in the paper.

## Methodology for the reported deviation

The paper reports 86.88% (plus or minus 0.16) on the 500-instance
unbiased split. The standard deviation in this camera-ready release is
kept as reported in the underlying experiment notes. A multi-seed
evaluation with fixed random seeds and held-out formality splits is
part of the planned follow-up work, aiming to produce a tighter
empirical confidence interval and to explicitly separate inter-seed
variability from inter-formality variability. Those numbers will be
released in a dedicated evaluation update alongside the next version
of this repository.

## Upper-bound interpretation

The 86.88% figure is treated as an upper bound for unbiased performance
of Mistral Small on the PIX domain. It should not be interpreted as a
ceiling on all LLMs. Broader model-family comparisons (proprietary,
open-source, SLMs) are planned as follow-up work.
