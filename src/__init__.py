"""
Trabalho de Redes Neurais Artificiais - Diagnóstico de Doenças em Culturas

Este pacote implementa e compara MLP com Backpropagation vs CNN com Transfer Learning
para diagnóstico automático de doenças em folhas/frutos de soja, milho e café.

Módulos:
- models: Classes MLP e CNN
- data_loader: DataLoaders para PlantDoc, BRACOL, RoCoLe
- training: Loop de treino e validação
- interpretability: Grad-CAM, saliência, oclusão
- utils: Funções auxiliares
"""

__version__ = "0.1.0"
__author__ = "Grupo de RNA - UEL"

from . import models
from . import data_loader
from . import training
from . import interpretability
from . import utils

__all__ = [
    "models",
    "data_loader",
    "training",
    "interpretability",
    "utils",
]
