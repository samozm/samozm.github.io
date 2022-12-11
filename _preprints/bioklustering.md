---
title: "BioKlustering: a web app for semi-supervised learning of maximally imbalanced genomic data"
collection: preprints
permalink: /preprints/bioklustering
paperurl: 'https://arxiv.org/abs/2209.11730'
---

Summary: Accurate phenotype prediction from genomic sequences is a highly coveted task in biological and medical research. While machine-learning holds the key to accurate prediction in a variety of fields, the complexity of biological data can render many methodologies inapplicable. We introduce BioKlustering, a user-friendly open-source and publicly available web app for unsupervised and semi-supervised learning specialized for cases when sequence alignment and/or experimental phenotyping of all classes are not possible. Among its main advantages, BioKlustering 1) allows for maximally imbalanced settings of partially observed labels including cases when only one class is observed, which is currently prohibited in most semi-supervised methods, 2) takes unaligned sequences as input and thus, allows learning for widely diverse sequences (impossible to align) such as virus and bacteria, 3) is easy to use for anyone with little or no programming expertise, and 4) works well with small sample sizes.
Availability and Implementation: BioKlustering [this https URL](https://bioklustering.wid.wisc.edu/) is a freely available web app implemented with Django, a Python-based framework, with all major browsers supported. The web app does not need any installation, and it is publicly available and open-source [this https URL](https://github.com/solislemuslab/bioklustering).

[Download paper here](https://arxiv.org/abs/2209.11730)

Recommended citation: 

```
@article{Ozminkowski2022,
author = {Ozminkowski, S. and Wu, Y. and Yang L. and Xu, Z. and Selberg, L. and Huang, C. and Sol'{i}s-Lemus, C.},
year = {2022},
title = {BioKlustering: a web app for semi-supervised learning of maximally imbalanced genomic data},
journal = {arXiv:2209.11730}
}
```