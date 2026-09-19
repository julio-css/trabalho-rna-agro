"""
Script para baixar e preparar os 3 datasets
Datasets: PlantDoc, BRACOL, RoCoLe
"""

import os
import subprocess
from pathlib import Path

# Configurações
DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("DOWNLOAD E PREPARAÇÃO DE DATASETS")
print("=" * 70)

# ============================================================================
# 1. PLANTDOC (Milho + Soja)
# ============================================================================

print("\n[1/3] Baixando PlantDoc (Milho + Soja)...")
print("-" * 70)

plantdoc_dir = RAW_DIR / "PlantDoc-Dataset"

if not plantdoc_dir.exists():
    os.chdir(RAW_DIR)
    subprocess.run(
        ["git", "clone", "https://github.com/pratikkayal/PlantDoc-Dataset.git"],
        check=True
    )
    os.chdir("../..")
    print("✅ PlantDoc clonado com sucesso")
else:
    print("✅ PlantDoc já existe, pulando download")

# ============================================================================
# 2. BRACOL (Café Arábica)
# ============================================================================

print("\n[2/3] Baixando BRACOL (Café Arábica)...")
print("-" * 70)

bracol_dir = RAW_DIR / "bracol"

if not bracol_dir.exists():
    os.chdir(RAW_DIR)
    subprocess.run(
        ["git", "clone", "https://github.com/dataset-ninja/bracol.git"],
        check=True
    )
    os.chdir("../..")
    print("✅ BRACOL clonado com sucesso")
else:
    print("✅ BRACOL já existe, pulando download")

# ============================================================================
# 3. ROCOLE (Café Robusta)
# ============================================================================

print("\n[3/3] Baixando RoCoLe (Café Robusta)...")
print("-" * 70)

rocole_dir = RAW_DIR / "rocole"

if not rocole_dir.exists():
    os.chdir(RAW_DIR)
    subprocess.run(
        ["git", "clone", "https://github.com/dataset-ninja/rocole.git"],
        check=True
    )
    os.chdir("../..")
    print("✅ RoCoLe clonado com sucesso")
else:
    print("✅ RoCoLe já existe, pulando download")

# ============================================================================
# RESUMO
# ============================================================================

print("\n" + "=" * 70)
print("✅ DOWNLOAD CONCLUÍDO")
print("=" * 70)

print("\nDatasets baixados em:")
print(f"  - {plantdoc_dir}")
print(f"  - {bracol_dir}")
print(f"  - {rocole_dir}")

print("\n📊 Próximos passos:")
print("  1. Execute: python scripts/prepare_datasets.py")
print("  2. Isso irá preprocessar e fazer os splits treino/val/teste")
print("  3. Então execute os notebooks: 01_eda.ipynb → 02_mlp.ipynb → 03_cnn.ipynb")
