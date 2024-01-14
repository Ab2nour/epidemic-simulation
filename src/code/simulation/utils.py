import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import kstest


def plot_zn_distribution(resultats_simulation: list[int], nb_epoques: int) -> None:
    _, ax = plt.subplots(1, 2, figsize=(10, 4))

    ax[0].set_title(f"Distribution des $Z_n$,\n$n = {nb_epoques}$")
    ax[1].set_title(f"Distribution des $Z_n$,\n$n = {nb_epoques}$")

    ax[0].hist(resultats_simulation)
    ax[1].hist(resultats_simulation)

    ax[0].set_xlabel("$Z_n$")
    ax[1].set_xlabel("$Z_n$")

    ax[0].set_ylabel("compte")
    ax[1].set_ylabel("compte (échelle logarithmique)")
    ax[1].set_yscale("log")


def test_loi_exponentielle(donnees: np.ndarray) -> float:
    lambda_estime = 1.0 / np.mean(donnees)  # maximum de vraisemblance

    statistique_ks, p_value = kstest(donnees, "expon", args=(0, 1 / lambda_estime))

    print(f"{statistique_ks = }")
    print(f"{p_value = }")

    # Interprétation du résultat
    alpha = 0.05  # Niveau de signification
    if p_value < alpha:
        print("Les données ne suivent pas une loi exponentielle.")
    else:
        print("Les données suivent une loi exponentielle.")

    return p_value
