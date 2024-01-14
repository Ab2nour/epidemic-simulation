import numpy as np
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
        self.nb_descendants = nb_descendants
        self.liste_descendants: list[list[int]] = []  # fixme: ce sont des listes de np.ndarray
        self.n: int = 0  # numéro de l'époque

    def simule(self, nb_epoques: int) -> int:
        epoque_actuelle = 0

        while epoque_actuelle < nb_epoques and self.nb_descendants > 0:
            liste_descendants = self.loi.rvs(size=self.nb_descendants)
            self.liste_descendants.append(liste_descendants)
            self.nb_descendants = np.sum(liste_descendants)

            epoque_actuelle += 1

        self.n = len(self.liste_descendants)

        return self.nb_descendants
