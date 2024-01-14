"""Galton-Watson process."""
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import rv_discrete


class GaltonWatson:
    def __init__(self, loi: rv_discrete, nb_descendants: int = 1):
        self.loi = loi
        self.m = loi.mean()

        self.nb_descendants_initial = nb_descendants
        self.nb_descendants = nb_descendants
        self.historique_nb_descendants: list[int] = [self.nb_descendants_initial]

        self.liste_descendants: list[list[int]] = []  # fixme: ce sont des listes de np.ndarray
        self.n: int = 0  # numéro de l'époque

    def reset(self) -> None:
        """Réinitialise le processus de Galton-Watson.

        Returns
        -------

        """
        self.nb_descendants = self.nb_descendants_initial
        self.historique_nb_descendants = [self.nb_descendants_initial]

        self.liste_descendants = []
        self.n = 0

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

    def plot_historique_descendants(self, logscale: bool = False, affiche_moyenne: bool = False) -> None:
        """
        Affiche l'historique des descendants.

        Parameters
        ----------
        logscale: active l'échelle logarithmique
        affiche_moyenne: affiche l'évolution de E[L]^m

        Returns
        -------

        """
        plt.plot(self.historique_nb_descendants, label="Nombre de descendants")

        if affiche_moyenne:
            x = np.arange(self.n + 1)
            plt.plot(x, self.m ** x, label=r"Nombre de descendants prévu ($\mathbb{E}[L]^m$)")

        plt.title("Historique du nombre de descendants")
        plt.xlabel("Numéro d'époque n")
        plt.ylabel("Nombre de descendants")

        plt.legend()

        if logscale:
            plt.yscale("log")

    def get_zn_sur_n(self):
        hist = np.array(self.historique_nb_descendants[1:])
        r = range(1, len(hist) + 1)  # fixme: choisir un meilleur nom de variable
        return hist / r

    def plot_zn_sur_n(self, logscale: bool = False) -> None:
        hist = np.array(self.historique_nb_descendants[1:])
        r = range(1, len(hist) + 1)  # fixme: choisir un meilleur nom de variable
        plt.plot(r, self.get_zn_sur_n())

        plt.title(r"Évolution de $\dfrac{Z_n}{n}$")
        plt.xlabel("Numéro d'époque n")
        plt.ylabel(r"$\dfrac{Z_n}{n}$")

        if logscale:
            plt.yscale("log")

    def __repr__(self):
        nom_loi = self.loi.dist.name

        representation = (f"Processus Galton-Watson\n"
                          f"- loi de reproduction L : {nom_loi}\n"
                          f"- espérance E[L] = {self.m}\n"
                          f"- époque n = {self.n}\n"
                          f"- nombre de survivants Z_n = {self.nb_descendants}")

        return representation
