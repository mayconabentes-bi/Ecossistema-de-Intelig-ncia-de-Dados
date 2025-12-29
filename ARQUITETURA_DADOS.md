# TAREFA 1: ARQUITETURA DE DADOS
## Estrutura do Data Lake Simplificado para CDL Manaus

### 1. VISÃO GERAL DA ARQUITETURA

```
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA 1: FONTE (ERP)                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              CAMADA 2: RAW DATA (Dados Brutos)              │
│  • Extração diária via API/ODBC do ERP                      │
│  • Formato: CSV/Parquet (baixo custo)                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│          CAMADA 3: STAGING (Transformação & Limpeza)        │
│  • Power Query / Python pandas                              │
│  • Aplicação de regras de negócio                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│           CAMADA 4: ANALYTICAL (Modelo Dimensional)         │
│  • Tabelas Fato e Dimensão                                  │
│  • Modelo Star Schema                                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│            CAMADA 5: PRESENTATION (Dashboards)              │
│  • Power BI / Excel Avançado                                │
│  • Atualização automática (refresh schedule)               │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. TABELAS DO ERP - MAPEAMENTO ESSENCIAL

### 2.1 TABELAS FINANCEIRAS (Core)

#### **Tabela: `tb_faturamento`**
**Propósito**: Registro de todas as faturas emitidas (competência contábil)

| Campo | Tipo | Descrição | Uso no KPI |
|-------|------|-----------|------------|
| `id_fatura` | INT | Chave primária | - |
| `id_cliente` | INT | FK para tb_clientes | ICIO, IRR |
| `data_emissao` | DATE | Data de emissão da fatura | IAR, Burn Rate |
| `data_vencimento` | DATE | Data de vencimento | Inadimplência |
| `valor_fatura` | DECIMAL(15,2) | Valor total da fatura | IAR (numerador) |
| `tipo_receita` | VARCHAR(50) | 'MENSALIDADE', 'CONSULTA_SPC', 'CERTIFICADO', 'OUTROS' | IRR, Margem SPC |
| `status_fatura` | VARCHAR(20) | 'EMITIDA', 'PAGA', 'CANCELADA', 'SUSPENSA' | Burn Rate |
| `mes_referencia` | VARCHAR(7) | 'YYYY-MM' para análise temporal | Tendências |

**SQL para IAR (Numerador)**:
```sql
SELECT 
    mes_referencia,
    SUM(valor_fatura) AS faturamento_contabil
FROM tb_faturamento
WHERE status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
GROUP BY mes_referencia;
```

---

#### **Tabela: `tb_recebimentos`**
**Propósito**: Registro de pagamentos efetivamente recebidos (regime de caixa)

| Campo | Tipo | Descrição | Uso no KPI |
|-------|------|-----------|------------|
| `id_recebimento` | INT | Chave primária | - |
| `id_fatura` | INT | FK para tb_faturamento | Vincular caixa x competência |
| `data_recebimento` | DATE | Data da entrada no caixa | IAR (denominador) |
| `valor_recebido` | DECIMAL(15,2) | Valor efetivamente pago | Burn Rate |
| `forma_pagamento` | VARCHAR(30) | 'BOLETO', 'PIX', 'CARTAO', etc. | Análise de cobrança |

**SQL para IAR (Denominador)**:
```sql
SELECT 
    DATE_FORMAT(data_recebimento, '%Y-%m') AS mes_recebimento,
    SUM(valor_recebido) AS arrecadacao_caixa
FROM tb_recebimentos
GROUP BY mes_recebimento;
```

**SQL COMPLETO - ÍNDICE IAR**:
```sql
WITH faturamento AS (
    SELECT 
        mes_referencia,
        SUM(valor_fatura) AS fat_contabil
    FROM tb_faturamento
    WHERE status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
    GROUP BY mes_referencia
),
caixa AS (
    SELECT 
        DATE_FORMAT(data_recebimento, '%Y-%m') AS mes_caixa,
        SUM(valor_recebido) AS arrec_caixa
    FROM tb_recebimentos
    GROUP BY mes_caixa
)
SELECT 
    f.mes_referencia,
    f.fat_contabil,
    c.arrec_caixa,
    ROUND(f.fat_contabil / c.arrec_caixa, 2) AS IAR,
    CASE 
        WHEN (f.fat_contabil / c.arrec_caixa) > 1.05 THEN '🔴 Crítico: Caixa 5% abaixo da competência'
        WHEN (f.fat_contabil / c.arrec_caixa) > 1.00 THEN '🟡 Atenção: Caixa abaixo da competência'
        ELSE '🟢 Saudável'
    END AS status_iar
FROM faturamento f
JOIN caixa c ON f.mes_referencia = c.mes_caixa
ORDER BY f.mes_referencia DESC;
```

---

### 2.2 TABELAS COMERCIAIS

#### **Tabela: `tb_clientes`**
**Propósito**: Cadastro de clientes ativos, suspensos e cancelados

| Campo | Tipo | Descrição | Uso no KPI |
|-------|------|-----------|------------|
| `id_cliente` | INT | Chave primária | - |
| `razao_social` | VARCHAR(200) | Nome do cliente | ICIO (Top 20) |
| `cnpj` | VARCHAR(18) | CNPJ do cliente | Chave natural |
| `status_cliente` | VARCHAR(20) | 'ATIVO', 'SUSPENSO', 'CANCELADO' | **CRÍTICO** |
| `data_adesao` | DATE | Data de entrada na carteira | Cohort analysis |
| `data_suspensao` | DATE | Data da suspensão (se aplicável) | Estoque Suspensos |
| `data_cancelamento` | DATE | Data do cancelamento | Churn real |
| `categoria` | VARCHAR(50) | 'GRANDE_VAREJISTA', 'PME', 'MEI' | Segmentação |

**REGRA DE NEGÓCIO CRÍTICA - DISTINÇÃO SUSPENSO vs. CANCELADO**:

```sql
-- CLIENTE SUSPENSO: Cliente com fatura atrasada >90 dias, mas ainda com interesse em retornar
-- Status: 'SUSPENSO'
-- Tratamento: NÃO deve entrar no cálculo de inadimplência padrão
--             DEVE ser isolado no KPI "Estoque de Suspensos Recuperável"

-- CLIENTE CANCELADO: Cliente que solicitou cancelamento formal ou está inativo >180 dias
-- Status: 'CANCELADO'
-- Tratamento: Entra no cálculo de Churn Real para o IRR

-- SQL para limpar inadimplência (excluir suspensos):
SELECT 
    COUNT(DISTINCT id_cliente) AS clientes_inadimplentes_real,
    SUM(valor_fatura) AS valor_inadimplencia_real
FROM tb_faturamento
WHERE status_fatura = 'EMITIDA'
  AND data_vencimento < CURDATE() - INTERVAL 30 DAY
  AND id_cliente IN (
      SELECT id_cliente 
      FROM tb_clientes 
      WHERE status_cliente = 'ATIVO'  -- Exclui SUSPENSOS
  );
```

**SQL para Estoque de Suspensos**:
```sql
SELECT 
    c.razao_social,
    c.data_suspensao,
    SUM(f.valor_fatura) AS valor_travado,
    DATEDIFF(CURDATE(), c.data_suspensao) AS dias_suspenso
FROM tb_clientes c
JOIN tb_faturamento f ON c.id_cliente = f.id_cliente
WHERE c.status_cliente = 'SUSPENSO'
  AND f.status_fatura = 'EMITIDA'
GROUP BY c.id_cliente, c.razao_social, c.data_suspensao
ORDER BY valor_travado DESC;
```

---

#### **Tabela: `tb_top_clientes`** (Materializada/View)
**Propósito**: Pre-calcular o Top 20 para performance do ICIO

```sql
CREATE VIEW vw_top20_clientes AS
SELECT 
    c.id_cliente,
    c.razao_social,
    SUM(f.valor_fatura) AS receita_12m,
    ROUND(
        SUM(f.valor_fatura) / (SELECT SUM(valor_fatura) FROM tb_faturamento WHERE data_emissao >= CURDATE() - INTERVAL 12 MONTH) * 100, 
        2
    ) AS share_receita
FROM tb_clientes c
JOIN tb_faturamento f ON c.id_cliente = f.id_cliente
WHERE f.data_emissao >= CURDATE() - INTERVAL 12 MONTH
  AND f.status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
GROUP BY c.id_cliente, c.razao_social
ORDER BY receita_12m DESC
LIMIT 20;
```

**SQL COMPLETO - ÍNDICE ICIO (Índice de Concentração)**:
```sql
WITH top20 AS (
    SELECT SUM(receita_12m) AS receita_top20
    FROM vw_top20_clientes
),
total AS (
    SELECT SUM(valor_fatura) AS receita_total
    FROM tb_faturamento
    WHERE data_emissao >= CURDATE() - INTERVAL 12 MONTH
      AND status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
)
SELECT 
    ROUND((top20.receita_top20 / total.receita_total) * 100, 2) AS icio_percentual,
    CASE 
        WHEN (top20.receita_top20 / total.receita_total) > 0.60 THEN '🔴 Risco Alto: >60% concentrado'
        WHEN (top20.receita_top20 / total.receita_total) > 0.40 THEN '🟡 Monitorar: 40-60% concentrado'
        ELSE '🟢 Diversificado'
    END AS status_icio
FROM top20, total;
```

---

### 2.3 TABELAS DE CUSTOS (Para Margem SPC)

#### **Tabela: `tb_custos_variaveis`**
**Propósito**: Registrar custos diretos por tipo de produto/serviço

| Campo | Tipo | Descrição | Uso no KPI |
|-------|------|-----------|------------|
| `id_custo` | INT | Chave primária | - |
| `tipo_servico` | VARCHAR(50) | 'CONSULTA_SPC', 'CERTIFICADO', etc. | Margem por produto |
| `mes_referencia` | VARCHAR(7) | 'YYYY-MM' | Matching com receita |
| `custo_insumo` | DECIMAL(15,2) | Custo de API/licença pago | Margem SPC |
| `quantidade` | INT | Nº de transações | Custo unitário |

**SQL COMPLETO - MARGEM DE CONTRIBUIÇÃO SPC**:
```sql
WITH receita_spc AS (
    SELECT 
        mes_referencia,
        SUM(valor_fatura) AS receita
    FROM tb_faturamento
    WHERE tipo_receita = 'CONSULTA_SPC'
      AND status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
    GROUP BY mes_referencia
),
custo_spc AS (
    SELECT 
        mes_referencia,
        SUM(custo_insumo) AS custo
    FROM tb_custos_variaveis
    WHERE tipo_servico = 'CONSULTA_SPC'
    GROUP BY mes_referencia
)
SELECT 
    r.mes_referencia,
    r.receita AS receita_spc,
    c.custo AS custo_spc,
    ROUND(((r.receita - c.custo) / r.receita) * 100, 2) AS margem_contribuicao,
    CASE 
        WHEN ((r.receita - c.custo) / r.receita) < 0.60 THEN '🔴 CRÍTICO: Margem <60%'
        WHEN ((r.receita - c.custo) / r.receita) < 0.70 THEN '🟡 Atenção: Margem 60-70%'
        ELSE '🟢 Saudável: Margem >70%'
    END AS status_margem
FROM receita_spc r
JOIN custo_spc c ON r.mes_referencia = c.mes_referencia
ORDER BY r.mes_referencia DESC;
```

---

### 2.4 TABELAS DE FLUXO DE CAIXA

#### **Tabela: `tb_despesas_operacionais`**
**Propósito**: Registrar todas as saídas de caixa

| Campo | Tipo | Descrição | Uso no KPI |
|-------|------|-----------|------------|
| `id_despesa` | INT | Chave primária | - |
| `data_pagamento` | DATE | Data da saída do caixa | Burn Rate |
| `valor_despesa` | DECIMAL(15,2) | Valor pago | Burn Rate |
| `categoria` | VARCHAR(50) | 'FOLHA', 'ALUGUEL', 'TI', etc. | Análise de eficiência |

**SQL COMPLETO - BURN RATE LÍQUIDO**:
```sql
WITH entradas AS (
    SELECT 
        DATE_FORMAT(data_recebimento, '%Y-%m') AS mes,
        SUM(valor_recebido) AS total_entradas
    FROM tb_recebimentos
    GROUP BY mes
),
saidas AS (
    SELECT 
        DATE_FORMAT(data_pagamento, '%Y-%m') AS mes,
        SUM(valor_despesa) AS total_saidas
    FROM tb_despesas_operacionais
    GROUP BY mes
)
SELECT 
    e.mes,
    e.total_entradas,
    s.total_saidas,
    (e.total_entradas - s.total_saidas) AS burn_rate_liquido,
    CASE 
        WHEN (e.total_entradas - s.total_saidas) < 0 THEN '🔴 ALERTA: Queimando caixa'
        WHEN (e.total_entradas - s.total_saidas) < 50000 THEN '🟡 Atenção: Margem baixa'
        ELSE '🟢 Saudável'
    END AS status_burn_rate
FROM entradas e
JOIN saidas s ON e.mes = s.mes
ORDER BY e.mes DESC
LIMIT 3;  -- Últimos 3 meses
```

---

## 3. ESTRUTURA FÍSICA DO DATA LAKE

### 3.1 Organização de Pastas (Storage Local/OneDrive)

```
/CDL_DataLake/
├── 01_RAW/                          # Dados brutos do ERP
│   ├── faturamento/
│   │   ├── 2025-11-30_faturamento.csv
│   │   ├── 2025-12-01_faturamento.csv
│   │   └── ...
│   ├── recebimentos/
│   ├── clientes/
│   ├── despesas/
│   └── custos_variaveis/
│
├── 02_STAGING/                      # Dados transformados
│   ├── fato_financeiro.parquet      # Consolidado diário
│   ├── dim_clientes_clean.parquet   # Clientes com status normalizado
│   └── dim_tempo.parquet            # Calendário fiscal
│
├── 03_ANALYTICAL/                   # Modelo dimensional
│   ├── fato_receita.parquet         # Fact table principal
│   ├── fato_despesa.parquet
│   ├── dim_cliente.parquet
│   ├── dim_produto.parquet
│   └── dim_tempo.parquet
│
└── 04_KPIS/                         # Agregações pré-calculadas
    ├── kpi_iar_monthly.csv
    ├── kpi_icio_top20.csv
    ├── kpi_burn_rate.csv
    └── kpi_margem_spc.csv
```

---

## 4. FLUXO DE ETL (Extração, Transformação, Carga)

### 4.1 Ferramentas Recomendadas (Baixo Custo)

**Opção 1: Power Query (Excel/Power BI)**
- **Custo**: Gratuito (incluído no Microsoft 365)
- **Uso**: ETL visual sem código
- **Limite**: ~1M linhas (suficiente para CDL)

**Opção 2: Python + Pandas** (se >1M linhas)
- **Custo**: Gratuito
- **Uso**: Script ETL automatizado
- **Exemplo**:
```python
import pandas as pd
from datetime import datetime

# Carregar dados brutos
df_fat = pd.read_csv('/CDL_DataLake/01_RAW/faturamento/2025-11-30_faturamento.csv')
df_cli = pd.read_csv('/CDL_DataLake/01_RAW/clientes/clientes_master.csv')

# Transformação: Normalizar status de cliente
def normalizar_status(row):
    if row['status_cliente'] == 'SUSPENSO':
        return 'SUSPENSO'  # Manter isolado
    elif row['data_cancelamento'] is not None:
        return 'CANCELADO'
    else:
        return 'ATIVO'

df_cli['status_normalizado'] = df_cli.apply(normalizar_status, axis=1)

# Salvar staging
df_cli.to_parquet('/CDL_DataLake/02_STAGING/dim_clientes_clean.parquet')
```

---

### 4.2 Regras de Transformação Críticas

#### **Regra 1: Limpeza de Status de Cliente**
```python
# PROBLEMA: ERP mistura "Suspenso" (temporário) com "Cancelado" (definitivo)
# SOLUÇÃO: Criar flag binária

df_clientes['churn_real'] = df_clientes['status_cliente'].apply(
    lambda x: 1 if x == 'CANCELADO' else 0
)

df_clientes['churn_oculto'] = df_clientes['status_cliente'].apply(
    lambda x: 1 if x == 'SUSPENSO' else 0
)
```

#### **Regra 2: Cálculo de Share Individual (para ICIO)**
```python
# Calcular receita de cada cliente nos últimos 12 meses
df_fat_12m = df_faturamento[df_faturamento['data_emissao'] >= '2024-12-01']

receita_por_cliente = df_fat_12m.groupby('id_cliente')['valor_fatura'].sum()
receita_total = df_fat_12m['valor_fatura'].sum()

df_share = pd.DataFrame({
    'id_cliente': receita_por_cliente.index,
    'receita_12m': receita_por_cliente.values,
    'share_percentual': (receita_por_cliente.values / receita_total * 100)
}).sort_values('receita_12m', ascending=False)

# Identificar Top 20
df_top20 = df_share.head(20)
df_top20.to_csv('/CDL_DataLake/04_KPIS/kpi_icio_top20.csv', index=False)
```

#### **Regra 3: Separação de Receita Recorrente vs. Variável (IRR)**
```python
# Classificar tipo de receita
df_faturamento['tipo_receita_irr'] = df_faturamento['tipo_receita'].apply(
    lambda x: 'RECORRENTE' if x == 'MENSALIDADE' else 'VARIAVEL'
)

# Calcular IRR por tipo
irr_recorrente = df_faturamento[df_faturamento['tipo_receita_irr'] == 'RECORRENTE'].groupby('mes_referencia')['valor_fatura'].sum()
irr_variavel = df_faturamento[df_faturamento['tipo_receita_irr'] == 'VARIAVEL'].groupby('mes_referencia')['valor_fatura'].sum()
```

---

## 5. MODELO DIMENSIONAL (STAR SCHEMA)

```
                    ┌─────────────────────┐
                    │   FATO_RECEITA      │
                    ├─────────────────────┤
                    │ id_fato (PK)        │
                    │ id_cliente (FK)     │───┐
                    │ id_produto (FK)     │───┼───┐
                    │ id_tempo (FK)       │───┼───┼───┐
                    │ valor_fatura        │   │   │   │
                    │ valor_recebido      │   │   │   │
                    │ status_fatura       │   │   │   │
                    └─────────────────────┘   │   │   │
                                              │   │   │
      ┌───────────────────────────────────────┘   │   │
      │                                           │   │
      ▼                                           │   │
┌─────────────────────┐                          │   │
│   DIM_CLIENTE       │                          │   │
├─────────────────────┤                          │   │
│ id_cliente (PK)     │                          │   │
│ razao_social        │                          │   │
│ cnpj                │                          │   │
│ status_cliente      │                          │   │
│ categoria           │                          │   │
│ churn_real (flag)   │                          │   │
│ churn_oculto (flag) │                          │   │
└─────────────────────┘                          │   │
                                                 │   │
                  ┌──────────────────────────────┘   │
                  │                                  │
                  ▼                                  │
            ┌─────────────────────┐                 │
            │   DIM_PRODUTO       │                 │
            ├─────────────────────┤                 │
            │ id_produto (PK)     │                 │
            │ nome_produto        │                 │
            │ tipo_receita        │                 │
            │ categoria_irr       │                 │
            └─────────────────────┘                 │
                                                    │
                             ┌──────────────────────┘
                             │
                             ▼
                       ┌─────────────────────┐
                       │   DIM_TEMPO         │
                       ├─────────────────────┤
                       │ id_tempo (PK)       │
                       │ data_completa       │
                       │ ano                 │
                       │ mes                 │
                       │ trimestre           │
                       │ nome_mes            │
                       │ dia_semana          │
                       └─────────────────────┘
```

---

## 6. CRONOGRAMA DE ATUALIZAÇÃO

| Frequência | Processo | Ferramenta | Horário |
|------------|----------|------------|---------|
| **Diária** | Extração do ERP | Script Python/Power Query | 06:00 AM |
| **Diária** | Transformação Staging | Power Query | 06:30 AM |
| **Diária** | Carga Analytical | Power BI Dataset Refresh | 07:00 AM |
| **Semanal** | Recálculo Top 20 (ICIO) | SQL View Refresh | Segunda 08:00 AM |
| **Mensal** | Backup Data Lake | OneDrive Sync | 1º dia do mês |

---

## 7. CHECKLIST DE IMPLEMENTAÇÃO

### Fase 1: Setup Inicial (1 semana)
- [ ] Criar estrutura de pastas no OneDrive/Storage
- [ ] Mapear credenciais de acesso ao ERP (API/ODBC)
- [ ] Configurar extração inicial de tabelas (script Python ou Power Query)
- [ ] Validar dados brutos (comparar total com relatório ERP)

### Fase 2: Transformação (1 semana)
- [ ] Implementar regras de limpeza de status de cliente
- [ ] Criar tabela dimensional de tempo (dim_tempo)
- [ ] Aplicar cálculos de KPIs (IAR, ICIO, Burn Rate, Margem SPC)
- [ ] Gerar arquivos CSV pré-agregados para dashboards

### Fase 3: Testes (3 dias)
- [ ] Validar IAR de Nov/2025 = 1.01 (baseline)
- [ ] Validar ICIO Bemol = 12% (baseline)
- [ ] Validar Burn Rate Nov/2025 = -R$ 83.923 (baseline)
- [ ] Validar Estoque Suspensos = R$ 742.779 (baseline)

### Fase 4: Go-Live
- [ ] Conectar Power BI aos arquivos .parquet/.csv
- [ ] Configurar refresh automático
- [ ] Documentar processo de ETL para equipe de TI

---

## 8. CUSTOS ESTIMADOS

| Item | Ferramenta | Custo Mensal |
|------|------------|--------------|
| Storage (50GB) | OneDrive Business | R$ 20 (incluído M365) |
| ETL | Power Query / Python | R$ 0 (gratuito) |
| BI Tool | Power BI Desktop | R$ 0 (gratuito) |
| BI Cloud (Opcional) | Power BI Pro | R$ 55/usuário |
| **TOTAL** | | **R$ 20 - R$ 75** |

**Comparação**: Solução enterprise (Tableau + Snowflake) = R$ 5.000-15.000/mês

---

## PRÓXIMOS PASSOS

1. **Validar acesso ao ERP**: Confirmar que há API/ODBC disponível para extração
2. **Definir responsável técnico**: Quem executará o ETL? (Analista de BI interno ou externo?)
3. **Priorizar tabelas**: Se o ERP tiver 100+ tabelas, começar apenas com as 5 listadas acima
4. **Testar extração manual**: Exportar 1 mês de dados para validar estrutura

---

**Documento elaborado por**: Arquiteto de Soluções BI - Ecossistema de Inteligência CDL Manaus  
**Versão**: 1.0  
**Data**: Dezembro 2025
