# Skill/RAG Module: Parameters and Retrieval Mechanics

This document describes the retrieval method, passage selection
criteria, and knowledge-base composition used by the Skill/RAG module.
It reflects the implementation shipped in `../code/strategies.py` and
the prompt shipped in `../code/prompt_templates.py` (`SKILL_TEMPLATE`).

## Retrieval method

The Skill/RAG module performs **deterministic context injection**: the
entire curated FAQ document for the target product is inserted verbatim
into the `[CONTEXT]` block of the prompt, without embedding-based
retrieval, chunking, or passage ranking. The model is instructed to
consult the injected context first and to fall back on internal training
knowledge about the regulatory reference when the context does not cover
the question. This design trades scalability for reproducibility and
strict factual grounding in curated material.

The relevant prompt lives in `prompt_templates.SKILL_TEMPLATE` and binds
four fields:

- `dominio_produto`: product domain label (e.g. "PIX instant payment system").
- `referencia_regulatoria`: regulatory reference name (e.g. "Banco Central do Brasil").
- `conteudo_faq`: the full curated FAQ document, injected verbatim.
- `pergunta`: the user question.

## Source documents

The PIX FAQ shipped in `../faqs/faq_pix.md` was manually compiled from
public Banco Central do Brasil materials covering PIX availability,
nighttime transfer limits, the MED (Mecanismo Especial de Devolução),
PIX Automático, fee policies, and key-registration rules. Content is
structured by topic, with short paragraphs suitable for direct injection.

## Combo strategy

The Combo architecture chains Self-Help (prompt rewriting that removes
framing and other adversarial cues while preserving the core factual
question) and Skill/RAG (deterministic FAQ injection with the rewritten
question as input). The chaining is implemented in
`strategies.combo()` and reuses `SKILL_TEMPLATE` directly.

## Parameters

- Retrieval method: none (full-document injection).
- Chunking: none.
- Passage ranking: none.
- Context ordering: a single `[CONTEXT]` block, followed by the user
  question inside `[USER QUESTION]`.
- Binary output enforced by prompt rules (only "Sim" or "Não").

## Evaluation coverage

The paper reports the full-scale Skill/RAG and Self-Help evaluation on
the 500-instance PIX dataset. Combo is reported at the proof-of-concept
scale in this release; a full-scale Combo ablation across all eight
bias types is part of the planned follow-up work.
