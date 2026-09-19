"""
planilha_rastreamento_fase4.py - Gerar planilha de rastreamento para Fase 4

Este script cria arquivos CSV para acompanhamento em tempo real da coleta de dados.
"""

import csv
from datetime import datetime
from pathlib import Path

def criar_planilha_propriedades():
    """Criar planilha de propriedades a contatar"""
    
    propriedades = [
        {
            "id": "PROP_001",
            "nome": "Propriedade A - Soja",
            "cultura": "Soja",
            "localizacao": "Londrina - Norte",
            "proprietario": "[NOME]",
            "telefone": "[TELEFONE]",
            "email": "[EMAIL]",
            "data_contato": "",
            "confirmado": "⏳",
            "data_coleta_planejada": "",
            "data_coleta_real": "",
            "imagens_coletadas": 0,
            "imagens_aceitas": 0,
            "taxa_aceitacao": "0%",
            "status": "⏳ Pendente contato",
            "observacoes": ""
        },
        {
            "id": "PROP_002",
            "nome": "Propriedade B - Soja",
            "cultura": "Soja",
            "localizacao": "Londrina - Sul",
            "proprietario": "[NOME]",
            "telefone": "[TELEFONE]",
            "email": "[EMAIL]",
            "data_contato": "",
            "confirmado": "⏳",
            "data_coleta_planejada": "",
            "data_coleta_real": "",
            "imagens_coletadas": 0,
            "imagens_aceitas": 0,
            "taxa_aceitacao": "0%",
            "status": "⏳ Pendente contato",
            "observacoes": ""
        },
        {
            "id": "PROP_003",
            "nome": "Propriedade C - Soja",
            "cultura": "Soja",
            "localizacao": "Londrina - Leste",
            "proprietario": "[NOME]",
            "telefone": "[TELEFONE]",
            "email": "[EMAIL]",
            "data_contato": "",
            "confirmado": "⏳",
            "data_coleta_planejada": "",
            "data_coleta_real": "",
            "imagens_coletadas": 0,
            "imagens_aceitas": 0,
            "taxa_aceitacao": "0%",
            "status": "⏳ Pendente contato",
            "observacoes": ""
        },
        {
            "id": "PROP_004",
            "nome": "Propriedade D - Milho",
            "cultura": "Milho",
            "localizacao": "Londrina - Oeste",
            "proprietario": "[NOME]",
            "telefone": "[TELEFONE]",
            "email": "[EMAIL]",
            "data_contato": "",
            "confirmado": "⏳",
            "data_coleta_planejada": "",
            "data_coleta_real": "",
            "imagens_coletadas": 0,
            "imagens_aceitas": 0,
            "taxa_aceitacao": "0%",
            "status": "⏳ Pendente contato",
            "observacoes": ""
        },
        {
            "id": "PROP_005",
            "nome": "Propriedade E - Milho",
            "cultura": "Milho",
            "localizacao": "Londrina - Centro",
            "proprietario": "[NOME]",
            "telefone": "[TELEFONE]",
            "email": "[EMAIL]",
            "data_contato": "",
            "confirmado": "⏳",
            "data_coleta_planejada": "",
            "data_coleta_real": "",
            "imagens_coletadas": 0,
            "imagens_aceitas": 0,
            "taxa_aceitacao": "0%",
            "status": "⏳ Pendente contato",
            "observacoes": ""
        },
        {
            "id": "PROP_006",
            "nome": "Propriedade F - Café Robusta",
            "cultura": "Café",
            "localizacao": "Londrina - Norte",
            "proprietario": "[NOME]",
            "telefone": "[TELEFONE]",
            "email": "[EMAIL]",
            "data_contato": "",
            "confirmado": "⏳",
            "data_coleta_planejada": "",
            "data_coleta_real": "",
            "imagens_coletadas": 0,
            "imagens_aceitas": 0,
            "taxa_aceitacao": "0%",
            "status": "⏳ Pendente contato",
            "observacoes": ""
        },
        {
            "id": "PROP_007",
            "nome": "Propriedade G - Café Arábica",
            "cultura": "Café",
            "localizacao": "Londrina - Sul",
            "proprietario": "[NOME]",
            "telefone": "[TELEFONE]",
            "email": "[EMAIL]",
            "data_contato": "",
            "confirmado": "⏳",
            "data_coleta_planejada": "",
            "data_coleta_real": "",
            "imagens_coletadas": 0,
            "imagens_aceitas": 0,
            "taxa_aceitacao": "0%",
            "status": "⏳ Pendente contato",
            "observacoes": ""
        },
        {
            "id": "PROP_008",
            "nome": "Propriedade H - Soja + Milho",
            "cultura": "Mista",
            "localizacao": "Londrina - Leste",
            "proprietario": "[NOME]",
            "telefone": "[TELEFONE]",
            "email": "[EMAIL]",
            "data_contato": "",
            "confirmado": "⏳",
            "data_coleta_planejada": "",
            "data_coleta_real": "",
            "imagens_coletadas": 0,
            "imagens_aceitas": 0,
            "taxa_aceitacao": "0%",
            "status": "⏳ Pendente contato",
            "observacoes": ""
        }
    ]
    
    # Salvar CSV
    csv_path = Path("docs/FASE_4_Propriedades.csv")
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=propriedades[0].keys())
        writer.writeheader()
        writer.writerows(propriedades)
    
    print(f"✅ Planilha de propriedades criada: {csv_path}")
    return csv_path


def criar_planilha_coleta_diaria():
    """Criar template para rastreamento diário de coleta"""
    
    template = """
RASTREAMENTO DIÁRIO DE COLETA - FASE 4
Data: __/__/____
Propriedade: ________________
Técnico: ________________
Agrônomo: ________________

═══════════════════════════════════════════════════════════════════

RESUMO DO DIA:

Total de imagens coletadas: ____
Total de imagens aceitas: ____
Taxa de aceitação: _____%

Distribuição por classe:
  ☐ Saudável: ____ imagens
  ☐ Doença leve: ____ imagens
  ☐ Doença moderada: ____ imagens
  ☐ Doença severa: ____ imagens

═══════════════════════════════════════════════════════════════════

PROBLEMAS ENCONTRADOS:

☐ Nenhum
☐ Iluminação inadequada
☐ Smartphone com bateria baixa
☐ Discordância validadores
☐ Imagens borradas
☐ Dificuldade GPS
☐ Outro: ________________

Ação corretiva: ________________

═══════════════════════════════════════════════════════════════════

BACKUP REALIZADO:

☐ Sim - Disco externo 1: ✅ 
☐ Sim - Disco externo 2: ✅
☐ Sim - Nuvem: ✅
☐ Não - Motivo: ________________

═══════════════════════════════════════════════════════════════════

OBSERVAÇÕES:

[Escrever observações sobre a coleta]

═══════════════════════════════════════════════════════════════════

PRÓXIMAS AÇÕES:

☐ Contato com próxima propriedade
☐ Processamento de dados
☐ Validação de discordâncias
☐ Ajuste de protocolo

═══════════════════════════════════════════════════════════════════
"""
    
    # Salvar template
    txt_path = Path("docs/FASE_4_Template_Coleta_Diaria.txt")
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"✅ Template de coleta diária criado: {txt_path}")
    return txt_path


def criar_planilha_progresso_fase4():
    """Criar planilha de progresso geral da Fase 4"""
    
    progresso = {
        "Métrica": [
            "Total de propriedades confirmadas",
            "Total de imagens coletadas",
            "Total de imagens aceitas",
            "Taxa de aceitação média",
            "Propriedades completadas",
            "Propriedades em andamento",
            "Propriedades pendentes",
            "Data inicial",
            "Data final planejada",
            "Dias decorridos",
            "Dias restantes",
            "Status geral"
        ],
        "Meta": [
            "5-10",
            "600-1.300",
            "570-1.235 (95%)",
            ">95%",
            "0-10",
            "0-2",
            "0-10",
            "19/09/2026",
            "09/10/2026",
            "0",
            "20",
            "🟡 INICIANDO"
        ],
        "Progresso Atual": [
            "0",
            "0",
            "0",
            "0%",
            "0",
            "0",
            "0",
            "19/09/2026",
            "09/10/2026",
            "0",
            "20",
            "⏳ Aguardando confirmação de propriedades"
        ]
    }
    
    csv_path = Path("docs/FASE_4_Progresso.csv")
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(progresso.keys())
        for i in range(len(progresso["Métrica"])):
            writer.writerow([
                progresso["Métrica"][i],
                progresso["Meta"][i],
                progresso["Progresso Atual"][i]
            ])
    
    print(f"✅ Planilha de progresso criada: {csv_path}")
    return csv_path


def criar_checklist_diario():
    """Criar checklist para cada dia de coleta"""
    
    checklist = """
CHECKLIST DIÁRIO - COLETA DE DADOS FASE 4
═══════════════════════════════════════════════════════════════════

ANTES DE SAIR (Verificar 1 hora antes):

Equipamento:
  ☐ Smartphone 100% bateria (ou carregador extra)
  ☐ Verificar app GPS está funcionando
  ☐ Verificar app de câmera com metadados
  ☐ Testar tirar 1 foto de teste
  ☐ Tripé/suporte na mochila
  ☐ Cabos/carregadores na mochila

Documentação:
  ☐ Protocolo de coleta impresso (10 cópias)
  ☐ Planilha de rastreamento em mão
  ☐ Caderno + caneta preta + caneta vermelha
  ☐ Etiquetas para identificar fotos

Proteção/Higiene:
  ☐ Álcool gel
  ☐ Luvas descartáveis
  ☐ Protetor solar
  ☐ Chapéu/boné
  ☐ Garrafa de água

Backup:
  ☐ Disco externo 1 (vazio, 2TB)
  ☐ Disco externo 2 (backup, 2TB)
  ☐ Cabo USB para transferência
  ☐ Mochila com proteção contra água/poeira

Confirmação:
  ☐ Ligou para proprietário (confirmar hora)
  ☐ Rota planejada (GPS)
  ☐ Tempo de viagem estimado: ___ minutos
  ☐ Parou para combustível? ☐ Sim ☐ Não

═══════════════════════════════════════════════════════════════════

DURANTE COLETA (A cada 20 imagens):

Qualidade de Foto:
  ☐ Imagens com foco claro (não borradas)
  ☐ Folha/fruto visível (não escondido)
  ☐ Lesão (se houver) em boa posição
  ☐ GPS capturando localização
  ☐ Ângulos variados (perpendicular, 45°, 30°)

Metadados:
  ☐ Timestamp sendo registrado
  ☐ Severidade anotada (0/1/2/3)
  ☐ Validação dupla iniciada (agrônomo + técnico)
  ☐ Discordâncias sendo documentadas

Backup em Tempo Real:
  ☐ A cada 50 imagens: backup em disco externo 1
  ☐ Verificar integridade dos arquivos

═══════════════════════════════════════════════════════════════════

APÓS COLETA (Fim do dia):

Transferência de Dados:
  ☐ Conectar smartphone ao computador
  ☐ Copiar todas as imagens + metadados
  ☐ Salvar em: data/campo_2026/raw/[propriedade]/
  ☐ Verificar integridade (nenhum arquivo corrompido)

Backup Triplo:
  ☐ Backup 1: Disco externo USB 1 ✓
  ☐ Backup 2: Disco externo USB 2 ✓
  ☐ Backup 3: Google Drive/Nuvem ✓
  ☐ Verificar 3 cópias estão íntegras

Processamento:
  ☐ Rodar script de validação:
    python scripts/process_field_images.py
  ☐ Gerar relatório de qualidade
  ☐ Verificar taxa de aceitação (>95%?)

Documentação:
  ☐ Preencher planilha de progresso
  ☐ Preencher template de coleta diária
  ☐ Atualizar checklist de propriedades
  ☐ Enviar relatório para equipe

Limpeza:
  ☐ Limpar smartphone (liberar espaço)
  ☐ Carregar smartphone para próximo dia
  ☐ Guardar discos externos em local seguro
  ☐ Organizar documentação

═══════════════════════════════════════════════════════════════════

COMUNICAÇÃO (Fim do dia):

  ☐ Enviar email para equipe com:
    - Número de imagens coletadas
    - Taxa de aceitação
    - Problemas encontrados
    - Ações para amanhã

  ☐ Atualizar grupo WhatsApp/Slack

  ☐ Enviar agradecimento ao proprietário

═══════════════════════════════════════════════════════════════════

ASSINATURAS:

Técnico de Coleta: ________________  Data: __/__/____
Agrônomo Validador: ________________  Data: __/__/____
Responsável Backup: ________________  Data: __/__/____

═══════════════════════════════════════════════════════════════════
"""
    
    txt_path = Path("docs/FASE_4_Checklist_Diario.txt")
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(checklist)
    
    print(f"✅ Checklist diário criado: {txt_path}")
    return txt_path


def main():
    """Gerar todas as planilhas de rastreamento"""
    
    print("\n" + "="*70)
    print("GERANDO PLANILHAS DE RASTREAMENTO - FASE 4")
    print("="*70 + "\n")
    
    criar_planilha_propriedades()
    criar_planilha_coleta_diaria()
    criar_planilha_progresso_fase4()
    criar_checklist_diario()
    
    print("\n" + "="*70)
    print("✅ TODAS AS PLANILHAS CRIADAS COM SUCESSO!")
    print("="*70)
    print("""
Arquivos criados em docs/:
  • FASE_4_Propriedades.csv - Preencher com contatos
  • FASE_4_Template_Coleta_Diaria.txt - Copiar para cada dia
  • FASE_4_Progresso.csv - Atualizar diariamente
  • FASE_4_Checklist_Diario.txt - Usar antes/durante/após coleta

Próximo passo: Preencher nomes/telefones/emails das propriedades
""")


if __name__ == "__main__":
    main()
