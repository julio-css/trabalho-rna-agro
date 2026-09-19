# Fase 4: Execução - Coleta de Dados em Campo
## Plano de Ação Imediato (19 setembro - 9 outubro 2026)

**Objetivo:** Coletar 400-1.300 imagens reais de campo em propriedades de Londrina/PR

**Timeline:** 2-3 semanas

**Status:** ⏳ INICIANDO AGORA

---

## SEMANA 1 (19-25 de setembro)

### DIA 1-2 (Quinta-Sexta, 19-20 set)
**OBJETIVO:** Identificar e contatar propriedades

#### Tarefas:
- [ ] **Listar propriedades candidatas em Londrina:**
  ```
  SOJA:
    1. Propriedade A (Fazenda Exemplo, Londrina)
    2. Propriedade B (Região norte, ~100ha)
    3. Propriedade C (Região sul, ~150ha)
  
  MILHO:
    4. Propriedade D (Sorriso do agrônomo, ~80ha)
    5. Propriedade E (Fundo de vale, ~120ha)
  
  CAFÉ:
    6. Propriedade F (Café Robusta, ~50ha)
    7. Propriedade G (Café Arábica, ~30ha)
  
  MISTA:
    8. Propriedade H (Soja + Milho, ~200ha)
  ```

- [ ] **Criar template de contato:**
  ```
  Olá [Proprietário],
  
  Somos estudantes de Redes Neurais Artificiais da UEL.
  Estamos desenvolvendo um sistema de diagnóstico de doenças
  em plantas usando IA.
  
  Gostaríamos de coletar ~100 fotos de folhas/frutos em sua
  propriedade para validar nosso modelo.
  
  Benefício para você:
  - Relatório gratuito sobre saúde das culturas
  - Diagnóstico de possíveis doenças
  - Sem custos
  
  Duração: 1-2 dias
  
  Disponível? Qual melhor data?
  ```

- [ ] **Enviar emails/ligar para 8-10 propriedades**

- [ ] **Rastrear respostas em planilha:**
  | Propriedade | Contato | Data Resposta | Confirmado | Data Coleta |
  |---|---|---|---|---|
  | Prop A | João | 20/set | ✅ | 23/set |
  | Prop B | Maria | - | ⏳ | - |

#### Responsável: [NOME DO MEMBRO 1]
#### Deadline: Fim do dia 20 de setembro

---

### DIA 3-4 (Segunda-Terça, 23-24 set)
**OBJETIVO:** Validar protocolo em propriedade piloto + coletar primeira remessa

#### Tarefas:
- [ ] **Preparar kit de coleta:**
  ```
  CHECKLIST:
  ☐ Smartphone com câmera ≥12MP (bateria carregada)
  ☐ App de foto com metadados (Timestamp, GPS)
  ☐ Tripé/suporte para estabilidade
  ☐ Caderno + caneta (backup de anotações)
  ☐ Mochila/bolsa para transporte seguro
  ☐ Planilha de anotações impressa
  ☐ Álcool gel + luvas (higiene)
  ☐ Protetor solar + chapéu
  ☐ Garrafa de água
  ```

- [ ] **Imprimir protocolo de coleta:**
  ```
  PROTOCOLO DE COLETA - PROPRIEDADE PILOTO
  
  Propriedade: ________________
  Data: ____/____/______
  Técnico: ________________
  Agrônomo: ________________
  
  POR FOLHA/FRUTO:
  [ ] Nº da foto: ____
  [ ] Cultura: [ ] Soja [ ] Milho [ ] Café
  [ ] Localização GPS: ________________
  [ ] Hora: ____:____
  [ ] Condição: [ ] Saudável [ ] Doente
  [ ] Se doente - Severidade:
      [ ] Leve (1-5% de cobertura)
      [ ] Moderada (5-20%)
      [ ] Severa (>20%)
  [ ] Doença suspeita: ________________
  [ ] Observações: ________________
  [ ] Foto de ângulo 1 (perpendicular): ✓
  [ ] Foto de ângulo 2 (45°): ✓
  [ ] Foto de ângulo 3 (30°): ✓
  [ ] Validação agrônomo: ________________
  ```

- [ ] **Treinar técnico de coleta (30 min):**
  - Como usar o app de GPS/foto
  - Onde/como posicionar a folha
  - Como anotar corretamente
  - O que rejeitar (imagens ruins)

- [ ] **Coletar 100 imagens em Propriedade Piloto:**
  - ~30 saudáveis
  - ~30 doença leve
  - ~30 doença moderada
  - ~10 doença severa
  - Mínimo 3 ângulos por folha

- [ ] **Validação dupla (Agrônomo + Técnico):**
  - Concordância >90%
  - Se discordar, 3º validador decide
  - Documentar discordâncias

#### Responsável: [NOME DO MEMBRO 2]
#### Deadline: Fim do dia 24 de setembro

#### Saída esperada:
- 100 imagens + metadados
- Checklist de validação preenchido
- Feedback do protocolo

---

### DIA 5 (Quarta, 25 set)
**OBJETIVO:** Processar dados piloto + ajustar protocolo

#### Tarefas:
- [ ] **Fazer backup das 100 imagens:**
  ```bash
  # Em disco externo 2TB
  /backup/campo_2026/propriedade_piloto_100imgs/
  /backup/campo_2026/propriedade_piloto_100imgs_backup2/
  ```

- [ ] **Rodar script de validação:**
  ```bash
  python scripts/process_field_images.py
  # Input: data/campo_2026/raw/propriedade_piloto/
  # Output: relatório_piloto.json
  ```

- [ ] **Analisar relatório:**
  - Taxa de aceitação (esperado >95%)
  - Distribuição de classes
  - Problemas identificados

- [ ] **Reunião de ajustes:**
  - O que funcionou bem?
  - O que precisa melhorar?
  - Protocolo final aprovado?

- [ ] **Aprovar protocolo para próximas propriedades**

#### Responsável: [NOME DO MEMBRO 1 + 3]
#### Deadline: Fim do dia 25 de setembro

---

## SEMANA 2 (26 setembro - 2 outubro)

### DIA 1-2 (Quinta-Sexta, 26-27 set)
**OBJETIVO:** Coletar em Propriedade 2 (Soja)

#### Tarefas:
- [ ] Ir para propriedade 2
- [ ] Coletar 100 imagens (mesmo protocolo)
- [ ] Validação dupla
- [ ] Backup imediato

#### Responsável: [NOME DO MEMBRO 2]
#### Saída: 100 imagens + metadados

---

### DIA 3-4 (Segunda-Terça, 30 set - 1 out)
**OBJETIVO:** Coletar em Propriedade 3 (Milho) + Propriedade 4 (Milho)

#### Tarefas:
- [ ] Propriedade 3: 100 imagens
- [ ] Propriedade 4: 100 imagens
- [ ] Validação dupla ambas
- [ ] Backup

#### Responsável: [NOME DO MEMBRO 3]
#### Saída: 200 imagens + metadados

---

### DIA 5 (Quarta, 2 out)
**OBJETIVO:** Processamento intermediário

#### Tarefas:
- [ ] Rodar script em todas as imagens coletadas (300)
- [ ] Gerar estatísticas preliminares
- [ ] Identificar classes com poucos exemplos
- [ ] Ajustar próximas coletas se necessário

#### Responsável: [NOME DO MEMBRO 1]

---

## SEMANA 3 (3-9 outubro)

### DIA 1-2 (Quinta-Sexta, 3-4 out)
**OBJETIVO:** Coletar em Propriedade 5 (Café) + Propriedade 6 (Café)

#### Tarefas:
- [ ] Propriedade 5: 100 imagens
- [ ] Propriedade 6: 100 imagens
- [ ] Validação dupla ambas
- [ ] Backup

#### Responsável: [NOME DO MEMBRO 2 + 3]
#### Saída: 200 imagens + metadados

---

### DIA 3-4 (Segunda-Terça, 7-8 out)
**OBJETIVO:** Coletar em Propriedade 7 (Mista)

#### Tarefas:
- [ ] Coletar 100 imagens (mix soja + milho)
- [ ] Validação dupla
- [ ] Backup

#### Responsável: [NOME DO MEMBRO 1]
#### Saída: 100 imagens + metadados

---

### DIA 5 (Quarta, 9 out)
**OBJETIVO:** Finalizar coleta e processar todos os dados

#### Tarefas:
- [ ] Backup final de TODAS as imagens (2TB externo + nuvem)
- [ ] Rodar script de processamento completo
- [ ] Gerar relatório final de validação
- [ ] Validação de anotações discordantes
- [ ] Criar splits treino/validação/teste
- [ ] Preparar dados para Notebook 07

#### Responsável: [NOME DO MEMBRO 1]
#### Saída: Dataset completo pronto para análise

---

## ESTRUTURA DE DADOS ESPERADA

```
data/campo_2026/
├── raw/
│   ├── propriedade_piloto_soja/
│   │   ├── 20260923_110430_soja_saudavel_001.jpg
│   │   ├── 20260923_110430_soja_saudavel_001.json
│   │   ├── 20260923_110445_soja_ferrugem_002.jpg
│   │   ├── 20260923_110445_soja_ferrugem_002.json
│   │   └── ... (100 imagens)
│   ├── propriedade_2_soja/
│   │   └── ... (100 imagens)
│   ├── propriedade_3_milho/
│   │   └── ... (100 imagens)
│   └── ... (total 700 imagens)
│
├── processed/
│   ├── metadata_index.csv
│   ├── train/ (490 imagens)
│   ├── val/ (105 imagens)
│   └── test/ (105 imagens)
│
└── results/
    ├── validation_report.json
    ├── class_distribution.csv
    └── processing_log.txt
```

---

## FORMATO DO METADADO JSON

Cada imagem `.jpg` deve ter um arquivo `.json` correspondente:

```json
{
  "timestamp": "2026-09-23T11:04:30",
  "gps": {
    "latitude": -23.3045,
    "longitude": -51.1696,
    "accuracy_meters": 5
  },
  "camera": {
    "phone_model": "Samsung Galaxy A12",
    "resolution": "4000x3000",
    "iso": 400
  },
  "agronomist_label": "soja_ferrugem",
  "severity": 2,
  "property": "propriedade_piloto",
  "culture": "soja",
  "angle_degrees": 0,
  "lighting": "sunny",
  "validators": {
    "agronomist": "João Silva",
    "technician": "Maria Santos",
    "agreement": true
  },
  "notes": "Lesão típica de ferrugem asiática. Localizata em folha média.",
  "quality_check": {
    "focused": true,
    "leaf_visible": true,
    "artifacts": false,
    "accepted": true
  }
}
```

---

## CHECKLIST DIÁRIO

### Antes de sair para coleta:
- [ ] Smartphone 100% bateria
- [ ] App GPS funcionando
- [ ] Tripé testado
- [ ] Protocolo impresso
- [ ] Caderno + caneta
- [ ] Backup externo na mochila

### Durante coleta:
- [ ] Validação dupla sendo feita
- [ ] Fotos salvas com GPS
- [ ] Metadados sendo registrados
- [ ] Rejeições documentadas
- [ ] Ângulos múltiplos capturados

### Após coleta:
- [ ] Backup imediato em disco externo
- [ ] Backup em segundo local
- [ ] Planilha atualizada
- [ ] Email com progresso enviado

---

## MATRIZ DE RESPONSABILIDADES

| Tarefa | Membro 1 | Membro 2 | Membro 3 |
|--------|----------|----------|----------|
| Contatar proprietários | ✅ | - | - |
| Coleta Propriedade Piloto | - | ✅ | - |
| Processamento/Scripts | ✅ | - | - |
| Coleta Prop 2 (Soja) | - | ✅ | - |
| Coleta Prop 3-4 (Milho) | - | - | ✅ |
| Coleta Prop 5-6 (Café) | - | ✅ | ✅ |
| Coleta Prop 7 (Mista) | ✅ | - | - |
| Processamento Final | ✅ | - | - |
| Relatório | ✅ | - | - |
| Análise (Notebook 07) | ✅ | ✅ | ✅ |

---

## RISCOS E PLANOS B

### Risco 1: Proprietário cancela no último momento
- **Mitigação:** Manter 2-3 propriedades backup confirmadas
- **Plano B:** Contatar propriedade de backup imediatamente

### Risco 2: Doença não aparece na safra
- **Mitigação:** Escolher propriedades com histórico de doença
- **Plano B:** Coletar mesmo com doença leve/moderada (ajusta limiar)

### Risco 3: Dados perdidos/corrompidos
- **Mitigação:** Backup triplo (disco externo 1, disco externo 2, nuvem)
- **Plano B:** Recoletar em propriedade de backup

### Risco 4: Discordância validadores >10%
- **Mitigação:** Trazer agrônomo specialist como 3º validador
- **Plano B:** Aceitar maior discrepância (rejeição <5% das imagens)

### Risco 5: Falta de tempo
- **Mitigação:** Coletar em paralelo (2 técnicos simultâneos em propriedades diferentes)
- **Plano B:** Reduzir para 3-4 propriedades (600 imagens mínimo)

---

## SAÍDAS ESPERADAS AO FIM DE FASE 4

### Dados:
- ✅ 600-1.300 imagens reais de campo
- ✅ Anotações validadas (90%+ concordância)
- ✅ Metadados completos (GPS, hora, severidade, etc)
- ✅ Splits treino/validação/teste sem vazamento

### Análise:
- ✅ Notebook 07 executado com dados reais
- ✅ Comparação MLP vs CNN vs Agrônomo
- ✅ Degradação calculada (esperado <15%)
- ✅ Erros analisados

### Documentação:
- ✅ Relatório de coleta (metodologia, desafios, lições)
- ✅ Protocolo finalizado (replicável para próximas safras)
- ✅ Log de processamento com timestamps

### Próximos passos:
- ✅ Dataset pronto para retreinamento
- ✅ Decisão: MLP vs CNN para deployment?
- ✅ Plano para Fase 5 (App mobile) definido

---

## COMUNICAÇÃO E ATUALIZAÇÕES

### Reunião diária (5 min):
- Standup: O que fez ontem? O que faz hoje? Bloqueadores?
- Horário: 08:00 da manhã

### Relatório semanal:
- Dados coletados/processados
- Bloqueadores encontrados
- Ajustes no protocolo
- Próximas ações

### Grupo de comunicação:
- WhatsApp/Slack para updates rápidos
- Google Drive para planilhas compartilhadas
- GitHub para código e scripts

---

## PRÓXIMA ETAPA APÓS FASE 4

Assim que dados forem coletados e processados:

1. **Rodar Notebook 07** (validação comparativa)
2. **Analisar degradação** (esperado <15%)
3. **Retreinar modelos** com dados de campo
4. **Gerar relatório** de validação
5. **Apresentar resultados** para professor/orientador
6. **Decidir:** CNN para deployment ou continuar refinando?

---

**Status:** ⏳ PRONTO PARA INICIAR
**Primeira ação:** Contatar propriedades (hoje, 19 set)
**Timeline:** 19 set - 9 out (20 dias)
**Objetivo:** 600+ imagens validadas
