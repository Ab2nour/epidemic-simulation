import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import rv_discrete


def galton_watson(loi: rv_discrete, nb_epoques: int):
    nb_descendants = 1

    epoque_actuelle = 0

    while epoque_actuelle < nb_epoques and nb_descendants > 0:
        liste_descendants = loi.rvs(size=nb_descendants)
        nb_descendants = np.sum(liste_descendants)
        epoque_actuelle += 1

    return nb_descendants


class GaltonWatson:
    def __init__(self, loi: rv_discrete, nb_descendants: int = 1):
        self.loi = loi
        self.m = loi.mean()

        self.nb_descendants = nb_descendants
        self.historique_nb_descendants: list[int] = [nb_descendants]

        self.liste_descendants: list[list[int]] = []  # fixme: ce sont des listes de np.ndarray
        self.n: int = 0  # numéro de l'époque

    def simule(self, nb_epoques: int) -> int:
        """
        Simule le processus de Galton-Watson pendant nb_epoques époques.

        Parameters
        ----------
        nb_epoques: Nombre d'époques à simuler

        Returns
        -------
        Nombre de descendants
        """
        epoque_actuelle = 0

        while epoque_actuelle < nb_epoques and self.nb_descendants > 0:
            liste_descendants = self.loi.rvs(size=self.nb_descendants)
            self.liste_descendants.append(liste_descendants)

            self.nb_descendants = np.sum(liste_descendants)
            self.historique_nb_descendants.append(self.nb_descendants)

            epoque_actuelle += 1

        self.n = len(self.liste_descendants)

        return self.nb_descendants

    def plot_historique_descendants(self, log: bool = False, affiche_moyenne: bool = False) -> None:
        """
        Affiche l'historique des descendants.

        Parameters
        ----------
        log: active l'échelle logarithmique
        affiche_moyenne: affiche l'évolution de E[L]^m

        Returns
        -------

        """
        plt.plot(self.historique_nb_descendants, label="Nombre de descendants")

        if affiche_moyenne:
            x = np.arange(self.n)
            plt.plot(x, self.m ** x, label=r"Nombre de descendants prévu ($\mathbb{E}[L]^m$)")

        plt.title("Historique du nombre de descendants")
        plt.xlabel("Numéro d'époque n")
        plt.ylabel("Nombre de descendants")

        plt.legend()

        if log:
            plt.yscale("log")

    def plot_zn_sur_n(self, log: bool = False) -> None:
        hist = np.array(self.historique_nb_descendants[1:])
        r = range(1, len(hist) + 1)  # fixme: choisir un meilleur nom de variable
        plt.plot(r, hist / r)

        plt.title(r"Évolution de $\dfrac{Z_n}{n}$")
        plt.xlabel("Numéro d'époque n")
        plt.ylabel(r"$\dfrac{Z_n}{n}$")

        if log:
            plt.yscale("log")
