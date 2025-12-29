# TAREFA 3: SISTEMA DE ALERTAS (GATILHOS)
## Automação de Notificações para Decisão Estratégica

---

## ÍNDICE
1. [Visão Geral do Sistema de Alertas](#1-visão-geral-do-sistema-de-alertas)
2. [Regra 1: Queda Crítica de Cliente Top 20](#2-regra-1-queda-crítica-de-cliente-top-20)
3. [Regra 2: Burn Rate Negativo Consecutivo](#3-regra-2-burn-rate-negativo-consecutivo)
4. [Regra 3: Margem SPC Abaixo do Limite](#4-regra-3-margem-spc-abaixo-do-limite)
5. [Regras Complementares (Opcional)](#5-regras-complementares-opcional)
6. [Implementação Técnica](#6-implementação-técnica)
7. [Matriz de Responsabilidades](#7-matriz-de-responsabilidades)

---

## 1. VISÃO GERAL DO SISTEMA DE ALERTAS

### 1.1 Conceito

**Objetivo**: Transformar dados em ações proativas através de notificações automáticas quando indicadores ultrapassarem limites críticos.

**Canais de Comunicação**:
1. **WhatsApp Business API** (prioritário)
2. **E-mail** (backup)
3. **Power BI Mobile App** (notificação push)

**Frequência de Verificação**: 
- Alertas Críticos (🔴): Verificação a cada 1 hora (8h-18h)
- Alertas de Atenção (🟡): Verificação diária (8h)

---

### 1.2 Arquitetura do Sistema

```
┌──────────────────────────────────────────────────────────────┐
│                    CAMADA 1: DADOS                           │
│  Power BI Dataset / SQL Database                             │
└──────────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│               CAMADA 2: MOTOR DE ALERTAS                     │
│  Power Automate (Flow) ou Python Script                     │
│  • Verificação de condições (queries SQL)                   │
│  • Cálculo de variações                                     │
│  • Classificação de severidade                              │
└──────────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│              CAMADA 3: CANAIS DE NOTIFICAÇÃO                 │
│  • WhatsApp Business API (Twilio/MessageBird)               │
│  • E-mail (Outlook/Gmail)                                   │
│  • Power BI Data Alerts                                     │
└──────────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│                CAMADA 4: DESTINATÁRIOS                       │
│  Diretoria / Gerentes / Analistas                           │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. REGRA 1: QUEDA CRÍTICA DE CLIENTE TOP 20

### 2.1 Definição da Regra

**Nome**: `ALERT_001_QUEDA_CLIENTE_TOP20`

**Condição de Disparo**:
```
SE:
  Cliente pertence ao Top 20 (últimos 12 meses)
  E
  Faturamento da semana atual < (Média últimas 4 semanas - 10%)
  
ENTÃO:
  Disparar alerta VERMELHO 🔴
```

---

### 2.2 Lógica de Cálculo (SQL)

```sql
-- Passo 1: Identificar Top 20 clientes
WITH top20 AS (
    SELECT 
        id_cliente,
        razao_social,
        SUM(valor_fatura) AS receita_12m
    FROM tb_faturamento f
    JOIN tb_clientes c ON f.id_cliente = c.id_cliente
    WHERE f.data_emissao >= CURDATE() - INTERVAL 12 MONTH
      AND f.status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
    GROUP BY id_cliente, razao_social
    ORDER BY receita_12m DESC
    LIMIT 20
),

-- Passo 2: Calcular média das últimas 4 semanas
media_4_semanas AS (
    SELECT 
        id_cliente,
        AVG(receita_semanal) AS media_receita
    FROM (
        SELECT 
            id_cliente,
            YEARWEEK(data_emissao) AS semana,
            SUM(valor_fatura) AS receita_semanal
        FROM tb_faturamento
        WHERE data_emissao >= CURDATE() - INTERVAL 4 WEEK
          AND status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
        GROUP BY id_cliente, semana
    ) sub
    GROUP BY id_cliente
),

-- Passo 3: Calcular receita da semana atual
semana_atual AS (
    SELECT 
        id_cliente,
        SUM(valor_fatura) AS receita_semana_atual
    FROM tb_faturamento
    WHERE YEARWEEK(data_emissao) = YEARWEEK(CURDATE())
      AND status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
    GROUP BY id_cliente
),

-- Passo 4: Detectar quedas >10%
alertas AS (
    SELECT 
        t.id_cliente,
        t.razao_social,
        m.media_receita,
        s.receita_semana_atual,
        ROUND(((s.receita_semana_atual - m.media_receita) / m.media_receita) * 100, 2) AS variacao_pct,
        CASE 
            WHEN ((s.receita_semana_atual - m.media_receita) / m.media_receita) < -0.10 THEN 'CRÍTICO'
            ELSE 'OK'
        END AS status_alerta
    FROM top20 t
    JOIN media_4_semanas m ON t.id_cliente = m.id_cliente
    LEFT JOIN semana_atual s ON t.id_cliente = s.id_cliente
    WHERE ((s.receita_semana_atual - m.media_receita) / m.media_receita) < -0.10
)

-- Passo 5: Retornar clientes em alerta
SELECT 
    razao_social,
    CONCAT('R$ ', FORMAT(media_receita, 2, 'de_DE')) AS media_4_semanas,
    CONCAT('R$ ', FORMAT(receita_semana_atual, 2, 'de_DE')) AS semana_atual,
    CONCAT(variacao_pct, '%') AS queda_percentual,
    NOW() AS data_hora_alerta
FROM alertas
ORDER BY variacao_pct ASC;  -- Maiores quedas primeiro
```

---

### 2.3 Mensagem de Alerta (WhatsApp)

**Template**:
```
🔴 ALERTA CRÍTICO - QUEDA DE CLIENTE TOP 20

Cliente: {razao_social}
Queda: {variacao_pct}% vs. média 4 semanas

📊 Dados:
• Média 4 semanas: {media_4_semanas}
• Semana atual: {semana_atual}
• Diferença: {diferenca_real}

⚠️ AÇÃO RECOMENDADA:
Agendar reunião com cliente nas próximas 48h para entender motivo da redução.

🔗 Ver dashboard: https://powerbi.com/cdl/painel-b
📅 {data_hora_alerta}
```

**Exemplo Real**:
```
🔴 ALERTA CRÍTICO - QUEDA DE CLIENTE TOP 20

Cliente: Bemol S.A.
Queda: -25,3% vs. média 4 semanas

📊 Dados:
• Média 4 semanas: R$ 42.500
• Semana atual: R$ 31.745
• Diferença: -R$ 10.755

⚠️ AÇÃO RECOMENDADA:
Agendar reunião com cliente nas próximas 48h para entender motivo da redução.

🔗 Ver dashboard: https://powerbi.com/cdl/painel-b
📅 29/12/2025 14:32
```

---

### 2.4 Destinatários

| Nome | Cargo | WhatsApp | E-mail | Prioridade |
|------|-------|----------|--------|------------|
| João Silva | Diretor Comercial | +55 92 99999-1234 | joao@cdlmanaus.com.br | Alta |
| Maria Santos | Gerente Relacionamento | +55 92 99999-5678 | maria@cdlmanaus.com.br | Alta |
| Carlos Oliveira | Diretor Presidente | +55 92 99999-9012 | carlos@cdlmanaus.com.br | Média (CC) |

---

### 2.5 Frequência de Verificação

**Horário**: Segunda a Sexta, a cada 2 horas (8h, 10h, 12h, 14h, 16h, 18h)

**Proteção contra Spam**: 
- Mesmo cliente só pode disparar alerta 1x por dia
- Implementar flag `alerta_enviado_hoje` no banco de dados

---

## 3. REGRA 2: BURN RATE NEGATIVO CONSECUTIVO

### 3.1 Definição da Regra

**Nome**: `ALERT_002_BURN_RATE_NEGATIVO`

**Condição de Disparo**:
```
SE:
  Burn Rate Líquido < 0 (negativo)
  E
  Burn Rate Líquido do mês anterior < 0 (negativo)
  
ENTÃO:
  Disparar alerta VERMELHO 🔴
```

**Justificativa**: 
- 1 mês negativo pode ser sazonal (ex: 13º salário em Dezembro)
- 2 meses consecutivos indica problema estrutural de receita

---

### 3.2 Lógica de Cálculo (SQL)

```sql
-- Calcular Burn Rate dos últimos 2 meses
WITH burn_rate_mensal AS (
    SELECT 
        DATE_FORMAT(data_mes, '%Y-%m') AS mes_ref,
        mes_numero,
        (
            (SELECT COALESCE(SUM(valor_recebido), 0) 
             FROM tb_recebimentos 
             WHERE DATE_FORMAT(data_recebimento, '%Y-%m') = DATE_FORMAT(data_mes, '%Y-%m'))
            -
            (SELECT COALESCE(SUM(valor_despesa), 0) 
             FROM tb_despesas_operacionais 
             WHERE DATE_FORMAT(data_pagamento, '%Y-%m') = DATE_FORMAT(data_mes, '%Y-%m'))
        ) AS burn_rate
    FROM (
        SELECT 
            CURDATE() - INTERVAL 0 MONTH AS data_mes, 
            0 AS mes_numero
        UNION ALL
        SELECT 
            CURDATE() - INTERVAL 1 MONTH AS data_mes, 
            1 AS mes_numero
    ) meses
),

-- Verificar se os 2 últimos meses são negativos
status_alerta AS (
    SELECT 
        COUNT(*) AS meses_negativos
    FROM burn_rate_mensal
    WHERE burn_rate < 0
)

-- Disparar alerta se 2 meses consecutivos negativos
SELECT 
    CASE 
        WHEN meses_negativos = 2 THEN 'ALERTA_ATIVO'
        ELSE 'OK'
    END AS status,
    (SELECT burn_rate FROM burn_rate_mensal WHERE mes_numero = 0) AS burn_rate_mes_atual,
    (SELECT burn_rate FROM burn_rate_mensal WHERE mes_numero = 1) AS burn_rate_mes_anterior,
    (SELECT mes_ref FROM burn_rate_mensal WHERE mes_numero = 0) AS mes_atual,
    (SELECT mes_ref FROM burn_rate_mensal WHERE mes_numero = 1) AS mes_anterior
FROM status_alerta
WHERE meses_negativos = 2;
```

---

### 3.3 Mensagem de Alerta (WhatsApp)

**Template**:
```
🔴 ALERTA CRÍTICO - BURN RATE NEGATIVO 2 MESES

⚠️ Situação: Queimando caixa por 2 meses consecutivos

📊 Dados:
• {mes_anterior}: {burn_rate_mes_anterior}
• {mes_atual}: {burn_rate_mes_atual}
• Total queimado: {total_queimado}

💡 Projeção:
Se mantiver ritmo, caixa zerado em: {data_projecao_zero}

🚨 AÇÃO IMEDIATA NECESSÁRIA:
1. Reunião emergencial Diretoria (24h)
2. Plano de contingência:
   - Cortar despesas não-essenciais
   - Intensificar cobrança
   - Rever precificação

🔗 Ver dashboard: https://powerbi.com/cdl/painel-a
📅 {data_hora_alerta}
```

**Exemplo Real**:
```
🔴 ALERTA CRÍTICO - BURN RATE NEGATIVO 2 MESES

⚠️ Situação: Queimando caixa por 2 meses consecutivos

📊 Dados:
• Out/2025: -R$ 45.200
• Nov/2025: -R$ 83.923
• Total queimado: -R$ 129.123

💡 Projeção:
Se mantiver ritmo, caixa zerado em: Abril/2026

🚨 AÇÃO IMEDIATA NECESSÁRIA:
1. Reunião emergencial Diretoria (24h)
2. Plano de contingência:
   - Cortar despesas não-essenciais
   - Intensificar cobrança
   - Rever precificação

🔗 Ver dashboard: https://powerbi.com/cdl/painel-a
📅 29/12/2025 09:00
```

---

### 3.4 Destinatários

| Nome | Cargo | WhatsApp | E-mail | Prioridade |
|------|-------|----------|--------|------------|
| Carlos Oliveira | Diretor Presidente | +55 92 99999-9012 | carlos@cdlmanaus.com.br | **CRÍTICA** |
| Ana Costa | Diretora Financeira | +55 92 99999-3456 | ana@cdlmanaus.com.br | **CRÍTICA** |
| João Silva | Diretor Comercial | +55 92 99999-1234 | joao@cdlmanaus.com.br | Alta (CC) |

---

### 3.5 Frequência de Verificação

**Horário**: 
- Dia 1 de cada mês, às 9h (após fechamento do mês anterior)
- Verificação única mensal (não é diária)

---

## 4. REGRA 3: MARGEM SPC ABAIXO DO LIMITE

### 4.1 Definição da Regra

**Nome**: `ALERT_003_MARGEM_SPC_BAIXA`

**Condição de Disparo**:
```
SE:
  Margem de Contribuição SPC < 60%
  
ENTÃO:
  Disparar alerta AMARELO 🟡 (se 55% ≤ Margem < 60%)
  OU
  Disparar alerta VERMELHO 🔴 (se Margem < 55%)
```

**Justificativa**: 
- Meta mínima: 60% (ponto de equilíbrio operacional)
- Abaixo de 55%: Risco de prejuízo no produto

---

### 4.2 Lógica de Cálculo (SQL)

```sql
-- Calcular Margem SPC do mês atual
WITH receita_spc AS (
    SELECT 
        DATE_FORMAT(data_emissao, '%Y-%m') AS mes_ref,
        SUM(valor_fatura) AS receita
    FROM tb_faturamento
    WHERE tipo_receita = 'CONSULTA_SPC'
      AND status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
      AND data_emissao >= DATE_FORMAT(CURDATE(), '%Y-%m-01')  -- Primeiro dia do mês atual
    GROUP BY mes_ref
),

custo_spc AS (
    SELECT 
        DATE_FORMAT(CURDATE(), '%Y-%m') AS mes_ref,
        SUM(custo_insumo) AS custo
    FROM tb_custos_variaveis
    WHERE tipo_servico = 'CONSULTA_SPC'
      AND mes_referencia = DATE_FORMAT(CURDATE(), '%Y-%m')
),

margem AS (
    SELECT 
        r.mes_ref,
        r.receita,
        c.custo,
        ROUND(((r.receita - c.custo) / r.receita) * 100, 2) AS margem_pct,
        CASE 
            WHEN ((r.receita - c.custo) / r.receita) < 0.55 THEN 'CRÍTICO'
            WHEN ((r.receita - c.custo) / r.receita) < 0.60 THEN 'ATENÇÃO'
            ELSE 'OK'
        END AS status_alerta
    FROM receita_spc r
    JOIN custo_spc c ON r.mes_ref = c.mes_ref
)

-- Retornar alerta se margem < 60%
SELECT 
    mes_ref,
    CONCAT('R$ ', FORMAT(receita, 2, 'de_DE')) AS receita_spc,
    CONCAT('R$ ', FORMAT(custo, 2, 'de_DE')) AS custo_spc,
    CONCAT(margem_pct, '%') AS margem_contribuicao,
    status_alerta,
    NOW() AS data_hora_alerta
FROM margem
WHERE margem_pct < 60.00;
```

---

### 4.3 Mensagem de Alerta (WhatsApp)

**Template (Alerta Amarelo - 55% ≤ Margem < 60%)**:
```
🟡 ALERTA - MARGEM SPC ABAIXO DA META

⚠️ Margem SPC: {margem_pct}% (Meta: >60%)

📊 Dados {mes_ref}:
• Receita SPC: {receita_spc}
• Custo SPC: {custo_spc}
• Margem: {margem_contribuicao}

💡 AÇÕES RECOMENDADAS (Priorizar):
1. Renegociar tarifa com fornecedor SPC
2. Revisar precificação (aumento de 5-10%)
3. Reduzir custo por consulta (volume)

🔗 Ver dashboard: https://powerbi.com/cdl/painel-c
📅 {data_hora_alerta}
```

**Template (Alerta Vermelho - Margem < 55%)**:
```
🔴 ALERTA CRÍTICO - MARGEM SPC EM PREJUÍZO

⚠️ Margem SPC: {margem_pct}% (Meta: >60%)

📊 Dados {mes_ref}:
• Receita SPC: {receita_spc}
• Custo SPC: {custo_spc}
• Margem: {margem_contribuicao}

🚨 AÇÃO IMEDIATA NECESSÁRIA:
Produto SPC está próximo do prejuízo operacional.

1. URGENTE: Reunião com fornecedor (48h)
2. Considerar:
   - Suspender promoções temporariamente
   - Reajuste emergencial de preço
   - Migrar clientes para planos premium

🔗 Ver dashboard: https://powerbi.com/cdl/painel-c
📅 {data_hora_alerta}
```

**Exemplo Real (Amarelo)**:
```
🟡 ALERTA - MARGEM SPC ABAIXO DA META

⚠️ Margem SPC: 57,2% (Meta: >60%)

📊 Dados Nov/2025:
• Receita SPC: R$ 650.000
• Custo SPC: R$ 278.280
• Margem: 57,2%

💡 AÇÕES RECOMENDADAS (Priorizar):
1. Renegociar tarifa com fornecedor SPC
2. Revisar precificação (aumento de 5-10%)
3. Reduzir custo por consulta (volume)

🔗 Ver dashboard: https://powerbi.com/cdl/painel-c
📅 29/12/2025 11:30
```

---

### 4.4 Destinatários

| Nome | Cargo | WhatsApp | E-mail | Prioridade |
|------|-------|----------|--------|------------|
| Ana Costa | Diretora Financeira | +55 92 99999-3456 | ana@cdlmanaus.com.br | Alta |
| Pedro Alves | Diretor de Operações | +55 92 99999-7890 | pedro@cdlmanaus.com.br | Alta |
| Carlos Oliveira | Diretor Presidente | +55 92 99999-9012 | carlos@cdlmanaus.com.br | Média (CC) |

---

### 4.5 Frequência de Verificação

**Horário**: 
- Segunda a Sexta, às 17h (final do dia para avaliar margem acumulada)
- Sábado: Sem verificação
- Domingo: Sem verificação

**Proteção contra Spam**: 
- Alerta só dispara 1x por dia (mesmo que margem continue baixa)

---

## 5. REGRAS COMPLEMENTARES (OPCIONAL)

### 5.1 REGRA 4: Estoque de Suspensos Crítico

**Condição**:
```
SE Estoque_Suspensos > R$ 1.000.000
ENTÃO Alerta 🟡
```

**Mensagem**:
```
🟡 ALERTA - ESTOQUE DE SUSPENSOS ELEVADO

Valor travado: R$ {valor_suspensos}
Meta: <R$ 500.000

{qtd_clientes} clientes suspensos
Média de suspensão: {media_dias} dias

AÇÃO: Iniciar campanha de reativação
```

---

### 5.2 REGRA 5: IAR Acima de 1.05

**Condição**:
```
SE IAR > 1.05 (faturamento 5% acima do caixa)
ENTÃO Alerta 🟡
```

**Mensagem**:
```
🟡 ALERTA - DISCREPÂNCIA FATURAMENTO x CAIXA

IAR: {iar_valor} (Ideal: 0.95-1.00)

Isso significa que:
• Faturamos R$ {faturamento}
• Mas recebemos apenas R$ {caixa}
• Diferença: R$ {diferenca}

AÇÃO: Revisar política de crédito e intensificar cobrança
```

---

### 5.3 REGRA 6: Churn Real Acima de 5%

**Condição**:
```
SE Churn_Real_Mensal > 5%
ENTÃO Alerta 🟡
```

**Mensagem**:
```
🟡 ALERTA - CHURN ELEVADO

Churn Real: {churn_pct}% (Meta: <5%)

{qtd_cancelados} clientes cancelados em {mes}

Top 3 motivos de cancelamento:
1. {motivo_1}
2. {motivo_2}
3. {motivo_3}

AÇÃO: Revisar experiência do cliente e realizar pesquisa de satisfação
```

---

## 6. IMPLEMENTAÇÃO TÉCNICA

### 6.1 Opção 1: Power Automate (Microsoft Flow) - RECOMENDADO

**Custo**: Incluído no Microsoft 365 Business

**Fluxo de Implementação**:

1. **Criar Fluxo Recorrente**:
   ```
   Power Automate > Create > Scheduled cloud flow
   ├── Name: "ALERT_001_Cliente_Top20_Queda"
   ├── Frequency: Every 2 hours
   └── Time: 8AM to 6PM (workdays)
   ```

2. **Adicionar Ação: Executar Query SQL**:
   ```
   Add action > SQL Server > Execute SQL query
   ├── Connection: [ERP Database]
   ├── Query: [Copiar SQL da seção 2.2]
   └── Output: ResultSet
   ```

3. **Adicionar Condição**:
   ```
   Add action > Control > Condition
   ├── If: length(body('Execute_SQL_query')?['ResultSets']?['Table1']) greater than 0
   └── Then: Send message
   ```

4. **Adicionar Ação: Enviar WhatsApp**:
   ```
   Add action > Twilio > Send WhatsApp Message
   ├── From: whatsapp:+14155238886 (Twilio sandbox)
   ├── To: whatsapp:+5592999991234
   └── Body: [Copiar template da seção 2.3]
   ```

5. **Adicionar Ação: Enviar E-mail (Backup)**:
   ```
   Add action > Office 365 Outlook > Send an email
   ├── To: joao@cdlmanaus.com.br
   ├── Subject: 🔴 Alerta CDL - Cliente Top 20 em Queda
   └── Body: [Mesmo conteúdo do WhatsApp]
   ```

**Diagrama Visual**:
```
┌────────────────────────────────────┐
│  TRIGGER: Recurrence               │
│  Every 2 hours (8AM-6PM)          │
└────────────────────────────────────┘
                ↓
┌────────────────────────────────────┐
│  ACTION 1: Execute SQL Query       │
│  (Verificar quedas >10%)          │
└────────────────────────────────────┘
                ↓
┌────────────────────────────────────┐
│  CONDITION: Há clientes em alerta? │
│  IF length(ResultSet) > 0          │
└────────────────────────────────────┘
          ↓ YES          ↓ NO
┌─────────────────┐   [END]
│  ACTION 2:      │
│  Send WhatsApp  │
└─────────────────┘
          ↓
┌─────────────────┐
│  ACTION 3:      │
│  Send Email     │
└─────────────────┘
```

---

### 6.2 Opção 2: Python Script (Para casos avançados)

**Requisitos**:
- Python 3.8+
- Bibliotecas: `pymysql`, `twilio`, `schedule`

**Código Exemplo**:
```python
import pymysql
from twilio.rest import Client
import schedule
import time
from datetime import datetime

# Configurações
DB_CONFIG = {
    'host': 'seu_servidor_erp.com',
    'user': 'cdl_bi',
    'password': 'senha_segura',
    'database': 'cdl_manaus'
}

TWILIO_CONFIG = {
    'account_sid': 'AC...',  # Obter no Twilio Console
    'auth_token': 'token...',
    'from_whatsapp': 'whatsapp:+14155238886',
    'to_whatsapp': 'whatsapp:+5592999991234'
}

# Função para executar alerta 1
def verificar_queda_cliente_top20():
    """
    Verifica se algum cliente Top 20 teve queda >10% na semana
    """
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # SQL da seção 2.2
    query = """
    -- [Copiar SQL completo da seção 2.2]
    """
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    if len(resultados) > 0:
        # Enviar alertas para cada cliente em queda
        for row in resultados:
            razao_social = row[0]
            media_4sem = row[1]
            semana_atual = row[2]
            variacao_pct = row[3]
            
            mensagem = f"""
🔴 ALERTA CRÍTICO - QUEDA DE CLIENTE TOP 20

Cliente: {razao_social}
Queda: {variacao_pct}% vs. média 4 semanas

📊 Dados:
• Média 4 semanas: {media_4sem}
• Semana atual: {semana_atual}

⚠️ AÇÃO RECOMENDADA:
Agendar reunião com cliente nas próximas 48h.

📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}
            """
            
            enviar_whatsapp(mensagem)
    
    cursor.close()
    conn.close()

def enviar_whatsapp(mensagem):
    """
    Envia mensagem via Twilio WhatsApp API
    """
    client = Client(TWILIO_CONFIG['account_sid'], TWILIO_CONFIG['auth_token'])
    
    message = client.messages.create(
        from_=TWILIO_CONFIG['from_whatsapp'],
        body=mensagem,
        to=TWILIO_CONFIG['to_whatsapp']
    )
    
    print(f"WhatsApp enviado: {message.sid}")

# Agendar verificações
schedule.every(2).hours.do(verificar_queda_cliente_top20)

# Loop infinito
print("🤖 Sistema de Alertas CDL iniciado...")
while True:
    schedule.run_pending()
    time.sleep(60)  # Verificar a cada 60 segundos
```

**Executar Script**:
```bash
# Instalar dependências
pip install pymysql twilio schedule

# Executar
python alertas_cdl.py

# Manter rodando em background (Linux)
nohup python alertas_cdl.py > alertas.log 2>&1 &
```

---

### 6.3 Opção 3: Power BI Data Alerts (Limitado)

**Configuração**:
1. Abrir Dashboard no Power BI Service
2. Clicar em "..." no Card do KPI
3. Manage alerts > New alert rule
4. Configurar:
   - Condition: Above/Below threshold
   - Threshold value: (ex: IAR > 1.05)
   - Notification: Email only

**Limitações**:
- ❌ Não suporta WhatsApp (apenas e-mail)
- ❌ Limitado a KPIs visuais (não executa SQL complexo)
- ❌ Máximo 1 verificação por hora

**Recomendação**: Usar apenas para alertas secundários (não críticos)

---

### 6.4 Custo Estimado por Opção

| Solução | Custo Mensal | Complexidade | Flexibilidade |
|---------|--------------|--------------|---------------|
| Power Automate | R$ 0-50* | Baixa | Média |
| Python Script | R$ 0** | Alta | Alta |
| Power BI Alerts | R$ 0*** | Muito Baixa | Baixa |
| Twilio WhatsApp | ~R$ 0,10/msg**** | - | - |

\* Incluído no Microsoft 365 Business (até 750 flows/mês)  
\** Requer servidor próprio ou Azure VM (~R$ 100/mês)  
\*** Incluído no Power BI Pro  
\*\*\*\* 1.000 mensagens/mês = ~R$ 100

**Recomendação para CDL**: 
- **Power Automate** para 3 alertas principais (baixo custo, fácil manutenção)
- **Python** se precisar de >10 alertas ou lógica muito complexa

---

## 7. MATRIZ DE RESPONSABILIDADES

### 7.1 Fluxo de Ação por Alerta

| Alerta | 1º Responsável | Prazo Ação | Ação Obrigatória |
|--------|----------------|------------|------------------|
| **ALERT_001**: Queda Cliente Top 20 | Gerente Relacionamento | 48h | Contato direto com cliente |
| **ALERT_002**: Burn Rate Negativo | Diretor Presidente | 24h | Reunião emergencial Diretoria |
| **ALERT_003**: Margem SPC Baixa | Diretor Financeiro | 72h | Renegociação com fornecedor |
| **ALERT_004**: Estoque Suspensos | Gerente Cobrança | 7 dias | Campanha de reativação |
| **ALERT_005**: IAR Elevado | Gerente Cobrança | 72h | Revisão política de crédito |
| **ALERT_006**: Churn Elevado | Diretor Comercial | 7 dias | Pesquisa de satisfação |

---

### 7.2 Protocolo de Escalação

**Nível 1 (Alerta Amarelo 🟡)**:
1. Notificação para responsável direto
2. Prazo de resposta: Até 72h
3. Se não resolvido: Escalar para Nível 2

**Nível 2 (Alerta Vermelho 🔴)**:
1. Notificação para responsável direto + Diretor da Área
2. Prazo de resposta: Até 48h
3. Se não resolvido: Escalar para Nível 3

**Nível 3 (Crítico 🔴🔴)**:
1. Notificação para Diretoria completa
2. Prazo de resposta: Até 24h
3. Reunião emergencial obrigatória

---

### 7.3 Registro de Alertas (Log)

**Criar tabela de auditoria**:
```sql
CREATE TABLE tb_log_alertas (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    nome_alerta VARCHAR(100),  -- Ex: 'ALERT_001_QUEDA_CLIENTE_TOP20'
    data_hora_disparo DATETIME,
    severidade ENUM('AMARELO', 'VERMELHO'),
    detalhes_json TEXT,  -- JSON com dados do alerta
    destinatarios TEXT,  -- Lista de quem recebeu
    status_resposta ENUM('PENDENTE', 'EM_ANDAMENTO', 'RESOLVIDO'),
    data_hora_resolucao DATETIME,
    observacoes TEXT
);
```

**Benefícios**:
- Rastrear quantos alertas foram disparados
- Medir tempo médio de resposta
- Identificar alertas recorrentes (problema estrutural)

---

## RESUMO EXECUTIVO

### Alertas Implementados

| # | Nome | Severidade | Frequência | Destinatários |
|---|------|------------|------------|---------------|
| 1 | Queda Cliente Top 20 | 🔴 Crítico | A cada 2h (8h-18h) | Dir. Comercial + Ger. Relacionamento |
| 2 | Burn Rate Negativo | 🔴 Crítico | 1x/mês (dia 1, 9h) | Dir. Presidente + Dir. Financeiro |
| 3 | Margem SPC Baixa | 🟡/🔴 | Diária (17h) | Dir. Financeiro + Dir. Operações |

### Custos Totais Estimados

- **Infraestrutura**: R$ 50/mês (Power Automate)
- **WhatsApp API**: R$ 100/mês (~1.000 mensagens)
- **Total**: **R$ 150/mês**

### Próximos Passos

1. ✅ Validar credenciais de acesso ao banco de dados
2. ✅ Cadastrar números de WhatsApp dos destinatários
3. ✅ Criar conta Twilio (https://www.twilio.com/try-twilio)
4. ✅ Configurar flows no Power Automate
5. ✅ Testar alertas em ambiente de homologação
6. ✅ Go-live com monitoramento por 1 semana

---

**Documento elaborado por**: Arquiteto de Soluções BI - Ecossistema de Inteligência CDL Manaus  
**Versão**: 1.0  
**Data**: Dezembro 2025
