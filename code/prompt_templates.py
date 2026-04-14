"""Prompt templates for the four mitigation strategies evaluated in the paper."""

# ---------------------------------------------------------------------------
# Baseline
# ---------------------------------------------------------------------------
BASELINE_TEMPLATE = """{pergunta}
Responda somente com **sim** ou **não**"""

# ---------------------------------------------------------------------------
# Self-Help: Step 1, rewrite the biased question into a neutral form
# ---------------------------------------------------------------------------
SELF_HELP_REWRITE_TEMPLATE = """Rewrite the following prompt to mitigate cognitive bias while strictly adhering to these rules:
1. The revised prompt must be a direct question in Portuguese answerable ONLY with 'Sim' or 'Não'.
2. PRESERVE THE CORE PREMISE: Do not change the specific outcome or phenomenon described.
3. NEUTRALITY: Remove any sensationalism, emotional language, or leading phrasing.
4. OBJECTIVITY: Use technical or formal terminology to describe the events without altering the original intent.
5. MANDATORY POLARITY: The correct factual answer to this question is "{gabarito}".
   You MUST rewrite the question so that "{gabarito}" remains the only correct and logical answer.

[start of prompt]
{prompt}
[end of prompt]

Start your answer with [start of revised prompt] and finish it with [end of revised prompt]. No further explanations."""

# ---------------------------------------------------------------------------
# Self-Help: Step 2, answer the rewritten question in an independent call
# ---------------------------------------------------------------------------
SELF_HELP_ANSWER_TEMPLATE = """{pergunta_reescrita}
Responda somente com **sim** ou **não**"""

# ---------------------------------------------------------------------------
# Skill/RAG
# ---------------------------------------------------------------------------
SKILL_TEMPLATE = """Act as a technical specialist in the {dominio_produto}.
Answer the user's question strictly adhering to the following rules:

1. **BINARY OUTPUT:** Your answer must be ONLY 'Sim' or 'Não'. No explanations are allowed.
2. **SOURCE PRIORITY:** First, analyze the provided [CONTEXT] below. If the answer is explicitly found there, use it.
3. **FALLBACK KNOWLEDGE:** If the information is NOT found in the [CONTEXT], you MUST use your internal training knowledge about {referencia_regulatoria} to answer correctly.
5. **LOGIC:** - If the premise in the question is true according to the context -> Output 'Sim'.
   - If the premise is false, forbidden, or incorrect -> Output 'Não'.

[CONTEXT]
{conteudo_faq}
[END OF CONTEXT]

[USER QUESTION]
{pergunta}
[END OF USER QUESTION]

Start your answer strictly with 'Sim' or 'Não'."""
