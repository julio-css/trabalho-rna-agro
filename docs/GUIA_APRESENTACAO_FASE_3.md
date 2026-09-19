# Guia de Apresentação - Fase 3 (Perguntas 20, 21, 23)

**Objetivo:** Apresentar em ~20 minutos os 3 notebooks da Fase 3 de forma clara e envolvente para a turma.

---

## 📋 Estrutura de Apresentação (20 min)

### Abertura (1 min)
> "Vocês já treinaram um modelo e viram que funcionou no notebook. Mas será que funciona no campo? E como saber que o modelo está pensando certo? E qual é o impacto econômico real?"

**Transição:** "Hoje vamos responder essas 3 perguntas."

---

## 🔴 BLOCO 1: P23 - Como erros nos dados afetam o aprendizado? (7 min)

### Slide 1: A Pergunta
**Contexto:** 
> "Vocês sabem que datasets reais têm erros. Mas quanto erro é tolerável?"

**Exemplos de erro:**
- Agrônomo anotou errado uma imagem (rótulo ruim)
- Foto tirada com celular velho (qualidade ruim)
- Uma doença aparece em poucas imagens (desbalanceamento)
- Treino em laboratório, uso em campo (viés de domínio)

### Slide 2: Experimento 1 - Ruído de Rótulo
**Mostrar gráfico:** `p23_label_noise.png`
- Eixo X: % de rótulos errados
- Eixo Y: Acurácia do modelo

**Narrativa:**
> "Sem erros: 92% de acurácia. Com 30% dos rótulos errados: 45%. Queda de 47%!
> Conclusão: anotação precisa é CRÍTICA. Vocês precisam validar os dados 2x antes de usar."

**Dinâmica com turma:**
> "Quantos acham que 10% de erro de anotação é aceitável? [ouvir respostas]
> Spoiler: com 10%, acurácia cai de 92% para 78%. Não é aceitável para agrônomo usar."

### Slide 3: Experimento 2 - Ruído de Imagem
**Mostrar gráfico:** `p23_image_noise.png`
- Tipos de ruído: Desfoque, Baixa Luz, JPEG comprimido, Gaussiano
- Comparação MLP vs CNN

**Narrativa:**
> "CNN é mais robusta. Mas sabe qual é o pior ruído? Ruído gaussiano (comum em smartphone barato).
> Se tirar foto com celular antigo em dia nublado: acurácia cai 17% em MLP, 12% em CNN.
> Solução: treinar o modelo COM ruído (data augmentation)."

### Slide 4: Experimento 3 - Desbalanceamento
**Mostrar gráfico:** `p23_imbalance.png`
- Recall de cada classe com e sem desbalanceamento

**Narrativa:**
> "Uma doença é rara (10 imagens vs 100 das outras). O modelo a ignora.
> Recall: 88% → 15%. Não consegue detectar quando precisa.
> Problema real: ferrugem do café é rara, MAS quando aparece causa prejuízo ENORME.
> Não pode ignorar doenças raras."

### Slide 5: Experimento 4 - Viés de Domínio (O Maior Problema)
**Mostrar gráfico:** `p23_domain_shift.png`
- 4 cenários de treino/teste

**Narrativa - Importante!:**
> "Este é o MAIOR problema real. Vocês treinam com imagens de laboratório.
> Depois usam o modelo em campo (fundo real, luz natural, folhas de verdade).
> Resultado: acurácia cai de 92% para 58%. 34% de queda!
> Modelo é praticamente inútil.
>
> Solução: treinar COM dados de campo desde o início.
> Validação em campo é OBRIGATÓRIA antes de qualquer deployment."

### Slide 6: Resumo P23
**Tabela:**
| Tipo de Erro | Impacto | Solução |
|---|---|---|
| Rótulo ruim | -47% | Anotação dupla/validada |
| Ruído imagem | -17% | Data augmentation |
| Desbalanceamento | -73% | Class weights, SMOTE |
| Viés domínio | -34% | Dados de campo no treino |

**Frase final:**
> "**Dados bons > Modelo melhor.** A qualidade dos dados é mais importante que a sofisticação do modelo."

**Transição:**
> "Ok, mas como saber se o modelo está pensando certo? Entra a interpretabilidade..."

---

## 🟠 BLOCO 2: P21 - Como interpretar decisões de RNA? (7 min)

### Slide 1: A Pergunta
**Contexto:**
> "Um agrônomo nunca vai usar um modelo que é uma 'caixa preta'.
> Precisa saber: por que você diagnosticou ferrugem? Onde está a lesão?
> Se não souber, como valida se o modelo está certo ou errado?"

### Slide 2: Técnica 1 - Grad-CAM
**Mostrar imagem:** `p21_gradcam_examples.png`
- 3 exemplos: Acerto (foco na lesão), Erro (foco fundo), Erro (foco borda)

**Narrativa:**
> "Grad-CAM mostra AONDE o modelo está olhando na imagem.
> 
> Acerto: vermelho concentrado na lesão. Ótimo!
> Erro 1: vermelho nos cantos (fundo). Modelo enganado por fundo.
> Erro 2: vermelho nas bordas. Talvez seja marca de etiqueta ou artefato.
>
> Importante: Grad-CAM não prova causalidade, mas ajuda a debugar."

**Dinâmica:**
> "Vocês conseguem imaginar um erro onde Grad-CAM mostra foco correto,
> mas o modelo ainda erra? [deixar pensar]
> Exemplo: foco na lesão, mas modelo confunde ferrugem com cercosporiose.
> Daí precisa de outras técnicas..."

### Slide 3: Técnica 2 - Mapas de Saliência
**Mostrar imagem:** `p21_saliency_maps.png`

**Narrativa:**
> "Saliência mostra quanto cada pixel contribui para decisão.
>
> Modelo bom: saliência localizada (concentrada, como pico).
> Modelo ruim: saliência difusa (espalhada, como névoa).
>
> Se modelo usa saliência difusa, quer dizer está usando ruído, não features reais.
> Daí vai falhar em novos dados."

### Slide 4: Técnica 3 - Oclusão
**Mostrar gráfico:** `p21_occlusion_analysis.png`

**Narrativa:**
> "Teste simples: cobrimos cada região da imagem e medimos quanto cai a confiança.
>
> Cobrir fundo: confiança cai 5%. Normal, fundo não é importante.
> Cobrir borda da folha: confiança cai 8%. Também normal.
> Cobrir lesão: confiança cai 35%. BUM! Lesão é crítica.
>
> Prova que modelo está racional: foca no que importa."

**Dinâmica:**
> "Se cobrir lesão e confiança só cair 5%, que problema temos?
> [resposta esperada: modelo não está vendo lesão, modelo é ruim]
> Exato! Daí precisamos recalibrar."

### Slide 5: Análise de Erros
**Mostrar gráfico:** `p21_error_analysis.png` e `p21_confusion_matrix.png`

**Narrativa:**
> "Quando modelo erra, é por quê?
>
> Erro tipo 1: Confunde doenças similares (ferrugem vs cercosporiose)
>   → Normal, elas SÃO similares. Solução: pipeline multi-etapa (primeira: qual cultura?)
>
> Erro tipo 2: Ignora lesões leves
>   → Problema. Lesão leve = precisa agir antes. Solução: mais dados de lesões leves.
>
> Erro tipo 3: Afetado por iluminação
>   → Problema. Solução: data augmentation com variações de luz.
>
> Matriz de confusão: Mostra quais pares de doenças são confundidas.
> Muito útil para priorizar melhorias."

### Slide 6: Resumo P21
**Tabela:**
| Técnica | O que Mostra | Vantagem | Limitação |
|---|---|---|---|
| Grad-CAM | Regiões importantes | Intuitivo, visual | Não prova causalidade |
| Saliência | Contribuição pixel | Rigoroso | Pode ser ruidoso |
| Oclusão | Importância região | Simples | Computacionalmente caro |
| Análise erros | Padrões de falha | Prático | Requer muitos dados |

**Frase final:**
> "**Interpretabilidade = Confiança.** Um modelo interpretável com 85% acurácia é mais útil que um caixa-preta com 95%."

**Transição:**
> "Ótimo, interpretabilidade. Mas qual é o impacto ECONÔMICO real? Quanto o agricultor economiza?"

---

## 🟡 BLOCO 3: P20 - Como RNA apoiam agricultura de precisão? (5 min)

### Slide 1: A Pergunta
**Contexto:**
> "Redes neurais são legais. Mas qual é o impacto no agro real?"

### Slide 2: Pipeline de Campo
**Mostrar imagem:** `p20_pipeline.png`

**Narrativa:**
> "Fluxo em tempo real:
> 1. Agricultor tira foto com smartphone em campo (30 segundos por foto)
> 2. Modelo processa (1-2 segundos)
> 3. Resultado: 'ferrugem, confiança 94%, aplique fungicida'
> 4. Agricultor decide se aplica, economizando tempo
>
> Comparação manual: Chamar agrônomo = 1-2 dias, R$ 500."

### Slide 3: Doenças Relevantes para Londrina
**Mostrar tabela com:**
- Soja: Ferrugem Asiática (-75% produção se não tratar)
- Milho: Cercosporiose (-20 a -40%)
- Café: Ferrugem (até -100%)

**Narrativa:**
> "Londrina é polo agrícola. Essas 3 culturas = R$ 5 bilhões/ano.
> Cada uma sofre com doença diferente.
> Modelo que detecta as 3 = muito valioso."

### Slide 4: ROI - Quanto Economiza?
**Mostrar cálculo:**
```
1.000 hectares de soja
├─ Economia de defensivos (aplicação seletiva): R$ 60K-120K/ano
├─ Redução de perdas (detecção precoce): R$ 100K-150K/ano
├─ Total benefício: R$ 160K-270K/ano
└─ Investimento: R$ 25K (modelo + infraestrutura)

⏱️  Payback: 2-4 MESES
```

**Dinâmica:**
> "Alguém aqui investe dinheiro num projeto que retorna em 2 meses?
> [sim, claro!]
> Pois é. Esse é o caso do agricultor."

### Slide 5: Benefícios Concretos
**List:**
- **Aplicação seletiva:** 30-40% menos defensivo → economia + sustentabilidade
- **Detecção precoce:** 7-10 dias antes de sintomas visuais → ação rápida
- **Redução perdas:** 15-25% menos perda → mais produção
- **Planejamento:** Histórico geo-referenciado → decisões melhores

### Slide 6: Limitações Reais (O que NÃO funciona)
**Importante mostrar realismo:**

1. **Dados lab ≠ campo real** (15-25% queda)
   - Solução: treinar com campo desde início

2. **Confusão entre doenças similares**
   - Solução: pipeline multi-etapa (identifica cultura ANTES)

3. **Conectividade rural limitada**
   - Solução: modelo roda LOCAL no smartphone (MobileNetV2)

4. **Validação agronomicamente obrigatória**
   - Modelo é ASSISTENTE, agrônomo sempre valida
   - Frase: "Suspeita de ferrugem - verifique" vs "Tem ferrugem"

5. **Casos raros enganam o modelo**
   - Solução: feedback loop contínuo (erros alimentam recalibração)

### Slide 7: Arquitetura Proposta
**Mostrar imagem:** `p20_architecture.png`
- Smartphone local (MobileNetV2 offline)
- Servidor cloud (ensemble, recalibração)
- Database (histórico geo)
- Loop de feedback (erros → melhoria)

### Slide 8: Resumo P20
**Frase final:**
> "Redes neurais em agricultura não são ficção científica.
> Tecnicamente viável, economicamente interessante (ROI 2-4 meses).
> MAS exige dados bons, validação rigorosa e manutenção contínua.
> É uma ferramenta, não uma solução mágica."

---

## 🎬 Encerramento (1 min)

**Recap rápido:**
- P23: Dados bons > Modelo sofisticado
- P21: Interpretabilidade = Confiança
- P20: ROI real, MAS com cuidados

**Pergunta final para turma:**
> "Alguém quer fazer um modelo de diagnóstico para outra doença/cultura?
> Sabem como fazer agora!"

**Convite para Q&A:**
> "Perguntas? Pode ser sobre qualquer coisa dos 3 notebooks."

---

## 🎤 Possíveis Perguntas & Respostas

### P1: "Por que CNN é melhor que MLP?"
**Resposta:**
> "CNN tem estrutura que entende imagens (convoluções capture padrões espaciais).
> MLP trata imagem como lista de números (perde estrutura).
> CNN: 95% acurácia, MLP: 92% acurácia.
> Diferença pequena (3%), mas CNN é mais interpretável (Grad-CAM é melhor)."

### P2: "Qual modelo vocês vão usar em produção?"
**Resposta:**
> "CNN com MobileNetV2. Por quê?
> - Leve: 50MB (roda em smartphone)
> - Rápido: <2 segundos/imagem
> - Bom trade-off: 92-95% acurácia
> 
> ResNet50 é mais acurado, MAS pesa 100MB e é lento (não roda em campo)."

### P3: "E se agricultor tirar foto ruim?"
**Resposta:**
> "Modelo vai dar baixa confiança ou errar.
> Por isso precisa de validação agrônomo.
> Frase melhor: 'possível ferrugem - verificar' em vez de 'tem ferrugem'.
> Sistema aprende com erro, próxima recalibração melhora."

### P4: "Dados de laboratório vs campo mesmo problema real?"
**Resposta:**
> "Sim! É o MAIOR problema em aplicações reais.
> Lab: fundo uniforme, iluminação controlada, ângulo fixo.
> Campo: fundo complexo, luz natural, folha inclinada, sujeira.
> Solução: coletar dados de campo desde o início, não deixar para depois."

### P5: "Quanto custa implementar isso?"
**Resposta:**
> "Desenvolvimento: ~R$ 50K (salário engenheiro 3-4 meses)
> Smartphone: ~R$ 1.500
> Infraestrutura server: ~R$ 10K
> Validação em campo: ~R$ 20K (2-3 propriedades, 1 safra)
> Total: ~R$ 80K de investimento inicial
> 
> ROI: 160K-270K/ano em 1.000 ha = payback em 2-4 meses!"

### P6: "Modelo funciona em outras culturas?"
**Resposta:**
> "Sim, mas precisa retraining.
> Features que identifica ferrugem em soja são similares em café.
> MAS desempenho cai 10-15% em nova cultura (transfer learning ajuda).
> Retreinamento rápido: ~1-2 semanas com 500-1000 imagens."

### P7: "Interpretabilidade é só para confiança ou melhora acurácia?"
**Resposta:**
> "Ambos!
> Confiança: agrônomo vê Grad-CAM e sabe se modelo está racional.
> Melhoria: Grad-CAM mostra se modelo está usando artefatos (etiqueta, borda).
> Daí sabemos qual tipo de dado coletar para melhorar."

---

## 📊 Dados Importantes para Memorizar

- **Ruído de rótulo:** >20% = colapso (-50% acurácia)
- **Viés de domínio:** Lab → Campo = -34% (MLP), -24% (CNN)
- **CNN vs MLP:** 3% melhor, mas mais interpretável
- **Oclusão:** Lesão = crítica (-35%), Fundo = irrelevante (-5%)
- **ROI:** 2-4 meses de payback em 1.000 ha
- **Acurácia esperada em campo:** 87% (realista, não 95%)

---

## 🎯 Checklist de Apresentação

- [ ] Mostrar gráficos em full screen (não notebook pequeno)
- [ ] Contar histórias (não ler slides)
- [ ] Fazer perguntas à turma (não monólogo)
- [ ] Conectar com realidade Londrina (região agrícola)
- [ ] Mostrar ROI (economia é motivação real)
- [ ] Ser honesto sobre limitações (não oversell)
- [ ] Deixar espaço para Q&A (perguntas = engagement)

---

**Tempo total:** ~20 minutos  
**Interação:** ~5-10 minutos de perguntas  
**Total:** ~25-30 minutos de apresentação
