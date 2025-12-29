# Sistema Interno - CDL Manaus
## Ecossistema de Inteligência de Dados

Sistema web para visualização de dados e entrada de informações do ecossistema de BI da CDL Manaus.

## 📋 Funcionalidades

### 1. Dashboard de Visualização (Público)
- **Painel A - O Pulmão**: Indicadores financeiros e fluxo de caixa
- **Painel B - O Motor**: Métricas comerciais e carteira de clientes
- **Painel C - A Máquina**: Análise de produtos e margem de contribuição
- Atualização em tempo real via API
- Interface responsiva e moderna

### 2. Sistema de Login
- Autenticação segura com senha hash
- Sessões protegidas
- Controle de acesso

### 3. Entrada de Dados (Protegida)
- Formulário para registro de faturamento
- Validação de dados
- Histórico de registros
- Múltiplos tipos de receita (Mensalidade, SPC, Certificado Digital, etc.)

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Navegue até o diretório do webapp:**
```bash
cd webapp
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação:**
```bash
python app.py
```

4. **Acesse no navegador:**
```
http://localhost:5000
```

## 🔐 Credenciais de Acesso

### Usuários Padrão:

**Administrador:**
- Usuário: `admin`
- Senha: `cdl2025`

**Gestor:**
- Usuário: `gestor`
- Senha: `gestor2025`

> ⚠️ **IMPORTANTE**: Altere estas credenciais em ambiente de produção!

## 📁 Estrutura do Projeto

```
webapp/
├── app.py                  # Aplicação Flask principal
├── requirements.txt        # Dependências Python
├── data/                   # Dados persistidos (JSON)
│   └── entries.json        # Registros de entrada
├── static/                 # Arquivos estáticos
│   ├── css/
│   │   └── style.css      # Estilos CSS
│   └── js/
│       └── script.js      # JavaScript
└── templates/             # Templates HTML
    ├── base.html          # Template base
    ├── index.html         # Dashboard principal
    ├── login.html         # Página de login
    └── data_entry.html    # Entrada de dados
```

## 🌐 Endpoints da API

### GET `/`
Página principal com dashboard de visualização

### GET/POST `/login`
Sistema de autenticação

### GET `/logout`
Encerrar sessão

### GET/POST `/data-entry`
Entrada de dados (requer autenticação)

### GET `/api/entries`
Retorna todos os registros em JSON

### GET `/api/stats`
Retorna estatísticas consolidadas:
- Total de entradas
- Valor total registrado
- Data da última atualização

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Autenticação**: Werkzeug Security
- **Armazenamento**: JSON (para simplicidade)
- **UI**: Design responsivo customizado

## 📊 Integração com Power BI

Este sistema complementa os dashboards Power BI descritos na documentação principal:
- Os dados podem ser exportados para integração com Power BI
- API REST disponível para consumo de dados
- Estrutura de dados compatível com o modelo dimensional

## 🔒 Segurança

### Implementado:
- ✅ Senhas com hash (Werkzeug)
- ✅ Sessões seguras com secret key
- ✅ Proteção de rotas com decorator `@login_required`
- ✅ Sanitização de inputs

### Recomendações para Produção:
- [ ] Alterar `app.secret_key` para valor seguro único
- [ ] Usar HTTPS (SSL/TLS)
- [ ] Implementar rate limiting
- [ ] Adicionar logs de auditoria
- [ ] Migrar de JSON para banco de dados (PostgreSQL/MySQL)
- [ ] Implementar backup automático
- [ ] Adicionar validação CSRF

## 🚀 Deploy em Produção

### Opção 1: Heroku
```bash
# Adicionar Procfile
echo "web: gunicorn app:app" > Procfile
pip install gunicorn
heroku create cdl-manaus-bi
git push heroku main
```

### Opção 2: Azure App Service
1. Criar App Service no Azure Portal
2. Configurar Python 3.8+
3. Deploy via Git ou GitHub Actions

### Opção 3: AWS Elastic Beanstalk
```bash
pip install awsebcli
eb init -p python-3.8 cdl-manaus
eb create cdl-production
eb deploy
```

### Opção 4: Servidor Próprio (Ubuntu)
```bash
# Instalar dependências
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Configurar aplicação
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Executar com Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 📈 Próximas Melhorias

- [ ] Integração direta com ERP
- [ ] Gráficos interativos (Chart.js)
- [ ] Export para Excel/CSV
- [ ] Sistema de notificações
- [ ] Dashboard de métricas em tempo real
- [ ] Integração com WhatsApp (alertas)
- [ ] Relatórios PDF automáticos
- [ ] Análise preditiva com Machine Learning

## 🐛 Troubleshooting

### Erro: "Address already in use"
```bash
# Matar processo na porta 5000
lsof -ti:5000 | xargs kill -9
```

### Erro: "Module not found"
```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Dados não aparecem
- Verificar se arquivo `data/entries.json` existe
- Verificar permissões de escrita no diretório `data/`

## 📞 Suporte

Para questões técnicas sobre este sistema web:
1. Consultar a documentação principal do projeto
2. Verificar logs da aplicação Flask
3. Revisar issues no repositório GitHub

## 📄 Licença

MIT License - Ver arquivo LICENSE na raiz do projeto

---

**Desenvolvido para CDL Manaus** | Versão 1.0 | Dezembro 2025
