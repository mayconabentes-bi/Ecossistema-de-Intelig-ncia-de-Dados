# GUIA RÁPIDO DE REFERÊNCIA
## Ecossistema de Inteligência de Dados - CDL Manaus

---

## 🎯 O QUE É ESTE PROJETO?

Sistema de Business Intelligence em Tempo Real que transforma relatórios PDF estáticos em dashboards interativos com alertas automáticos no WhatsApp.

**Problema**: Diretoria toma decisões 30-45 dias após o problema (quando recebe o PDF mensal)  
**Solução**: Alertas em tempo real quando clientes Top 20 caem >10% na semana

---

## 📚 DOCUMENTAÇÃO (6 ARQUIVOS)

### 1. [README.md](./README.md) - COMECE AQUI
**Tempo de leitura**: 10 minutos  
**Para quem**: Todos (Diretores, Gerentes, Analistas)

**O que tem**:
- Visão geral do projeto
- Problema x Solução
- Custos e ROI (R$ 591k de retorno/ano)
- Stack tecnológica

---

### 2. [ARQUITETURA_DADOS.md](./ARQUITETURA_DADOS.md) - FUNDAÇÃO TÉCNICA
**Tempo de leitura**: 45 minutos  
**Para quem**: Analista BI, TI, Diretor de TI

**O que tem**:
- Estrutura do Data Lake (5 camadas)
- Mapeamento de 5 tabelas do ERP
- SQLs completos para cada KPI
- Regras de transformação (ETL)
- Fluxo de extração/carga

**Quando usar**: Fase 1 e 2 (Semanas 1-2 do projeto)

---

### 3. [DESIGN_DASHBOARDS.md](./DESIGN_DASHBOARDS.md) - VISUAL E LAYOUT
**Tempo de leitura**: 60 minutos  
**Para quem**: Analista BI, Diretoria (para validação visual)

**O que tem**:
- Wireframes dos 3 painéis (ASCII art)
- Especificação de cada um dos 18 KPIs
- Medidas DAX (Power BI)
- Paleta de cores CDL Manaus
- Gráfico "Batalha Naval" (feature crítica)

**Quando usar**: Fase 3 (Semanas 3-4 do projeto)

**DESTAQUES**:
- **Painel A "O Pulmão"**: IAR, Burn Rate, Estoque Suspensos
- **Painel B "O Motor"**: ICIO, Batalha Naval, Churn Real
- **Painel C "A Máquina"**: Margem SPC, Rentabilidade por produto

---

### 4. [SISTEMA_ALERTAS.md](./SISTEMA_ALERTAS.md) - AUTOMAÇÃO
**Tempo de leitura**: 40 minutos  
**Para quem**: Analista BI, Gerentes (entender alertas)

**O que tem**:
- 3 regras de alerta críticas
- Templates de mensagem WhatsApp
- Código Power Automate + Python
- Matriz de responsabilidades
- Configuração Twilio (WhatsApp API)

**Quando usar**: Fase 4 (Semana 5 do projeto)

**3 ALERTAS PRINCIPAIS**:
1. **Queda Cliente Top 20** → WhatsApp para Dir. Comercial
2. **Burn Rate Negativo 2 meses** → WhatsApp para Diretoria completa
3. **Margem SPC <60%** → WhatsApp para Dir. Financeiro

---

### 5. [ROTEIRO_IMPLEMENTACAO.md](./ROTEIRO_IMPLEMENTACAO.md) - PLANO DE AÇÃO
**Tempo de leitura**: 50 minutos  
**Para quem**: Gerente de Projeto, Analista BI, Diretoria

**O que tem**:
- Cronograma detalhado (6 semanas)
- Checklist de cada fase
- Análise de custos (R$ 21k total)
- Análise de ROI (2.632%)
- Matriz RACI (responsabilidades)

**Quando usar**: Desde o início até o final do projeto

**CRONOGRAMA**:
```
Semana 1: Preparação (mapear ERP)
Semana 2: Data Lake (extrair dados)
Semanas 3-4: Dashboards (construir painéis)
Semana 5: Alertas (configurar automação)
Semana 6: Go-Live (testes e treinamento)
```

---

### 6. [FORMULAS_KPIS.md](./FORMULAS_KPIS.md) - REFERÊNCIA TÉCNICA
**Tempo de leitura**: 30 minutos (consulta)  
**Para quem**: Analista BI (referência rápida)

**O que tem**:
- 15 fórmulas de KPIs
- SQL + DAX para cada métrica
- Interpretação (verde/amarelo/vermelho)
- Baselines de Nov/2025

**Quando usar**: Durante todo o projeto (consulta)

**EXEMPLO**:
```
IAR = Faturamento Contábil / Arrecadação de Caixa
Meta: 0.95-1.00 (🟢)
Baseline: 1.01 (🟡 Atenção)
```

---

## 🚀 GUIA PARA DIFERENTES PERSONAS

### Se você é **DIRETOR** (Tomador de Decisão):

**1. Leia primeiro** (30 min):
- [ ] README.md completo
- [ ] ROTEIRO_IMPLEMENTACAO.md → Seção 9 (Custos e ROI)

**2. Decisão**:
- [ ] Aprovar orçamento: R$ 12k inicial + R$ 785/mês
- [ ] Designar Analista BI responsável
- [ ] Aprovar cronograma (6 semanas)

**3. Envolvimento durante o projeto**:
- Semana 1: Reunião kickoff (2h)
- Semana 6: Testes UAT (2h) + Treinamento (2h)
- **Total**: 6 horas

**4. Após Go-Live**:
- Reunião semanal (30 min) para revisar dashboards
- Responder alertas WhatsApp (ação em 24-48h)

---

### Se você é **ANALISTA DE BI** (Implementador):

**1. Prepare-se** (Semana 0):
- [ ] Ler TODOS os 6 documentos (4 horas)
- [ ] Instalar Power BI Desktop
- [ ] Obter credenciais do ERP
- [ ] Configurar ambiente OneDrive

**2. Siga o cronograma**:
```
Semana 1:
[ ] ARQUITETURA_DADOS.md → Seção 3 (Checklist ERP)
[ ] Mapear 5 tabelas essenciais
[ ] Validar baseline (IAR=1.01, ICIO, Burn Rate)

Semana 2:
[ ] ARQUITETURA_DADOS.md → Seções 4-7 (ETL)
[ ] Extrair dados (RAW)
[ ] Transformar (STAGING)
[ ] Modelar (ANALYTICAL)

Semanas 3-4:
[ ] DESIGN_DASHBOARDS.md → Seções 2-4 (Painéis A, B, C)
[ ] FORMULAS_KPIS.md (referência)
[ ] Construir dashboards no Power BI
[ ] Aplicar visual design

Semana 5:
[ ] SISTEMA_ALERTAS.md → Seção 6 (Implementação)
[ ] Configurar Power Automate (3 flows)
[ ] Cadastrar Twilio
[ ] Testar alertas

Semana 6:
[ ] ROTEIRO_IMPLEMENTACAO.md → Seção 7 (Go-Live)
[ ] UAT com Diretoria
[ ] Treinamento
[ ] Publicar em produção
```

**3. Documentos de consulta frequente**:
- **FORMULAS_KPIS.md**: Para validar cálculos
- **ARQUITETURA_DADOS.md**: Para SQLs prontos
- **DESIGN_DASHBOARDS.md**: Para medidas DAX

---

### Se você é **GERENTE** (Usuário Final):

**1. Entenda o sistema** (15 min):
- [ ] README.md → Seções "O Problema" e "A Solução"
- [ ] DESIGN_DASHBOARDS.md → Ver wireframes (visual) do seu painel:
  - Dir. Financeiro → Painel A "O Pulmão"
  - Dir. Comercial → Painel B "O Motor"
  - Dir. Operações → Painel C "A Máquina"

**2. Prepare-se para alertas**:
- [ ] SISTEMA_ALERTAS.md → Seção 7 (Matriz de Responsabilidades)
- Saber qual alerta você receberá
- Conhecer o prazo de ação (24h, 48h, 72h)

**3. Envolvimento**:
- Semana 6: Participar UAT (2h) para validar dashboards
- Após Go-Live: Usar dashboards semanalmente (30 min)

---

## 📊 18 KPIs POR PAINEL

### PAINEL A: "O PULMÃO" (Financeiro/Caixa)
1. Saldo de Caixa Atual
2. IAR (Índice de Arrecadação Real)
3. Projeção de Caixa 30 dias
4. Burn Rate Líquido (Tendência 3 meses)
5. Estoque de Suspensos
6. Eficiência de Cobrança (Inadimplência Real)

### PAINEL B: "O MOTOR" (Comercial/Carteira)
7. ICIO (Índice de Concentração Top 20)
8. Churn Real (% clientes cancelados)
9. Gráfico "Batalha Naval" (variação semanal)
10. Share of Wallet (Top 5)
11. Movimentação de Carteira (entradas/saídas)
12. IRR (Receita Recorrente vs. Variável)

### PAINEL C: "A MÁQUINA" (Produtos/Margem)
13. Margem de Contribuição SPC
14. Vendas Certificado Digital vs. Meta
15. Margem por Produto (Tabela)
16. Evolução Margem SPC (6 meses)
17. Custo Variável vs Receita
18. Performance de Novos Produtos

---

## 🔔 3 ALERTAS AUTOMÁTICOS

### ALERTA 1: Queda Cliente Top 20
**Gatilho**: Cliente Top 20 com queda >10% na semana  
**Canal**: WhatsApp  
**Destinatário**: Diretor Comercial + Gerente Relacionamento  
**Ação**: Contatar cliente em 48h  

### ALERTA 2: Burn Rate Negativo
**Gatilho**: Burn Rate < 0 por 2 meses consecutivos  
**Canal**: WhatsApp  
**Destinatário**: Diretoria completa  
**Ação**: Reunião emergencial em 24h  

### ALERTA 3: Margem SPC Baixa
**Gatilho**: Margem SPC < 60%  
**Canal**: WhatsApp  
**Destinatário**: Dir. Financeiro + Dir. Operações  
**Ação**: Renegociar com fornecedor em 72h  

---

## 💰 RESUMO FINANCEIRO

| Item | Valor |
|------|-------|
| **Investimento Inicial** | R$ 12.215 |
| **Custo Mensal** | R$ 785 |
| **Custo Anual** | R$ 21.635 |
| **Retorno Esperado (12 meses)** | R$ 591.000 |
| **ROI** | 2.632% |
| **Payback** | 2 meses |

**Comparação**: Solução enterprise (Tableau + Snowflake) custaria R$ 60k-180k/ano

---

## 🛠️ STACK TECNOLÓGICA

| Camada | Ferramenta | Custo |
|--------|------------|-------|
| **Storage** | OneDrive Business (50GB) | R$ 20/mês |
| **ETL** | Power Query / Python | Grátis |
| **BI** | Power BI Desktop | Grátis |
| **BI Cloud** | Power BI Pro (3 usuários) | R$ 165/mês |
| **Automação** | Power Automate | R$ 0-50/mês |
| **WhatsApp** | Twilio API | R$ 100/mês |

---

## ✅ CHECKLIST PRÉ-INÍCIO

Antes de começar, confirmar:

**TÉCNICO**:
- [ ] ERP possui API ou ODBC funcional
- [ ] Dados históricos disponíveis (mínimo 12 meses)
- [ ] Microsoft 365 Business ativo
- [ ] Power BI Desktop instalado

**ORGANIZACIONAL**:
- [ ] Diretoria comprometida com uso dos dashboards
- [ ] Analista BI disponível 20h/semana × 6 semanas
- [ ] Orçamento aprovado
- [ ] Contatos de TI e áreas de negócio disponíveis

**DADOS**:
- [ ] Status de cliente padronizado no ERP
- [ ] Custos variáveis rastreados por produto
- [ ] Receitas classificadas por tipo

---

## 🎓 RECURSOS ADICIONAIS

### Tutoriais Online (Gratuitos)
- [Power BI para Iniciantes](https://learn.microsoft.com/pt-br/power-bi/)
- [Power Automate Quickstart](https://learn.microsoft.com/pt-br/power-automate/)
- [Twilio WhatsApp API Docs](https://www.twilio.com/docs/whatsapp)

### Comunidades
- [Power BI Community](https://community.powerbi.com/)
- [Stack Overflow - Power BI](https://stackoverflow.com/questions/tagged/powerbi)

---

## ❓ FAQ

### P: Quanto tempo demora a implementação?
**R**: 6 semanas (42 dias corridos) com 120 horas de esforço.

### P: Preciso contratar consultoria externa?
**R**: Não necessariamente. Com um Analista BI interno dedicado e esta documentação, é possível implementar internamente.

### P: E se meu ERP não tiver API?
**R**: Alternativas: (1) Export CSV automatizado via agendamento, (2) Conexão ODBC, (3) Replicação de banco de dados.

### P: Power BI é obrigatório ou posso usar Excel?
**R**: Power BI é recomendado pela capacidade de refresh automático e alertas. Excel é viável para MVP (prova de conceito), mas limitado.

### P: Quanto custa o WhatsApp Business API?
**R**: ~R$ 0,10 por mensagem via Twilio. Estimativa: 1.000 mensagens/mês = R$ 100/mês.

### P: Preciso saber programar?
**R**: Básico de SQL é recomendado. Python é opcional (pode usar apenas Power Query). DAX do Power BI é aprendido durante o projeto.

### P: Posso começar com apenas 1 painel?
**R**: Sim! Recomendação: Começar com Painel A "O Pulmão" (mais crítico) e expandir depois.

### P: Como faço manutenção após Go-Live?
**R**: Ver ROTEIRO_IMPLEMENTACAO.md → Seção 8 (Plano de Sustentação). Estimativa: 5h/mês de Analista BI.

---

## 🚀 PRÓXIMOS PASSOS

### HOJE (30 minutos):
1. [ ] Ler este guia completo
2. [ ] Ler README.md
3. [ ] Decidir: Aprovar projeto?

### ESTA SEMANA (se aprovado):
1. [ ] Ler ROTEIRO_IMPLEMENTACAO.md completo
2. [ ] Designar Analista BI responsável
3. [ ] Agendar reunião de kickoff
4. [ ] Solicitar credenciais do ERP

### SEMANAS 1-6:
1. [ ] Seguir cronograma do ROTEIRO_IMPLEMENTACAO.md
2. [ ] Usar ARQUITETURA_DADOS.md e DESIGN_DASHBOARDS.md como guias
3. [ ] Reportar progresso semanalmente

### APÓS GO-LIVE:
1. [ ] Coletar feedback (1 semana)
2. [ ] Implementar ajustes rápidos
3. [ ] Planejar Fase 2 (evolução)

---

## 📞 SUPORTE

Para dúvidas durante a implementação:

| Tipo de Dúvida | Consultar |
|----------------|-----------|
| **Técnica (SQL, DAX)** | FORMULAS_KPIS.md + ARQUITETURA_DADOS.md |
| **Visual (Layout)** | DESIGN_DASHBOARDS.md |
| **Processo** | ROTEIRO_IMPLEMENTACAO.md |
| **Alertas** | SISTEMA_ALERTAS.md |

---

**Boa sorte na implementação! 🎉**

**Lembre-se**: Este sistema vai transformar a CDL Manaus de uma gestão reativa para proativa. A Diretoria terá visibilidade em tempo real e poderá agir ANTES dos problemas se agravarem.

**Transforme dados em decisões. Decisões em resultados.** 💡

---

**Documento elaborado por**: Arquiteto de Soluções BI - Ecossistema de Inteligência CDL Manaus  
**Versão**: 1.0  
**Data**: Dezembro 2025
