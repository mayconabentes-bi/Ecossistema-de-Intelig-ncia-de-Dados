# GUIA DE TESTES - Sistema de Alertas Online

## 🚀 Sistema Disponível Online

**URL Principal**: https://mayconabentes-bi.github.io/Ecossistema-de-Intelig-ncia-de-Dados/

---

## 📋 Objetivo dos Testes

Este guia documenta como testar o sistema de alertas online implantado via GitHub Pages. O ambiente de testes permite simular os 3 alertas principais do Ecossistema de Inteligência de Dados da CDL Manaus sem necessidade de integração com sistemas reais.

---

## 🧪 Como Realizar os Testes

### 1. Acessar o Dashboard Principal

1. Abrir o navegador (Chrome, Firefox, Safari, Edge)
2. Acessar: https://mayconabentes-bi.github.io/Ecossistema-de-Intelig-ncia-de-Dados/
3. Verificar se a página carrega corretamente com os 3 painéis (A, B, C)

**Pontos de Verificação**:
- ✅ Banner de teste vermelho aparece no topo
- ✅ Painel de Testes de Alertas está visível
- ✅ Os 3 painéis principais (Pulmão, Motor, Máquina) são exibidos
- ✅ KPIs mostram valores de exemplo

---

### 2. Testar Alerta 1: Queda Cliente Top 20

**Passos**:
1. No Painel de Testes, clicar no botão **"🔴 Testar Alerta 1: Queda Cliente Top 20"**
2. Observar o aparecimento de uma notificação no canto inferior direito da tela
3. Ler o conteúdo do alerta simulado

**Validações**:
- ✅ Notificação aparece com animação suave
- ✅ Conteúdo mostra:
  - Nome do cliente (Bemol S.A.)
  - Percentual de queda (-25,3%)
  - Dados comparativos (média 4 semanas vs. semana atual)
  - Ação recomendada (reunião em 48h)
  - Data/hora do alerta
- ✅ Botão de fechar (X) funciona
- ✅ Alerta fecha automaticamente após 10 segundos

**Cenário de Uso Real**:
> "Quando um cliente Top 20 como Bemol reduz faturamento em mais de 10% em uma semana, o Diretor Comercial e Gerente de Relacionamento recebem alerta no WhatsApp para ação imediata."

---

### 3. Testar Alerta 2: Burn Rate Negativo

**Passos**:
1. No Painel de Testes, clicar no botão **"🟡 Testar Alerta 2: Burn Rate Negativo"**
2. Observar o aparecimento de uma notificação no canto inferior direito
3. Ler o conteúdo do alerta simulado

**Validações**:
- ✅ Notificação aparece com badge amarelo "ALERTA CRÍTICO"
- ✅ Conteúdo mostra:
  - Situação (queimando caixa por 2 meses)
  - Valores mensais (Out/2025 e Nov/2025)
  - Total queimado (R$ -129.123)
  - Projeção de caixa zero (Abril/2026)
  - Plano de ação imediata em 3 etapas
- ✅ Badge de severidade é exibido
- ✅ Alerta fecha após 10 segundos ou ao clicar X

**Cenário de Uso Real**:
> "No dia 1º de cada mês, o sistema verifica se o Burn Rate foi negativo por 2 meses consecutivos. Se positivo, dispara alerta para toda a Diretoria exigindo reunião emergencial em 24h."

---

### 4. Testar Alerta 3: Margem SPC Baixa

**Passos**:
1. No Painel de Testes, clicar no botão **"🔵 Testar Alerta 3: Margem SPC Abaixo do Limite"**
2. Observar o aparecimento de uma notificação
3. Ler o conteúdo do alerta simulado

**Validações**:
- ✅ Notificação aparece com badge azul "ALERTA DE ATENÇÃO"
- ✅ Conteúdo mostra:
  - Margem atual (57,2%) vs. meta (>60%)
  - Receita e custo SPC do mês
  - Ações recomendadas em 3 etapas:
    1. Renegociar com fornecedor
    2. Revisar precificação
    3. Reduzir custo por consulta
- ✅ Formatação e dados são claros
- ✅ Alerta fecha após 10 segundos

**Cenário de Uso Real**:
> "Diariamente às 17h, o sistema verifica a margem SPC. Se abaixo de 60%, alerta Dir. Financeiro e Dir. Operações para renegociação com fornecedor em 72h."

---

### 5. Acessar Página do Sistema de Alertas

**Passos**:
1. No menu de navegação, clicar em **"Sistema de Alertas"**
2. OU acessar diretamente: https://mayconabentes-bi.github.io/Ecossistema-de-Intelig-ncia-de-Dados/alerts.html

**Validações**:
- ✅ Página carrega com 3 cards de alertas
- ✅ Cada card mostra:
  - Ícone e código do alerta
  - Condição de disparo
  - Ação automatizada
  - Destinatários com contatos
  - Frequência de verificação
  - Botão "Testar Este Alerta"
- ✅ Seção de Histórico de Alertas está visível
- ✅ Tabela de log mostra 5 alertas simulados
- ✅ Badges de status funcionam (Resolvido, Em andamento, Crítico)

---

### 6. Testar Alertas pela Página de Alertas

**Passos**:
1. Na página de Sistema de Alertas, rolar até um card de alerta
2. Clicar no botão **"🧪 Testar Este Alerta"**
3. Ser redirecionado para a página principal
4. Observar o alerta sendo disparado automaticamente

**Validações**:
- ✅ Redirecionamento funciona
- ✅ Alerta dispara automaticamente após redirect
- ✅ Conteúdo do alerta corresponde ao botão clicado

---

### 7. Testar Responsividade (Mobile)

**Passos**:
1. Abrir a página no celular OU usar DevTools (F12) para simular mobile
2. Redimensionar a janela para diferentes tamanhos:
   - 320px (smartphone pequeno)
   - 768px (tablet)
   - 1024px (desktop)

**Validações**:
- ✅ Layout se adapta ao tamanho da tela
- ✅ Painéis de KPI empilham verticalmente em telas pequenas
- ✅ Menu de navegação permanece funcional
- ✅ Botões de teste são acessíveis
- ✅ Alertas aparecem corretamente em mobile
- ✅ Texto permanece legível

---

### 8. Verificar Links e Navegação

**Passos**:
1. Testar todos os links no menu de navegação
2. Clicar em links para documentação (.md files)
3. Testar link "Ver dashboard" nas notificações de alerta

**Validações**:
- ✅ Link "Dashboard" leva para index.html
- ✅ Link "Sistema de Alertas" leva para alerts.html
- ✅ Link "Documentação" tenta acessar README.md
- ✅ Links internos funcionam
- ✅ Não há links quebrados (404)

---

## 📊 Checklist de Testes Completo

### Funcionalidade Básica
- [ ] Dashboard principal carrega sem erros
- [ ] CSS está sendo aplicado corretamente
- [ ] JavaScript executa sem erros no console
- [ ] Todos os 3 painéis (A, B, C) são exibidos
- [ ] KPIs mostram valores de exemplo

### Sistema de Alertas
- [ ] Alerta 1 (Queda Cliente) funciona
- [ ] Alerta 2 (Burn Rate) funciona
- [ ] Alerta 3 (Margem SPC) funciona
- [ ] Notificações aparecem no canto inferior direito
- [ ] Botão fechar (X) funciona
- [ ] Auto-close após 10s funciona
- [ ] Conteúdo dos alertas está completo e formatado

### Página de Alertas
- [ ] Página alerts.html carrega
- [ ] 3 cards de alertas são exibidos
- [ ] Informações de cada alerta estão completas
- [ ] Histórico de alertas está visível
- [ ] Botões "Testar Este Alerta" funcionam

### Navegação e Links
- [ ] Menu de navegação funciona
- [ ] Links entre páginas funcionam
- [ ] Links para documentação existem
- [ ] Não há erros 404

### Responsividade
- [ ] Layout funciona em desktop (1920px)
- [ ] Layout funciona em tablet (768px)
- [ ] Layout funciona em mobile (375px)
- [ ] Texto permanece legível em todas as resoluções

### Performance
- [ ] Página carrega em menos de 3 segundos
- [ ] Não há erros no console do navegador
- [ ] Imagens/recursos carregam corretamente
- [ ] Animações são suaves

---

## 🐛 Problemas Conhecidos e Soluções

### Problema: CSS não carrega
**Solução**: Verificar se o caminho `webapp/static/css/style.css` está correto

### Problema: Alerta não aparece
**Solução**: Verificar console do navegador (F12) por erros JavaScript

### Problema: Página não carrega no GitHub Pages
**Solução**: 
1. Verificar se GitHub Pages está habilitado nas configurações do repositório
2. Verificar se a branch correta está selecionada
3. Aguardar alguns minutos após o push (deploy pode demorar)

---

## 📝 Relatório de Testes

### Ambiente de Teste Local
- **Data**: 29/12/2025
- **Navegador**: Chrome/Firefox/Safari
- **Servidor**: Python HTTP Server (porta 8080)
- **Status**: ✅ Todos os testes passaram

### Resultados
```
✅ Dashboard principal carrega corretamente
✅ Alerta 1 (Queda Cliente Top 20) funciona
✅ Alerta 2 (Burn Rate Negativo) funciona
✅ Alerta 3 (Margem SPC Baixa) funciona
✅ Página de Sistema de Alertas carrega
✅ Navegação entre páginas funciona
✅ CSS e JavaScript carregam sem erros
✅ Layout responsivo funciona
```

---

## 🚀 Próximos Passos Após Testes

1. **Validar no GitHub Pages**: Após merge, verificar em produção
2. **Coletar Feedback**: Apresentar para Diretoria e Gerentes
3. **Ajustes Finos**: Implementar melhorias baseadas em feedback
4. **Implementação Real**: Seguir [SISTEMA_ALERTAS.md](./SISTEMA_ALERTAS.md) para configurar Power Automate + Twilio
5. **Integração com Dados Reais**: Conectar ao ERP da CDL Manaus

---

## 📞 Suporte

Para problemas técnicos ou dúvidas sobre os testes:
- Consultar [SISTEMA_ALERTAS.md](./SISTEMA_ALERTAS.md) para detalhes técnicos
- Verificar console do navegador (F12) para erros
- Testar em navegador diferente para descartar incompatibilidades

---

**Documento criado**: 29/12/2025  
**Última atualização**: 29/12/2025  
**Versão**: 1.0
