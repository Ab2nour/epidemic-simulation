"""Galton-Watson process."""
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import rv_discrete

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

    def plot_arbre(self) -> None:
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
        pos = hierarchy_pos(e)

        nx.draw_networkx(e, pos=pos, with_labels=True, **color_options)

        plt.axis("off")
        plt.title("Arbre de Galton-Watson")

        # todo: implémenter l'affichage circulaire des noeuds ?
        # pos = hierarchy_pos(e, 0, width = 2*math.pi, xcenter=0)
        # new_pos = {u:(r*math.cos(theta),r*math.sin(theta)) for u, (theta, r) in pos.items()}
        # nx.draw(e, pos=new_pos, node_size = 50)
        # nx.draw_networkx_nodes(G, pos=new_pos, nodelist = [0], node_color = 'blue', node_size = 200)

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