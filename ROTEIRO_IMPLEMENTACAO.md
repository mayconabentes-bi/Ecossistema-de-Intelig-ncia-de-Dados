# ROTEIRO DE IMPLEMENTAÇÃO
## Ecossistema de Inteligência de Dados - CDL Manaus

---

## ÍNDICE
1. [Visão Executiva](#1-visão-executiva)
2. [Cronograma de Implementação (6 Semanas)](#2-cronograma-de-implementação-6-semanas)
3. [Fase 1: Preparação e Descoberta (Semana 1)](#3-fase-1-preparação-e-descoberta-semana-1)
4. [Fase 2: Configuração do Data Lake (Semana 2)](#4-fase-2-configuração-do-data-lake-semana-2)
5. [Fase 3: Construção dos Dashboards (Semanas 3-4)](#5-fase-3-construção-dos-dashboards-semanas-3-4)
6. [Fase 4: Sistema de Alertas (Semana 5)](#6-fase-4-sistema-de-alertas-semana-5)
7. [Fase 5: Testes e Go-Live (Semana 6)](#7-fase-5-testes-e-go-live-semana-6)
8. [Plano de Sustentação e Evolução](#8-plano-de-sustentação-e-evolução)
9. [Análise de Custos e ROI](#9-análise-de-custos-e-roi)
10. [Matriz RACI](#10-matriz-raci)

---

## 1. VISÃO EXECUTIVA

### 1.1 Objetivo do Projeto

Implementar um **Ecossistema de Inteligência de Dados em Tempo Real** que permita à Diretoria da CDL Manaus tomar decisões estratégicas **antes do fechamento do mês**, transformando a gestão de reativa para proativa.

---

### 1.2 Problema Atual vs. Solução Proposta

| Aspecto | ANTES (Situação Atual) | DEPOIS (Com o Ecossistema) |
|---------|------------------------|----------------------------|
| **Tomada de Decisão** | Retroativa (após fechamento do mês) | Preditiva (durante o mês) |
| **Formato de Relatórios** | PDF estático (manual) | Dashboard interativo (automático) |
| **Visibilidade de Crises** | Tardia (ex: Bemol já caiu 25%) | Antecipada (alerta na 1ª semana de queda) |
| **Análise de Margem** | Não monitorada | Acompanhamento diário |
| **Tempo de Resposta** | 30-45 dias (pós-mês) | Tempo real (mesmo dia) |
| **Custo Operacional** | Alto (analistas gerando PDF) | Baixo (automação) |

---

### 1.3 Benefícios Esperados (Primeiros 6 Meses)

**Financeiros**:
- ✅ Redução de 30% no tempo de inadimplência (alertas de cobrança)
- ✅ Recuperação de 40% do "Estoque de Suspensos" (R$ 297k de R$ 743k)
- ✅ Melhoria de 5-10% na Margem SPC (renegociação proativa)

**Operacionais**:
- ✅ Economia de 20h/mês de analistas (automação de relatórios)
- ✅ Reuniões de Diretoria com dados em tempo real
- ✅ Decisões baseadas em fatos, não em "achismos"

**Estratégicos**:
- ✅ Evitar perda de clientes Top 20 (retenção proativa)
- ✅ Identificar produtos não-rentáveis rapidamente
- ✅ Cultura data-driven na organização

---

### 1.4 Premissas Críticas

Para o sucesso do projeto, é essencial que:

1. ✅ **Acesso ao ERP**: CDL Manaus possua API ou ODBC do ERP financeiro
2. ✅ **Qualidade de Dados**: Tabelas do ERP estejam minimamente organizadas
3. ✅ **Patrocínio Executivo**: Diretoria apoie e utilize os dashboards
4. ✅ **Responsável Técnico**: 1 analista de BI dedicado (20h/semana) durante implementação

---

## 2. CRONOGRAMA DE IMPLEMENTAÇÃO (6 SEMANAS)

```
SEMANA 1        SEMANA 2        SEMANA 3        SEMANA 4        SEMANA 5        SEMANA 6
─────────       ─────────       ─────────       ─────────       ─────────       ─────────
PREPARAÇÃO      DATA LAKE       DASHBOARD A     DASHBOARD B     ALERTAS         TESTES
& DESCOBERTA                    (Pulmão)        (Motor)         & DASHBOARD C   & GO-LIVE
                                                                (Máquina)
│                │               │               │               │               │
├─ Kickoff       ├─ Estrutura   ├─ Painel A     ├─ Painel B     ├─ Regra 1      ├─ Testes UAT
├─ Mapeamento   ├─ ETL          ├─ KPIs 1-6     ├─ KPIs 7-12    ├─ Regra 2      ├─ Ajustes
│  ERP          ├─ Validação    │                │  (Gráfico     ├─ Regra 3      ├─ Treinamento
├─ Infraestr.   │                │                │   Batalha     ├─ Painel C     ├─ Go-Live
└─ Requisitos   └─ Baseline     └─ Testes       │   Naval)      └─ KPIs 13-18   └─ Monitoramento
                                                 └─ Testes
```

**Duração Total**: 6 semanas (42 dias corridos)  
**Esforço Estimado**: 120 horas (20h/semana × 6 semanas)  
**Data de Início Sugerida**: 1ª semana de Janeiro/2026 (após férias)  
**Go-Live**: Meados de Fevereiro/2026

---

## 3. FASE 1: PREPARAÇÃO E DESCOBERTA (SEMANA 1)

### 3.1 Objetivos

- Mapear tabelas do ERP necessárias
- Validar qualidade dos dados
- Configurar infraestrutura básica
- Definir responsabilidades

---

### 3.2 Atividades Detalhadas

#### **DIA 1-2: Kickoff e Mapeamento do ERP**

**Reunião de Kickoff (2h)**:
- Participantes: Diretoria + Responsável TI + Analista BI
- Agenda:
  1. Apresentação do projeto (objetivos, cronograma)
  2. Definição de expectativas
  3. Nomeação de responsáveis
  4. Definição de horários de reunião semanal (status)

**Checklist de Mapeamento do ERP**:
```
☐ Identificar nome e versão do ERP utilizado
   └─ Ex: SAP, TOTVS, Oracle, sistema próprio?
   
☐ Validar existência das 5 tabelas essenciais:
   ├─ ☐ tb_faturamento (ou equivalente)
   ├─ ☐ tb_recebimentos (ou equivalente)
   ├─ ☐ tb_clientes (ou equivalente)
   ├─ ☐ tb_despesas_operacionais (ou equivalente)
   └─ ☐ tb_custos_variaveis (ou equivalente)
   
☐ Obter credenciais de acesso (somente leitura):
   ├─ Usuário: _____________
   ├─ Senha: _____________
   ├─ Servidor: _____________
   └─ Tipo de conexão: [ ] API  [ ] ODBC  [ ] Export CSV
   
☐ Validar permissões de segurança:
   └─ Analista BI pode acessar dados financeiros sensíveis? (aprovar com Diretoria)
```

**Entregável**:
- Documento "Mapeamento_ERP_CDL.xlsx" com:
  - Nome real das tabelas
  - Campos disponíveis
  - Amostra de dados (10 linhas)

---

#### **DIA 3-4: Validação de Qualidade de Dados**

**Queries de Validação** (executar no ERP):

```sql
-- VALIDAÇÃO 1: Faturamento tem dados dos últimos 12 meses?
SELECT 
    DATE_FORMAT(data_emissao, '%Y-%m') AS mes,
    COUNT(*) AS qtd_faturas,
    SUM(valor_fatura) AS total_faturado
FROM tb_faturamento
WHERE data_emissao >= CURDATE() - INTERVAL 12 MONTH
GROUP BY mes
ORDER BY mes;

-- VALIDAÇÃO 2: Status de cliente está normalizado?
SELECT 
    status_cliente,
    COUNT(*) AS qtd
FROM tb_clientes
GROUP BY status_cliente;
-- Resultado esperado: 'ATIVO', 'SUSPENSO', 'CANCELADO'

-- VALIDAÇÃO 3: Recebimentos batem com faturamento (IAR)?
SELECT 
    '2025-11' AS mes,
    (SELECT SUM(valor_fatura) FROM tb_faturamento WHERE mes_referencia = '2025-11') AS faturamento,
    (SELECT SUM(valor_recebido) FROM tb_recebimentos WHERE DATE_FORMAT(data_recebimento, '%Y-%m') = '2025-11') AS recebimento,
    ROUND(
        (SELECT SUM(valor_fatura) FROM tb_faturamento WHERE mes_referencia = '2025-11') / 
        (SELECT SUM(valor_recebido) FROM tb_recebimentos WHERE DATE_FORMAT(data_recebimento, '%Y-%m') = '2025-11'),
        2
    ) AS IAR;
-- Resultado esperado: IAR = 1,01 (conforme baseline Nov/2025)

-- VALIDAÇÃO 4: Identificar Top 20 (ICIO)
SELECT 
    c.razao_social,
    SUM(f.valor_fatura) AS receita_12m
FROM tb_clientes c
JOIN tb_faturamento f ON c.id_cliente = f.id_cliente
WHERE f.data_emissao >= CURDATE() - INTERVAL 12 MONTH
GROUP BY c.razao_social
ORDER BY receita_12m DESC
LIMIT 20;
-- Resultado esperado: Bemol aparece no Top 1 ou Top 2
```

**Checklist de Qualidade**:
```
☐ Dados históricos disponíveis (mínimo 12 meses)
☐ Status de cliente está padronizado
☐ IAR calculado = 1,01 (validar baseline)
☐ Top 20 clientes identificados (Bemol, Nova Era, etc.)
☐ Custos variáveis existem na base (para Margem SPC)
```

**Entregável**:
- Relatório "Validacao_Dados_CDL.pdf" com:
  - ✅ Aprovado / ❌ Problemas identificados
  - Ações corretivas (se necessário)

---

#### **DIA 5: Configuração de Infraestrutura**

**Opção A: OneDrive + Power BI Desktop (Recomendado - Baixo Custo)**

1. **Criar estrutura de pastas no OneDrive**:
```
OneDrive > CDL_DataLake/
├── 01_RAW/
├── 02_STAGING/
├── 03_ANALYTICAL/
└── 04_KPIS/
```

2. **Instalar ferramentas**:
   - Power BI Desktop (gratuito): https://powerbi.microsoft.com/desktop/
   - Python 3.8+ (se optar por ETL em Python): https://www.python.org/downloads/

3. **Configurar acesso ao ERP**:
   - Se API: Obter token de autenticação
   - Se ODBC: Instalar driver ODBC do ERP
   - Se CSV: Configurar export automático (cron job)

**Opção B: Azure Data Lake + Power BI Service (Maior Escala)**

Custos adicionais: ~R$ 200/mês (Azure Storage + Power BI Pro)

**Checklist**:
```
☐ Estrutura de pastas criada
☐ Power BI Desktop instalado
☐ Conexão com ERP testada (conseguiu extrair 1 tabela?)
☐ Backup configurado (OneDrive sincroniza automaticamente)
```

---

### 3.3 Entregáveis da Semana 1

| # | Documento | Responsável | Status |
|---|-----------|-------------|--------|
| 1 | Mapeamento_ERP_CDL.xlsx | TI + BI | ☐ |
| 2 | Validacao_Dados_CDL.pdf | BI | ☐ |
| 3 | Infraestrutura_Configurada (OneDrive) | BI | ☐ |
| 4 | Credenciais_Acesso.txt (seguro) | TI | ☐ |

---

## 4. FASE 2: CONFIGURAÇÃO DO DATA LAKE (SEMANA 2)

### 4.1 Objetivos

- Extrair dados do ERP para o Data Lake
- Transformar dados (limpeza e normalização)
- Criar modelo dimensional (Star Schema)
- Validar baseline (IAR, ICIO, Burn Rate)

---

### 4.2 Atividades Detalhadas

#### **DIA 1-2: Extração Inicial (RAW Layer)**

**Método 1: Power Query (Excel/Power BI)**

1. Abrir Power BI Desktop
2. Get Data > Database > SQL Server (ou tipo do ERP)
3. Conectar e extrair as 5 tabelas:
   - tb_faturamento
   - tb_recebimentos
   - tb_clientes
   - tb_despesas_operacionais
   - tb_custos_variaveis

4. Salvar como `.pbix` (Power BI) ou exportar para CSV

**Método 2: Python Script**

```python
import pymysql
import pandas as pd
from datetime import datetime

# Configuração
DB_CONFIG = {
    'host': 'seu_erp.com',
    'user': 'cdl_bi',
    'password': 'senha',
    'database': 'cdl_manaus'
}

# Conectar
conn = pymysql.connect(**DB_CONFIG)

# Extrair tabelas
tabelas = ['tb_faturamento', 'tb_recebimentos', 'tb_clientes', 
           'tb_despesas_operacionais', 'tb_custos_variaveis']

for tabela in tabelas:
    print(f"Extraindo {tabela}...")
    df = pd.read_sql(f"SELECT * FROM {tabela}", conn)
    
    # Salvar em RAW
    caminho = f"/OneDrive/CDL_DataLake/01_RAW/{tabela}_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(caminho, index=False)
    print(f"✅ {len(df)} linhas extraídas")

conn.close()
```

**Checklist**:
```
☐ tb_faturamento extraída (últimos 12-24 meses)
☐ tb_recebimentos extraída
☐ tb_clientes extraída
☐ tb_despesas_operacionais extraída
☐ tb_custos_variaveis extraída
```

---

#### **DIA 3: Transformação (STAGING Layer)**

**Regras de Transformação**:

1. **Normalizar Status de Cliente**:
```python
df_clientes['status_normalizado'] = df_clientes['status_cliente'].apply(
    lambda x: 'SUSPENSO' if x in ['SUSPENSO', 'BLOQUEADO'] else
              'CANCELADO' if x in ['CANCELADO', 'INATIVO'] else
              'ATIVO'
)
```

2. **Criar Dimensão Tempo** (se não existir no ERP):
```python
import pandas as pd

# Gerar calendário 2023-2026
datas = pd.date_range(start='2023-01-01', end='2026-12-31', freq='D')

dim_tempo = pd.DataFrame({
    'data_completa': datas,
    'ano': datas.year,
    'mes': datas.month,
    'trimestre': datas.quarter,
    'nome_mes': datas.strftime('%B'),
    'dia_semana': datas.strftime('%A'),
    'ano_mes': datas.strftime('%Y-%m')
})

dim_tempo.to_parquet('/OneDrive/CDL_DataLake/02_STAGING/dim_tempo.parquet')
```

3. **Classificar Tipo de Receita (IRR)**:
```python
def classificar_receita(tipo):
    if tipo == 'MENSALIDADE':
        return 'RECORRENTE'
    else:
        return 'VARIAVEL'

df_faturamento['categoria_irr'] = df_faturamento['tipo_receita'].apply(classificar_receita)
```

**Checklist**:
```
☐ Status de cliente normalizado
☐ dim_tempo criada
☐ Categoria IRR adicionada ao faturamento
☐ Dados salvos em /02_STAGING/ (formato .parquet)
```

---

#### **DIA 4: Modelagem Dimensional (ANALYTICAL Layer)**

**Criar Star Schema**:

```python
# FATO_RECEITA (Grain: 1 linha por fatura)
fato_receita = df_faturamento.merge(
    df_clientes[['id_cliente', 'razao_social', 'status_normalizado']], 
    on='id_cliente'
).merge(
    df_recebimentos[['id_fatura', 'valor_recebido', 'data_recebimento']],
    on='id_fatura',
    how='left'
)[['id_fatura', 'id_cliente', 'data_emissao', 'valor_fatura', 
   'valor_recebido', 'tipo_receita', 'status_fatura', 'categoria_irr']]

fato_receita.to_parquet('/OneDrive/CDL_DataLake/03_ANALYTICAL/fato_receita.parquet')

# DIM_CLIENTE
dim_cliente = df_clientes[[
    'id_cliente', 'razao_social', 'cnpj', 'status_normalizado', 
    'categoria', 'data_adesao'
]]
dim_cliente.to_parquet('/OneDrive/CDL_DataLake/03_ANALYTICAL/dim_cliente.parquet')

# DIM_PRODUTO (se houver tabela de produtos no ERP)
# Caso contrário, criar manualmente:
dim_produto = pd.DataFrame({
    'id_produto': [1, 2, 3, 4, 5],
    'nome_produto': ['Mensalidade', 'Consulta SPC', 'Certificado Digital', 
                     'SPC Score', 'Outros'],
    'tipo_receita': ['MENSALIDADE', 'CONSULTA_SPC', 'CERTIFICADO', 
                     'SPC_SCORE', 'OUTROS'],
    'categoria_irr': ['RECORRENTE', 'VARIAVEL', 'VARIAVEL', 'VARIAVEL', 'VARIAVEL']
})
dim_produto.to_parquet('/OneDrive/CDL_DataLake/03_ANALYTICAL/dim_produto.parquet')
```

**Checklist**:
```
☐ fato_receita criada (todas as faturas)
☐ dim_cliente criada
☐ dim_produto criada
☐ dim_tempo criada (já foi na etapa anterior)
☐ Arquivos salvos em /03_ANALYTICAL/
```

---

#### **DIA 5: Validação de Baseline**

**Recalcular KPIs de Nov/2025 para validar**:

```python
import pandas as pd

# Carregar dados
fato = pd.read_parquet('/OneDrive/CDL_DataLake/03_ANALYTICAL/fato_receita.parquet')

# 1. Validar IAR (Esperado: 1,01)
fat_nov = fato[fato['data_emissao'].dt.strftime('%Y-%m') == '2025-11']['valor_fatura'].sum()
rec_nov = fato[fato['data_recebimento'].dt.strftime('%Y-%m') == '2025-11']['valor_recebido'].sum()
iar_calculado = fat_nov / rec_nov
print(f"IAR Nov/2025: {iar_calculado:.2f} (Esperado: 1.01)")

# 2. Validar ICIO (Esperado: Bemol ~12%)
top20 = fato.groupby('id_cliente')['valor_fatura'].sum().nlargest(20)
icio = (top20.sum() / fato['valor_fatura'].sum()) * 100
print(f"ICIO: {icio:.1f}% (Esperado: ~45%)")

# 3. Validar Burn Rate (Esperado: -R$ 83.923)
# (Precisa dos dados de tb_despesas_operacionais)
```

**Checklist**:
```
☐ IAR = 1,01 ±0.05 (tolerância)
☐ Top 20 identificados (Bemol aparece?)
☐ Burn Rate Nov = negativo (aproximadamente -R$ 83k)
☐ Estoque Suspensos = ~R$ 743k
```

**Se validações falharem**: Revisar mapeamento de dados da Fase 1.

---

### 4.3 Entregáveis da Semana 2

| # | Entregável | Status |
|---|------------|--------|
| 1 | Dados extraídos (01_RAW) | ☐ |
| 2 | Dados transformados (02_STAGING) | ☐ |
| 3 | Modelo dimensional (03_ANALYTICAL) | ☐ |
| 4 | Validação de baseline aprovada | ☐ |

---

## 5. FASE 3: CONSTRUÇÃO DOS DASHBOARDS (SEMANAS 3-4)

### 5.1 Objetivos

- Construir os 3 painéis no Power BI
- Implementar todos os KPIs (18 ao total)
- Aplicar visual design (paleta CDL Manaus)
- Validar com stakeholders

---

### 5.2 SEMANA 3: Painéis A e B

#### **DIA 1-3: PAINEL A - "O PULMÃO"**

**Passos no Power BI**:

1. **Criar Nova Página**:
   - Name: "Painel A - O Pulmão"
   - Background: Cinza Claro (#F8F9FA)

2. **Adicionar Cards KPIs 1-3** (Saldo, IAR, Projeção):
```dax
// Medida: Saldo de Caixa
Saldo_Caixa = 
SUM(fato_receita[valor_recebido]) - 
CALCULATE(SUM(fato_despesa[valor_despesa]))

// Medida: IAR
IAR = 
VAR Faturamento = SUM(fato_receita[valor_fatura])
VAR Arrecadacao = SUM(fato_receita[valor_recebido])
RETURN
DIVIDE(Faturamento, Arrecadacao, 0)
```

3. **Adicionar Gráfico Burn Rate** (Line Chart):
   - X-axis: dim_tempo[ano_mes]
   - Y-axis: Burn_Rate_Mensal (medida)
   - Filtro: Últimos 3 meses

4. **Adicionar Estoque Suspensos** (Card + Tabela):
   - Card: Total suspenso
   - Tabela: Top 5 clientes suspensos

5. **Aplicar Formatação**:
   - Cores: Verde/Amarelo/Vermelho (conditional formatting)
   - Fonte: Segoe UI
   - Ícones: 🫁 no título

**Validação**:
- [ ] IAR exibindo 1,01?
- [ ] Burn Rate mostrando tendência negativa?
- [ ] Estoque Suspensos = R$ 742.779?

---

#### **DIA 4-5: PAINEL B - "O MOTOR"**

**Feature Crítica: Gráfico "Batalha Naval"**

1. **Preparar dados**:
```dax
// Medida: Receita Semanal por Cliente
Receita_Semana = 
CALCULATE(
    SUM(fato_receita[valor_fatura]),
    FILTER(
        fato_receita,
        fato_receita[semana_ano] = MAX(fato_receita[semana_ano])
    )
)

// Medida: Média 4 Semanas
Media_4_Semanas = 
CALCULATE(
    AVERAGE(fato_receita[valor_fatura]),
    DATESINPERIOD(dim_tempo[data_completa], MAX(dim_tempo[data_completa]), -4, WEEK)
)

// Medida: Variação %
Variacao_Pct = 
VAR Atual = [Receita_Semana]
VAR Media = [Media_4_Semanas]
RETURN
DIVIDE(Atual - Media, Media, 0) * 100

// Medida: Status Visual
Status_Semana = 
VAR Var = [Variacao_Pct]
RETURN
IF(Var >= -5, "🟢",
   IF(Var >= -10, "🟡", "🔴"))
```

2. **Criar Matrix Visual**:
   - Rows: dim_cliente[razao_social] (Top 20 apenas)
   - Columns: Semana (1, 2, 3, 4)
   - Values: Status_Semana

3. **Aplicar Conditional Formatting**:
   - Background color por status
   - Tooltip: Exibir valor exato + variação %

**Validação**:
- [ ] Bemol aparece com 🔴🔴 nas semanas 3 e 4?
- [ ] Top 20 clientes visíveis?
- [ ] ICIO calculado corretamente?

---

### 5.3 SEMANA 4: Painel C

#### **DIA 1-3: PAINEL C - "A MÁQUINA"**

1. **Adicionar Tabela de Margem por Produto**:
```dax
// Medida: Margem de Contribuição
Margem_Contribuicao = 
VAR Receita = SUM(fato_receita[valor_fatura])
VAR Custo = SUM(fato_custo[custo_insumo])
RETURN
DIVIDE(Receita - Custo, Receita, 0) * 100
```

2. **Adicionar Gráfico de Margem SPC** (Line Chart):
   - X-axis: Últimos 6 meses
   - Y-axis: Margem %
   - Linha de Referência: 60% (meta)

3. **Adicionar Área Chart** (Custo vs Receita):
   - Série 1: Receita Total
   - Série 2: Custo Variável
   - Preenchimento: Área entre as curvas

**Validação**:
- [ ] Margem SPC = 62,3%?
- [ ] Certificado Digital mostrando margem baixa (23%)?
- [ ] Gráficos com paleta CDL Manaus?

---

#### **DIA 4-5: Testes e Ajustes**

**Checklist de Qualidade**:
```
FUNCIONALIDADE:
☐ Todos os 18 KPIs estão calculando corretamente?
☐ Filtros (slicers) funcionam em todos os painéis?
☐ Navegação entre painéis (tabs) funciona?

VISUAL:
☐ Paleta de cores CDL Manaus aplicada?
☐ Conditional formatting (verde/amarelo/vermelho) aplicado?
☐ Ícones (🫁⚙️🏭) nos títulos dos painéis?

PERFORMANCE:
☐ Dashboards carregam em <5 segundos?
☐ Filtros respondem em <2 segundos?
```

---

### 5.4 Entregáveis das Semanas 3-4

| # | Entregável | Status |
|---|------------|--------|
| 1 | Painel A (O Pulmão) completo | ☐ |
| 2 | Painel B (O Motor) + Batalha Naval | ☐ |
| 3 | Painel C (A Máquina) completo | ☐ |
| 4 | Arquivo .pbix (Power BI) | ☐ |

---

## 6. FASE 4: SISTEMA DE ALERTAS (SEMANA 5)

### 6.1 Objetivos

- Configurar 3 alertas principais (ver SISTEMA_ALERTAS.md)
- Testar envio de WhatsApp
- Validar destinatários

---

### 6.2 Atividades

#### **DIA 1-2: Configurar Power Automate**

**Criar Flow 1: Queda Cliente Top 20**

1. Acessar https://flow.microsoft.com
2. Create > Scheduled cloud flow
3. Configurar:
   - Name: ALERT_001_Queda_Cliente_Top20
   - Recurrence: Every 2 hours (8AM-6PM, weekdays)
4. Add action: SQL Server > Execute SQL query
   - Query: (copiar da SISTEMA_ALERTAS.md seção 2.2)
5. Add action: Condition
   - If: length(body('Execute_SQL')) > 0
6. Add action: Twilio > Send WhatsApp Message
   - From: whatsapp:+14155238886
   - To: whatsapp:+5592XXXXXXXX
   - Body: (copiar template da SISTEMA_ALERTAS.md seção 2.3)

**Repetir para Flows 2 e 3**.

---

#### **DIA 3: Cadastrar Conta Twilio**

1. Acessar https://www.twilio.com/try-twilio
2. Criar conta gratuita (trial: US$ 15 grátis)
3. Ativar WhatsApp Sandbox:
   - Console > Messaging > Try WhatsApp
   - Enviar "join [código]" para +1 415 523 8886
4. Obter credenciais:
   - Account SID: AC...
   - Auth Token: ...
5. Configurar no Power Automate (adicionar conexão Twilio)

---

#### **DIA 4-5: Testes**

**Teste 1: Simular Queda de Cliente**

```sql
-- Reduzir faturamento da Bemol na semana atual (temporariamente)
UPDATE tb_faturamento
SET valor_fatura = valor_fatura * 0.6  -- Reduzir 40%
WHERE id_cliente = (SELECT id_cliente FROM tb_clientes WHERE razao_social = 'Bemol')
  AND YEARWEEK(data_emissao) = YEARWEEK(CURDATE());

-- Rodar flow manualmente (Power Automate > Run)
-- Verificar se WhatsApp chegou

-- REVERTER:
UPDATE tb_faturamento
SET valor_fatura = valor_fatura / 0.6  -- Restaurar
WHERE id_cliente = (SELECT id_cliente FROM tb_clientes WHERE razao_social = 'Bemol')
  AND YEARWEEK(data_emissao) = YEARWEEK(CURDATE());
```

**Checklist**:
```
☐ Alerta 1 (Queda Cliente) funcionando?
☐ Alerta 2 (Burn Rate) funcionando?
☐ Alerta 3 (Margem SPC) funcionando?
☐ WhatsApp chegando corretamente?
☐ E-mails de backup configurados?
```

---

### 6.3 Entregáveis da Semana 5

| # | Entregável | Status |
|---|------------|--------|
| 1 | 3 Flows Power Automate configurados | ☐ |
| 2 | Conta Twilio ativada | ☐ |
| 3 | Testes de alertas aprovados | ☐ |
| 4 | Destinatários cadastrados | ☐ |

---

## 7. FASE 5: TESTES E GO-LIVE (SEMANA 6)

### 7.1 Objetivos

- Testes de aceitação com usuários (UAT)
- Ajustes finais
- Treinamento da Diretoria
- Go-Live

---

### 7.2 Atividades

#### **DIA 1-2: Testes UAT (User Acceptance Testing)**

**Participantes**:
- Diretor Financeiro
- Diretor Comercial
- Diretor de Operações
- Analista BI

**Roteiro de Teste**:
```
PAINEL A:
☐ Visualizar Saldo de Caixa atual
☐ Confirmar IAR de Nov/2025 = 1,01
☐ Analisar tendência Burn Rate (3 meses)
☐ Identificar Top 5 clientes suspensos
☐ Filtrar por período (slicer)

PAINEL B:
☐ Verificar ICIO (concentração Top 20)
☐ Analisar "Batalha Naval" (Bemol em queda?)
☐ Ver Share of Wallet do Top 5
☐ Verificar movimentação de carteira (entradas/saídas)
☐ Filtrar por categoria de cliente

PAINEL C:
☐ Verificar Margem SPC (esperado: 62,3%)
☐ Analisar tabela de margem por produto
☐ Ver evolução da margem (6 meses)
☐ Verificar performance de Certificado Digital vs. meta

ALERTAS:
☐ Simular alerta e confirmar recebimento no WhatsApp
```

**Feedback**:
- Coletar sugestões de melhorias
- Priorizar apenas ajustes críticos (restante vai para backlog)

---

#### **DIA 3: Ajustes Finais**

Implementar apenas ajustes críticos identificados no UAT:
- Correções de cálculos (se houver)
- Ajustes de layout (ex: aumentar fonte)
- Correções de filtros

---

#### **DIA 4: Treinamento**

**Sessão de Treinamento (2h)**:

**Agenda**:
1. Visão geral do ecossistema (15 min)
2. Navegação nos 3 painéis (30 min)
3. Como interpretar KPIs (30 min)
4. Como responder a alertas (15 min)
5. Boas práticas de uso (15 min)
6. Q&A (15 min)

**Material**:
- Guia rápido (1 página por painel)
- Vídeo tutorial (5-10 min)
- Contato para suporte (Analista BI)

---

#### **DIA 5: Go-Live**

**Checklist de Go-Live**:
```
PRÉ-GO-LIVE:
☐ Backup dos arquivos .pbix
☐ Documentação completa (README.md)
☐ Credenciais documentadas (seguras)
☐ Plano de contingência (se algo der errado)

GO-LIVE:
☐ Publicar dashboards no Power BI Service (se aplicável)
☐ Configurar refresh schedule (horário: 7h diariamente)
☐ Ativar alertas (Power Automate)
☐ Enviar e-mail de comunicação para Diretoria

PÓS-GO-LIVE:
☐ Monitorar por 48h (alertas funcionando?)
☐ Coletar feedback inicial
☐ Agendar reunião de retrospectiva (1 semana após)
```

---

### 7.3 Entregáveis da Semana 6

| # | Entregável | Status |
|---|------------|--------|
| 1 | UAT aprovado | ☐ |
| 2 | Ajustes finais implementados | ☐ |
| 3 | Treinamento realizado | ☐ |
| 4 | Sistema em produção (Go-Live) | ☐ |
| 5 | Documentação completa | ☐ |

---

## 8. PLANO DE SUSTENTAÇÃO E EVOLUÇÃO

### 8.1 Atividades Recorrentes (Pós Go-Live)

| Atividade | Frequência | Responsável | Tempo |
|-----------|------------|-------------|-------|
| Monitorar refresh dos dados | Diária | Analista BI | 5 min |
| Verificar alertas disparados | Diária | Analista BI | 10 min |
| Revisar KPIs com Diretoria | Semanal | Diretoria | 30 min |
| Atualizar metadados (novos clientes) | Mensal | Analista BI | 1h |
| Backup dos dados | Mensal | TI | 15 min |

---

### 8.2 Roadmap de Evolução (Próximos 6 Meses)

**MÊS 1-2 (Estabilização)**:
- Ajustes finos baseados em feedback
- Adicionar 2-3 alertas complementares (Regras 4, 5, 6)
- Integrar dados de CRM (última interação com cliente)

**MÊS 3-4 (Expansão)**:
- Adicionar Painel D: "Operacional" (Eficiência interna)
- Integrar dados de RH (custo de folha)
- Criar análise preditiva (forecast de receita)

**MÊS 5-6 (Inteligência Avançada)**:
- Machine Learning: Prever churn de clientes
- Análise de cohort (geração de clientes)
- Dashboard mobile (Power BI App)

---

## 9. ANÁLISE DE CUSTOS E ROI

### 9.1 Investimento Inicial (One-Time)

| Item | Custo | Obs |
|------|-------|-----|
| Analista BI (120h × R$ 100/h) | R$ 12.000 | Implementação (6 semanas) |
| Licenças Power BI Pro (3 usuários) | R$ 165 | Primeiro mês (R$ 55/usuário) |
| Conta Twilio (WhatsApp) | R$ 50 | Créditos iniciais |
| **TOTAL INICIAL** | **R$ 12.215** | |

---

### 9.2 Custos Recorrentes (Mensal)

| Item | Custo/mês |
|------|-----------|
| Power BI Pro (3 usuários) | R$ 165 |
| OneDrive Business (50GB) | R$ 20 |
| Twilio WhatsApp API (~1.000 msgs) | R$ 100 |
| Manutenção (Analista BI 5h/mês) | R$ 500 |
| **TOTAL MENSAL** | **R$ 785** |

**Custo Anual**: R$ 785 × 12 = **R$ 9.420**

---

### 9.3 Comparação com Alternativas

| Solução | Custo Anual | Limitações |
|---------|-------------|------------|
| **Solução CDL (Power BI)** | R$ 9.420 | ✅ Baixo custo, customizável |
| Tableau + Snowflake | R$ 60.000+ | ❌ Alto custo, overkill para CDL |
| Consultoria BI (on-demand) | R$ 30.000+ | ❌ Dependência externa |
| Planilhas Excel manuais | R$ 0 | ❌ Não é tempo real, propenso a erros |

---

### 9.4 ROI Projetado (12 Meses)

**Benefícios Quantificáveis**:

| Benefício | Valor Anual | Fonte |
|-----------|-------------|-------|
| Recuperação Estoque Suspensos (40%) | R$ 297.000 | 40% de R$ 743k |
| Redução Inadimplência (5% a menos) | R$ 120.000 | Cobrança mais eficiente |
| Retenção de 1 cliente Top 20 | R$ 150.000 | Bemol (R$ 150k/ano) |
| Economia analistas (20h/mês) | R$ 24.000 | R$ 100/h × 20h × 12 meses |
| **TOTAL BENEFÍCIOS** | **R$ 591.000** | |

**Custos Totais** (Inicial + 12 meses):
- Investimento Inicial: R$ 12.215
- Custos Recorrentes: R$ 9.420
- **TOTAL CUSTOS**: R$ 21.635

**ROI**:
```
ROI = (Benefícios - Custos) / Custos × 100
ROI = (R$ 591.000 - R$ 21.635) / R$ 21.635 × 100
ROI = 2.632%
```

**Payback**: < 2 meses (recuperação do investimento em 45-60 dias)

---

## 10. MATRIZ RACI

**Legenda**:
- **R** (Responsible): Quem executa a tarefa
- **A** (Accountable): Quem aprova/decide
- **C** (Consulted): Quem deve ser consultado
- **I** (Informed): Quem deve ser informado

| Atividade | Analista BI | Dir. TI | Dir. Financeiro | Dir. Comercial | Dir. Presidente |
|-----------|-------------|---------|-----------------|----------------|-----------------|
| **Fase 1: Preparação** |
| Mapeamento ERP | R | C | I | I | A |
| Validação de Dados | R | C | C | I | I |
| Configurar Infraestrutura | R | A | I | I | I |
| **Fase 2: Data Lake** |
| Extração de Dados | R | C | I | I | I |
| Transformação | R | C | I | I | I |
| Validação Baseline | R | I | C | C | A |
| **Fase 3: Dashboards** |
| Construir Painel A | R | I | A | I | C |
| Construir Painel B | R | I | I | A | C |
| Construir Painel C | R | I | A | I | C |
| Testes Visuais | R | I | C | C | A |
| **Fase 4: Alertas** |
| Configurar Power Automate | R | C | I | I | A |
| Cadastrar Twilio | R | A | I | I | I |
| Testes de Alertas | R | C | C | C | A |
| **Fase 5: Go-Live** |
| UAT | C | I | R | R | A |
| Treinamento | R | I | C | C | C |
| Go-Live | R | A | I | I | I |

---

## ANEXOS

### ANEXO A: Checklist de Pré-Requisitos

Antes de iniciar o projeto, confirmar:

```
TÉCNICO:
☐ ERP possui API ou ODBC funcional
☐ Dados históricos disponíveis (mínimo 12 meses)
☐ Existe servidor/VM para rodar scripts (se Python)
☐ Rede permite acesso ao Power BI Service (não bloqueado)

ORGANIZACIONAL:
☐ Diretoria comprometida com uso dos dashboards
☐ Analista BI disponível 20h/semana (6 semanas)
☐ Orçamento aprovado (R$ 12k inicial + R$ 785/mês)
☐ Contatos de TI e áreas de negócio disponíveis

DADOS:
☐ Status de cliente está padronizado no ERP
☐ Custos variáveis são rastreados por produto
☐ Receitas estão classificadas por tipo (mensalidade, SPC, etc.)
```

---

### ANEXO B: Glossário de Termos

| Termo | Definição |
|-------|-----------|
| **IAR** | Índice de Arrecadação Real = Faturamento Contábil / Arrecadação de Caixa |
| **ICIO** | Índice de Concentração = % da receita do Top 20 clientes |
| **Burn Rate** | Resultado do Fluxo de Caixa Mensal (Entradas - Saídas) |
| **IRR** | Índice de Renovação de Receita (Recorrente vs. Variável) |
| **Churn Real** | % clientes cancelados (excluindo suspensos) |
| **Churn Oculto** | Clientes suspensos (não cancelados formalmente) |
| **Margem de Contribuição** | (Receita - Custo Variável) / Receita |
| **Data Lake** | Repositório centralizado de dados brutos e processados |
| **ETL** | Extract, Transform, Load (processo de integração de dados) |
| **UAT** | User Acceptance Testing (testes de aceitação) |

---

## CONCLUSÃO

Este roteiro fornece um caminho claro e executável para implementar o Ecossistema de Inteligência de Dados da CDL Manaus em apenas **6 semanas**, com:

✅ **Baixo Custo**: R$ 12k inicial + R$ 785/mês  
✅ **Alto ROI**: 2.632% (payback em 2 meses)  
✅ **Decisões Proativas**: Alertas em tempo real  
✅ **Gestão Data-Driven**: 3 dashboards estratégicos  

**Próximo Passo**: Aprovar o projeto e iniciar Fase 1 (Semana 1).

---

**Documento elaborado por**: Arquiteto de Soluções BI - Ecossistema de Inteligência CDL Manaus  
**Versão**: 1.0  
**Data**: Dezembro 2025
