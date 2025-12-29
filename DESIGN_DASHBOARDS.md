# TAREFA 2: DESIGN DO DASHBOARD ESTRATÉGICO
## Especificação Visual e Funcional dos 3 Painéis

---

## ÍNDICE
1. [Visão Geral da Arquitetura](#1-visão-geral-da-arquitetura)
2. [Painel A: "O Pulmão" (Financeiro/Caixa)](#2-painel-a-o-pulmão-financeirocaixa)
3. [Painel B: "O Motor" (Comercial/Carteira)](#3-painel-b-o-motor-comercialcarteira)
4. [Painel C: "A Máquina" (Produtos/Margem)](#4-painel-c-a-máquina-productosmargem)
5. [Especificações Técnicas Power BI](#5-especificações-técnicas-power-bi)
6. [Paleta de Cores e Padrões Visuais](#6-paleta-de-cores-e-padrões-visuais)

---

## 1. VISÃO GERAL DA ARQUITETURA

### 1.1 Estrutura de Navegação

```
┌─────────────────────────────────────────────────────────────────┐
│  CDL MANAUS - ECOSSISTEMA DE INTELIGÊNCIA DE DADOS             │
│  ─────────────────────────────────────────────────────────────  │
│  [PAINEL A: O PULMÃO] [PAINEL B: O MOTOR] [PAINEL C: A MÁQUINA]│
└─────────────────────────────────────────────────────────────────┘
```

**Tecnologia**: Power BI com 3 páginas (tabs) ou Excel com 3 abas interligadas

**Refresh**: Automático a cada 1 hora (horário comercial: 8h-18h)

**Público-alvo**:
- **Painel A**: Diretor Financeiro + Gerente de Cobrança
- **Painel B**: Diretor Comercial + Gerente de Relacionamento
- **Painel C**: Diretor de Operações + Gerente de Produtos

---

## 2. PAINEL A: "O PULMÃO" (FINANCEIRO/CAIXA)

### 2.1 Objetivo Estratégico
**Pergunta Central**: *"Temos dinheiro para operar nos próximos 3 meses?"*

**Decisão Esperada**:
- Se Burn Rate negativo por 2 meses consecutivos → Acionar plano de contingência
- Se IAR > 1.05 → Intensificar cobrança ou rever política de crédito
- Se Estoque Suspensos > R$ 1M → Campanha de reativação

---

### 2.2 Layout Visual (Wireframe)

```
┌────────────────────────────────────────────────────────────────────┐
│  🫁 PAINEL A: O PULMÃO (Financeiro/Caixa)            Atualizado: 14h32 │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌─────────────────┬─────────────────┬─────────────────┐         │
│  │ SALDO CAIXA     │ IAR (Nov/25)    │ PROJEÇÃO 30d    │         │
│  │ R$ 1.245.680    │ 1,01            │ R$ 982.450      │         │
│  │ 🟢 +12% vs Out  │ 🟡 Atenção      │ 🔴 Insuficiente │         │
│  └─────────────────┴─────────────────┴─────────────────┘         │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ BURN RATE LÍQUIDO - TENDÊNCIA 3 MESES                       │ │
│  │                                                              │ │
│  │  R$                                                          │ │
│  │  200k ┌──────────────────────────────────────────┐          │ │
│  │       │         ╱╲                                │          │ │
│  │  100k │        ╱  ╲                               │          │ │
│  │       │       ╱    ╲                              │          │ │
│  │    0k ├──────────────╲─────────────────────────── │          │ │
│  │       │               ╲                           │          │ │
│  │ -100k │                ╲___________               │          │ │
│  │       │                            ▼              │          │ │
│  │       └──────────────────────────────────────────┘          │ │
│  │         SET/25    OUT/25    NOV/25                          │ │
│  │                                                              │ │
│  │  🟢 SET: +R$ 124.500   🟡 OUT: +R$ 45.200   🔴 NOV: -R$ 83.923 │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────┬────────────────────────────────────┐│
│  │ ESTOQUE DE SUSPENSOS     │ TOP 5 SUSPENSOS RECUPERÁVEIS      ││
│  │                          │                                    ││
│  │  R$ 742.779              │ 1. Magazine Luiza - R$ 124.500    ││
│  │  ━━━━━━━━━━━━━━━━━ 67%  │ 2. Bemol - R$ 98.200              ││
│  │  Meta: <R$ 500k          │ 3. Lojas Avenida - R$ 76.450      ││
│  │                          │ 4. Fast Shop - R$ 54.300          ││
│  │  127 clientes suspensos  │ 5. Ponto Frio - R$ 48.900         ││
│  │  Média: 145 dias         │                                    ││
│  │                          │ [BOTÃO: GERAR LISTA P/ COBRANÇA]  ││
│  └──────────────────────────┴────────────────────────────────────┘│
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ EFICIÊNCIA DE COBRANÇA (Inadimplência Real)                 │ │
│  │                                                              │ │
│  │  Taxa: 8,2% (excluindo suspensos)                          │ │
│  │  ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░                   │ │
│  │  Meta: <10%                                                 │ │
│  │                                                              │ │
│  │  Valor: R$ 245.600 (apenas clientes ATIVOS com atraso >30d) │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

### 2.3 KPIs e Especificações Técnicas

#### **KPI 1: Saldo de Caixa Atual**
- **Fórmula**: `SUM(tb_recebimentos.valor_recebido) - SUM(tb_despesas_operacionais.valor_despesa)`
- **Período**: Acumulado até data atual
- **Visual**: Card com ícone de 💰
- **Alerta**:
  - 🟢 Verde: Saldo > R$ 1M
  - 🟡 Amarelo: Saldo entre R$ 500k - R$ 1M
  - 🔴 Vermelho: Saldo < R$ 500k

#### **KPI 2: IAR (Índice de Arrecadação Real)**
- **Fórmula**: Ver ARQUITETURA_DADOS.md seção 2.1
- **Visual**: Card com velocímetro (gauge)
- **Escala**: 0.80 a 1.20
- **Alerta**:
  - 🟢 Verde: 0.95 ≤ IAR ≤ 1.00
  - 🟡 Amarelo: 1.00 < IAR ≤ 1.05
  - 🔴 Vermelho: IAR > 1.05

#### **KPI 3: Projeção de Caixa 30 dias**
- **Fórmula**: 
  ```
  Saldo Atual + 
  (Média Recebimentos 30d) - 
  (Média Despesas 30d)
  ```
- **Visual**: Card com trend line (linha de tendência)
- **Alerta**: Se < R$ 500k → 🔴 Vermelho

#### **KPI 4: Burn Rate Líquido (Tendência 3 meses)**
- **Fórmula**: Ver ARQUITETURA_DADOS.md seção 2.4
- **Visual**: Gráfico de linhas (line chart)
- **Eixo X**: Meses (SET, OUT, NOV)
- **Eixo Y**: Valores em R$ mil
- **Linha de Referência**: R$ 0 (linha tracejada vermelha)
- **Anotações**: Exibir valor exato em cada ponto

**DAX (Power BI)**:
```dax
Burn_Rate_Mensal = 
CALCULATE(
    SUM(tb_recebimentos[valor_recebido]) - SUM(tb_despesas_operacionais[valor_despesa]),
    DATESINPERIOD(dim_tempo[data_completa], MAX(dim_tempo[data_completa]), -3, MONTH)
)
```

#### **KPI 5: Estoque de Suspensos**
- **Fórmula**: Ver ARQUITETURA_DADOS.md seção 2.2 (SQL Estoque Suspensos)
- **Visual**: 
  - Parte superior: Card com barra de progresso (vs. meta R$ 500k)
  - Parte inferior: Tabela dos Top 5 clientes suspensos com maior valor travado
- **Colunas da Tabela**:
  1. Razão Social
  2. Valor Travado (R$)
  3. Dias Suspenso
  4. Última Interação (campo adicional do CRM)
- **Botão de Ação**: "Gerar Lista para Cobrança" → Exporta Excel com dados completos

#### **KPI 6: Eficiência de Cobrança (Inadimplência Real)**
- **Fórmula**: 
  ```
  (Valor Inadimplente Real / Faturamento Total) * 100
  
  Onde:
  Valor Inadimplente Real = SUM(faturas em atraso >30d)
  EXCLUINDO clientes com status = 'SUSPENSO'
  ```
- **Visual**: Barra de progresso horizontal com meta
- **Meta**: <10%
- **Alerta**:
  - 🟢 Verde: <10%
  - 🟡 Amarelo: 10-15%
  - 🔴 Vermelho: >15%

---

### 2.4 Filtros Dinâmicos (Slicers)

**Localização**: Topo direito do painel

```
┌─────────────────────────────────┐
│ FILTROS                         │
├─────────────────────────────────┤
│ Período: [Nov/25 ▼]            │
│ Forma Pgto: [Todas ▼]          │
│ Regional: [Todas ▼]            │
└─────────────────────────────────┘
```

---

## 3. PAINEL B: "O MOTOR" (COMERCIAL/CARTEIRA)

### 3.1 Objetivo Estratégico
**Pergunta Central**: *"Estamos perdendo clientes importantes? Qual o risco de concentração?"*

**Decisão Esperada**:
- Se Top 20 > 60% da receita → Diversificar carteira urgente
- Se cliente Top 5 cair >10% em 4 semanas → Visita comercial imediata
- Se churn real > 5%/mês → Rever experiência do cliente

---

### 3.2 Layout Visual (Wireframe)

```
┌────────────────────────────────────────────────────────────────────┐
│  ⚙️ PAINEL B: O MOTOR (Comercial/Carteira)          Atualizado: 14h32 │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌─────────────────┬─────────────────┬─────────────────┐         │
│  │ ICIO (Top 20)   │ CHURN REAL      │ NOVOS CLIENTES  │         │
│  │ 45,3%           │ 3,8%/mês        │ 12 em Nov/25    │         │
│  │ 🟡 Monitorar    │ 🟢 Saudável     │ 🟢 +20% vs Out  │         │
│  └─────────────────┴─────────────────┴─────────────────┘         │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ GRÁFICO "BATALHA NAVAL" - TOP 20 CLIENTES                   │ │
│  │ (Variação Semanal de Receita - Últimas 4 Semanas)          │ │
│  │                                                              │ │
│  │        SEM 1   SEM 2   SEM 3   SEM 4   TENDÊNCIA           │ │
│  │ 1. Bemol       🟢      🟡      🔴      🔴    ↘️ -25%        │ │
│  │ 2. Nova Era    🟢      🟢      🟢      🟢    → Estável      │ │
│  │ 3. TV Lar      🟢      🟢      🟡      🟢    → Estável      │ │
│  │ 4. Lojas Avenida 🟡    🟡      🟡      🟡    → Estável      │ │
│  │ 5. Fast Shop   🟢      🟢      🟢      🟡    ↘️ -8%         │ │
│  │ 6. Ponto Frio  🔴      🔴      🟡      🟢    ↗️ +15%        │ │
│  │ 7. Magazine Luiza 🟢   🟢      🟢      🟢    → Estável      │ │
│  │ 8. Riachuelo   🟡      🟡      🟡      🟡    → Estável      │ │
│  │ 9. C&A         🟢      🟡      🟡      🟡    ↘️ -5%         │ │
│  │ 10. Marisa     🟢      🟢      🟢      🟢    → Estável      │ │
│  │ 11-20. [...]   (Outros 10 clientes)                        │ │
│  │                                                              │ │
│  │ LEGENDA:                                                     │ │
│  │ 🟢 Crescimento ou estabilidade (+/- 5%)                     │ │
│  │ 🟡 Queda leve (5-10% vs média 4 semanas)                   │ │
│  │ 🔴 Queda crítica (>10% vs média 4 semanas)                 │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────┬────────────────────────────────────┐│
│  │ SHARE OF WALLET (Top 5)  │ MOVIMENTAÇÃO DE CARTEIRA          ││
│  │                          │                                    ││
│  │  🥇 Bemol        12,0%   │ Entradas (Nov/25): 12 clientes    ││
│  │  🥈 Nova Era     10,5%   │ Saídas (Nov/25): 8 clientes       ││
│  │  🥉 TV Lar       8,2%    │ Suspensos (Nov/25): 5 clientes    ││
│  │  4º Fast Shop    7,1%    │                                    ││
│  │  5º Ponto Frio   6,5%    │ Net Add Rate: +4 (🟢)             ││
│  │                          │                                    ││
│  │  [VER RANKING COMPLETO]  │ [DETALHES CHURNS]                 ││
│  └──────────────────────────┴────────────────────────────────────┘│
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ IRR - ÍNDICE DE RENOVAÇÃO DE RECEITA (12 MESES)            │ │
│  │                                                              │ │
│  │  ┌─────────────────┬─────────────────┐                     │ │
│  │  │ RECORRENTE      │ VARIÁVEL        │                     │ │
│  │  │ (Mensalidades)  │ (Consultas SPC) │                     │ │
│  │  ├─────────────────┼─────────────────┤                     │ │
│  │  │ R$ 1.250.000    │ R$ 850.000      │                     │ │
│  │  │ ██████████ 60%  │ ██████ 40%      │                     │ │
│  │  │ 🟢 +2% vs 2024  │ 🔴 -15% vs 2024 │                     │ │
│  │  └─────────────────┴─────────────────┘                     │ │
│  │                                                              │ │
│  │  ALERTA: Receita variável caindo. Clientes reduzindo       │ │
│  │          consultas ao SPC. Investigar concorrência.         │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

### 3.3 KPIs e Especificações Técnicas

#### **KPI 7: ICIO (Índice de Concentração)**
- **Fórmula**: Ver ARQUITETURA_DADOS.md seção 2.2
- **Visual**: Card com percentual
- **Alerta**:
  - 🟢 Verde: ICIO < 40%
  - 🟡 Amarelo: 40% ≤ ICIO ≤ 60%
  - 🔴 Vermelho: ICIO > 60%

#### **KPI 8: Churn Real**
- **Fórmula**:
  ```
  (Nº Clientes Cancelados no Mês / Total Clientes Ativos Início do Mês) * 100
  
  Excluindo status = 'SUSPENSO'
  ```
- **Visual**: Card com trend line (últimos 3 meses)
- **Alerta**:
  - 🟢 Verde: <5%
  - 🟡 Amarelo: 5-8%
  - 🔴 Vermelho: >8%

**DAX (Power BI)**:
```dax
Churn_Real = 
VAR ClientesAtivosInicio = 
    CALCULATE(
        DISTINCTCOUNT(tb_clientes[id_cliente]),
        tb_clientes[status_cliente] = "ATIVO",
        DATEADD(dim_tempo[data_completa], -1, MONTH)
    )
VAR ClientesCancelados = 
    CALCULATE(
        DISTINCTCOUNT(tb_clientes[id_cliente]),
        tb_clientes[status_cliente] = "CANCELADO",
        tb_clientes[data_cancelamento] >= STARTOFMONTH(dim_tempo[data_completa])
    )
RETURN
    DIVIDE(ClientesCancelados, ClientesAtivosInicio, 0) * 100
```

#### **KPI 9: Gráfico "Batalha Naval" (Feature Crítica)**

**Conceito**: Matriz visual mostrando performance semanal de cada cliente Top 20

**Estrutura de Dados Necessária**:
```sql
-- Criar tabela agregada semanal
WITH receita_semanal AS (
    SELECT 
        id_cliente,
        YEARWEEK(data_emissao) AS ano_semana,
        SUM(valor_fatura) AS receita_semana
    FROM tb_faturamento
    WHERE data_emissao >= CURDATE() - INTERVAL 4 WEEK
      AND status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
    GROUP BY id_cliente, ano_semana
),
media_4_semanas AS (
    SELECT 
        id_cliente,
        AVG(receita_semana) AS media_receita
    FROM receita_semanal
    GROUP BY id_cliente
),
variacao AS (
    SELECT 
        rs.id_cliente,
        rs.ano_semana,
        rs.receita_semana,
        m.media_receita,
        ((rs.receita_semana - m.media_receita) / m.media_receita * 100) AS perc_variacao,
        CASE 
            WHEN ((rs.receita_semana - m.media_receita) / m.media_receita * 100) >= -5 
                AND ((rs.receita_semana - m.media_receita) / m.media_receita * 100) <= 5 
                THEN '🟢'  -- Estável
            WHEN ((rs.receita_semana - m.media_receita) / m.media_receita * 100) < -5 
                AND ((rs.receita_semana - m.media_receita) / m.media_receita * 100) >= -10 
                THEN '🟡'  -- Queda leve
            WHEN ((rs.receita_semana - m.media_receita) / m.media_receita * 100) < -10 
                THEN '🔴'  -- Queda crítica
            ELSE '🟢'
        END AS status_semana
    FROM receita_semanal rs
    JOIN media_4_semanas m ON rs.id_cliente = m.id_cliente
)
SELECT 
    c.razao_social,
    v.ano_semana,
    v.receita_semana,
    v.perc_variacao,
    v.status_semana
FROM variacao v
JOIN tb_clientes c ON v.id_cliente = c.id_cliente
JOIN vw_top20_clientes t20 ON c.id_cliente = t20.id_cliente
ORDER BY t20.receita_12m DESC, v.ano_semana;
```

**Visual em Power BI**:
1. Usar "Matrix" visual
2. **Rows**: Razão Social (ordenado por receita desc)
3. **Columns**: Semana (1, 2, 3, 4)
4. **Values**: Status Semana (emoji 🟢🟡🔴)
5. **Conditional Formatting**: Background color baseado no status

**Visual em Excel**:
- Tabela dinâmica com formatação condicional
- Ícones personalizados (círculos verde/amarelo/vermelho)

#### **KPI 10: Share of Wallet (Top 5)**
- **Fórmula**: Ver ARQUITETURA_DADOS.md seção 2.2
- **Visual**: Lista ranqueada com medalhas (🥇🥈🥉)
- **Exibir**: Nome cliente + % da receita total

#### **KPI 11: Movimentação de Carteira**
- **Fórmula**:
  ```
  Entradas = COUNT(clientes com data_adesao no mês)
  Saídas = COUNT(clientes com data_cancelamento no mês)
  Suspensos = COUNT(clientes com data_suspensao no mês)
  Net Add Rate = Entradas - (Saídas + Suspensos)
  ```
- **Visual**: Card simples com valores numéricos
- **Alerta**:
  - 🟢 Verde: Net Add Rate > 0
  - 🔴 Vermelho: Net Add Rate < 0

#### **KPI 12: IRR (Índice de Renovação de Receita)**
- **Fórmula**:
  ```
  IRR Recorrente = SUM(receita_mensalidade_12m)
  IRR Variável = SUM(receita_consulta_spc_12m)
  ```
- **Visual**: Dois cards lado a lado com comparativo vs. ano anterior
- **Gráfico adicional**: Stacked bar chart mostrando evolução mensal dos 2 tipos

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
    tb_faturamento[tipo_receita] IN {"CONSULTA_SPC", "OUTROS"},
    DATESINPERIOD(dim_tempo[data_completa], MAX(dim_tempo[data_completa]), -12, MONTH)
)
```

---

### 3.4 Filtros Dinâmicos (Slicers)

```
┌─────────────────────────────────┐
│ FILTROS                         │
├─────────────────────────────────┤
│ Período: [Últimas 4 Semanas ▼] │
│ Categoria: [Todos ▼]           │
│   ☐ Grandes Varejistas         │
│   ☐ PME                        │
│   ☐ MEI                        │
└─────────────────────────────────┘
```

---

## 4. PAINEL C: "A MÁQUINA" (PRODUTOS/MARGEM)

### 4.1 Objetivo Estratégico
**Pergunta Central**: *"Nossos produtos são rentáveis? Precisamos ajustar preços ou cortar custos?"*

**Decisão Esperada**:
- Se Margem SPC < 60% → Negociar preço com fornecedor ou reajustar tarifa
- Se Certificado Digital < 80% da meta → Campanha promocional
- Se Custo Variável crescendo > 10%/mês → Revisar contratos

---

### 4.2 Layout Visual (Wireframe)

```
┌────────────────────────────────────────────────────────────────────┐
│  🏭 PAINEL C: A MÁQUINA (Produtos/Margem)           Atualizado: 14h32 │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌─────────────────┬─────────────────┬─────────────────┐         │
│  │ MARGEM SPC      │ CERT. DIGITAL   │ NOVOS PRODUTOS  │         │
│  │ 62,3%           │ R$ 124.500      │ R$ 45.200       │         │
│  │ 🟢 Acima Meta   │ 🟡 78% da Meta  │ 🟢 +35% vs Out  │         │
│  └─────────────────┴─────────────────┴─────────────────┘         │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ MARGEM DE CONTRIBUIÇÃO POR PRODUTO (Nov/25)                 │ │
│  │                                                              │ │
│  │  Produto             Receita    Custo     Margem   Status   │ │
│  │  ───────────────────────────────────────────────────────    │ │
│  │  Mensalidades       R$ 980k     R$ 120k   87,8%    🟢       │ │
│  │  Consulta SPC       R$ 650k     R$ 245k   62,3%    🟢       │ │
│  │  Certificado Digital R$ 124k    R$ 95k    23,4%    🔴       │ │
│  │  SPC Score          R$ 80k      R$ 48k    40,0%    🟡       │ │
│  │  Outros Serviços    R$ 45k      R$ 18k    60,0%    🟢       │ │
│  │  ───────────────────────────────────────────────────────    │ │
│  │  TOTAL              R$ 1.879k   R$ 526k   72,0%    🟢       │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────┬────────────────────────────────────┐│
│  │ EVOLUÇÃO MARGEM SPC      │ CUSTO VARIÁVEL vs RECEITA         ││
│  │ (Últimos 6 Meses)        │ (Tendência 2025)                  ││
│  │                          │                                    ││
│  │  %                       │  R$                                ││
│  │  80┌─────────────────┐   │ 2.5M┌──────────────────┐          ││
│  │    │     ╱─╲         │   │     │  ╱╱╱╱  Receita   │          ││
│  │  70│    ╱   ╲        │   │ 2.0M│ ╱╱╱╱             │          ││
│  │    │   ╱     ╲       │   │     │╱╱╱╱              │          ││
│  │  60├──╱───────╲─────►│   │ 1.5M├╱╱╱──────────────►│          ││
│  │    │              ▼  │   │     │╱╱  ▲              │          ││
│  │  50│                 │   │ 1.0M│╱  ╱╱  Custo Var. │          ││
│  │    └─────────────────┘   │     │  ╱╱               │          ││
│  │     J  J  A  S  O  N     │     └──────────────────┘          ││
│  │                          │      J F M A M J J A S O N D      ││
│  │  Meta: >60% (linha ref)  │                                    ││
│  └──────────────────────────┴────────────────────────────────────┘│
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ PERFORMANCE DE NOVOS PRODUTOS (2025)                        │ │
│  │                                                              │ │
│  │  ┌─────────────────────┬─────────┬──────────┬──────────┐   │ │
│  │  │ Produto             │ Lançado │ Vendas   │ vs Meta  │   │ │
│  │  ├─────────────────────┼─────────┼──────────┼──────────┤   │ │
│  │  │ SPC Score Premium   │ Mar/25  │ R$ 25k   │ 125% 🟢  │   │ │
│  │  │ Análise de Crédito  │ Jun/25  │ R$ 12k   │ 80% 🟡   │   │ │
│  │  │ Recuperação Express │ Set/25  │ R$ 8k    │ 60% 🔴   │   │ │
│  │  └─────────────────────┴─────────┴──────────┴──────────┘   │ │
│  │                                                              │ │
│  │  INSIGHT: "Recuperação Express" está abaixo. Revisar       │ │
│  │           estratégia de comunicação ou reduzir preço.       │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

### 4.3 KPIs e Especificações Técnicas

#### **KPI 13: Margem de Contribuição SPC**
- **Fórmula**: Ver ARQUITETURA_DADOS.md seção 2.3
- **Visual**: Card com percentual
- **Alerta**:
  - 🟢 Verde: Margem > 70%
  - 🟡 Amarelo: 60% ≤ Margem ≤ 70%
  - 🔴 Vermelho: Margem < 60%

#### **KPI 14: Vendas Certificado Digital**
- **Fórmula**:
  ```
  SUM(tb_faturamento.valor_fatura WHERE tipo_receita = 'CERTIFICADO')
  ```
- **Visual**: Card com comparação vs. meta mensal
- **Meta**: R$ 160.000/mês

**DAX (Power BI)**:
```dax
Vendas_Certificado = 
CALCULATE(
    SUM(tb_faturamento[valor_fatura]),
    tb_faturamento[tipo_receita] = "CERTIFICADO",
    tb_faturamento[status_fatura] <> "CANCELADA"
)

Vs_Meta_Certificado = 
VAR Meta = 160000
VAR Vendas = [Vendas_Certificado]
RETURN
    DIVIDE(Vendas, Meta, 0)
```

#### **KPI 15: Margem de Contribuição por Produto (Tabela)**
- **Colunas**:
  1. **Produto**: Nome do produto/serviço
  2. **Receita**: `SUM(valor_fatura)` filtrado por tipo_receita
  3. **Custo**: `SUM(custo_insumo)` da tb_custos_variaveis
  4. **Margem**: `((Receita - Custo) / Receita) * 100`
  5. **Status**: 🟢🟡🔴 baseado na margem

**SQL Completo**:
```sql
WITH receita AS (
    SELECT 
        tipo_receita AS produto,
        SUM(valor_fatura) AS receita_total
    FROM tb_faturamento
    WHERE mes_referencia = '2025-11'
      AND status_fatura NOT IN ('CANCELADA', 'SUSPENSA')
    GROUP BY tipo_receita
),
custo AS (
    SELECT 
        tipo_servico AS produto,
        SUM(custo_insumo) AS custo_total
    FROM tb_custos_variaveis
    WHERE mes_referencia = '2025-11'
    GROUP BY tipo_servico
)
SELECT 
    r.produto,
    r.receita_total,
    COALESCE(c.custo_total, 0) AS custo_total,
    ROUND(((r.receita_total - COALESCE(c.custo_total, 0)) / r.receita_total) * 100, 1) AS margem_pct,
    CASE 
        WHEN ((r.receita_total - COALESCE(c.custo_total, 0)) / r.receita_total) > 0.70 THEN '🟢'
        WHEN ((r.receita_total - COALESCE(c.custo_total, 0)) / r.receita_total) >= 0.60 THEN '🟡'
        ELSE '🔴'
    END AS status_margem
FROM receita r
LEFT JOIN custo c ON r.produto = c.produto
ORDER BY r.receita_total DESC;
```

**Visual em Power BI**:
- Usar "Table" visual
- Aplicar conditional formatting nas colunas:
  - **Margem**: Gradient de vermelho (0%) a verde (100%)
  - **Status**: Icon set (emoji)

#### **KPI 16: Evolução da Margem SPC (6 meses)**
- **Visual**: Line chart
- **Eixo X**: Meses (Jun a Nov)
- **Eixo Y**: Margem % (0-100%)
- **Linha de Referência**: 60% (linha tracejada vermelha - meta mínima)

#### **KPI 17: Custo Variável vs Receita (Tendência 2025)**
- **Visual**: Area chart com 2 áreas empilhadas
  - Área 1: Receita Total (azul)
  - Área 2: Custo Variável (vermelho)
- **Eixo X**: Meses (Jan a Dez)
- **Eixo Y**: Valores em R$ milhões

**Insight Visual**: Distância entre as 2 curvas = Margem de Contribuição Total

#### **KPI 18: Performance de Novos Produtos**
- **Estrutura de Dados Necessária**: Tabela `tb_produtos_novos` com:
  - `nome_produto`
  - `data_lancamento`
  - `meta_mensal` (R$)
  
- **Visual**: Tabela com colunas:
  1. Nome Produto
  2. Data Lançamento
  3. Vendas Acumuladas
  4. % vs. Meta
  5. Status (🟢🟡🔴)

**SQL**:
```sql
SELECT 
    p.nome_produto,
    p.data_lancamento,
    COALESCE(SUM(f.valor_fatura), 0) AS vendas_acumuladas,
    p.meta_mensal,
    ROUND((COALESCE(SUM(f.valor_fatura), 0) / p.meta_mensal) * 100, 0) AS perc_meta,
    CASE 
        WHEN (COALESCE(SUM(f.valor_fatura), 0) / p.meta_mensal) >= 1.00 THEN '🟢'
        WHEN (COALESCE(SUM(f.valor_fatura), 0) / p.meta_mensal) >= 0.80 THEN '🟡'
        ELSE '🔴'
    END AS status
FROM tb_produtos_novos p
LEFT JOIN tb_faturamento f ON p.id_produto = f.id_produto
    AND f.mes_referencia = DATE_FORMAT(CURDATE(), '%Y-%m')
GROUP BY p.nome_produto, p.data_lancamento, p.meta_mensal
ORDER BY p.data_lancamento DESC;
```

---

### 4.4 Filtros Dinâmicos (Slicers)

```
┌─────────────────────────────────┐
│ FILTROS                         │
├─────────────────────────────────┤
│ Período: [Nov/25 ▼]            │
│ Categoria Produto: [Todos ▼]   │
│   ☐ Recorrente                 │
│   ☐ Variável                   │
│   ☐ Novos                      │
└─────────────────────────────────┘
```

---

## 5. ESPECIFICAÇÕES TÉCNICAS POWER BI

### 5.1 Modelo de Dados (Relationships)

```
FATO_RECEITA (1) ─────── (*) DIM_CLIENTE
FATO_RECEITA (1) ─────── (*) DIM_PRODUTO
FATO_RECEITA (1) ─────── (*) DIM_TEMPO
FATO_DESPESA (1) ─────── (*) DIM_TEMPO
```

**Tipo de Relacionamento**: One-to-Many (1:*)

**Cardinalidade**: 
- `FATO_RECEITA[id_cliente]` → `DIM_CLIENTE[id_cliente]`
- `FATO_RECEITA[id_produto]` → `DIM_PRODUTO[id_produto]`
- `FATO_RECEITA[data_emissao]` → `DIM_TEMPO[data_completa]`

---

### 5.2 Medidas DAX Essenciais

```dax
// ========== PAINEL A: O PULMÃO ==========

// Saldo de Caixa
Saldo_Caixa = 
CALCULATE(
    SUM(tb_recebimentos[valor_recebido])
) - 
CALCULATE(
    SUM(tb_despesas_operacionais[valor_despesa])
)

// IAR
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

// Burn Rate Líquido
Burn_Rate = 
CALCULATE(
    SUM(tb_recebimentos[valor_recebido]) - SUM(tb_despesas_operacionais[valor_despesa])
)

// Estoque de Suspensos
Estoque_Suspensos = 
CALCULATE(
    SUM(tb_faturamento[valor_fatura]),
    FILTER(
        tb_clientes,
        tb_clientes[status_cliente] = "SUSPENSO"
    ),
    tb_faturamento[status_fatura] = "EMITIDA"
)

// ========== PAINEL B: O MOTOR ==========

// ICIO
ICIO = 
VAR ReceitaTop20 = 
    CALCULATE(
        SUM(tb_faturamento[valor_fatura]),
        TOPN(20, ALL(tb_clientes), [Receita_12m], DESC)
    )
VAR ReceitaTotal = 
    SUM(tb_faturamento[valor_fatura])
RETURN
    DIVIDE(ReceitaTop20, ReceitaTotal, 0)

// Churn Real
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
        tb_clientes[data_cancelamento] >= STARTOFMONTH(dim_tempo[data_completa])
    )
RETURN
    DIVIDE(Cancelados, ClientesInicio, 0)

// IRR Recorrente
IRR_Recorrente = 
CALCULATE(
    SUM(tb_faturamento[valor_fatura]),
    tb_faturamento[tipo_receita] = "MENSALIDADE"
)

// IRR Variável
IRR_Variavel = 
CALCULATE(
    SUM(tb_faturamento[valor_fatura]),
    tb_faturamento[tipo_receita] IN {"CONSULTA_SPC", "CERTIFICADO", "OUTROS"}
)

// ========== PAINEL C: A MÁQUINA ==========

// Margem SPC
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
    DIVIDE(ReceitaSPC - CustoSPC, ReceitaSPC, 0)

// Vendas Certificado
Vendas_Certificado = 
CALCULATE(
    SUM(tb_faturamento[valor_fatura]),
    tb_faturamento[tipo_receita] = "CERTIFICADO"
)
```

---

### 5.3 Configurações de Refresh (Atualização)

**Gateway**: Power BI Gateway (On-premises data gateway)

**Cronograma**:
```
Segunda a Sexta: A cada 1 hora (8h-18h)
Sábado: Às 10h
Domingo: Sem atualização
```

**Fonte de Dados**:
- Opção 1: Arquivos .parquet no OneDrive (mais barato)
- Opção 2: Conexão direta SQL Server (se disponível)

**Configuração no Power BI Service**:
```
Settings > Dataset > Scheduled refresh
├── Frequency: Hourly
├── Time zone: (UTC-04:00) Manaus
├── Time: Every hour from 08:00 to 18:00
└── Send refresh failure notifications: Yes
    └── Email: diretor@cdlmanaus.com.br
```

---

## 6. PALETA DE CORES E PADRÕES VISUAIS

### 6.1 Identidade Visual CDL Manaus

**Cores Primárias**:
- **Azul CDL**: `#003366` (headers, títulos)
- **Laranja CDL**: `#FF6600` (destaques, CTAs)

**Cores Secundárias (Semáforo)**:
- **Verde**: `#28A745` (🟢 Saudável, metas atingidas)
- **Amarelo**: `#FFC107` (🟡 Atenção, monitorar)
- **Vermelho**: `#DC3545` (🔴 Crítico, ação urgente)

**Cores Neutras**:
- **Branco**: `#FFFFFF` (background cards)
- **Cinza Claro**: `#F8F9FA` (background painel)
- **Cinza Escuro**: `#343A40` (texto)

---

### 6.2 Tipografia

**Fonte Principal**: Segoe UI (Power BI default) ou Roboto (alternativa)

**Hierarquia**:
```
Título do Painel: 24pt, Bold, Azul CDL (#003366)
Subtítulo: 16pt, Regular, Cinza Escuro (#343A40)
KPI Valor: 36pt, Bold, cor contextual (verde/amarelo/vermelho)
KPI Label: 12pt, Regular, Cinza Escuro (#343A40)
Texto Corpo: 11pt, Regular, Cinza Escuro (#343A40)
```

---

### 6.3 Ícones e Elementos Visuais

**Ícones dos Painéis**:
- Painel A: 🫁 (Pulmão)
- Painel B: ⚙️ (Motor)
- Painel C: 🏭 (Máquina)

**Status Icons**:
- 🟢 Verde: Performance OK
- 🟡 Amarelo: Atenção necessária
- 🔴 Vermelho: Ação urgente
- ↗️ Seta para cima: Tendência positiva
- → Seta horizontal: Estável
- ↘️ Seta para baixo: Tendência negativa

**Medalhas (Ranking)**:
- 🥇 Ouro: 1º lugar
- 🥈 Prata: 2º lugar
- 🥉 Bronze: 3º lugar

---

### 6.4 Exemplo de Card (Componente Reutilizável)

```
┌─────────────────────────────────┐
│ LABEL DO KPI                    │  ← 12pt, Cinza Escuro
│                                 │
│ R$ 1.245.680                    │  ← 36pt, Bold, Verde/Amarelo/Vermelho
│                                 │
│ 🟢 +12% vs Outubro              │  ← 11pt, Ícone + texto
└─────────────────────────────────┘
  ↑                               ↑
  Background: #FFFFFF             Borda: 1px #E0E0E0
  Padding: 16px                   Border-radius: 8px
```

---

## IMPLEMENTAÇÃO RÁPIDA (Quick Start)

### Para Power BI:

1. **Criar Data Model**:
   - Importar arquivos .parquet da pasta `/CDL_DataLake/03_ANALYTICAL/`
   - Criar relacionamentos conforme seção 5.1

2. **Copiar Medidas DAX**:
   - Criar pasta "Medidas" no Power BI
   - Colar todas as medidas da seção 5.2

3. **Criar Páginas**:
   - Página 1: "O Pulmão" (usar layout da seção 2.2)
   - Página 2: "O Motor" (usar layout da seção 3.2)
   - Página 3: "A Máquina" (usar layout da seção 4.2)

4. **Aplicar Tema**:
   - View > Themes > Customize Current Theme
   - Inserir cores da seção 6.1

5. **Configurar Refresh**:
   - Publish to Power BI Service
   - Settings > Scheduled refresh (seção 5.3)

### Para Excel (Alternativa Baixo Custo):

1. **Conectar Dados**:
   - Data > Get Data > From File > From CSV
   - Importar arquivos da pasta `/CDL_DataLake/04_KPIS/`

2. **Criar Tabelas Dinâmicas**:
   - Insert > PivotTable para cada KPI

3. **Aplicar Formatação Condicional**:
   - Home > Conditional Formatting > Icon Sets
   - Usar semáforo (verde/amarelo/vermelho)

4. **Criar Gráficos**:
   - Insert > Charts (Line, Column, Matrix)

---

**Documento elaborado por**: Arquiteto de Soluções BI - Ecossistema de Inteligência CDL Manaus  
**Versão**: 1.0  
**Data**: Dezembro 2025
