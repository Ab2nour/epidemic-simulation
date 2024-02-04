import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns

from src.code.simulation.galton_watson import GaltonWatson
from src.code.simulation.utils import plot_zn_distribution, test_loi_exponentielle
from src.config.config import seed
from src.utils.utils import init_notebook


def processus_critique_survivant(gp: GaltonWatson, nb_simulations: int = 1_000, nb_epoques: int = 100) -> np.ndarray:
    simulations = gp.lance_simulations(nb_simulations, nb_epoques)
    simulations = np.array(simulations)

    zn_sup_zero = simulations[simulations > 0]

    return zn_sup_zero
