"""Reference implementation of the four mitigation strategies evaluated in the paper:
Baseline (control), Self-Help (prompt rewriting), Skill/RAG (deterministic FAQ
injection), and Combo (Self-Help chained into Skill/RAG).

The relative imports below reflect the original experiment package layout. See
`README.md` for schema and expected CSV columns.
"""

from .llm_provider import LLMProvider
from .prompt_templates import (
    BASELINE_TEMPLATE,
    SELF_HELP_REWRITE_TEMPLATE,
    SELF_HELP_ANSWER_TEMPLATE,
    SKILL_TEMPLATE,
)
from .response_parser import parse_sim_nao, normalize_expected
from .config import MAX_TOKENS


def baseline(provider: LLMProvider, pergunta: str) -> str:
    """Strategy 1: Baseline (control, no mitigation).

    Returns:
        Parsed response ('sim', 'nao', or 'indefinido').
    """
    prompt = BASELINE_TEMPLATE.format(pergunta=pergunta)
    raw = provider.call(prompt, max_tokens=MAX_TOKENS["baseline"])
    return parse_sim_nao(raw)


def self_help(
    provider: LLMProvider,
    pergunta: str,
    resposta_esperada: str,
) -> tuple[str, str]:
    """Strategy 2: Self-Help (neutral rewrite followed by an independent answer call).

    Step 1: the LLM rewrites the question in a neutral form.
    Step 2: the LLM answers the rewritten question in a separate call.

    Returns:
        Tuple of (rewritten_question, parsed_answer).
    """
    # Step 1: neutral rewrite
    gabarito = resposta_esperada
    rewrite_prompt = SELF_HELP_REWRITE_TEMPLATE.format(
        prompt=pergunta, gabarito=gabarito
    )
    raw_rewrite = provider.call(rewrite_prompt, max_tokens=MAX_TOKENS["self_help_rewrite"])

    # Extract the rewritten question from the delimiters
    pergunta_reescrita = _extract_rewrite(raw_rewrite)

    # Step 2: answer (independent call)
    answer_prompt = SELF_HELP_ANSWER_TEMPLATE.format(
        pergunta_reescrita=pergunta_reescrita
    )
    raw_answer = provider.call(answer_prompt, max_tokens=MAX_TOKENS["self_help_answer"])

    return pergunta_reescrita, parse_sim_nao(raw_answer)


def skill(
    provider: LLMProvider,
    pergunta: str,
    faq_content: str,
    domain: str,
    regulatory_ref: str,
) -> str:
    """Strategy 3: Skill/RAG (deterministic FAQ injection).

    Returns:
        Parsed response ('sim', 'nao', or 'indefinido').
    """
    prompt = SKILL_TEMPLATE.format(
        dominio_produto=domain,
        referencia_regulatoria=regulatory_ref,
        conteudo_faq=faq_content,
        pergunta=pergunta,
    )
    raw = provider.call(prompt, max_tokens=MAX_TOKENS["skill"])
    return parse_sim_nao(raw)


def combo(
    provider: LLMProvider,
    pergunta_reescrita: str,
    faq_content: str,
    domain: str,
    regulatory_ref: str,
) -> str:
    """Strategy 4: Combo (Self-Help chained into Skill/RAG).

    Uses the question already rewritten by Self-Help as input to Skill/RAG.

    Returns:
        Parsed response ('sim', 'nao', or 'indefinido').
    """
    prompt = SKILL_TEMPLATE.format(
        dominio_produto=domain,
        referencia_regulatoria=regulatory_ref,
        conteudo_faq=faq_content,
        pergunta=pergunta_reescrita,
    )
    raw = provider.call(prompt, max_tokens=MAX_TOKENS["combo"])
    return parse_sim_nao(raw)


def _extract_rewrite(raw: str) -> str:
    """Extract the rewritten question from the [start/end of revised prompt] delimiters."""
    if "[start of revised prompt]" in raw:
        try:
            extracted = (
                raw.split("[start of revised prompt]")[-1]
                .split("[end of revised prompt]")[0]
                .strip()
            )
            if extracted:
                return extracted
        except (IndexError, ValueError):
            pass

    # Fallback: strip delimiters and return the full text
    cleaned = raw.replace("[start of revised prompt]", "").replace(
        "[end of revised prompt]", ""
    )
    return cleaned.strip()
