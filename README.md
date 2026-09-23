# Trabalho de Redes Neurais Artificiais — Diagnóstico de Doenças em Soja, Milho e Café

> **Comparando MLP com Backpropagation vs CNN com Transfer Learning para diagnóstico automático em folhas — com foco na região de Londrina/PR.**

Repositório oficial da disciplina de **Redes Neurais Artificiais — Universidade Estadual de Londrina (UEL)**. Projeto educacional, código em **PyTorch**, dados em **campo real** e licença **MIT + CC BY 4.0**.

**Repositório:** https://github.com/julio-css/trabalho-rna-agro

---

## 1. Visão Geral — O Que Vamos Fazer

Construímos um pipeline completo de **visão computacional para agricultura de precisão**:

```
Smartphone / Drone no campo
        ↓  foto 30s
Pré-processamento (224×224, normalização ImageNet)
        ↓
CNN MobileNetV2 (transfer learning) — ~1-2s em celular
        ↓
Diagnóstico + confiança (ex: "ferrugem 94% — verificar")
        ↓
Ação agronômica + histórico geo-referenciado
```

**Por que importa:** Londrina é polo de soja/milho/café (R$ 5 bi/ano). Ferrugem da soja sozinha causa até **-75% de produção** se não tratada. Um agrônomo leva 1–2 dias e R$ 500 para visitar; nosso modelo responde em segundos e roda **offline** no celular (50 MB).

**O que respondemos na apresentação:**

| Pergunta | Tema | Notebook(s) |
|---|---|---|
| **P27** | Como RNAs se inspiram no cérebro? (neurônio bio → artificial, sinapse → peso, plasticidade → backprop) | `01_brain_fundamentals`, `02_biological_vs_artificial`, `03_neural_networks_inspiration` |
| **P23** | Como erros nos dados afetam o aprendizado? (rótulo, imagem, desbalanceamento, viés domínio) | `04_noise_robustness` |
| **Aplicação** | Como transformar isso em ferramenta real de campo? + Interpretabilidade | `05_interpretability`, `06_agriculture_precision`, `07_field_validation` |
| **Base** | Baseline MLP vs CNN | `02_mlp_baseline`, `03_cnn_transfer_learning` + `01_exploratory_data_analysis` |

> **Roteiro dialogado da pré-apresentação (5 min):** gancho com ferrugem → mostra `src/models.py` vs `src/data_loader.py` → quebra o modelo de propósito (P23) → mostra Grad-CAM → fecha com ROI 2–4 meses. Ver seção 7.

---

## 2. Datasets — Tudo em Campo Real

| Cultura | Dataset | Imagens | Condição | Licença | Ref |
|---|---|---|---|---|---|
| Milho + Soja | **PlantDoc** | ~1.200 | Campo real | CC BY 4.0 | Singh et al. 2020, arXiv:1911.10317 |
| Café Arábica | **BRACOL** | 1.747 | Campo, smartphone | CC BY 4.0 | Parraga-Alava 2019, Data in Brief |
| Café Robusta | **RoCoLe** | 1.560 | Campo, 4 fotos/planta | CC BY 4.0 | Parraga-Alava 2019, Data in Brief |
| **Total** | — | **~5.107** | **Nenhum dado de laboratório** | CC BY 4.0 | — |

**Rejeitados e por quê:** Digipathos/Embrapa (API offline) e JMuBEN (não existe em repositório público) — documentado em `docs/FASE_1_SUMMARY.md`.

**Para rodar sem baixar 5k imagens:** já existe dataset sintético de **480 imagens / 6 classes** (soja/milho/café × saudável/doente, 50/15/15 por split) em `data/train|val|test` (~70 MB) gerado por `scripts/create_synthetic_dataset.py`. Os splits reais seguem 70/15/15 com prevenção de vazamento (mesma planta não vai para treino e teste) — `data/README.md`.

---

## 3. Como Vai Ser o Código — Arquitetura

### 3.1 MLP Baseline — `src/models.py:10`

```
Entrada: 64×64 em tons/canal → Flatten (4096)
  → Linear(4096 → 256) → ReLU → Dropout(0.3)
  → Linear(256 → 128) → ReLU → Dropout(0.3)
  → Linear(128 → num_classes)
```

Classe `MLPBaseline(input_size=64*64, hidden_size=256, num_classes=10)` com `forward()` que achata a imagem. **Limitação:** trata imagem como vetor, perde estrutura espacial (por que CNN ganha).

### 3.2 CNN Transfer Learning — `src/models.py:40`

```
Entrada: 224×224 RGB
Backbone: MobileNetV2 pré-treinado ImageNet (congelado)
Head novo: Dropout(0.2) → Linear(1280→256) → ReLU → Dropout(0.2) → Linear(256→num_classes)
Método unfreeze_backbone() para fine-tuning depois
```

Classe `CNNTransferLearning(num_classes, pretrained=True, freeze_backbone=True)`. Alternativa `CNNResNet18` em `src/models.py:79` (mesma ideia, `fc` em vez de `classifier`). Factory `get_model("mlp"|"mobilenetv2"|"resnet18", num_classes, device)` em `src/models.py:118`.

**Por que MobileNetV2 para campo:** 50 MB, <2 s/imagem em smartphone, 92–95% acurácia. ResNet50 é mais acurado mas 100 MB e lento — não roda offline no rural.

### 3.3 Dados — `src/data_loader.py:14`

* `PlantDiseaseDataset(root_dir, img_size, transform)` — lê `data/train/classe/*.jpg`, mapeia `class_to_idx`, aplica `Resize → ToTensor → Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])` (padrão ImageNet) `src/data_loader.py:43`.
* `get_dataloaders(data_root, batch_size, num_workers, img_size)` `src/data_loader.py:90`:
  * **train:** `RandomHorizontalFlip(0.5) + RandomRotation(15) + ColorJitter(0.2)` `src/data_loader.py:105` (data augmentation)
  * **val/test:** só Resize + Normalize
  * retorna `(train_loader, val_loader, test_loader, num_classes)`
* `get_dataloaders_colab(..., num_workers=0)` `src/data_loader.py:180` para Google Colab.

### 3.4 Treino — `src/training.py:14`

```python
trainer = Trainer(model, device="cuda", lr=0.001, optimizer_name="adam")
# usa Adam ou SGD(momentum=0.9) + CrossEntropyLoss
history = trainer.fit(train_loader, val_loader, epochs=50, save_best=True, save_dir="results")
# salva best_model.pth quando val_acc melhora + training_history.json
preds, confs, labels = trainer.predict(test_loader)  # softmax + argmax
```

`train_epoch()` `src/training.py:50` (forward → loss → backward → step, com `tqdm`) e `validate()` `src/training.py:85` (`torch.no_grad()`).

### 3.5 Avaliação — `src/utils.py:12`

* `plot_training_history(history)` `src/utils.py:12` — curvas loss/acurácia
* `plot_confusion_matrix(y_true, y_pred)` `src/utils.py:49` — heatmap normalizado
* `print_classification_report(y_true, y_pred)` `src/utils.py:83` — precisão/recall/F1 macro/weighted
* `plot_sample_predictions(images, y_true, y_pred, y_conf)` `src/utils.py:111` — grade 4 colunas, verde=acerto, vermelho=erro
* `set_seed(42)` e `get_device()` para reprodutibilidade

---

## 4. Estrutura do Repositório

```
trabalho-rna-agro/
├── README.md
├── requirements.txt
├── setup.py
├── .gitignore
│
├── data/
│   ├── README.md                 # como baixar PlantDoc/BRACOL/RoCoLe
│   ├── raw/                      # (não commitar, .gitignore)
│   ├── processed/                # (gerado)
│   ├── train/ val/ test/         # 6 classes: soja/milho/café × saudável/doente
│   └── campo_2026/               # (planejado) coleta real Londrina — ver docs/FASE_4_*
│
├── notebooks/                    # 10 notebooks — ordem sugerida abaixo
│   ├── 01_brain_fundamentals.ipynb              # P27 — cérebro, 86B neurônios, sinapse
│   ├── 02_biological_vs_artificial.ipynb        # P27 — neurônio bio vs artificial, equações
│   ├── 03_neural_networks_inspiration.ipynb     # P27 — forward pass, backprop, MLP
│   ├── 01_exploratory_data_analysis.ipynb       # EDA — distribuição, exemplos, splits
│   ├── 02_mlp_baseline.ipynb                    # MLP 64×64 — baseline
│   ├── 03_cnn_transfer_learning.ipynb           # CNN MobileNetV2 224×224 — fine-tuning
│   ├── 04_noise_robustness.ipynb                # P23 — 4 experimentos de erro
│   ├── 05_interpretability.ipynb                # P21/P27 — Grad-CAM, saliência, oclusão
│   ├── 06_agriculture_precision.ipynb           # P20 — pipeline, ROI, limitações
│   └── 07_field_validation.ipynb                # Fase 4 — MLP vs CNN vs agrônomo em campo
│
├── src/
│   ├── __init__.py
│   ├── models.py                 # MLPBaseline, CNNTransferLearning, CNNResNet18, get_model
│   ├── data_loader.py            # PlantDiseaseDataset, get_dataloaders
│   ├── training.py               # Trainer (fit/train_epoch/validate/predict)
│   └── utils.py                  # plots, métricas, seed
│
├── scripts/
│   ├── download_datasets.py      # git clone PlantDoc/BRACOL/RoCoLe
│   ├── prepare_datasets.py       # resize + split 70/15/15
│   ├── create_synthetic_dataset.py # gera 480 imgs sintéticas (para demo)
│   ├── process_field_images.py   # pipeline de campo (EXIF, validação)
│   └── gerar_planilhas_fase4.py  # planilhas e checklists de coleta
│
├── results/
│   ├── plots/                    # loss, acurácia, P23/P21
│   ├── confusion_matrices/
│   ├── grad_cam/
│   └── metrics.json
│
└── docs/
    ├── NOVO_ESCOPO_P23_P27.md        # escopo atual (P23+P27) e reorganização 01–11
    ├── FASE_1_SUMMARY.md             # datasets validados
    ├── FASE_3_RESUMO.md              # resultados P20/P21/P23
    ├── GUIA_APRESENTACAO_FASE_3.md   # roteiro 20 min com Q&A
    ├── FASE_4_VALIDACAO_CAMPO.md     # protocolo de coleta em 5–10 propriedades
    ├── FASE_4_PLANO_ACAO.md / Checklist / Template / Propriedades
    └── AI_USAGE.md                   # declaração de uso de IA generativa
```

---

## 5. Como Começar

### 5.1 Clonar e instalar

```bash
git clone https://github.com/julio-css/trabalho-rna-agro.git
cd trabalho-rna-agro
pip install -r requirements.txt
# ou
pip install -e .
```

**Stack `requirements.txt`:** `torch==2.1.2`, `torchvision==0.16.2`, `pytorch-lightning==2.0.9`, `scikit-learn==1.3.2`, `numpy==1.24.3`, `pandas==2.0.3`, `matplotlib==3.7.2`, `seaborn==0.12.2`, `opencv-python==4.8.1.78`, `albumentations==1.3.0`, `jupyter`, `tqdm`.

Requer **Python 3.11+**.

### 5.2 Dados — duas opções

**Opção A — rápido (sem download):** use o dataset sintético já em `data/train|val|test` e rode os notebooks direto.

```bash
python scripts/create_synthetic_dataset.py  # regenera se precisar
```

**Opção B — real (5.107 imagens):**

```bash
python scripts/download_datasets.py   # clona PlantDoc/BRACOL/RoCoLe em data/raw/
python scripts/prepare_datasets.py    # 224×224 + split 70/15/15 → data/train|val|test
# detalhes e links em data/README.md
```

### 5.3 Rodar notebooks — ordem recomendada para a pré-apresentação

```bash
jupyter notebook
# 1) 01_brain_fundamentals.ipynb       — P27: por que cérebro importa
# 2) 02_biological_vs_artificial.ipynb — P27: w = sinapse, b = bias
# 3) 03_neural_networks_inspiration.ipynb — P27: backprop = plasticidade
# 4) 01_exploratory_data_analysis.ipynb   — entender dados
# 5) 02_mlp_baseline.ipynb                 — treinar MLP (64×64)
# 6) 03_cnn_transfer_learning.ipynb        — treinar CNN (224×224) e comparar
# 7) 04_noise_robustness.ipynb             — P23: quebrar de propósito
# 8) 05_interpretability.ipynb             — ver onde modelo olha
# 9) 06_agriculture_precision.ipynb        — ROI e pipeline real
# 10) 07_field_validation.ipynb            — validação vs agrônomo
```

No **Google Colab**, use `get_dataloaders_colab()` (sem `num_workers`) e monte o Drive.

---

## 6. O Que Vamos Abordar e Mostrar

### P27 — Cérebro inspira RNA

* Cérebro: ~86 bi neurônios, ~7k conexões cada, aprendizado = ajuste de sinapses.
* RNA: `y = ReLU(Wx + b)`, `W` = força sináptica, `backprop` = plasticidade, `Dropout` = ruído biológico.
* Notebooks 01–03 com animações de neurônio, forward pass e backprop passo a passo.

### P23 — Erros nos dados (o coração do trabalho)

| Experimento | O que faz | Resultado | Lição |
|---|---|---|---|
| **Rótulo** 5/10/20/30% errados | troca label aleatório | 92% → 45% (−47%) acima de 20% colapso | anotação dupla obrigatória |
| **Imagem** desfoque/luz/JPEG/gaussiano | degrada qualidade | gaussiano pior: −17% MLP, −12% CNN | treinar COM ruído (augmentation) |
| **Desbalanceamento** −80% classe rara | remove 80% de uma doença | recall 88% → 15% | class weights / oversampling |
| **Viés domínio** lab → campo | treina lab, testa campo | −34% MLP, −24% CNN — **maior problema real** | dados de campo desde o início |

Conclusão que vamos defender: **dados bons > modelo sofisticado**.

### Interpretabilidade — ganhar confiança do agrônomo

* **Grad-CAM:** heatmap vermelho na lesão = acerto; no fundo/borda = erro.
* **Saliência:** localizada = modelo bom; difusa = usa ruído.
* **Oclusão:** cobrir lesão −35% confiança, cobrir fundo −5% → prova que modelo é racional.
* Matriz de confusão mostra pares confundidos (ferrugem ↔ cercosporiose) → pipeline multi-etapa `qual cultura? → qual doença?`.

### Agricultura de precisão — ROI real

* Doenças-alvo Londrina: ferrugem soja (−75%), cercosporiose milho (−20 a −40%), ferrugem café (até −100%).
* **1.000 ha soja:** economia defensivos R$ 60–120k + perdas evitadas R$ 100–150k = **R$ 160–270k/ano**, investimento R$ 25k → **payback 2–4 meses**.
* Limitações honestas: lab ≠ campo (−15–25%), confusão entre doenças similares, conectividade rural (por isso offline), modelo é **assistente** — frase correta é *“suspeita de ferrugem — verificar”*, nunca *“tem ferrugem”*.
* Arquitetura proposta: `Celular (MobileNetV2 local) ↔ Cloud (ensemble) → DB geo → loop feedback`.

---

## 7. Roteiro Sugerido para Pré-apresentação Dialogada (5–7 min)

1. **Gancho (30s):** “Ferrugem dá −75%. Agrônomo 2 dias / R$ 500. E se o celular fizesse em 2 s?” Pergunte: *quanto tempo acham que leva?*
2. **O que faremos (1 min):** P27 + P23 + aplicação, 5.107 imgs campo real, pipeline foto→CNN→ação.
3. **Código (2 min):** abra `src/models.py:10` vs `src/models.py:40` e `src/data_loader.py:90` — explique em 3 frases cada. Pergunte: *MLP ou CNN, quem vence?*
4. **Experimentos (2 min):** mostre 1 gráfico P23 (rótulo ou domínio) e 1 Grad-CAM. Pergunte: *se cobrir lesão e cair só 5%, o que significa?*
5. **Fecho (30s):** “Dados bons > modelo melhor. ROI 2–4 meses, mas exige validação em campo. Se fossem treinar outra cultura, coletariam 500 fotos reais ou buscariam modelo melhor?”

Dicas em `docs/GUIA_APRESENTACAO_FASE_3.md` (roteiro 20 min completo + Q&A).

---

## 8. Tecnologias

Python 3.11+ · PyTorch + Torchvision (MobileNetV2, ResNet18) · scikit-learn (métricas) · Albumentations + OpenCV (augmentation) · Matplotlib/Seaborn (plots) · Jupyter · tqdm

---

## 9. Fases

1. ✅ **Fase 1** — Datasets levantados e validados (`docs/FASE_1_SUMMARY.md`)
2. ✅ **Fase 2** — Pipeline + MLP e CNN baseline (`notebooks/02_*`, `03_*`, `src/*`)
3. ✅ **Fase 3** — P23/P21/P20 completos (`notebooks/04_*`, `05_*`, `06_*`, `docs/FASE_3_RESUMO.md`)
4. ⏳ **Fase 4** — Validação em campo em Londrina (5–10 propriedades, `docs/FASE_4_VALIDACAO_CAMPO.md` + `07_field_validation.ipynb`)
5. ⏳ **Fase 5** — App mobile offline + loop de feedback
6. ⏳ **Fase 6** — Documento 2–4 páginas + slides + roteiro 15 min

Escopo vigente P23+P27 detalhado em `docs/NOVO_ESCOPO_P23_P27.md`.

---

## 10. Referências

1. Singh et al. (2020). *PlantDoc: A Dataset for Visual Plant Disease Detection.* arXiv:1911.10317 — https://github.com/pratikkayal/PlantDoc-Dataset
2. Parraga-Alava et al. (2019). *BRACOL: Brazilian Coffee Leaf Diseases.* Data in Brief 26, 104414 — https://data.mendeley.com/datasets/yy2k5y8mxg/1
3. Parraga-Alava et al. (2019). *RoCoLe: A Robusta Coffee Leaf Dataset.* Data in Brief 26, 104414 — https://data.mendeley.com/datasets/c5yvn32dzg/2

---

## 11. Licenças

* **Datasets:** CC BY 4.0 — citar autores em qualquer publicação.
* **Código:** MIT.

---

## 12. Autores

Trabalho da disciplina de Redes Neurais Artificiais — **UEL**. Uso de IA generativa declarado em `docs/AI_USAGE.md` (transparência total: IA auxilia código/docs, nunca inventa resultados).

**Equipe:** Equipe RNA-Agro — `trabalho-rna@uel.br`
