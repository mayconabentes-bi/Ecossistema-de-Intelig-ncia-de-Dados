# Instruções de Configuração do GitHub Pages

## ⚠️ Configuração Necessária

Para que o sistema funcione corretamente via GitHub Pages, o administrador do repositório precisa configurar o GitHub Pages nas configurações do repositório.

---

## 📋 Passos para Habilitar GitHub Pages

### 1. Acessar Configurações do Repositório

1. Ir para: https://github.com/mayconabentes-bi/Ecossistema-de-Intelig-ncia-de-Dados/settings
2. No menu lateral esquerdo, clicar em **"Pages"**

### 2. Configurar Source

Na seção **"Build and deployment"**:

- **Source**: Selecionar **"GitHub Actions"**
- Não precisa selecionar branch manualmente (o workflow cuida disso)

### 3. Salvar e Aguardar

- Clicar em **"Save"** se houver botão
- O GitHub Actions já está configurado via `.github/workflows/deploy-pages.yml`
- A cada push nas branches `main` ou `copilot/deploy-github-pages`, o deploy acontecerá automaticamente

### 4. Verificar Deploy

Após configurar e fazer um novo push:

1. Ir para a aba **"Actions"** do repositório
2. Verificar o workflow **"Deploy to GitHub Pages"**
3. Aguardar conclusão (geralmente 1-3 minutos)
4. Acessar: https://mayconabentes-bi.github.io/Ecossistema-de-Intelig-ncia-de-Dados/

---

## 🔧 Workflow GitHub Actions

O arquivo `.github/workflows/deploy-pages.yml` já está configurado e fará o seguinte automaticamente:

1. **Trigger**: Executa a cada push em `main` ou `copilot/deploy-github-pages`
2. **Checkout**: Baixa o código do repositório
3. **Setup Pages**: Configura o ambiente do GitHub Pages
4. **Upload**: Empacota todos os arquivos estáticos
5. **Deploy**: Publica no GitHub Pages

---

## 📁 Arquivos Estáticos Publicados

Os seguintes arquivos serão servidos pelo GitHub Pages:

```
/
├── index.html              → Dashboard principal
├── alerts.html             → Sistema de alertas
├── webapp/
│   └── static/
│       ├── css/style.css   → Estilos
│       └── js/script.js    → Scripts
├── *.md                    → Documentação (README, etc.)
└── .github/workflows/      → Workflows (não visível ao público)
```

---

## 🧪 Testando Localmente (Opcional)

Antes de publicar, você pode testar localmente:

```bash
# Opção 1: Python
cd /caminho/para/Ecossistema-de-Intelig-ncia-de-Dados
python -m http.server 8000
# Acessar: http://localhost:8000

# Opção 2: Node.js
npx http-server -p 8000
# Acessar: http://localhost:8000

# Opção 3: PHP
php -S localhost:8000
```

---

## 🐛 Troubleshooting

### Problema: Workflow falha com "Pages not configured"

**Solução**: 
1. Ir em **Settings** → **Pages**
2. Alterar Source para **"GitHub Actions"**
3. Fazer um novo push ou re-run do workflow

### Problema: Página mostra 404

**Possíveis causas**:
1. Deploy ainda não completou (aguardar 2-3 minutos)
2. GitHub Pages não está habilitado
3. URL incorreta (verificar se é https://mayconabentes-bi.github.io/Ecossistema-de-Intelig-ncia-de-Dados/)

**Solução**:
1. Verificar aba **Actions** para ver status do deploy
2. Confirmar GitHub Pages está habilitado em Settings
3. Limpar cache do navegador (Ctrl+Shift+R)

### Problema: CSS/JS não carregam

**Solução**:
- Verificar console do navegador (F12) para erros
- Confirmar que os caminhos estão corretos: `webapp/static/css/style.css`
- Aguardar alguns minutos (pode ser cache do CDN do GitHub)

---

## ✅ Checklist de Configuração

- [ ] GitHub Pages habilitado em Settings → Pages
- [ ] Source configurado para "GitHub Actions"
- [ ] Workflow executado com sucesso (verificar em Actions)
- [ ] Site acessível em: https://mayconabentes-bi.github.io/Ecossistema-de-Intelig-ncia-de-Dados/
- [ ] Dashboard carrega com os 3 painéis (A, B, C)
- [ ] Botões de teste de alertas funcionam
- [ ] Página alerts.html carrega corretamente
- [ ] CSS está sendo aplicado (cores, layout)
- [ ] JavaScript funciona (alertas aparecem)

---

## 📞 Suporte

Se após seguir esses passos o sistema não funcionar:

1. Verificar logs do workflow em **Actions** → **Deploy to GitHub Pages**
2. Confirmar que todos os arquivos foram commitados:
   - `index.html`
   - `alerts.html`
   - `.github/workflows/deploy-pages.yml`
   - `webapp/static/css/style.css`
   - `webapp/static/js/script.js`
3. Consultar [GUIA_TESTES_ALERTAS.md](./GUIA_TESTES_ALERTAS.md) para testes completos

---

**Última atualização**: 29/12/2025  
**Versão**: 1.0
