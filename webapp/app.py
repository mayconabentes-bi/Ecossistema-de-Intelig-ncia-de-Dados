"""
Ecossistema de Inteligência de Dados - CDL Manaus
Sistema Interno de Visualização e Entrada de Dados
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import json
import os
from datetime import datetime

app = Flask(__name__)
# IMPORTANTE: Em produção, usar variável de ambiente: app.secret_key = os.environ.get('SECRET_KEY')
app.secret_key = os.environ.get('SECRET_KEY', 'cdl-manaus-secret-key-change-in-production')

# Configurações
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'entries.json')

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
