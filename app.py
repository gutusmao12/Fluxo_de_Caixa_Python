from flask import Flask, render_template, request, redirect, url_for, session
from db_config import get_db_connection
from datetime import datetime
import hashlib

app = Flask(__name__)
app.secret_key = 'chave_super_secreta'

# Usuário fixo (podemos migrar pro banco depois)
USUARIO = {
    "username": "Gustavo Vilela",
    "password": hashlib.sha256("T3st$".encode()).hexdigest()  # senha: 1234
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        if usuario == USUARIO['username'] and senha_hash == USUARIO['password']:
            session['usuario'] = usuario
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', erro='Usuário ou senha inválidos')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(valor) FROM entradas")
    total_entradas = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(valor) FROM saidas")
    total_saidas = cursor.fetchone()[0] or 0

    saldo = total_entradas - total_saidas

    cursor.close()
    conn.close()

    return render_template('dashboard.html', entradas=total_entradas, saidas=total_saidas, saldo=saldo)

# --- ADICIONAR ENTRADA ---
@app.route('/adicionar_entrada', methods=['GET', 'POST'])
def adicionar_entrada():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = float(request.form['valor'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entradas (descricao, valor) VALUES (%s, %s)", (descricao, valor))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('dashboard'))

    return render_template('entrada.html')


# --- ADICIONAR SAÍDA ---
@app.route('/adicionar_saida', methods=['GET', 'POST'])
def adicionar_saida():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = float(request.form['valor'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO saidas (descricao, valor) VALUES (%s, %s)", (descricao, valor))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('dashboard'))

    return render_template('saida.html')


if __name__ == '__main__':
    app.run(debug=True)