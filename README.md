# Ecossistema de Inteligência de Dados - CDL Manaus

## 🚀 Sistema Online via GitHub Pages

**[👉 ACESSAR SISTEMA ONLINE](https://mayconabentes-bi.github.io/Ecossistema-de-Intelig-ncia-de-Dados/)**

- **Dashboard Interativo**: [https://mayconabentes-bi.github.io/Ecossistema-de-Intelig-ncia-de-Dados/](https://mayconabentes-bi.github.io/Ecossistema-de-Intelig-ncia-de-Dados/)
- **Sistema de Alertas**: [https://mayconabentes-bi.github.io/Ecossistema-de-Intelig-ncia-de-Dados/alerts.html](https://mayconabentes-bi.github.io/Ecossistema-de-Intelig-ncia-de-Dados/alerts.html)

🧪 **Ambiente de Testes**: Demonstração funcional com simulação de alertas em tempo real.

---

## 🎯 Visão Geral

Sistema de Business Intelligence em Tempo Real para a CDL Manaus, transformando a gestão de **reativa** (baseada em relatórios mensais em PDF) para **proativa** (dashboards em tempo real com alertas automatizados).

---

## 📊 O Problema

A CDL Manaus enfrenta um paradoxo:
- ✅ **Eficiência Operacional Alta**: Custos controlados
- ❌ **Crise de Receita (Top Line)**: Perda de volume dos grandes varejistas
  - Exemplo: Bemol caiu de 25% para 12% do share de receita
  - Burn Rate negativo em Nov/2025: -R$ 83.923
  - Estoque de clientes suspensos: R$ 742.779

**Causa Raiz**: Gestão baseada em "Resumos Executivos" estáticos e retroativos (PDF), impedindo ação preventiva.

---

## 💡 A Solução

Ecossistema de Inteligência composto por:

### 1. **3 Dashboards Estratégicos**
- **Painel A: "O Pulmão"** (Financeiro/Caixa)
  - IAR (Índice de Arrecadação Real)
  - Burn Rate Líquido
  - Estoque de Suspensos
  
- **Painel B: "O Motor"** (Comercial/Carteira)
  - ICIO (Índice de Concentração Top 20)
  - Gráfico "Batalha Naval" (variação semanal de clientes)
  - IRR (Índice de Renovação de Receita)
  
- **Painel C: "A Máquina"** (Produtos/Margem)
  - Margem de Contribuição SPC (meta: >60%)
  - Performance de Certificado Digital
  - Rentabilidade por produto

### 2. **Sistema de Alertas Automáticos**
- Alerta 1: Queda >10% de cliente Top 20 (WhatsApp)
- Alerta 2: Burn Rate negativo por 2 meses consecutivos
- Alerta 3: Margem SPC abaixo de 60%

### 3. **Data Lake Simplificado**
- Extração automatizada do ERP
- Modelo dimensional (Star Schema)
- Atualização diária (refresh schedule)

---

## 📁 Estrutura de Documentação

| Documento | Descrição |
|-----------|-----------|
| [**ARQUITETURA_DADOS.md**](./ARQUITETURA_DADOS.md) | Estrutura do Data Lake, tabelas do ERP, SQLs e ETL |
| [**DESIGN_DASHBOARDS.md**](./DESIGN_DASHBOARDS.md) | Wireframes, KPIs e especificações visuais dos 3 painéis |
| [**SISTEMA_ALERTAS.md**](./SISTEMA_ALERTAS.md) | 3 regras de alerta com lógica SQL e templates de mensagem |
| [**ROTEIRO_IMPLEMENTACAO.md**](./ROTEIRO_IMPLEMENTACAO.md) | Cronograma de 6 semanas, custos e análise de ROI |

---

## 🚀 Quick Start

### Pré-Requisitos

```
☑ ERP financeiro com API/ODBC
☑ Dados históricos (mínimo 12 meses)
☑ Microsoft 365 Business (Power BI Desktop incluído)
☑ Analista BI disponível (20h/semana × 6 semanas)
☑ Orçamento aprovado: R$ 12k inicial + R$ 785/mês
```

### Implementação em 6 Semanas

1. **Semana 1**: Preparação e Descoberta
   - Mapear tabelas do ERP
   - Validar qualidade dos dados
   - Configurar infraestrutura

2. **Semana 2**: Data Lake
   - Extrair dados (RAW layer)
   - Transformar (STAGING layer)
   - Modelar (ANALYTICAL layer)

3. **Semanas 3-4**: Dashboards
   - Construir Painéis A, B e C no Power BI
   - Implementar 18 KPIs
   - Aplicar visual design

4. **Semana 5**: Alertas
   - Configurar Power Automate
   - Integrar Twilio (WhatsApp API)
   - Testar flows

5. **Semana 6**: Go-Live
   - Testes UAT com Diretoria
   - Treinamento
   - Publicação em produção

**Detalhes completos**: Ver [ROTEIRO_IMPLEMENTACAO.md](./ROTEIRO_IMPLEMENTACAO.md)

---

## 💰 Custos e ROI

### Investimento

| Item | Valor |
|------|-------|
| **Inicial** (6 semanas implementação) | R$ 12.215 |
| **Recorrente** (mensal) | R$ 785 |
| **Anual** | R$ 21.635 |

### Retorno Projetado (12 meses)

| Benefício | Valor |
|-----------|-------|
| Recuperação Estoque Suspensos (40%) | R$ 297.000 |
| Redução Inadimplência | R$ 120.000 |
| Retenção cliente Top 20 | R$ 150.000 |
| Economia de analistas | R$ 24.000 |
| **TOTAL** | **R$ 591.000** |

**ROI**: 2.632% | **Payback**: 2 meses

---

## 📊 KPIs Monitorados (18 Indicadores)

### Painel A: O Pulmão (Financeiro)
1. Saldo de Caixa Atual
2. IAR (Índice de Arrecadação Real)
3. Projeção de Caixa 30 dias
4. Burn Rate Líquido (Tendência 3 meses)
5. Estoque de Suspensos
6. Eficiência de Cobrança (Inadimplência Real)

### Painel B: O Motor (Comercial)
7. ICIO (Índice de Concentração Top 20)
8. Churn Real (% clientes cancelados)
9. Gráfico "Batalha Naval" (variação semanal)
10. Share of Wallet (Top 5)
11. Movimentação de Carteira (entradas/saídas)
12. IRR (Receita Recorrente vs. Variável)

### Painel C: A Máquina (Produtos)
13. Margem de Contribuição SPC
14. Vendas Certificado Digital vs. Meta
15. Margem por Produto (Tabela)
16. Evolução Margem SPC (6 meses)
17. Custo Variável vs Receita
18. Performance de Novos Produtos

---

## 🔔 Sistema de Alertas

### Regra 1: Queda Crítica Cliente Top 20
```
Condição: Cliente Top 20 com queda >10% na semana vs. média 4 semanas
Ação: WhatsApp para Diretor Comercial + Gerente Relacionamento
Prazo: Contato com cliente em 48h
```

### Regra 2: Burn Rate Negativo Consecutivo
```
Condição: Burn Rate < 0 por 2 meses consecutivos
Ação: WhatsApp para Diretoria completa
Prazo: Reunião emergencial em 24h
```

### Regra 3: Margem SPC Abaixo do Limite
```
Condição: Margem SPC < 60%
Ação: WhatsApp para Dir. Financeiro + Dir. Operações
Prazo: Renegociação com fornecedor em 72h
```

**Detalhes completos**: Ver [SISTEMA_ALERTAS.md](./SISTEMA_ALERTAS.md)

---

## 🧪 Como Testar os Alertas

### Ambiente de Demonstração Online

1. **Acessar o Dashboard Online**: [https://mayconabentes-bi.github.io/Ecossistema-de-Intelig-ncia-de-Dados/](https://mayconabentes-bi.github.io/Ecossistema-de-Intelig-ncia-de-Dados/)

2. **Testar Alertas Individuais**:
   - Na página principal, use o **Painel de Testes de Alertas**
   - Clique nos botões para simular cada tipo de alerta:
     - 🔴 **Alerta 1**: Queda de Cliente Top 20
     - 🟡 **Alerta 2**: Burn Rate Negativo Consecutivo
     - 🔵 **Alerta 3**: Margem SPC Abaixo do Limite

3. **Visualizar Sistema de Alertas Completo**:
   - Acesse [alerts.html](https://mayconabentes-bi.github.io/Ecossistema-de-Intelig-ncia-de-Dados/alerts.html)
   - Veja as regras detalhadas de cada alerta
   - Visualize o histórico de alertas simulado
   - Teste cada alerta individualmente

### Funcionalidades do Ambiente de Testes

✅ **Dashboard Interativo**: Visualização dos 3 painéis principais (A, B, C)  
✅ **Simulação de Alertas**: Testes em tempo real com notificações visuais  
✅ **Documentação Integrada**: Acesso direto às especificações técnicas  
✅ **Histórico de Alertas**: Exemplo de log de alertas disparados  
✅ **Detalhes por Alerta**: Condições, ações, destinatários e frequências  

### Para Implementação Real

Para implementar o sistema de alertas com WhatsApp e e-mail reais:
1. Configure o Power Automate conforme [SISTEMA_ALERTAS.md](./SISTEMA_ALERTAS.md)
2. Integre com Twilio WhatsApp API
3. Configure os destinatários e números de contato
4. Ajuste as frequências de verificação conforme necessidade

---

## 🛠️ Stack Tecnológica

### Camada de Dados
- **Fonte**: ERP financeiro (API/ODBC/CSV)
- **Storage**: OneDrive Business (50GB)
- **ETL**: Power Query ou Python + pandas
- **Formato**: Parquet (compressão e performance)

### Camada de Visualização
- **BI Tool**: Power BI Desktop (gratuito)
- **Publicação**: Power BI Service (R$ 55/usuário/mês)
- **Mobile**: Power BI Mobile App

### Camada de Alertas
- **Orquestração**: Power Automate (Microsoft Flow)
- **WhatsApp**: Twilio API (~R$ 0,10/mensagem)
- **E-mail**: Office 365 Outlook

---

## 📈 Roadmap de Evolução (6 Meses)

### Fase 1: Estabilização (Mês 1-2)
- Ajustes finos baseados em feedback
- Adicionar alertas complementares (Regras 4, 5, 6)
- Integrar dados de CRM

### Fase 2: Expansão (Mês 3-4)
- Painel D: "Operacional" (Eficiência interna)
- Integrar dados de RH (custo de folha)
- Análise preditiva (forecast de receita)

### Fase 3: Inteligência Avançada (Mês 5-6)
- Machine Learning: Predição de churn
- Análise de cohort (geração de clientes)
- Dashboard mobile nativo

---

## 👥 Equipe e Responsabilidades

| Papel | Responsabilidade | Dedicação |
|-------|------------------|-----------|
| **Analista BI** | Implementação técnica completa | 20h/semana × 6 semanas |
| **Diretor TI** | Acesso ao ERP e infraestrutura | 2h/semana (consultas) |
| **Diretoria** | Validação de requisitos e UAT | 4h (total) |
| **Gerentes** | Testes e feedback | 2h (total) |

---

## 📚 Como Usar Esta Documentação

### Se você é **Diretor/Tomador de Decisão**:
1. Leia este README.md (visão geral)
2. Veja [ROTEIRO_IMPLEMENTACAO.md](./ROTEIRO_IMPLEMENTACAO.md) → Seção 9 (Custos e ROI)
3. Aprove o projeto e designe responsáveis

### Se você é **Analista de BI/Implementador**:
1. Leia [ROTEIRO_IMPLEMENTACAO.md](./ROTEIRO_IMPLEMENTACAO.md) completo (cronograma)
2. Siga [ARQUITETURA_DADOS.md](./ARQUITETURA_DADOS.md) para setup do Data Lake
3. Use [DESIGN_DASHBOARDS.md](./DESIGN_DASHBOARDS.md) como blueprint visual
4. Configure [SISTEMA_ALERTAS.md](./SISTEMA_ALERTAS.md) no Power Automate

### Se você é **Gerente de Área**:
1. Leia este README.md
2. Veja wireframes em [DESIGN_DASHBOARDS.md](./DESIGN_DASHBOARDS.md)
3. Prepare-se para sessão de UAT (Semana 6)

---

## 🎓 Recursos Adicionais

### Tutoriais Recomendados
- [Power BI para Iniciantes (Microsoft Learn)](https://learn.microsoft.com/pt-br/power-bi/)
- [Power Automate Quickstart](https://learn.microsoft.com/pt-br/power-automate/)
- [Twilio WhatsApp API](https://www.twilio.com/docs/whatsapp)

### Comunidade
- [Power BI Community](https://community.powerbi.com/)
- [Stack Overflow - Power BI](https://stackoverflow.com/questions/tagged/powerbi)

---

## 📞 Suporte

Para dúvidas sobre a implementação:

- **Técnicas**: Consultar [ARQUITETURA_DADOS.md](./ARQUITETURA_DADOS.md) e [DESIGN_DASHBOARDS.md](./DESIGN_DASHBOARDS.md)
- **Processo**: Consultar [ROTEIRO_IMPLEMENTACAO.md](./ROTEIRO_IMPLEMENTACAO.md)
- **Alertas**: Consultar [SISTEMA_ALERTAS.md](./SISTEMA_ALERTAS.md)

---

## ⚠️ Avisos Importantes

1. **Dados Sensíveis**: Nunca commitar credenciais de banco de dados no repositório
2. **LGPD**: Anonimizar dados pessoais em ambientes de teste
3. **Backup**: Sempre fazer backup antes de modificar dados de produção
4. **Testes**: Validar em ambiente de homologação antes de go-live

---

## 🚀 Deployment (GitHub Pages)

### Sistema Online

O sistema está publicado e acessível via GitHub Pages:
- **URL Principal**: https://mayconabentes-bi.github.io/Ecossistema-de-Intelig-ncia-de-Dados/
- **Deploy Automático**: Configurado via GitHub Actions

### Como Funciona

1. **GitHub Actions Workflow**: Automaticamente deploy na branch `main` ou `copilot/deploy-github-pages`
2. **Conteúdo Estático**: Dashboard HTML/CSS/JS para demonstração
3. **Simulação de Alertas**: Interface de testes sem necessidade de backend
4. **Atualização Contínua**: Cada push na branch deploy automaticamente

### Estrutura de Arquivos para GitHub Pages

```
/
├── index.html              # Dashboard principal
├── alerts.html             # Sistema de alertas
├── webapp/
│   └── static/
│       ├── css/
│       │   └── style.css   # Estilos do sistema
│       └── js/
│           └── script.js   # Scripts interativos
├── .github/
│   └── workflows/
│       └── deploy-pages.yml # Workflow de deployment
└── *.md                    # Documentação
```

### Para Desenvolvedores

Para testar localmente antes do deploy:
```bash
# Servir localmente com Python
python -m http.server 8000

# Ou com Node.js
npx http-server -p 8000

# Acessar em: http://localhost:8000
```

---

## 📄 Licença

MIT License - Ver arquivo [LICENSE](./LICENSE)

---

## 🏆 Sobre o Projeto

**Autor**: Maycon Bentes  
**Organização**: CDL Manaus  
**Versão**: 1.0  
**Data**: Dezembro 2025  

**Objetivo**: Democratizar Business Intelligence para associações e pequenas empresas, provando que é possível ter inteligência de dados de classe mundial com orçamento limitado.

---

## ✅ Próximos Passos

### Para Demonstração e Testes
1. ✅ **Sistema Online**: Acessar [https://mayconabentes-bi.github.io/Ecossistema-de-Intelig-ncia-de-Dados/](https://mayconabentes-bi.github.io/Ecossistema-de-Intelig-ncia-de-Dados/)
2. ✅ **Testar Alertas**: Usar o painel de testes no dashboard principal
3. ✅ **Revisar Documentação**: Ler especificações completas em [SISTEMA_ALERTAS.md](./SISTEMA_ALERTAS.md)
4. ⬜ **Feedback**: Coletar impressões da Diretoria e Gerentes sobre o sistema

### Para Implementação Produtiva
1. ✅ Ler esta documentação completa
2. ⬜ Aprovar orçamento e cronograma (ver custos detalhados acima)
3. ⬜ Designar Analista BI responsável
4. ⬜ Iniciar Fase 1 (Semana de Preparação) - seguir [ROTEIRO_IMPLEMENTACAO.md](./ROTEIRO_IMPLEMENTACAO.md)
5. ⬜ Configurar alertas reais com WhatsApp/E-mail
6. ⬜ Integrar com dados reais do ERP
7. ⬜ Acompanhar progresso semanal
8. ⬜ Celebrar o Go-Live produtivo! 🎉

---

**Transforme dados em decisões. Decisões em resultados.**