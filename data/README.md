# data/README.md

## Instruções de Download e Preparação dos Dados

Este diretório contém os dados de treino, validação e teste para o projeto de diagnóstico de doenças em culturas.

### Datasets Utilizados

#### 1. PlantDoc (Milho + Soja)

**Link:** https://github.com/pratikkayal/PlantDoc-Dataset

**Download:**
```bash
cd data/raw
git clone https://github.com/pratikkayal/PlantDoc-Dataset.git
cd PlantDoc-Dataset
# Arquivos já estão em data/raw/PlantDoc-Dataset/
```

**Características:**
- 2.598 imagens originais
- Imagens de campo real (não laboratório)
- Culturas: Milho (corn), Soja (soybean) + outras
- Formato: JPG com bounding boxes em XML

**Licença:** CC BY 4.0 — Singh et al. (2020)

---

#### 2. BRACOL (Café Arábica)

**Link:** https://data.mendeley.com/datasets/yy2k5y8mxg/1

**Download (opção 1 - Mendeley):**
```bash
# Acesse o link acima e faça download manual
# Extraia para data/raw/BRACOL/
```

**Download (opção 2 - GitHub Dataset Ninja):**
```bash
cd data/raw
git clone https://github.com/dataset-ninja/bracol.git
```

**Características:**
- 1.747 imagens
- Imagens de campo real com smartphones
- Doenças: bicho-mineiro, ferrugem, cercosporiose, phoma
- Anotações: classificação + severity levels (0-4)

**Licença:** CC BY 4.0 — Parraga-Alava et al. (2019)

---

#### 3. RoCoLe (Café Robusta)

**Link:** https://data.mendeley.com/datasets/c5yvn32dzg/2

**Download (opção 1 - Mendeley):**
```bash
# Acesse o link acima e faça download manual
# Extraia para data/raw/RoCoLe/
```

**Download (opção 2 - GitHub Dataset Ninja):**
```bash
cd data/raw
git clone https://github.com/dataset-ninja/rocole.git
```

**Características:**
- 1.560 imagens (4 por planta × 390 plantas)
- Campo real
- Segmentação semântica pixel-level
- Doenças: ferrugem, ácaros vermelhos

**Licença:** CC BY 4.0 — Parraga-Alava et al. (2019)

---

### Estrutura Após Download

```
data/
├── raw/
│   ├── PlantDoc-Dataset/          # PlantDoc clonado
│   ├── bracol/                    # BRACOL extraído
│   └── rocole/                    # RoCoLe extraído
├── processed/                      # (Gerado após preprocessamento)
├── train/                          # (Gerado após split)
├── val/
└── test/
```

---

### Preprocessamento e Split

Execute o notebook ou script:
```bash
python scripts/prepare_datasets.py
```

Isto irá:
1. Redimensionar imagens para 224×224 (para CNN)
2. Normalizar valores de pixel
3. Fazer split 70% treino / 15% validação / 15% teste
4. Salvar em `train/`, `val/`, `test/`
5. Documentar quantas imagens por classe em cada split

---

### Prevenção de Vazamento de Dados

**Importante:** As mesmas folhas/plantas não devem aparecer em treino e teste.

- **PlantDoc:** Splits já predefinidos no repositório
- **BRACOL e RoCoLe:** Agrupar por planta antes de dividir (script faz isso automaticamente)
- **Seed:** Fixada em 42 para reprodutibilidade

---

### Total de Imagens

| Cultura | Dataset | Total | Treino (70%) | Val (15%) | Teste (15%) |
|---------|---------|-------|--------------|-----------|------------|
| Milho | PlantDoc | ~600 | ~420 | ~90 | ~90 |
| Soja | PlantDoc | ~600 | ~420 | ~90 | ~90 |
| Café Arábica | BRACOL | 1.747 | ~1.223 | ~262 | ~262 |
| Café Robusta | RoCoLe | 1.560 | ~1.092 | ~234 | ~234 |
| **TOTAL** | — | ~5.107 | ~3.155 | ~676 | ~676 |

---

### Licenças

Todos os datasets usam **CC BY 4.0** (Creative Commons Attribution 4.0 International).

**Você deve:**
- Citar os autores/datasets em qualquer publicação
- Indicar "CC BY 4.0" nos materiais
- Manter a licença em repositórios derivados

**Atribuição sugerida:**
```
PlantDoc Dataset (Singh et al., 2020) - CC BY 4.0
BRACOL Dataset (Parraga-Alava et al., 2019) - CC BY 4.0
RoCoLe Dataset (Parraga-Alava et al., 2019) - CC BY 4.0
```

---

**Última atualização:** 19 de setembro de 2026
