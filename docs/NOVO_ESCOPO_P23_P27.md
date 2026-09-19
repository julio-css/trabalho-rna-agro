# Trabalho de Redes Neurais Artificiais - UEL 2026
## Novo Escopo: Perguntas 23 e 27

**Perguntas a Responder:**
- **P23:** Como erros nos dados afetam o aprendizado?
- **P27:** Como redes neurais artificiais se inspiram no cérebro?

**Aplicação:** Diagnóstico de doenças em plantas (Soja, Milho, Café - Londrina/PR)

---

## NOVA ESTRUTURA DO PROJETO

### Fase 1: Fundamentos Biológicos (P27)
- Como o cérebro funciona
- Neurônios biológicos vs artificiais
- Sinapses, potencial de ação, aprendizado

### Fase 2: Inspiração em Redes Neurais (P27)
- MLP inspirado no cérebro
- Aprendizado por experiência
- Plasticidade sináptica = Ajuste de pesos

### Fase 3: Erros nos Dados (P23)
- Ruído de rótulo
- Ruído de imagem
- Desbalanceamento
- Viés de domínio

### Fase 4: Aplicação Prática
- Diagnóstico de doenças em plantas
- Comparação MLP vs CNN
- Interpretabilidade

### Fase 5: Documento + Apresentação
- Texto 2-4 páginas
- Slides + Roteiro 15+ min

---

## NOVOS NOTEBOOKS (Reorganizados)

```
notebooks/

FASE 1-2 (Biologia + Inspiração Neural):
├── 01_brain_fundamentals.ipynb          (Como o cérebro funciona)
├── 02_biological_vs_artificial.ipynb    (Neurônios: bio vs IA)
├── 03_neural_networks_inspiration.ipynb (Como RNA se inspira no cérebro)
│
FASE 3 (Erros nos Dados):
├── 04_label_noise_effects.ipynb         (Ruído de rótulo)
├── 05_image_noise_robustness.ipynb      (Ruído de imagem)
├── 06_class_imbalance.ipynb             (Desbalanceamento)
├── 07_domain_bias.ipynb                 (Viés de domínio)
│
FASE 4 (Aplicação):
├── 08_plant_disease_detection.ipynb     (MLP vs CNN para plantas)
├── 09_interpretability_grad_cam.ipynb   (Explicabilidade)
│
SUPORTE:
├── 10_datasets_analysis.ipynb           (Análise PlantDoc, BRACOL, RoCoLe)
└── 11_agriculture_precision.ipynb       (Aplicação prática)
```

---

## REORGANIZAÇÃO DE NOTEBOOKS EXISTENTES

**Manter (foram criados para P23):**
- 04_noise_robustness.ipynb → 04-07 (reorganizar)
- 05_interpretability.ipynb → 09_interpretability
- 06_agriculture_precision.ipynb → 11_agriculture_precision

**Criar (P27 - Cérebro e Inspiração):**
- 01_brain_fundamentals.ipynb (NOVO)
- 02_biological_vs_artificial.ipynb (NOVO)
- 03_neural_networks_inspiration.ipynb (NOVO)

**Remover (não se encaixam):**
- 08_mlp_fundamentals.ipynb (revisar se vale manter como suporte)

---

## CRONOGRAMA FASE 4 (Reorganização)

### Semana 1 (19-25 set):
- [ ] Criar Notebook 01: Brain Fundamentals
- [ ] Criar Notebook 02: Biological vs Artificial
- [ ] Criar Notebook 03: Neural Networks Inspiration

### Semana 2 (26 set - 2 out):
- [ ] Reorganizar 04-07: Erros nos dados (P23)
- [ ] Criar 08: Plant disease + MLP vs CNN
- [ ] Validar 09-11

### Semana 3 (3-9 out):
- [ ] Síntese e análise
- [ ] Preparar documento final
- [ ] Slides + roteiro

---

## PERGUNTAS E RESPOSTAS ESPERADAS

### P27: Como redes neurais se inspiram no cérebro?

**Resposta esperada:**
1. O cérebro tem ~86 bilhões de neurônios
2. Cada neurônio conecta a ~7.000 outros
3. Aprendizado ocorre através de ajustes nas sinapses (pesos)
4. RNA artificial simula esse processo:
   - Neurônio bio → Neurônio artificial
   - Sinapse → Peso (w)
   - Aprendizado → Backpropagation

**Analogias para plantas:**
- Cérebro detecta informações complexas
- RNA detecta padrões em imagens de plantas
- Ambos aprendem com experiência

### P23: Como erros nos dados afetam o aprendizado?

**Resposta esperada:**
1. Rótulos errados (-50% acurácia com 30% erro)
2. Ruído de imagem (gaussiano é pior: -17%)
3. Desbalanceamento (recall 88% → 15%)
4. Viés de domínio (lab→campo: -34%)
5. Conclusão: Dados bons > Modelo sofisticado

**Implicação para plantas:**
- Anotações precisas são críticas
- Dados de campo desde o início
- Não pode ignorar doenças raras

---

## ESTRUTURA FINAL DE ENTREGA

```
docs/
├── PROJETO.md                     (2-4 páginas)
├── APRESENTACAO_ROTEIRO.md        (Roteiro 15+ min)
├── AI_USAGE.md                    (Declaração IA)
├── NOVO_P23_ERROS_DADOS.md        (Análise P23)
├── NOVO_P27_CEREBRO.md            (Análise P27)
└── FASE_4_NOVA_ESTRUTURA.md       (Este documento)

notebooks/ (11 total)
├── 01-03: P27 (Cérebro e Inspiração)
├── 04-07: P23 (Erros nos dados)
├── 08-11: Aplicação (Plantas + Interpretabilidade)

results/
└── plots/ (20+ gráficos)
```

---

## PRÓXIMAS AÇÕES

1. **HOJE (19 set):**
   - [ ] Deletar notebook 08_mlp_fundamentals
   - [ ] Criar Notebook 01: Brain Fundamentals
   - [ ] Fazer commit da nova estrutura

2. **Próxima semana:**
   - [ ] Notebooks 02-03 (P27)
   - [ ] Reorganizar 04-07 (P23)
   - [ ] Integração

3. **Semana 3:**
   - [ ] Documento + Slides
   - [ ] Apresentação

---

**Status:** ⏳ Pronto para refazer tudo com novo escopo

