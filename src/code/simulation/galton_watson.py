"""Galton-Watson process."""
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import rv_discrete
from joblib import Parallel, delayed

from src.code.plot.plot_tree import color_options, hierarchy_pos


class GaltonWatson:
    def __init__(self, loi: rv_discrete, nb_descendants: int = 1):
        self.loi = loi
        self.m = loi.mean()

        self.nb_descendants_initial = nb_descendants
        self.nb_descendants = nb_descendants
        self.historique_nb_descendants: list[int] = [self.nb_descendants_initial]

        self.liste_descendants: list[
            list[int]
        ] = []  # fixme: ce sont des listes de np.ndarray
        self.n: int = 0  # numéro de l'époque

        self.simulations: list[int] = []

    def reset(self, nb_descendants: int | None = None) -> None:
        """Réinitialise le processus de Galton-Watson.

        todo: documenter le fait qu'on peut changer le nombre de descendants initiaux
        Returns
        -------

        """
        if nb_descendants is None:
            self.nb_descendants = self.nb_descendants_initial
        else:
            self.nb_descendants = nb_descendants

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

    def plot_historique_descendants(
        self, logscale: bool = False, affiche_moyenne: bool = False
    ) -> None:
        """
        Affiche l'historique des descendants.

        Parameters
        ----------
        logscale: active l'échelle logarithmique
        affiche_moyenne: affiche l'évolution de E[L]^m

        Returns
        -------

        """
        plt.plot(self.historique_nb_descendants)

        if affiche_moyenne:
            x = np.arange(self.n + 1)
            plt.plot(
                x, self.m**x, label=r"Nombre de descendants prévu ($\mathbb{E}[L]^n$)"
            )
            plt.legend()

        plt.title("Historique du nombre de descendants")
        plt.xlabel("Numéro d'époque n")
        plt.ylabel("Nombre de descendants")

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

    def plot_arbre(self, with_labels: bool = True, circular: bool = False) -> None:
        """
        Affiche l'arbre de Galton Watson du processus.

        Returns
        -------

        """
        liste_adjacence = []

        numero = 0

        for generation in self.liste_descendants:
            for nb_descendants in generation:
                for _ in range(nb_descendants):
                    liste_adjacence.append([numero])
                numero += 1

        edge_list = []

        for i in range(len(liste_adjacence)):
            edge_list.append((liste_adjacence[i][0], i + 1))

        e = nx.DiGraph(edge_list)

        if circular:
            pos = hierarchy_pos(e, 0, width=2 * np.pi)
            new_pos = {
                u: (r * np.cos(theta), r * np.sin(theta))
                for u, (theta, r) in pos.items()
            }
            nx.draw_networkx(e, pos=new_pos, with_labels=with_labels, **color_options)
        else:
            pos = hierarchy_pos(e)
            nx.draw_networkx(e, pos=pos, with_labels=with_labels, **color_options)

        plt.axis("off")
        plt.title("Arbre de Galton-Watson")

    def lance_simulations(self, nb_simulations: int, nb_epoques: int) -> list[int]:
        self.simulations = []

        for _ in range(nb_simulations):
            self.reset()
            resultat = self.simule(nb_epoques)
            self.simulations.append(resultat)

        return self.simulations

    def plot_distribution_zn(self) -> None:
        plt.title(f"Distribution des $Z_n$,\n$n = {self.n}$")
        plt.hist(self.simulations)
        plt.yscale("log")

    def resultat_simulations_survie(self, nb_simulations: int, nb_epoques: int):
        self.simulations = self.lance_simulations(nb_simulations, nb_epoques)

    def __repr__(self) -> str:
        nom_loi = self.loi.dist.name

        representation = (
            f"Processus Galton-Watson\n"
            f"- loi de reproduction L : {nom_loi}\n"
            f"- espérance E[L] = {self.m}\n"
            f"- époque n = {self.n}\n"
            f"- nombre de survivants Z_n = {self.nb_descendants}"
        )

        return representation


class SimulateurGaltonWatson:
    def __init__(
        self, loi: rv_discrete, nb_descendants: int = 1, nb_processus: int = 1_000
    ):
        self.nb_processus = nb_processus
        self.simulations: list[GaltonWatson] = [
            GaltonWatson(loi, nb_descendants) for _ in range(nb_processus)
        ]

    def simule(self, nb_epoques: int = 10) -> None:
        for i in range(self.nb_processus):
            self.simulations[i].simule(nb_epoques)
        # todo: add parallelization
        # _ = Parallel(n_jobs=-2)(delayed())
        # Parallel(n_jobs=1)(delayed(sqrt)(i ** 2) for i in range(10))

    def get_n(self) -> np.ndarray:
        return np.array([self.simulations[i].n for i in range(self.nb_processus)])

    def nombre_survivants(self) -> np.ndarray:
        return np.array(
            [self.simulations[i].nb_descendants for i in range(self.nb_processus)]
        )

    def survecus_seulement(self) -> list[GaltonWatson]:
        """Renvoie la liste des processus de Galton-Watson ayant survécu :
        on conditionne donc à la survie."""
        survecus = []

        for i in range(self.nb_processus):
            processus_actuel = self.simulations[i]

            if processus_actuel.nb_descendants > 0:
                survecus.append(processus_actuel)

        self.nb_processus = len(survecus)

        return survecus

    def retire_processus_eteints(self) -> None:
        """Retire les processus éteints du simulateur."""
        self.simulations = self.survecus_seulement()

    def get_zn_sur_n(self):
        return self.nombre_survivants() / self.get_n()
