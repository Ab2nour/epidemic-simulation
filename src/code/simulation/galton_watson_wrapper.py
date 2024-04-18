from src.code.simulation.galton_watson import GaltonWatson
from typing import Any


class GaltonWatsonWrapper:
    def __init__(self, gw: GaltonWatson | "GaltonWatsonWrapper"):
        self.gw = gw

    def __getattr__(self, attr: str) -> Any:
        return getattr(self.gw, attr)


class GaltonWatsonSaveWrapper(GaltonWatsonWrapper):
    def __init__(self, gw: GaltonWatson | "GaltonWatsonWrapper"):
        super().__init__(gw)

