import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns
from scipy.stats import rv_discrete

from src.code.simulation.galton_watson import GaltonWatson, SimulateurGaltonWatson
from src.code.simulation.utils import plot_zn_distribution, test_loi_exponentielle
from src.config.config import seed
from src.utils.utils import init_notebook


def processus_critique_survivant(
    gp: GaltonWatson, nb_simulations: int = 1_000, nb_epoques: int = 100
) -> np.ndarray:
    simulations = gp.lance_simulations(nb_simulations, nb_epoques)
    simulations = np.array(simulations)

    zn_sup_zero = simulations[simulations > 0]

    return zn_sup_zero


def simulation_yaglom(
    loi: rv_discrete,
    nb_processus: int = 1_000,
    taille_pas: int = 5,
    nb_repetitions: int = 10,
    taille_echantillon: int = 50,
    affichage: bool = False,
) -> tuple[list[float], list[float], list[float]]:
    """Renvoie la liste contenant l'évolution des p-values.

    Simule `nb_processus` processus de Galton-Watson.
    Récupère la p-value du test de Kolmogorov-Smirnov exponentiel sur la distribution des Z_n / n,
    tous les `taille_pas` époques, et ce, `nb_repetitions` fois.

    `taille_echantillon` correspond, pour l'affichage, à la taille du sous-ensemble
    des Z_n / n affichés (car autrement, il y aurait beaucoup plus de processus
    ayant survécu pour n petit, que pour n grand, simple question d'équité pour
    l'affichage)"""
    evolution_p_value = []
    evolution_ks = []
    evolution_lambda = []

    sim = SimulateurGaltonWatson(loi, nb_processus=nb_processus)

    for i in range(nb_repetitions):
        sim.simule(nb_epoques=taille_pas)
        sim.retire_processus_eteints()

        zn_sur_n = sim.get_zn_sur_n()
        zn_sur_n_sample = zn_sur_n[taille_echantillon:]

        if affichage:
            plt.title(
                "Distribution des $\dfrac{Z_n}{n}$ à l'époque $n = "
                + str((i + 1) * taille_pas)
                + "$"
            )
            sns.histplot(zn_sur_n_sample, stat="density")
            plt.show()

        p_value, statistique_ks = test_loi_exponentielle(zn_sur_n)

        evolution_p_value.append(p_value)
        evolution_ks.append(statistique_ks)

        lambda_estime = 1.0 / np.mean(zn_sur_n)
        evolution_lambda.append(lambda_estime)

    return evolution_p_value, evolution_ks, evolution_lambda
