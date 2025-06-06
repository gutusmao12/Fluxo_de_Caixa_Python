from flask import Flask, render_template, request, redirect, url_for, session
from db_config import get_db_connection
from datetime import datetime
import hashlib

app = Flask(__name__)
app.secret_key = 'chave_super_secreta'

# Usuário fixo (podemos migrar pro banco depois)
USUARIO = {
    "username": "guga.vilelad@gmail.com",
    "password": hashlib.sha256("T3st$".encode()).hexdigest()  # senha: 1234
}

@app.template_filter('formata_data')
def formata_data(data):
    if data:
        return data.strftime('%d/%m/%Y')
    return ''



@app.template_filter('formata_brl')
def formata_brl(valor):
    if valor is None:
        return "R$ 0,00"
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")


@app.route('/detalhamento')
def detalhamento():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Buscar entradas
    cursor.execute("SELECT id, descricao, valor, data FROM entradas ORDER BY data DESC")
    entradas = cursor.fetchall()

    # Buscar saídas
    cursor.execute("SELECT id, descricao, valor, data FROM saidas ORDER BY data DESC")
    saidas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('detalhamento.html', entradas=entradas, saidas=saidas)

# --- Editar Entrada ---
@app.route('/editar_entrada/<int:id>', methods=['GET', 'POST'])
def editar_entrada(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        novo_valor = request.form['valor']
        nova_descricao = request.form['descricao']
        cursor.execute(
            "UPDATE entradas SET descricao = %s, valor = %s WHERE id = %s",
            (nova_descricao, novo_valor, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('detalhamento'))

    cursor.execute("SELECT id, descricao, valor FROM entradas WHERE id = %s", (id,))
    entrada = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('editar.html', tipo='entrada', item=entrada)


# --- Editar Saída ---
@app.route('/editar_saida/<int:id>', methods=['GET', 'POST'])
def editar_saida(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        novo_valor = request.form['valor']
        nova_descricao = request.form['descricao']
        cursor.execute(
            "UPDATE saidas SET descricao = %s, valor = %s WHERE id = %s",
            (nova_descricao, novo_valor, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('detalhamento'))

    cursor.execute("SELECT id, descricao, valor FROM saidas WHERE id = %s", (id,))
    saida = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('editar.html', tipo='saida', item=saida)

@app.route('/excluir_entrada/<int:id>')
def excluir_entrada(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entradas WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('detalhamento'))

@app.route('/excluir_saida/<int:id>')
def excluir_saida(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM saidas WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('detalhamento'))

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

@app.route('/adicionar_entrada', methods=['GET', 'POST'])
def adicionar_entrada():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = float(request.form['valor'])
        data = request.form['data']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entradas (descricao, valor, data) VALUES (%s, %s, %s)", (descricao, valor, data))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('dashboard'))

    return render_template('entrada.html')

@app.route('/adicionar_saida', methods=['GET', 'POST'])
def adicionar_saida():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = float(request.form['valor'])
        data = request.form['data']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO saidas (descricao, valor, data) VALUES (%s, %s, %s)", (descricao, valor, data))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('dashboard'))

    return render_template('saida.html')


if __name__ == '__main__':
    app.run(debug=True)