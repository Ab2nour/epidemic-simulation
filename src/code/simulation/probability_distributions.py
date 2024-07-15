import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats


def plot_distribution(
    distribution: stats.rv_discrete,
    sample_size: int = 5_000,
) -> None:
    tirage = distribution.rvs(sample_size)

    min_tirage = min(tirage)
    max_tirage = max(tirage)

    bins = np.arange(min_tirage - 0.5, max_tirage + 1.5, 1)
    ticks = list(range(min_tirage, max_tirage + 1))

    plt.hist(tirage, bins=bins)
    plt.xticks(ticks)


def create_distributions() -> dict[str, stats.rv_discrete]:
    distributions = {
        "Poisson (λ = 1)": stats.poisson(1),
        "Uniforme {0, 1, 2}": stats.randint(0, 3),
        "Binomiale (n=2, p=1/2)": stats.binom(n=2, p=1 / 2),
        "Binomiale (n=10, p=1/10)": stats.binom(n=10, p=1 / 10),
        "Binomiale (n=50, p=1/50)": stats.binom(n=50, p=1 / 50),
        "Bêta-Binomiale (n=2, α=3, β=3)": stats.betabinom(n=2, a=3, b=3),
        "Bêta-Binomiale (n=5, α=5, β=20)": stats.betabinom(n=5, a=5, b=20),
        "Bêta-Binomiale (n=3, α=5, β=10)": stats.betabinom(n=3, a=5, b=10),
        "Bêta-Binomiale (n=10, α=5, β=45)": stats.betabinom(n=10, a=5, b=45),
        "Négative Binomiale (n=1, p=0.5)": stats.nbinom(n=1, p=0.5),
        "Négative Binomiale (n=10, p=10/11)": stats.nbinom(n=10, p=10 / 11),
        # dans l'autre notation p = N / M, et N = M
        "Hyper-Géométrique (N=10, n=2, p=0.5)": stats.hypergeom(M=10, n=2, N=5),
        "Hyper-Géométrique (N=100, n=10, p=0.1)": stats.hypergeom(M=100, n=10, N=10),
    }

    return distributions


def create_distributions_df() -> pd.DataFrame:
    distributions = create_distributions()

    distributions_dict = {
        "Loi de reproduction": [],
        "Espérance": [],
        "Variance": [],
        "Lambda théorique loi exponentielle Z_n / n": [],
    }

    for name, distribution in distributions.items():
        distributions_dict["Loi de reproduction"].append(name)
        distributions_dict["Espérance"].append(1)
        distributions_dict["Variance"].append(round(distribution.var(), 5))
        distributions_dict["Lambda théorique loi exponentielle Z_n / n"].append(
            2 / distribution.var(),
        )

    df_distribution = pd.DataFrame(distributions_dict)

    return df_distribution
