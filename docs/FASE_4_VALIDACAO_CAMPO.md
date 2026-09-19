# Fase 4: Validação em Campo
## Planejamento e Execução

**Objetivo:** Validar que os modelos (MLP e CNN) funcionam em condições reais de campo antes de deployment.

**Data de Início:** 19 de setembro de 2026  
**Duração Estimada:** 2-3 semanas  
**Local:** Propriedades agrícolas em Londrina/PR

---

## 1. Planejamento da Coleta de Dados

### 1.1 Estrutura de Amostragem

```
PROPRIEDADES ALVO: 5-10 propriedades em Londrina/PR
├── Soja: 3 propriedades
├── Milho: 2 propriedades
├── Café: 2 propriedades
└── Mista (soja + milho): 1-2 propriedades

IMAGENS POR PROPRIEDADE:
├── Saudável: 30-50 imagens
├── Doença leve: 20-30 imagens
├── Doença moderada: 20-30 imagens
├── Doença severa: 10-20 imagens
└── Total por propriedade: 80-130 imagens

TOTAL ESPERADO: 400-1.300 imagens reais de campo
```

### 1.2 Protocolo de Coleta

**Equipamento:**
- [ ] Smartphone com câmera ≥12MP
- [ ] Tripé ou suporte para estabilidade
- [ ] App de foto com metadados (GPS, hora, direção)
- [ ] Caderno para anotações (backup)

**Procedimento por Imagem:**
1. Identificar folha/fruto com doença ou saudável
2. Tirar 3-5 fotos do mesmo alvo (ângulos diferentes)
3. Registrar:
   - Localização GPS (propriedade, talhão)
   - Hora da foto
   - Severidade (0=saudável, 1=leve, 2=moderada, 3=severa)
   - Anotação de agrônomo (nome da doença, observações)
4. Carregar no sistema

**Validação em Campo:**
- Cada imagem validada por 2 pessoas (agrônomo + técnico)
- Se houver discordância, terceira pessoa decide
- Garantir mínimo 90% de concordância

### 1.3 Cronograma de Coleta

```
SEMANA 1 (19-25 set):
├── Dia 1-2: Contato com proprietários + planejamento
├── Dia 3-4: Coleta propriedade 1 (soja) - 100 imagens
└── Dia 5: Coleta propriedade 2 (milho) - 100 imagens

SEMANA 2 (26 set - 2 out):
├── Dia 1-2: Coleta propriedade 3 (café) - 100 imagens
├── Dia 3-4: Coleta propriedade 4 (soja) - 100 imagens
└── Dia 5: Processamento/backup de dados

SEMANA 3 (3-9 out):
├── Dia 1-2: Coleta propriedade 5 (mista) - 100 imagens
├── Dia 3-4: Validação de anotações
└── Dia 5: Análise preliminar + correções
```

---

## 2. Processamento de Dados

### 2.1 Pipeline de Processamento

```python
FOR EACH imagem_coletada:
    1. Validar arquivo (não corrompido)
    2. Extrair metadados (GPS, hora, câmera)
    3. Redimensionar para 224x224 (CNN) e 64x64 (MLP)
    4. Verificar rótulo (agrônomo anotou corretamente?)
    5. Separar em treino/validação/teste (70/15/15)
    6. Salvar com rastreabilidade (origem, data, GPS)
```

### 2.2 Estrutura de Armazenamento

```
data/campo_2026/
├── raw/                           # Imagens originais (com metadados)
│   ├── propriedade_001_soja/
│   │   ├── 20260920_113045_soja_saudavel_001.jpg
│   │   ├── 20260920_113045_soja_saudavel_001.json  (metadados)
│   │   └── ...
│   └── propriedade_002_milho/
├── processed/                     # Redimensionadas + normalizadas
│   ├── train/
│   ├── val/
│   └── test/
└── metadata.csv                   # Índice de todas as imagens
```

### 2.3 Validação de Qualidade

**Critérios de Rejeição:**
- [ ] Imagem borrada/fora de foco
- [ ] Folha não visível claramente
- [ ] Artefatos muito óbvios (etiqueta, marca)
- [ ] Rótulo inconsistente com 2 validadores
- [ ] Exposição extrema (muito escura ou muito clara)

**Taxa de Rejeição Aceitável:** <10% (95% aceitação mínima)

---

## 3. Validação em Campo vs Modelo

### 3.1 Protocolo de Validação

Para cada imagem coletada:

```
1. AGRÔNOMO EXPERT valida em campo
   └─ Diagnóstico: [classe verdadeira]
   └─ Confiança: [0-100%]
   └─ Observações: [notas adicionais]

2. MODELO faz predição
   └─ Classe predita: [predição]
   └─ Confiança: [0-100%]
   └─ Grad-CAM: [visualização do raciocínio]

3. COMPARAÇÃO
   └─ Acerto? SIM/NÃO
   └─ Se NÃO, por quê?
      ├─ Confusão com doença similar
      ├─ Lesão muito leve (modelo não vê)
      ├─ Qualidade de imagem ruim
      └─ Modelo genuinamente errado
```

### 3.2 Métricas a Calcular

**Por Classe:**
- Acurácia (TP+TN)/(Total)
- Precisão (TP)/(TP+FP)
- Recall (TP)/(TP+FN)
- F1-Score

**Global:**
- Acurácia geral
- Matriz de confusão
- Curva ROC/AUC

**Degradação:**
- Comparar acurácia notebook vs campo
- Esperado: ~10-15% de queda é normal

### 3.3 Análise de Erros

```
POR CADA ERRO DO MODELO:
├─ Tipo 1: Confundiu com doença similar
│  └─ Ação: Adicionar mais dados dessa confusão ao treino
├─ Tipo 2: Lesão muito leve (modelo não viu)
│  └─ Ação: Coletar mais lesões leves
├─ Tipo 3: Qualidade de imagem ruim
│  └─ Ação: Orientação melhor para agrônomo (técnica foto)
└─ Tipo 4: Modelo genuinamente errado
   └─ Ação: Aumentar complexidade do modelo ou dados
```

---

## 4. Experimentos Adicionais em Campo

### 4.1 Robustez a Variações

**Teste 1: Iluminação**
- [ ] Fotos em sol pleno
- [ ] Fotos em sombra
- [ ] Fotos em dia nublado
- [ ] Comparar acurácia: modelo varia com iluminação?

**Teste 2: Ângulo de Foto**
- [ ] Perpendicular à folha
- [ ] 45°
- [ ] 30°
- [ ] Qual ângulo modelo prefere?

**Teste 3: Parte da Folha**
- [ ] Lesão no centro
- [ ] Lesão na borda
- [ ] Lesão na ponta
- [ ] Modelo detecta em todas as posições?

**Teste 4: Severidade**
- [ ] Lesão mínima (~1% de cobertura)
- [ ] Lesão leve (~5-10%)
- [ ] Lesão moderada (~20-30%)
- [ ] Lesão severa (>50%)
- [ ] Qual é o limiar de detecção?

### 4.2 Comparação MLP vs CNN

```
MÉTRICA           | MLP    | CNN    | Esperado
Acurácia geral    | ?      | ?      | CNN +3-5%
Tempo/imagem      | ?      | ?      | CNN ~1s vs MLP ~0.5s
Interpretável?    | Não    | Sim    | Grad-CAM mostra CNN melhor
Robustez luz      | ?      | ?      | CNN melhor
Robustez ângulo   | ?      | ?      | CNN melhor
Tamanho modelo    | 1MB    | 50MB   | Trade-off: acurácia vs tamanho
```

---

## 5. Saídas Esperadas

### 5.1 Relatório de Validação

Documento técnico incluindo:
- [ ] Resumo dos dados coletados (quantidade, distribuição)
- [ ] Taxa de aceitação das imagens
- [ ] Métricas por classe (tabela)
- [ ] Matriz de confusão
- [ ] Curvas de desempenho (ROC, etc)
- [ ] Análise de erros (top 10 confusões)
- [ ] Grad-CAM em exemplos reais
- [ ] Recomendações para melhoria

### 5.2 Dataset Validado em Campo

- [ ] 400-1.300 imagens reais de campo
- [ ] Anotações validadas (2+ validadores)
- [ ] Metadados completos (GPS, hora, propriedade)
- [ ] Splits treino/val/teste com garant. sem vazamento
- [ ] Pronto para retreinamento

### 5.3 Modelos Recalibrados

- [ ] MLP retreinado com dados de campo
- [ ] CNN retreinado com dados de campo
- [ ] Acurácia esperada: +2-5% de melhoria vs baseline

### 5.4 Documentação de Processo

- [ ] Protocolo de coleta (replicável)
- [ ] Lições aprendidas
- [ ] Recomendações para próxima safra
- [ ] Script de processamento de imagens

---

## 6. Recursos Necessários

### 6.1 Equipe

```
├─ 1 Engenheiro/Desenvolvedor (você!)
│  └─ Responsável por processamento + modelos
├─ 1-2 Agrônomos (validação em campo)
│  └─ Diagnóstico correto de doenças
├─ 1 Técnico de campo (coleta de imagens)
│  └─ Tirar fotos com protocolo
└─ 1 Gerenciador de dados (backup + validação)
   └─ Garantir integridade dos dados
```

### 6.2 Equipamento

```
✅ Smartphone com câmera ≥12MP
✅ Tripé ou suporte
✅ App de fotos com GPS/hora
✅ Armazenamento (externa 2TB)
✅ Notebook para processamento
✅ GitHub para versionamento
```

### 6.3 Custo Estimado

| Item | Quantidade | Custo |
|------|-----------|-------|
| Smartphone | 1 | R$ 1.500 |
| Tripé | 1 | R$ 200 |
| SSD 2TB | 1 | R$ 600 |
| Hora agrônomo (40h) | 40 | R$ 2.000 |
| Hora técnico (40h) | 40 | R$ 1.500 |
| Combustível | - | R$ 500 |
| **TOTAL** | - | **R$ 6.300** |

---

## 7. Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|------|--------------|--------|-----------|
| Proprietário nega acesso | Média | Alto | Contatar antecipadamente, oferecer relatório gratuito |
| Doença não aparece em safra | Média | Alto | Ter plano B (propriedades alternativas) |
| Dados perdidos | Baixa | Crítico | Backup duplo + nuvem |
| Discordância validadores | Alta | Médio | 3º validador (agrônomo expert) |
| Imagens de qualidade ruim | Média | Médio | Treinamento técnico de foto |
| Tempo insuficiente | Média | Médio | Coletar dados paralelamente com desenvolvimento |

---

## 8. Próximos Passos Imediatos

### Hoje (19 set):
- [ ] Criar script de processamento de imagens
- [ ] Planejar coleta (listar propriedades)
- [ ] Contatar proprietários

### Semana 1:
- [ ] Iniciar coleta de dados
- [ ] Validar protocolo em 1ª propriedade
- [ ] Fazer ajustes se necessário

### Semana 2-3:
- [ ] Continuar coleta
- [ ] Processar imagens conforme chegam
- [ ] Validação com agrônomo

### Fim da Fase 4:
- [ ] Dataset validado pronto
- [ ] Relatório de validação completo
- [ ] Modelos retreinados
- [ ] Pronto para Fase 5 (App Mobile)

---

## 9. Checklist de Validação

### Antes de Começar Coleta:
- [ ] Protocolo definido e testado
- [ ] Equipamento funcionando
- [ ] Propriedades confirmadas
- [ ] Agrônomo disponível para validação
- [ ] Armazenamento preparado

### Durante Coleta:
- [ ] Metadados sendo capturados
- [ ] Anotações sendo validadas
- [ ] Backup sendo feito
- [ ] Qualidade de imagens monitorada

### Fim da Coleta:
- [ ] 400+ imagens coletadas
- [ ] 95%+ taxa de aceitação
- [ ] Anotações 90%+ concordância
- [ ] Backup verificado
- [ ] Dataset pronto para processamento

### Análise Final:
- [ ] Métricas calculadas
- [ ] Comparação modelo vs agrônomo documentada
- [ ] Erros analisados
- [ ] Recomendações definidas

---

**Responsável:** Equipe de Desenvolvimento  
**Revisão:** Agrônomo Expert + Orientador  
**Status:** ⏳ Pronto para Iniciar
