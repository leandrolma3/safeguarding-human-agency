# Inter-Rater Process and Annotation Instrument

This document describes the annotation protocol that supported the
independent author review of the 500 questions and the annotation
instrument released alongside the dataset, which enables future formal
agreement studies.

## Annotation protocol used for the 500-instance PIX dataset

1. **Individual review.** Each question was independently evaluated by
   all authors against the regulatory references listed in
   `../data/README.md` and in the paper.
2. **Dimensions assessed.** Annotators evaluated each question along
   four dimensions on a 1-to-5 scale, adapted from the web application
   referenced below: quality of the bias injection, fit between the
   bias and the financial product category, correctness of the
   ground-truth answer, and quality of the formality variants.
3. **Consensus resolution.** Remaining disagreements were resolved by
   discussion among the authors until consensus was reached. Questions
   that could not reach consensus were dropped or rewritten and
   re-evaluated.
4. **Regulatory anchoring.** Ground-truth answers were validated against
   published Banco Central do Brasil material rather than majority
   opinion, to avoid compounding cognitive bias from the annotators
   themselves onto the gold labels.

## Annotation instrument (available on request)

A web application used during annotation implements the review
workflow. Its database schema includes the following key tables:

- `Rating` with Likert scores for the four dimensions described above,
  plus a free-text comment field.
- `ReviewerBatch` enforcing controlled overlap so that every question
  is assigned to multiple annotators and under-reviewed questions are
  prioritised.
- `UNIQUE(question_id, reviewer_id)` constraints to avoid duplicate
  ratings.

This infrastructure is the basis for the formal inter-rater agreement
study planned as follow-up work. The raw annotation logs from the PIX
evaluation cycle are available on request; they are not redistributed
here because free-text comments can contain annotator-identifying
language.

## Planned follow-up

A dedicated annotation cycle with three or more annotators and explicit
overlap quotas is planned for the next iteration, enabling direct
computation of Cohen's kappa (pairwise) and Fleiss' kappa (multi-rater)
for the bias injection and the ground-truth dimensions. Results will be
released in a future version of this repository.
