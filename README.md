# Safeguarding Human Agency in AI-Assisted Financial Decisions

Supplementary repository for the paper **"Safeguarding Human Agency in
AI-Assisted Financial Decisions: Detecting and Mitigating Cognitive Biases
in LLMs"**, accepted to IJCNN 2026 / IEEE WCCI 2026, Special Session SS11
("Engineering Trust: Ethical, Legal, and Societal Impacts of CI on Human
Agency").

This repository provides the PIX-Br dataset (500 instances), the curated
FAQ used by the Skill/RAG module, the prompt templates for the Self-Help,
Skill/RAG, and Combo strategies, and extended supplementary documentation
covering the bias-product applicability matrix, RAG parameters, survey
methodology, baseline error analysis, and the inter-rater review process.

## Authors

- Leandro Maciel Almeida, Universidade Federal de Pernambuco, `lma3@cin.ufpe.br`, ORCID [0000-0001-8025-0517](https://orcid.org/0000-0001-8025-0517).
- Alice Buarque Cadete, Universidade Federal de Pernambuco, `abc3@cin.ufpe.br`, ORCID [0009-0006-8218-4481](https://orcid.org/0009-0006-8218-4481).
- Victoria Xavier Queiroz, Universidade Federal de Pernambuco, `vxq@cin.ufpe.br`, ORCID [0009-0005-1368-5509](https://orcid.org/0009-0005-1368-5509).

## Repository layout

```
safeguarding-human-agency/
├── data/      PIX-Br dataset (500 instances, JSON and CSV)
├── faqs/      Curated FAQ used by the Skill/RAG module
├── code/      Prompt templates and evaluation scripts
└── docs/      Supplementary material (index in docs/SUPPLEMENTARY.md)
```

## Citation

If you use this dataset or code in your research, please cite:

```bibtex
@inproceedings{macielalmeida2026safeguarding,
  title={Safeguarding Human Agency in AI-Assisted Financial Decisions: Detecting and Mitigating Cognitive Biases in LLMs},
  author={Maciel Almeida, Leandro and Cadete, Alice Buarque and Queiroz, Victoria Xavier},
  booktitle={Proceedings of the International Joint Conference on Neural Networks (IJCNN), IEEE World Congress on Computational Intelligence (WCCI)},
  year={2026},
  note={To appear}
}
```

A machine-readable version is also available in `CITATION.cff`.

## Licensing

- Code: MIT (`LICENSE`).
- Dataset and documentation: CC-BY-4.0 (`data/LICENSE`).

## Scope

This public release covers the PIX domain evaluated in the paper. A
broader multi-product and multi-model extension is planned as follow-up
work and is not part of this release.

## Funding and Partnership

This research is developed as a partnership between the Centro de
Informática of the Universidade Federal de Pernambuco (UFPE-CIn) and
the Instituto Itaú de Ciência, Tecnologia e Inovação (ICTi), with
funding provided by the Instituto Itaú de Ciência, Tecnologia e
Inovação (ICTi).

## Disclosure

Prompt templates were manually authored by the authors and iteratively
refined against a held-out pilot of 31 questions before scaling to the
full 500-instance evaluation. All evaluation runs reported in the paper
used Mistral Small as the underlying model.
