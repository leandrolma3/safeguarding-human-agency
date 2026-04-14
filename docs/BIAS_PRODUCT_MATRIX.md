# Bias-Product Applicability Matrix (PIX scope)

This document provides a standalone version of the bias-product
applicability matrix referenced in the paper, covering the PIX product
and matching the evaluation scope of the camera-ready release.

## Matrix summary

The paper evaluates eight extrinsic cognitive biases against PIX. All
eight biases are applied systematically across the 500 instances, with
sampling weighted by thematic category so that the most vulnerable
interaction patterns (functionality, security, scams) are over-represented
relative to rarer topics (fees, recent regulatory updates).

| Bias | Typical PIX interaction where it surfaces |
|---|---|
| Loss aversion (`aversao_perda`) | Fear of losing funds in scams, account freeze scenarios, limits on nighttime transfers. |
| Status quo (`status_quo`) | Preference for existing transfer habits even when a newer and safer mechanism exists (e.g. PIX Automático). |
| Anchoring (`ancoragem`) | Over-reliance on values mentioned in the question (limits, fees), even when misleading. |
| Representativeness (`representatividade`) | Surface similarity between a fraudulent QR code and a legitimate one; scam patterns that mimic official channels. |
| Confirmation (`confirmacao`) | Users seeking validation for an already formed (often wrong) belief about how PIX works. |
| Availability (`disponibilidade`) | Recent news of scams skewing the perceived risk of specific PIX features. |
| Framing (`enquadramento`) | Emotional or sensationalist phrasing around fraud or loss to flip the model's answer. |
| Suggestion (`sugestao`) | Leading phrasing that implies the "expected" yes/no answer before asking the question. |

## Thematic weighting of the 500 PIX instances

The dataset sampling by thematic category is reproduced below. Bias
coverage within each category is balanced so that every bias label is
exercised across multiple categories.

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

See `../data/README.md` for the full list of subcategories.

## Notes

- The paper's main Table I presents the bias taxonomy with definitions and
  paper-level examples. This document is the applicability lens that maps
  each bias onto PIX interactions, complementing Table I.
- A broader version of this matrix covering additional products (credit
  card, digital checking account, loans) is planned as follow-up work and
  is not released here.
