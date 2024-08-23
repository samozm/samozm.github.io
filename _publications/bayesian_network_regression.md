---
title: "Identifying microbial drivers in biological phenotypes with a Bayesian Network Regression model"
collection: publications
permalink: /publications/bayesian_network_regression
paperurl: 'https://arxiv.org/abs/2208.05600'
pubdate: 2024-05-20
venue: "Ecology and Evolution"
---

Abstract: In Bayesian Network Regression models, networks are considered the predictors of continuous responses. These models have been successfully used in brain research to identify regions in the brain that are associated with specific human traits, yet their potential to elucidate microbial drivers in biological phenotypes for microbiome research remains unknown. In particular, microbial networks are challenging due to their high-dimension and high sparsity compared to brain networks. Furthermore, unlike in brain connectome research, in microbiome research, it is usually expected that the presence of microbes have an effect on the response (main effects), not just the interactions. Here, we develop the first thorough investigation of whether Bayesian Network Regression models are suitable for microbial datasets on a variety of synthetic data that was generated under realistic biological scenarios. We test whether the Bayesian Network Regression model that accounts only for interaction effects (edges in the network) is able to identify key drivers in phenotypic variability (microbes). We show that this model is indeed able to identify influential nodes and edges in the microbial networks that drive changes in the phenotype for most biological settings, but we also identify scenarios where this method performs poorly which allows us to provide practical advice for domain scientists aiming to apply these tools to their datasets. Finally, we implement the model in a Julia package available [via Github](https://github.com/solislemuslab/BayesianNetworkRegression.jl) or the Julia package repository.

[Download paper here](https://doi.org/10.1002/ece3.11039)

Recommended citation: 

```
@article{ozminkowski2024identifying,
  title={Identifying microbial drivers in biological phenotypes with a Bayesian network regression model},
  author={Ozminkowski, Samuel and Sol{\'\i}s-Lemus, Claudia},
  journal={Ecology and Evolution},
  volume={14},
  number={5},
  pages={e11039},
  year={2024},
  publisher={Wiley Online Library},
  url={https://doi.org/10.1002/ece3.11039}
}
```