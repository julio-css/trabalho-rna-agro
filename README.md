# Trabalho de Redes Neurais Artificiais - Diagnóstico de Doenças em Culturas

## Visão Geral

Projeto educacional que compara **MLP com Backpropagation** vs **CNN com Transfer Learning** para diagnóstico automático de doenças em folhas/frutos de **soja, milho e café** — culturas relevantes para a região de Londrina/PR.

### Perguntas que respondemos

- **P20:** Como redes neurais artificiais apoiam a agricultura de precisão?
- **P21:** Como interpretar decisões de uma rede neural artificial?
- **P23:** Como erros nos dados afetam o aprendizado?

---

## Datasets Utilizados

| Cultura | Dataset | Imagens | Licença | Tipo |
|---------|---------|---------|---------|------|
| Milho + Soja | PlantDoc | ~1.200 | CC BY 4.0 | Campo real |
| Café Arábica | BRACOL | 1.747 | CC BY 4.0 | Campo real |
| Café Robusta | RoCoLe | 1.560 | CC BY 4.0 | Campo real |

**Total:** ~5.107 imagens, todas em condições de campo real (não laboratório).

---

## Estrutura do Repositório

```
trabalho-rna-agro/
├── README.md                          # Este arquivo
├── requirements.txt                   # Dependências Python
├── .gitignore                         # Arquivos ignorados
├── setup.py                           # Setup do projeto
│
├── data/
│   ├── README.md                      # Instruções de download
│   ├── raw/                           # Imagens brutas (não commitar)
│   ├── processed/                     # Imagens preprocessadas
│   ├── train/                         # Split treino
│   ├── val/                           # Split validação
│   └── test/                          # Split teste
│
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_mlp_baseline.ipynb
│   ├── 03_cnn_transfer_learning.ipynb
│   ├── 04_noise_robustness.ipynb
│   ├── 05_interpretability.ipynb
│   └── 06_agriculture_precision.ipynb
│
├── src/
│   ├── __init__.py
│   ├── models.py                      # MLP e CNN classes
│   ├── data_loader.py                 # Dataset loaders
│   ├── training.py                    # Loop treino/validação
│   ├── interpretability.py            # Grad-CAM, saliência, oclusão
│   └── utils.py                       # Funções auxiliares
│
├── results/
│   ├── plots/                         # Gráficos (loss, acurácia, etc.)
│   ├── confusion_matrices/            # Matrizes de confusão
│   ├── grad_cam/                      # Visualizações Grad-CAM
│   └── metrics.json                   # Métricas finais
│
└── docs/
    ├── PROJETO.md                     # Documento principal (2-4 páginas)
    ├── APRESENTACAO_ROTEIRO.md        # Roteiro de apresentação (15+ min)
    └── AI_USAGE.md                    # Declaração de uso de IA generativas
```

---

## Como Começar

### 1. Clonar o repositório

```bash
git clone https://github.com/julio-css/trabalho-rna-agro.git
cd trabalho-rna-agro
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Download dos dados

```bash
python scripts/download_datasets.py
```

(Instruções detalhadas em `data/README.md`)

### 4. Executar notebooks

- `01_exploratory_data_analysis.ipynb` — Entender os dados
- `02_mlp_baseline.ipynb` — Treinar MLP (baseline)
- `03_cnn_transfer_learning.ipynb` — Treinar CNN (MobileNetV2)
- `04_noise_robustness.ipynb` — Testes de robustez (P23)
- `05_interpretability.ipynb` — Grad-CAM e saliência (P21)
- `06_agriculture_precision.ipynb` — Aplicação em agricultura (P20)

---

## Tecnologias

- **Python 3.11+**
- **PyTorch** — Modelos de deep learning
- **Torchvision** — Transfer learning (MobileNetV2, ResNet18)
- **Scikit-learn** — Métricas, matriz de confusão
- **Matplotlib, Seaborn** — Visualizações
- **OpenCV** — Processamento de imagens

---

## Fases do Desenvolvimento

1. **Fase 1** ✅ — Levantamento e validação de datasets
2. **Fase 2** — Pipeline de dados + baseline MLP e CNN
3. **Fase 3** — Experimentos de robustez (ruído, desbalanceamento)
4. **Fase 4** — Interpretabilidade (Grad-CAM, saliência, oclusão)
5. **Fase 5** — Agricultura de precisão (pipeline de campo)
6. **Fase 6** — Documento, slides, roteiro de apresentação

---

## Referências

1. **PlantDoc:** Singh et al. (2020). "PlantDoc: A Dataset for Visual Plant Disease Detection." arXiv:1911.10317
2. **BRACOL:** Parraga-Alava et al. (2019). "BRACOL: Brazilian Coffee Leaf Diseases Dataset." Data in Brief, 26, 104414
3. **RoCoLe:** Parraga-Alava et al. (2019). "RoCoLe: A Robusta Coffee Leaf Dataset." Data in Brief, 26, 104414

---

## Licenças

- Datasets: CC BY 4.0 (Creative Commons Attribution 4.0)
- Código: MIT

---

## Autores

Trabalho desenvolvido para a disciplina de Redes Neurais Artificiais - Universidade Estadual de Londrina (UEL)

---

**Repositório:** https://github.com/julio-css/trabalho-rna-agro


