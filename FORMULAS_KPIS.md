# FÓRMULAS DE CÁLCULO DOS KPIs
## Referência Rápida - Ecossistema CDL Manaus

---

## ÍNDICE ALFABÉTICO

1. [Burn Rate Líquido](#1-burn-rate-líquido)
2. [Churn Real](#2-churn-real)
3. [Eficiência de Cobrança](#3-eficiência-de-cobrança)
4. [Estoque de Suspensos](#4-estoque-de-suspensos)
5. [IAR (Índice de Arrecadação Real)](#5-iar-índice-de-arrecadação-real)
6. [ICIO (Índice de Concentração)](#6-icio-índice-de-concentração)
7. [IRR (Índice de Renovação de Receita)](#7-irr-índice-de-renovação-de-receita)
8. [Margem de Contribuição SPC](#8-margem-de-contribuição-spc)
9. [Net Add Rate](#9-net-add-rate)
10. [Projeção de Caixa 30 dias](#10-projeção-de-caixa-30-dias)
11. [Saldo de Caixa Atual](#11-saldo-de-caixa-atual)
12. [Share of Wallet](#12-share-of-wallet)
13. [Status Semana (Batalha Naval)](#13-status-semana-batalha-naval)
14. [Variação Percentual (Cliente Semanal)](#14-variação-percentual-cliente-semanal)
15. [Vendas vs Meta (Certificado Digital)](#15-vendas-vs-meta-certificado-digital)

---

## 1. BURN RATE LÍQUIDO

**Definição**: Resultado do fluxo de caixa mensal (Entradas - Saídas)

**Fórmula**:
```
Burn Rate = Total Recebimentos - Total Despesas
```

**SQL**:
```sql
SELECT 
    DATE_FORMAT(data_mes, '%Y-%m') AS mes,
    (
        SELECT SUM(valor_recebido) 
        FROM tb_recebimentos 
        WHERE DATE_FORMAT(data_recebimento, '%Y-%m') = DATE_FORMAT(data_mes, '%Y-%m')
    ) AS entradas,
    (
        SELECT SUM(valor_despesa) 
        FROM tb_despesas_operacionais 
        WHERE DATE_FORMAT(data_pagamento, '%Y-%m') = DATE_FORMAT(data_mes, '%Y-%m')
    ) AS saidas,
    (
        SELECT SUM(valor_recebido) 
        FROM tb_recebimentos 
        WHERE DATE_FORMAT(data_recebimento, '%Y-%m') = DATE_FORMAT(data_mes, '%Y-%m')
    ) - (
        SELECT SUM(valor_despesa) 
        FROM tb_despesas_operacionais 
        WHERE DATE_FORMAT(data_pagamento, '%Y-%m') = DATE_FORMAT(data_mes, '%Y-%m')
    ) AS burn_rate
FROM (
    SELECT CURDATE() AS data_mes
    UNION ALL
    SELECT CURDATE() - INTERVAL 1 MONTH
    UNION ALL
    SELECT CURDATE() - INTERVAL 2 MONTH
) meses
ORDER BY mes DESC;
```

**DAX (Power BI)**:
```dax
Burn_Rate = 
CALCULATE(SUM(tb_recebimentos[valor_recebido])) - 
CALCULATE(SUM(tb_despesas_operacionais[valor_despesa]))
```

**Interpretação**:
- 🟢 **Positivo**: Empresa gerando caixa
- 🔴 **Negativo**: Empresa queimando caixa
- **Meta**: Sempre positivo (mínimo R$ 50k/mês)

**Baseline Nov/2025**: -R$ 83.923 (🔴 Crítico)

---

## 2. CHURN REAL

**Definição**: Percentual de clientes que cancelaram formalmente (excluindo suspensos)

**Fórmula**:
```
Churn Real = (Nº Cancelados no Mês / Total Clientes Ativos Início Mês) × 100
```

**SQL**:
```sql
SELECT 
    DATE_FORMAT(CURDATE(), '%Y-%m') AS mes,
    (
        SELECT COUNT(*) 
        FROM tb_clientes 
        WHERE status_cliente = 'ATIVO'
          AND (data_cancelamento IS NULL OR data_cancelamento > LAST_DAY(CURDATE() - INTERVAL 1 MONTH))
    ) AS clientes_inicio_mes,
    (
        SELECT COUNT(*) 
        FROM tb_clientes 
        WHERE status_cliente = 'CANCELADO'
          AND data_cancelamento >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
          AND data_cancelamento <= LAST_DAY(CURDATE())
    ) AS cancelados_mes,
    ROUND(
        (
            SELECT COUNT(*) 
            FROM tb_clientes 
            WHERE status_cliente = 'CANCELADO'
              AND data_cancelamento >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
        ) / (
            SELECT COUNT(*) 
            FROM tb_clientes 
            WHERE status_cliente = 'ATIVO'
              AND (data_cancelamento IS NULL OR data_cancelamento > LAST_DAY(CURDATE() - INTERVAL 1 MONTH))
        ) * 100,
        2
    ) AS churn_real_pct;
```

**DAX (Power BI)**:
```dax
Churn_Real = 
VAR ClientesInicio = 
    CALCULATE(
        DISTINCTCOUNT(tb_clientes[id_cliente]),
        tb_clientes[status_cliente] = "ATIVO",
        DATEADD(dim_tempo[data_completa], -1, MONTH)
    )
VAR Cancelados = 
    CALCULATE(
        DISTINCTCOUNT(tb_clientes[id_cliente]),
        tb_clientes[status_cliente] = "CANCELADO",
        tb_clientes[data_cancelamento] >= STARTOFMONTH(dim_tempo[data_completa]),
        tb_clientes[data_cancelamento] <= ENDOFMONTH(dim_tempo[data_completa])
    )
RETURN
    DIVIDE(Cancelados, ClientesInicio, 0) * 100
```

**Interpretação**:
- 🟢 **<5%**: Saudável
- 🟡 **5-8%**: Atenção
- 🔴 **>8%**: Crítico

**Baseline Nov/2025**: 3,8% (🟢 Saudável)

---

## 3. EFICIÊNCIA DE COBRANÇA

**Definição**: Taxa de inadimplência real (excluindo clientes suspensos)

**Fórmula**:
```
Eficiência = (Valor Inadimplente Real / Faturamento Total) × 100

Onde:
Inadimplente Real = Faturas em atraso >30 dias de clientes ATIVOS
```

**SQL**:
```sql
SELECT 
    ROUND(
        (
            SELECT SUM(valor_fatura)
            FROM tb_faturamento f
            JOIN tb_clientes c ON f.id_cliente = c.id_cliente
            WHERE f.status_fatura = 'EMITIDA'
              AND f.data_vencimento < CURDATE() - INTERVAL 30 DAY
              AND c.status_cliente = 'ATIVO'
        ) / (
            SELECT SUM(valor_fatura)
            FROM tb_faturamento
            WHERE mes_referencia = DATE_FORMAT(CURDATE(), '%Y-%m')
              AND status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
        ) * 100,
        2
    ) AS taxa_inadimplencia_real;
```

**DAX (Power BI)**:
```dax
Eficiencia_Cobranca = 
VAR Inadimplente = 
    CALCULATE(
        SUM(tb_faturamento[valor_fatura]),
        tb_faturamento[status_fatura] = "EMITIDA",
        tb_faturamento[data_vencimento] < TODAY() - 30,
        FILTER(tb_clientes, tb_clientes[status_cliente] = "ATIVO")
    )
VAR Faturamento = 
    CALCULATE(
        SUM(tb_faturamento[valor_fatura]),
        tb_faturamento[status_fatura] <> "CANCELADA"
    )
RETURN
    DIVIDE(Inadimplente, Faturamento, 0) * 100
```

**Interpretação**:
- 🟢 **<10%**: Meta atingida
- 🟡 **10-15%**: Monitorar
- 🔴 **>15%**: Ação urgente

**Meta CDL**: <10%

---

## 4. ESTOQUE DE SUSPENSOS

**Definição**: Valor travado em clientes suspensos (churn oculto)

**Fórmula**:
```
Estoque Suspensos = SUM(Faturas Abertas de Clientes com status = 'SUSPENSO')
```

**SQL**:
```sql
SELECT 
    COUNT(DISTINCT c.id_cliente) AS qtd_suspensos,
    SUM(f.valor_fatura) AS valor_travado,
    ROUND(AVG(DATEDIFF(CURDATE(), c.data_suspensao)), 0) AS media_dias_suspenso
FROM tb_clientes c
JOIN tb_faturamento f ON c.id_cliente = f.id_cliente
WHERE c.status_cliente = 'SUSPENSO'
  AND f.status_fatura = 'EMITIDA'
GROUP BY c.status_cliente;
```

**DAX (Power BI)**:
```dax
Estoque_Suspensos = 
CALCULATE(
    SUM(tb_faturamento[valor_fatura]),
    FILTER(
        tb_clientes,
        tb_clientes[status_cliente] = "SUSPENSO"
    ),
    tb_faturamento[status_fatura] = "EMITIDA"
)
```

**Interpretação**:
- 🟢 **<R$ 500k**: Meta
- 🟡 **R$ 500k-1M**: Atenção
- 🔴 **>R$ 1M**: Crítico

**Baseline Nov/2025**: R$ 742.779 (🟡 Atenção)

---

## 5. IAR (ÍNDICE DE ARRECADAÇÃO REAL)

**Definição**: Relação entre faturamento contábil e arrecadação de caixa

**Fórmula**:
```
IAR = Faturamento Contábil / Arrecadação de Caixa

Onde:
Faturamento Contábil = SUM(faturas emitidas no mês X)
Arrecadação de Caixa = SUM(recebimentos no mês X)
```

**SQL**:
```sql
WITH faturamento AS (
    SELECT 
        mes_referencia AS mes,
        SUM(valor_fatura) AS fat_contabil
    FROM tb_faturamento
    WHERE status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
      AND mes_referencia = DATE_FORMAT(CURDATE(), '%Y-%m')
    GROUP BY mes_referencia
),
caixa AS (
    SELECT 
        DATE_FORMAT(data_recebimento, '%Y-%m') AS mes,
        SUM(valor_recebido) AS arrec_caixa
    FROM tb_recebimentos
    WHERE DATE_FORMAT(data_recebimento, '%Y-%m') = DATE_FORMAT(CURDATE(), '%Y-%m')
    GROUP BY mes
)
SELECT 
    f.mes,
    f.fat_contabil,
    c.arrec_caixa,
    ROUND(f.fat_contabil / c.arrec_caixa, 2) AS IAR
FROM faturamento f
JOIN caixa c ON f.mes = c.mes;
```

**DAX (Power BI)**:
```dax
IAR = 
VAR Faturamento = 
    CALCULATE(
        SUM(tb_faturamento[valor_fatura]),
        tb_faturamento[status_fatura] NOT IN {"CANCELADA", "SUSPENSA"}
    )
VAR Arrecadacao = 
    SUM(tb_recebimentos[valor_recebido])
RETURN
    DIVIDE(Faturamento, Arrecadacao, 0)
```

**Interpretação**:
- 🟢 **0.95-1.00**: Saudável (caixa = competência)
- 🟡 **1.00-1.05**: Atenção (caixa 5% abaixo)
- 🔴 **>1.05**: Crítico (discrepância alta)

**Baseline Nov/2025**: 1,01 (🟡 Atenção)

---

## 6. ICIO (ÍNDICE DE CONCENTRAÇÃO)

**Definição**: Percentual da receita concentrado nos Top 20 clientes

**Fórmula**:
```
ICIO = (Receita Top 20 / Receita Total) × 100

Onde:
Top 20 = 20 maiores clientes por receita (últimos 12 meses)
```

**SQL**:
```sql
WITH top20 AS (
    SELECT 
        c.id_cliente,
        c.razao_social,
        SUM(f.valor_fatura) AS receita_12m
    FROM tb_clientes c
    JOIN tb_faturamento f ON c.id_cliente = f.id_cliente
    WHERE f.data_emissao >= CURDATE() - INTERVAL 12 MONTH
      AND f.status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
    GROUP BY c.id_cliente, c.razao_social
    ORDER BY receita_12m DESC
    LIMIT 20
),
total AS (
    SELECT SUM(valor_fatura) AS receita_total
    FROM tb_faturamento
    WHERE data_emissao >= CURDATE() - INTERVAL 12 MONTH
      AND status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
)
SELECT 
    ROUND(
        (SELECT SUM(receita_12m) FROM top20) / 
        (SELECT receita_total FROM total) * 100,
        2
    ) AS icio_percentual;
```

**DAX (Power BI)**:
```dax
ICIO = 
VAR ReceitaTop20 = 
    CALCULATE(
        SUM(tb_faturamento[valor_fatura]),
        TOPN(20, ALL(tb_clientes), [Receita_12m], DESC)
    )
VAR ReceitaTotal = 
    SUM(tb_faturamento[valor_fatura])
RETURN
    DIVIDE(ReceitaTop20, ReceitaTotal, 0) * 100
```

**Interpretação**:
- 🟢 **<40%**: Carteira diversificada
- 🟡 **40-60%**: Monitorar concentração
- 🔴 **>60%**: Risco alto de dependência

**Baseline Nov/2025**: 45,3% (🟡 Monitorar)

---

## 7. IRR (ÍNDICE DE RENOVAÇÃO DE RECEITA)

**Definição**: Separação de receita em Recorrente (Mensalidades) vs. Variável (Consultas/SPC)

**Fórmula**:
```
IRR Recorrente = SUM(Mensalidades últimos 12 meses)
IRR Variável = SUM(Consultas SPC + Outros últimos 12 meses)

Percentual Recorrente = IRR Recorrente / (IRR Recorrente + IRR Variável) × 100
```

**SQL**:
```sql
SELECT 
    SUM(CASE WHEN tipo_receita = 'MENSALIDADE' THEN valor_fatura ELSE 0 END) AS irr_recorrente,
    SUM(CASE WHEN tipo_receita IN ('CONSULTA_SPC', 'CERTIFICADO', 'OUTROS') THEN valor_fatura ELSE 0 END) AS irr_variavel,
    ROUND(
        SUM(CASE WHEN tipo_receita = 'MENSALIDADE' THEN valor_fatura ELSE 0 END) / 
        SUM(valor_fatura) * 100,
        1
    ) AS pct_recorrente
FROM tb_faturamento
WHERE data_emissao >= CURDATE() - INTERVAL 12 MONTH
  AND status_fatura NOT IN ('CANCELADA', 'SUSPENSA');
```

**DAX (Power BI)**:
```dax
IRR_Recorrente = 
CALCULATE(
    SUM(tb_faturamento[valor_fatura]),
    tb_faturamento[tipo_receita] = "MENSALIDADE",
    DATESINPERIOD(dim_tempo[data_completa], MAX(dim_tempo[data_completa]), -12, MONTH)
)

IRR_Variavel = 
CALCULATE(
    SUM(tb_faturamento[valor_fatura]),
    tb_faturamento[tipo_receita] IN {"CONSULTA_SPC", "CERTIFICADO", "OUTROS"},
    DATESINPERIOD(dim_tempo[data_completa], MAX(dim_tempo[data_completa]), -12, MONTH)
)

Pct_Recorrente = 
DIVIDE([IRR_Recorrente], [IRR_Recorrente] + [IRR_Variavel], 0) * 100
```

**Interpretação**:
- 🟢 **Recorrente >60%**: Receita previsível
- 🟡 **Recorrente 40-60%**: Modelo misto
- 🔴 **Recorrente <40%**: Alta volatilidade

**Baseline Nov/2025**: 60% Recorrente / 40% Variável

---

## 8. MARGEM DE CONTRIBUIÇÃO SPC

**Definição**: Rentabilidade do produto SPC (receita - custo variável)

**Fórmula**:
```
Margem SPC = ((Receita SPC - Custo SPC) / Receita SPC) × 100

Onde:
Receita SPC = SUM(faturas tipo 'CONSULTA_SPC')
Custo SPC = SUM(custos insumo tipo 'CONSULTA_SPC')
```

**SQL**:
```sql
WITH receita_spc AS (
    SELECT 
        DATE_FORMAT(data_emissao, '%Y-%m') AS mes,
        SUM(valor_fatura) AS receita
    FROM tb_faturamento
    WHERE tipo_receita = 'CONSULTA_SPC'
      AND status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
      AND mes_referencia = DATE_FORMAT(CURDATE(), '%Y-%m')
    GROUP BY mes
),
custo_spc AS (
    SELECT 
        mes_referencia AS mes,
        SUM(custo_insumo) AS custo
    FROM tb_custos_variaveis
    WHERE tipo_servico = 'CONSULTA_SPC'
      AND mes_referencia = DATE_FORMAT(CURDATE(), '%Y-%m')
    GROUP BY mes
)
SELECT 
    r.mes,
    r.receita AS receita_spc,
    c.custo AS custo_spc,
    ROUND(((r.receita - c.custo) / r.receita) * 100, 2) AS margem_contribuicao
FROM receita_spc r
JOIN custo_spc c ON r.mes = c.mes;
```

**DAX (Power BI)**:
```dax
Margem_SPC = 
VAR ReceitaSPC = 
    CALCULATE(
        SUM(tb_faturamento[valor_fatura]),
        tb_faturamento[tipo_receita] = "CONSULTA_SPC"
    )
VAR CustoSPC = 
    CALCULATE(
        SUM(tb_custos_variaveis[custo_insumo]),
        tb_custos_variaveis[tipo_servico] = "CONSULTA_SPC"
    )
RETURN
    DIVIDE(ReceitaSPC - CustoSPC, ReceitaSPC, 0) * 100
```

**Interpretação**:
- 🟢 **>70%**: Excelente rentabilidade
- 🟡 **60-70%**: Dentro da meta
- 🔴 **<60%**: Abaixo do ponto de equilíbrio

**Baseline Nov/2025**: 62,3% (🟢 Acima da meta)

---

## 9. NET ADD RATE

**Definição**: Saldo líquido de movimentação de carteira (entradas - saídas)

**Fórmula**:
```
Net Add Rate = Novos Clientes - (Cancelados + Suspensos)
```

**SQL**:
```sql
SELECT 
    (
        SELECT COUNT(*) 
        FROM tb_clientes 
        WHERE data_adesao >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
    ) AS entradas,
    (
        SELECT COUNT(*) 
        FROM tb_clientes 
        WHERE data_cancelamento >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
    ) AS cancelados,
    (
        SELECT COUNT(*) 
        FROM tb_clientes 
        WHERE data_suspensao >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
    ) AS suspensos,
    (
        SELECT COUNT(*) 
        FROM tb_clientes 
        WHERE data_adesao >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
    ) - (
        SELECT COUNT(*) 
        FROM tb_clientes 
        WHERE data_cancelamento >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
          OR data_suspensao >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
    ) AS net_add_rate;
```

**DAX (Power BI)**:
```dax
Net_Add_Rate = 
VAR Entradas = 
    CALCULATE(
        DISTINCTCOUNT(tb_clientes[id_cliente]),
        tb_clientes[data_adesao] >= STARTOFMONTH(dim_tempo[data_completa])
    )
VAR Saidas = 
    CALCULATE(
        DISTINCTCOUNT(tb_clientes[id_cliente]),
        OR(
            tb_clientes[data_cancelamento] >= STARTOFMONTH(dim_tempo[data_completa]),
            tb_clientes[data_suspensao] >= STARTOFMONTH(dim_tempo[data_completa])
        )
    )
RETURN
    Entradas - Saidas
```

**Interpretação**:
- 🟢 **Positivo**: Crescendo carteira
- 🔴 **Negativo**: Perdendo clientes

---

## 10. PROJEÇÃO DE CAIXA 30 DIAS

**Definição**: Saldo projetado baseado em médias de entradas/saídas

**Fórmula**:
```
Projeção = Saldo Atual + Média Recebimentos 30d - Média Despesas 30d
```

**SQL**:
```sql
SELECT 
    (
        -- Saldo atual
        (SELECT SUM(valor_recebido) FROM tb_recebimentos) - 
        (SELECT SUM(valor_despesa) FROM tb_despesas_operacionais)
    ) AS saldo_atual,
    (
        -- Média recebimentos 30d
        SELECT AVG(total_dia) 
        FROM (
            SELECT DATE(data_recebimento) AS dia, SUM(valor_recebido) AS total_dia
            FROM tb_recebimentos
            WHERE data_recebimento >= CURDATE() - INTERVAL 30 DAY
            GROUP BY dia
        ) sub
    ) * 30 AS previsao_recebimentos_30d,
    (
        -- Média despesas 30d
        SELECT AVG(total_dia) 
        FROM (
            SELECT DATE(data_pagamento) AS dia, SUM(valor_despesa) AS total_dia
            FROM tb_despesas_operacionais
            WHERE data_pagamento >= CURDATE() - INTERVAL 30 DAY
            GROUP BY dia
        ) sub
    ) * 30 AS previsao_despesas_30d,
    (
        -- Projeção
        (SELECT SUM(valor_recebido) FROM tb_recebimentos) - 
        (SELECT SUM(valor_despesa) FROM tb_despesas_operacionais) +
        (
            SELECT AVG(total_dia) 
            FROM (
                SELECT DATE(data_recebimento) AS dia, SUM(valor_recebido) AS total_dia
                FROM tb_recebimentos
                WHERE data_recebimento >= CURDATE() - INTERVAL 30 DAY
                GROUP BY dia
            ) sub
        ) * 30 -
        (
            SELECT AVG(total_dia) 
            FROM (
                SELECT DATE(data_pagamento) AS dia, SUM(valor_despesa) AS total_dia
                FROM tb_despesas_operacionais
                WHERE data_pagamento >= CURDATE() - INTERVAL 30 DAY
                GROUP BY dia
            ) sub
        ) * 30
    ) AS projecao_30d;
```

**DAX (Power BI)**:
```dax
Projecao_Caixa_30d = 
VAR SaldoAtual = [Saldo_Caixa]
VAR MediaRecebimentos = 
    CALCULATE(
        AVERAGEX(
            VALUES(dim_tempo[data_completa]),
            [Total_Recebimentos_Dia]
        ),
        DATESINPERIOD(dim_tempo[data_completa], MAX(dim_tempo[data_completa]), -30, DAY)
    ) * 30
VAR MediaDespesas = 
    CALCULATE(
        AVERAGEX(
            VALUES(dim_tempo[data_completa]),
            [Total_Despesas_Dia]
        ),
        DATESINPERIOD(dim_tempo[data_completa], MAX(dim_tempo[data_completa]), -30, DAY)
    ) * 30
RETURN
    SaldoAtual + MediaRecebimentos - MediaDespesas
```

---

## 11. SALDO DE CAIXA ATUAL

**Definição**: Posição de caixa acumulada até a data

**Fórmula**:
```
Saldo Caixa = SUM(Recebimentos) - SUM(Despesas)
```

**SQL**:
```sql
SELECT 
    (SELECT SUM(valor_recebido) FROM tb_recebimentos) AS total_recebido,
    (SELECT SUM(valor_despesa) FROM tb_despesas_operacionais) AS total_despesas,
    (
        (SELECT SUM(valor_recebido) FROM tb_recebimentos) - 
        (SELECT SUM(valor_despesa) FROM tb_despesas_operacionais)
    ) AS saldo_caixa;
```

**DAX (Power BI)**:
```dax
Saldo_Caixa = 
SUM(tb_recebimentos[valor_recebido]) - 
SUM(tb_despesas_operacionais[valor_despesa])
```

---

## 12. SHARE OF WALLET

**Definição**: Percentual de receita de cada cliente Top 20 vs. total

**Fórmula**:
```
Share of Wallet = (Receita Cliente / Receita Total) × 100
```

**SQL**:
```sql
WITH receita_cliente AS (
    SELECT 
        c.id_cliente,
        c.razao_social,
        SUM(f.valor_fatura) AS receita_12m
    FROM tb_clientes c
    JOIN tb_faturamento f ON c.id_cliente = f.id_cliente
    WHERE f.data_emissao >= CURDATE() - INTERVAL 12 MONTH
      AND f.status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
    GROUP BY c.id_cliente, c.razao_social
),
total AS (
    SELECT SUM(receita_12m) AS receita_total
    FROM receita_cliente
)
SELECT 
    rc.razao_social,
    rc.receita_12m,
    ROUND((rc.receita_12m / t.receita_total) * 100, 2) AS share_wallet
FROM receita_cliente rc, total t
ORDER BY rc.receita_12m DESC
LIMIT 20;
```

---

## 13. STATUS SEMANA (BATALHA NAVAL)

**Definição**: Indicador visual de performance semanal do cliente

**Fórmula**:
```
Variação = ((Receita Semana Atual - Média 4 Semanas) / Média 4 Semanas) × 100

Status:
🟢 Se variação entre -5% e +5% (Estável)
🟡 Se variação entre -10% e -5% (Queda leve)
🔴 Se variação < -10% (Queda crítica)
```

**SQL**: Ver seção 14

---

## 14. VARIAÇÃO PERCENTUAL (CLIENTE SEMANAL)

**Definição**: Percentual de mudança na receita semanal vs. média móvel

**Fórmula**:
```
Variação% = ((Receita Semana Atual - Média 4 Semanas) / Média 4 Semanas) × 100
```

**SQL**:
```sql
WITH receita_semanal AS (
    SELECT 
        id_cliente,
        YEARWEEK(data_emissao) AS semana,
        SUM(valor_fatura) AS receita
    FROM tb_faturamento
    WHERE data_emissao >= CURDATE() - INTERVAL 4 WEEK
      AND status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
    GROUP BY id_cliente, semana
),
media_4sem AS (
    SELECT 
        id_cliente,
        AVG(receita) AS media_receita
    FROM receita_semanal
    GROUP BY id_cliente
)
SELECT 
    rs.id_cliente,
    rs.semana,
    rs.receita AS receita_semana_atual,
    m.media_receita,
    ROUND(((rs.receita - m.media_receita) / m.media_receita) * 100, 2) AS variacao_pct
FROM receita_semanal rs
JOIN media_4sem m ON rs.id_cliente = m.id_cliente
WHERE rs.semana = YEARWEEK(CURDATE());
```

---

## 15. VENDAS VS META (CERTIFICADO DIGITAL)

**Definição**: Comparação de vendas realizadas vs. meta estabelecida

**Fórmula**:
```
% Meta = (Vendas Realizadas / Meta) × 100
```

**SQL**:
```sql
SELECT 
    DATE_FORMAT(data_emissao, '%Y-%m') AS mes,
    SUM(valor_fatura) AS vendas_certificado,
    160000 AS meta_mensal,  -- Meta fixa: R$ 160k
    ROUND((SUM(valor_fatura) / 160000) * 100, 0) AS percentual_meta
FROM tb_faturamento
WHERE tipo_receita = 'CERTIFICADO'
  AND status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
  AND mes_referencia = DATE_FORMAT(CURDATE(), '%Y-%m')
GROUP BY mes;
```

**DAX (Power BI)**:
```dax
Vs_Meta_Certificado = 
VAR Meta = 160000
VAR Vendas = 
    CALCULATE(
        SUM(tb_faturamento[valor_fatura]),
        tb_faturamento[tipo_receita] = "CERTIFICADO"
    )
RETURN
    DIVIDE(Vendas, Meta, 0) * 100
```

**Interpretação**:
- 🟢 **≥100%**: Meta batida
- 🟡 **80-99%**: Próximo da meta
- 🔴 **<80%**: Abaixo da meta

---

## NOTAS FINAIS

### Convenções Usadas

- **SUM()**: Somatório
- **AVG()**: Média
- **COUNT()**: Contagem
- **DIVIDE()**: Divisão com tratamento de erro (retorna 0 se divisor = 0)
- **CALCULATE()**: Função DAX para aplicar filtros

### Periodicidades Padrão

- **Mensal**: Cálculos que usam mês completo
- **12 Meses**: Rolling 12 months (últimos 12 meses)
- **30 Dias**: Rolling 30 days (últimos 30 dias)
- **Semanal**: YEARWEEK() para agregação por semana

### Status de Fatura

- **EMITIDA**: Fatura gerada, aguardando pagamento
- **PAGA**: Fatura quitada
- **CANCELADA**: Fatura cancelada (não entra nos cálculos)
- **SUSPENSA**: Fatura de cliente suspenso (tratamento especial)

### Status de Cliente

- **ATIVO**: Cliente operacional
- **SUSPENSO**: Cliente com pagamento atrasado (churn oculto)
- **CANCELADO**: Cliente que solicitou cancelamento (churn real)

---

**Documento elaborado por**: Arquiteto de Soluções BI - Ecossistema de Inteligência CDL Manaus  
**Versão**: 1.0  
**Data**: Dezembro 2025
