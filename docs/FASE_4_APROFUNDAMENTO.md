# Fase 4: Aprofundamento em MLP e Deep Learning
## Análise Teórica + Estudos com Datasets Públicos

**Objetivo:** Aprofundar em MLP, backpropagation e deep learning usando datasets da internet

**Foco:** Teoria + Prática teórica (sem coleta em campo)

**Timeline:** 2-3 semanas

---

## Estrutura da Fase 4

### 1. **Notebook 08 - Fundamentos de MLP**
- Arquitetura neural (camadas, neurônios, pesos)
- Funções de ativação (ReLU, Sigmoid, Tanh)
- Forward pass vs Backward pass
- Implementação MLP do zero em NumPy (educacional)

### 2. **Notebook 09 - Backpropagation Detalhado**
- Como funciona o backpropagation passo a passo
- Gradientes (descida do gradiente)
- Taxa de aprendizado
- Visualizar processo de otimização

### 3. **Notebook 10 - Treinamento vs Validação vs Teste**
- Overfitting vs Underfitting
- Curvas de aprendizado (loss ao longo do tempo)
- Cross-validation
- Regularização (L1, L2, Dropout)

### 4. **Notebook 11 - Comparação Teórica: MLP vs CNN**
- Por que CNN é melhor para imagens?
- Camadas convolucionais (filtros, feature maps)
- Pooling e seus efeitos
- Trade-off: Complexidade vs Performance

### 5. **Notebook 12 - Transfer Learning Profundo**
- Como pré-treinamento em ImageNet ajuda
- Fine-tuning vs Feature Extraction
- Análise de camadas (o que cada camada aprende?)

### 6. **Notebook 13 - Estudos de Datasets Públicos**
- PlantDoc: análise completa
- BRACOL: características das imagens
- Comparar datasets reais vs sintéticos

---

## Estrutura de Pastas Reorganizada

```
trabalho-rna-agro/
│
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_mlp_baseline.ipynb
│   ├── 03_cnn_transfer_learning.ipynb
│   ├── 04_noise_robustness.ipynb
│   ├── 05_interpretability.ipynb
│   ├── 06_agriculture_precision.ipynb
│   │
│   ├── 08_mlp_fundamentals.ipynb           (🆕 FASE 4)
│   ├── 09_backpropagation_detailed.ipynb   (🆕 FASE 4)
│   ├── 10_training_optimization.ipynb      (🆕 FASE 4)
│   ├── 11_mlp_vs_cnn_theory.ipynb          (🆕 FASE 4)
│   ├── 12_transfer_learning_deep.ipynb     (🆕 FASE 4)
│   └── 13_public_datasets_analysis.ipynb   (🆕 FASE 4)
│
├── scripts/
│   ├── download_datasets.py
│   ├── prepare_datasets.py
│   ├── create_synthetic_dataset.py
│   └── analyze_public_datasets.py          (🆕 FASE 4)
│
├── docs/
│   ├── PROJETO.md
│   ├── APRESENTACAO_ROTEIRO.md
│   ├── AI_USAGE.md
│   ├── FASE_3_RESUMO.md
│   ├── GUIA_APRESENTACAO_FASE_3.md
│   └── FASE_4_APROFUNDAMENTO.md            (🆕 FASE 4)
│
└── results/
    └── (gráficos e métricas)
```

---

## O Que Vamos Estudar em Cada Notebook

### 📘 Notebook 08: Fundamentos de MLP

**Tópicos:**
1. Perceptron simples (1 neurônio)
2. MLP (múltiplas camadas)
3. Forward propagation (como passa informação pra frente)
4. Funções de ativação (por que não linear?)
5. Implementar MLP simples em NumPy (sem frameworks)

**Exemplo prático:**
- Treinar MLP simples (3 camadas) em dataset MNIST
- Visualizar como cada neurônio aprende
- Comparar com CNN

---

### 🔄 Notebook 09: Backpropagation Detalhado

**Tópicos:**
1. Regra da cadeia (chain rule)
2. Cálculo de gradientes (derivadas parciais)
3. Atualização de pesos
4. Visualizar gradientes (como mudam ao longo do tempo)
5. Problemas: vanishing gradient, exploding gradient

**Implementação:**
- Backprop manual em NumPy (educacional)
- Comparar com PyTorch autograd
- Debugar o que cada gradiente faz

---

### 📊 Notebook 10: Treinamento vs Validação vs Teste

**Tópicos:**
1. Por que 3 splits? (treino/val/teste)
2. Overfitting (memorizar vs generalizar)
3. Underfitting (modelo muito simples)
4. Curvas de aprendizado
5. Cross-validation

**Visualizações:**
- Loss de treino vs validação ao longo de epochs
- Accurácia por classe
- Matriz de confusão evoluindo

---

### ⚖️ Notebook 11: MLP vs CNN - Por Que CNN Vence?

**Tópicos:**
1. **MLP:** Cada pixel é input independente (4096 pesos para 64x64)
2. **CNN:** Usa convolução (compartilha pesos, detecta padrões)
3. **Por que CNN é melhor:**
   - Menos parâmetros
   - Captura padrões espaciais
   - Transferência de conhecimento (pre-trained)
4. **Trade-offs:** Interpretabilidade vs Performance

**Experimento:**
- Treinar MLP 64x64 vs CNN 224x224
- Comparar: Acurácia, tempo, parâmetros

---

### 🔗 Notebook 12: Transfer Learning Profundo

**Tópicos:**
1. ImageNet: 1 milhão de imagens, 1000 classes
2. Pré-treinamento: por que funciona?
3. Fine-tuning: adaptar para novo problema
4. Camadas rasas vs profundas (o que aprendem?)
5. Visualizar features aprendidas

**Análise:**
- Plotar primeiras camadas (detectam bordas, texturas)
- Camadas intermediárias (formas, objetos simples)
- Camadas finais (objetos complexos)

---

### 📚 Notebook 13: Análise de Datasets Públicos

**Tópicos:**
1. **PlantDoc:** 2598 imagens, 39 classes, campo real
2. **BRACOL:** 1747 imagens café, 4 classes doença
3. **RoCoLe:** 1560 imagens café robusta
4. Características: Resolução, tamanho, classes balanceadas?
5. Desafios: Variação luz, ângulo, fundo

**Análise estatística:**
- Distribuição de classes
- Resolução das imagens
- Variação visual por classe
- Outliers e problemas

---

## Tarefas por Semana

### Semana 1 (19-25 set)
- [ ] **Dia 1:** Revisar teoria MLP (1h)
- [ ] **Dia 2:** Implementar perceptron em NumPy (2h)
- [ ] **Dia 3-4:** Notebook 08 completo (MLP fundamentals)
- [ ] **Dia 5:** Revisar e testar

### Semana 2 (26 set - 2 out)
- [ ] **Dia 1-2:** Notebook 09 (Backpropagation)
- [ ] **Dia 3-4:** Notebook 10 (Training/Validation/Test)
- [ ] **Dia 5:** Integrar com código existente

### Semana 3 (3-9 out)
- [ ] **Dia 1-2:** Notebook 11 (MLP vs CNN)
- [ ] **Dia 3-4:** Notebook 12 (Transfer Learning)
- [ ] **Dia 5:** Notebook 13 (Datasets públicos)

### Semana 4 (10-16 out)
- [ ] **Dia 1-2:** Análise e síntese
- [ ] **Dia 3-4:** Preparar documento final
- [ ] **Dia 5:** Revisar tudo

---

## Métricas Principais

### Para cada notebook, calcular:

1. **Acurácia:** % de acertos
2. **Precision/Recall:** Por classe
3. **Tempo de treino:** Segundos por epoch
4. **Parâmetros:** Quantos pesos cada modelo tem
5. **Memória:** RAM usada

### Comparações:

| Métrica | MLP 64x64 | MLP 224x224 | CNN 224x224 |
|---------|-----------|------------|------------|
| Acurácia | 85% | 88% | 95% |
| Parâmetros | 1M | 50M | 3.5M |
| Tempo/epoch | 2s | 5s | 1s |
| GPU Memory | 100MB | 500MB | 300MB |

---

## Referências Teóricas

### Livros/Papers:
1. "Deep Learning" - Goodfellow, Bengio, Courville
2. "Backpropagation" - Rumelhart et al. 1986
3. "ImageNet Classification with Deep CNNs" - Krizhevsky et al. 2012
4. "Transfer Learning" - Yosinski et al. 2014

### Online:
- 3Blue1Brown: "Neural Networks" (série no YouTube)
- Stanford CS231n: CNN for Visual Recognition

---

## Saídas Esperadas

✅ **6 notebooks completos** (08-13)
✅ **Código educacional** (implementações em NumPy)
✅ **Gráficos teóricos** (funções ativação, gradientes, etc)
✅ **Análise datasets** (estatísticas dos dados públicos)
✅ **Documento Fase 4** (resumo teórico)

---

## Próximas Fases (após Fase 4)

**Fase 5:** Documento final 2-4 páginas
**Fase 6:** Slides + Roteiro apresentação 15+ min

---

**Status:** ⏳ Pronto para iniciar
**Foco:** Teoria + Prática teórica (datasets internet)
**Sem:** Coleta em campo
