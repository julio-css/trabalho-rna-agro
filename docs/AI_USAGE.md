# AI_USAGE.md

## Declaração de Uso de Ferramentas Generativas

Este documento declara todos os usos de inteligência artificial generativa (LLMs, modelos de visão, etc.) no projeto "Diagnóstico de Doenças em Culturas com Redes Neurais Artificiais".

**Projeto:** Trabalho de Redes Neurais Artificiais - UEL  
**Data:** 19 de setembro de 2026  
**Grupo:** [Nomes dos integrantes — preencher]

---

## Política do Projeto

**REGRA:** Toda ferramenta generativa deve ser **explicitamente declarada**. Não há uso de IA oculto.

- ✅ **Uso permitido:** Auxílio em pesquisa, geração de código boilerplate, explicação de conceitos, debugging
- ❌ **Uso proibido:** Inventar resultados, métricas ou referências fictícias; plagiar análises; esconder uso de IA

---

## Usos Declarados

### Fase 1: Levantamento e Validação de Datasets

| Tarefa | Ferramenta | O que foi feito | Verificação |
|--------|-----------|-----------------|-------------|
| Pesquisa de datasets públicos | Claude (Anthropic) | Pesquisou e validou existência de PlantDoc, BRACOL, RoCoLe, Digipathos, JMuBEN em repositórios reais (GitHub, Mendeley, arXiv) | ✅ Todos os links verificados manualmente |
| Estrutura do repositório | Claude | Propôs estrutura de pastas e arquivos | ✅ Baseado em boas práticas (não inventado) |
| Redação de documentação | Claude | Escreveu README.md, data/README.md, requirements.txt | ✅ Revisado para precisão e completude |

### Fase 2: Pipeline de Dados + Baseline (EM ANDAMENTO)

| Tarefa | Ferramenta | O que será feito | Status |
|--------|-----------|------------------|--------|
| Implementação de data loaders | Claude | Escrever código PyTorch para carregar PlantDoc, BRACOL, RoCoLe | Pendente |
| Implementação MLP | Claude | Código base para MLP com PyTorch | Pendente |
| Implementação CNN (transfer learning) | Claude | Código base para MobileNetV2 fine-tuning | Pendente |
| Testes e debugging | Claude | Ajudar com erros durante treinamento | Pendente |

### Fase 3: Experimentos de Robustez (PLANEJADO)

| Tarefa | Ferramenta | O que será feito | Status |
|--------|-----------|------------------|--------|
| Simulação de ruído | Claude | Código para adicionar ruído, desfoque, JPEG comprimido | Planejado |
| Análise de resultados | Claude | Interpretação de gráficos e tendências | Planejado |

### Fase 4: Interpretabilidade (PLANEJADO)

| Tarefa | Ferramenta | O que será feito | Status |
|--------|-----------|------------------|--------|
| Implementação de Grad-CAM | Claude | Código de Grad-CAM para visualizar regiões de interesse | Planejado |
| Saliência e oclusão | Claude | Implementar mapas de saliência e testes de oclusão | Planejado |

### Fase 5: Agricultura de Precisão (PLANEJADO)

| Tarefa | Ferramenta | O que será feito | Status |
|--------|-----------|------------------|--------|
| Redação e análise | Claude | Escrever sobre pipeline de campo, benefícios e limitações | Planejado |
| Prototipagem | Claude | Sugerir interface simples (ex: upload de imagem + diagnóstico) | Planejado |

### Fase 6: Documento e Apresentação (PLANEJADO)

| Tarefa | Ferramenta | O que será feito | Status |
|--------|-----------|------------------|--------|
| Estrutura do documento | Claude | Organizar seções, fluxo lógico | Planejado |
| Roteiro de apresentação | Claude | Estruturar apresentação de 15+ minutos | Planejado |

---

## O QUE NÃO FOI FEITO COM IA

- ❌ Resultados de experimentos (obtidos de código real que roda)
- ❌ Métricas (números vêm de notebooks executados)
- ❌ Referências fictícias (todas as citações são reais e verificáveis)
- ❌ Imagens (todas vêm dos datasets públicos)
- ❌ Análises críticas (análises são do grupo, IA só ajuda estrutura)

---

## Transparência: Como o Grupo Usou IA

1. **Pesquisa de datasets:** IA ajudou a pesquisar repositórios, mas o grupo verificou cada link
2. **Documentação:** IA redigiu estrutura, grupo revisou para correção
3. **Código boilerplate:** IA escreveu templates, grupo adaptou para o projeto
4. **Debugging:** IA sugeriu correções de erros, grupo testou e validou

**Filosofia:** IA é uma ferramenta, não um substituto. Todo resultado importante é verificado pelo grupo.

---

## Compromissos Futuros

- [ ] Fase 2: Registrar novo uso conforme surgirem
- [ ] Fase 3: Atualizar esta tabela
- [ ] Fase 4: Idem
- [ ] Fase 5: Idem
- [ ] Fase 6: Assinado e completo

---

## Assinatura do Grupo

**Declaramos que:**
1. Todo uso de ferramenta generativa foi explicitamente listado acima
2. Nenhum resultado foi inventado
3. Todas as referências são reais e verificáveis
4. O código escrito com ajuda de IA foi testado pelo grupo

| Membro | Assinatura | Data |
|--------|-----------|------|
| [Nome 1] | _________ | _____ |
| [Nome 2] | _________ | _____ |
| [Nome 3] | _________ | _____ |
| [Nome 4] | _________ | _____ |

---

**Última atualização:** 19 de setembro de 2026

**Próxima revisão:** Ao final de cada fase
