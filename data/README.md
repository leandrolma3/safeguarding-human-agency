# PIX-Br Dataset (PIX subset, 500 instances)

**Product:** PIX (Brazilian instant payment system).
**Language:** Brazilian Portuguese.
**Size:** 500 instances, each expanded into neutral and biased variants
across three linguistic formality levels (formal, informal, very informal).

## Files

| File | Purpose |
|---|---|
| `pix_500.json` | Canonical dataset with accents applied per the formality convention below. |
| `pix_500.csv`  | CSV mirror of the JSON for tabular tooling. |

## Record schema

```json
{
  "id": "PIX_0001",
  "produto": "PIX",
  "categoria": "limites",
  "subcategoria": "limite_diurno",
  "contexto": "Background text used by annotators and the RAG module.",
  "pergunta_neutra": "Neutral yes/no question.",
  "pergunta_viesada": "Biased yes/no question with prompt-induced cognitive bias.",
  "resposta_esperada": "Sim | Não",
  "vies_aplicado": "one of the eight bias labels",
  "justificativa": "Regulatory rationale for the ground-truth answer.",
  "variantes": {
    "neutra":  { "formal": "...", "informal": "...", "muito_informal": "..." },
    "viesada": { "formal": "...", "informal": "...", "muito_informal": "..." }
  }
}
```

## Label balance

Ground-truth polarity is strictly balanced: **250 Sim / 250 Não**.

## Taxonomy

### Eight extrinsic cognitive biases

Canonical bias label (Portuguese, as stored in `vies_aplicado`) with the
English mapping used in the paper:

| `vies_aplicado` | English |
|---|---|
| `aversao_perda` | Loss aversion |
| `status_quo` | Status quo |
| `ancoragem` | Anchoring |
| `representatividade` | Representativeness |
| `confirmacao` | Confirmation |
| `disponibilidade` | Availability |
| `enquadramento` | Framing |
| `sugestao` | Suggestion |

### Eight thematic categories used to balance the PIX sample

| Category | Weight |
|---|---|
| funcionalidade | 20% |
| segurança | 20% |
| golpes | 20% |
| chaves | 10% |
| limites | 10% |
| devolução | 10% |
| taxas | 5% |
| novidades | 5% |

Subcategories include transferência, saque, troco, automático, aproximação,
parcelado, cobrança, agendado, QR code, copia e cola, proteção, limite
noturno, bloqueio, verificação, autenticação, dispositivos, clonagem
WhatsApp, falsa central, golpe pix errado, golpe bug, golpe robô, QR
falso, phishing, tipos de chave (CPF, email, telefone, aleatória),
portabilidade, limites noturno e diurno, MED, prazos, obrigações,
gratuidade PF, cobrança PJ, taxa saque, taxa governo, PIX Automático 2025,
MED 2.0, pagamento de boletos.

## Formality levels and accent convention

| Level | Accents | Example |
|---|---|---|
| `formal` | present | "O PIX é seguro para fazer transferências?" |
| `informal` | present | "O PIX é seguro pra fazer transferência?" |
| `muito_informal` | absent | "o pix e seguro pra transferir?" |

This reflects a common pattern in Brazilian-Portuguese online writing and
is the convention adopted in the paper's evaluation.

## Regulatory references considered

- PIX available 24/7, including holidays.
- Nighttime transfer limit of BRL 1,000 between 20:00 and 06:00.
- MED (Mecanismo Especial de Devolução): 80-day window.
- PIX Automático launched in June 2025.
- Free of charge for natural persons (BCB regulation).
- Up to five PIX keys per institution for natural persons.

## Versioning

This release corresponds to dataset v3 (March 2026), which re-applied the
accent convention above and passed automated validation. Earlier internal
revisions (v1, v2) existed within the authoring pipeline and are not
released here.
