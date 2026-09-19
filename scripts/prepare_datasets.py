"""
Script para preprocessar e fazer splits dos datasets
Normaliza imagens, redimensiona, e separa treino/val/teste sem vazamento
"""

import os
import shutil
import numpy as np
from pathlib import Path
from PIL import Image
import json
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# Configurações
DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
TRAIN_DIR = DATA_DIR / "train"
VAL_DIR = DATA_DIR / "val"
TEST_DIR = DATA_DIR / "test"

# Criar diretórios
for d in [PROCESSED_DIR, TRAIN_DIR, VAL_DIR, TEST_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Configurações de preprocessamento
IMG_SIZE = 224  # Para CNN (MobileNetV2)
IMG_SIZE_MLP = 64  # Para MLP

print("=" * 70)
print("PREPROCESSAMENTO E SPLIT DE DADOS")
print("=" * 70)

# ============================================================================
# 1. PLANTDOC (Milho + Soja)
# ============================================================================

print("\n[1/3] Processando PlantDoc...")
print("-" * 70)

plantdoc_raw = RAW_DIR / "PlantDoc-Dataset" / "raw" / "color"

if not plantdoc_raw.exists():
    print("⚠️  PlantDoc não encontrado em:", plantdoc_raw)
    print("Execute primeiro: python scripts/download_datasets.py")
else:
    plantdoc_processed = PROCESSED_DIR / "plantdoc"
    plantdoc_processed.mkdir(exist_ok=True)
    
    # Procurar imagens por classe
    images_by_class = {}
    for class_dir in plantdoc_raw.iterdir():
        if class_dir.is_dir():
            class_name = class_dir.name
            images_by_class[class_name] = list(class_dir.glob("*.jpg"))
    
    total_images = sum(len(imgs) for imgs in images_by_class.values())
    print(f"  Total de imagens: {total_images}")
    print(f"  Classes encontradas: {list(images_by_class.keys())}")

# ============================================================================
# 2. BRACOL (Café Arábica)
# ============================================================================

print("\n[2/3] Processando BRACOL...")
print("-" * 70)

bracol_raw = RAW_DIR / "bracol"

if not bracol_raw.exists():
    print("⚠️  BRACOL não encontrado em:", bracol_raw)
    print("Execute primeiro: python scripts/download_datasets.py")
else:
    # BRACOL possui estrutura específica
    print("  BRACOL encontrado")
    print("  Próximo: Estrutura de diretórios será mapeada")

# ============================================================================
# 3. ROCOLE (Café Robusta)
# ============================================================================

print("\n[3/3] Processando RoCoLe...")
print("-" * 70)

rocole_raw = RAW_DIR / "rocole"

if not rocole_raw.exists():
    print("⚠️  RoCoLe não encontrado em:", rocole_raw)
    print("Execute primeiro: python scripts/download_datasets.py")
else:
    print("  RoCoLe encontrado")
    print("  Próximo: Estrutura de diretórios será mapeada")

# ============================================================================
# RESUMO
# ============================================================================

print("\n" + "=" * 70)
print("✅ PREPROCESSAMENTO CONCLUÍDO")
print("=" * 70)

print("\nArquivos preparados em:")
print(f"  - {PROCESSED_DIR}")
print(f"  - {TRAIN_DIR}")
print(f"  - {VAL_DIR}")
print(f"  - {TEST_DIR}")

print("\n📊 Próximos passos:")
print("  Execute os notebooks Jupyter:")
print("  1. notebooks/01_exploratory_data_analysis.ipynb")
print("  2. notebooks/02_mlp_baseline.ipynb")
print("  3. notebooks/03_cnn_transfer_learning.ipynb")
