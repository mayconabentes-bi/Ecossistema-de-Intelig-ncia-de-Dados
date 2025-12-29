"""
Ecossistema de Inteligência de Dados - CDL Manaus
Sistema Interno de Visualização e Entrada de Dados
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import json
import os
from datetime import datetime
import pandas as pd
import sqlite3

app = Flask(__name__)
# IMPORTANTE: Em produção, usar variável de ambiente: app.secret_key = os.environ.get('SECRET_KEY')
app.secret_key = os.environ.get('SECRET_KEY', 'cdl-manaus-secret-key-change-in-production')

# Configurações
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'entries.json')
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
DATABASE_FILE = os.path.join(os.path.dirname(__file__), 'database.db')
ALLOWED_EXTENSIONS = {'csv'}

# Criar pasta de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Usuários (em produção, usar banco de dados)
USERS = {
    'admin': generate_password_hash('cdl2025'),
    'gestor': generate_password_hash('gestor2025')
}

def login_required(f):
    """Decorator para proteger rotas que requerem autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def load_data():
    """Carrega dados do arquivo JSON"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    """Salva dados no arquivo JSON"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processar_csv_financeiro(filepath):
    """
    Processa arquivo CSV financeiro legado e salva no banco SQLite.
    
    Args:
        filepath: Caminho do arquivo CSV a ser processado
        
    Returns:
        tuple: (sucesso: bool, mensagem: str, linhas_processadas: int)
    """
    try:
        # Tentar ler CSV com encoding latin1 e pulando linhas de cabeçalho
        # O sistema legado geralmente tem 4-5 linhas de lixo antes dos dados reais
        df = pd.read_csv(filepath, encoding='latin1', header=4, on_bad_lines='skip')
        
        # Remover linhas completamente vazias
        df = df.dropna(how='all')
        
        # Se o dataframe estiver vazio após limpeza
        if df.empty:
            return False, "O arquivo CSV está vazio ou não contém dados válidos.", 0
        
        # Conectar ao banco SQLite
        conn = sqlite3.connect(DATABASE_FILE)
        
        # Adicionar metadados de importação
        df['data_importacao'] = datetime.now().isoformat()
        df['arquivo_origem'] = os.path.basename(filepath)
        
        # Salvar no banco de dados (append para criar histórico)
        linhas_inseridas = len(df)
        df.to_sql('financeiro', conn, if_exists='append', index=False)
        
        conn.close()
        
        return True, f"Arquivo processado com sucesso! {linhas_inseridas} linhas importadas.", linhas_inseridas
        
    except UnicodeDecodeError:
        return False, "Erro de codificação: O arquivo não está no formato esperado (latin1).", 0
    except pd.errors.EmptyDataError:
        return False, "Arquivo CSV vazio ou corrompido.", 0
    except Exception as e:
        return False, f"Erro ao processar arquivo: {str(e)}", 0

@app.route('/')
def index():
    """Página principal - Dashboard de visualização pública"""
    data = load_data()
    return render_template('index.html', entries_count=len(data))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and check_password_hash(USERS[username], password):
            session['username'] = username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('data_entry'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout do sistema"""
    session.pop('username', None)
    flash('Logout realizado com sucesso.', 'info')
    return redirect(url_for('index'))

@app.route('/data-entry', methods=['GET', 'POST'])
@login_required
def data_entry():
    """Página de entrada de dados (protegida)"""
    if request.method == 'POST':
        # Validar e sanitizar dados do formulário
        try:
            valor = float(request.form.get('valor', 0))
            if valor < 0:
                raise ValueError("Valor não pode ser negativo")
        except (ValueError, TypeError):
            flash('Valor inválido. Por favor, insira um número válido.', 'danger')
            data = load_data()
            return render_template('data_entry.html', entries=data)
        
        entry = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'timestamp': datetime.now().isoformat(),
            'usuario': escape(session['username']),
            'cliente': escape(request.form.get('cliente', '')),
            'tipo_receita': escape(request.form.get('tipo_receita', '')),
            'valor': valor,
            'mes_referencia': escape(request.form.get('mes_referencia', '')),
            'observacoes': escape(request.form.get('observacoes', ''))
        }
        
        # Carregar dados existentes e adicionar novo
        data = load_data()
        data.append(entry)
        save_data(data)
        
        flash('Dados registrados com sucesso!', 'success')
        return redirect(url_for('data_entry'))
    
    # Carregar dados para visualização (últimos 20 registros)
    data = load_data()
    recent_entries = data[-20:][::-1] if data else []  # Últimos 20, ordem reversa
    return render_template('data_entry.html', entries=recent_entries)

@app.route('/api/entries')
def api_entries():
    """API para obter dados em JSON"""
    data = load_data()
    return jsonify(data)

@app.route('/api/stats')
def api_stats():
    """API para estatísticas resumidas"""
    data = load_data()
    
    if not data:
        return jsonify({
            'total_entries': 0,
            'total_value': 0,
            'last_update': None
        })
    
    total_value = sum(entry.get('valor', 0) for entry in data)
    last_entry = max(data, key=lambda x: x.get('timestamp', ''))
    
    return jsonify({
        'total_entries': len(data),
        'total_value': total_value,
        'last_update': last_entry.get('timestamp')
    })

@app.route('/upload_csv', methods=['POST'])
@login_required
def upload_csv():
    """
    Rota para upload e processamento de arquivos CSV financeiros.
    Realiza ETL: Extract (upload), Transform (pandas), Load (SQLite).
    """
    try:
        # Verificar se o arquivo foi enviado
        if 'csv_file' not in request.files:
            flash('Nenhum arquivo foi selecionado.', 'danger')
            return redirect(url_for('data_entry'))
        
        file = request.files['csv_file']
        
        # Verificar se o usuário selecionou um arquivo
        if file.filename == '':
            flash('Nenhum arquivo foi selecionado.', 'danger')
            return redirect(url_for('data_entry'))
        
        # Verificar se o arquivo tem extensão permitida
        if file and allowed_file(file.filename):
            # Sanitizar nome do arquivo
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            # Salvar arquivo temporariamente
            file.save(filepath)
            
            # Processar CSV e carregar no banco
            sucesso, mensagem, linhas = processar_csv_financeiro(filepath)
            
            if sucesso:
                flash(mensagem, 'success')
            else:
                flash(mensagem, 'danger')
            
            # Opcional: Remover arquivo temporário após processamento
            # os.remove(filepath)
            
        else:
            flash('Formato de arquivo inválido. Por favor, envie um arquivo CSV.', 'danger')
    
    except Exception as e:
        flash(f'Erro ao processar upload: {str(e)}', 'danger')
    
    return redirect(url_for('data_entry'))

if __name__ == '__main__':
    # Para desenvolvimento: debug=True
    # Para produção: usar gunicorn ou waitress, debug=False
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
