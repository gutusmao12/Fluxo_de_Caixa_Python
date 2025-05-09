import psycopg2
import psycopg2.extras

# Conexão com o banco de dados PostgreSQL
conn = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='DragoN12$%',
    database='caixa_fluxo',
    port=5433  # padrão PostgreSQL
)

cursor = conn.cursor()

def adicionar_entrada(descricao, valor):
    cursor.execute("INSERT INTO entradas (descricao, valor) VALUES (%s, %s)", (descricao, valor))
    conn.commit()
    print("Entrada adicionada com sucesso.")

def adicionar_saida(descricao, valor):
    cursor.execute("INSERT INTO saidas (descricao, valor) VALUES (%s, %s)", (descricao, valor))
    conn.commit()
    print("Saída adicionada com sucesso.")

def calcular_fluxo():
    cursor.execute("SELECT SUM(valor) FROM entradas")
    total_entradas = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(valor) FROM saidas")
    total_saidas = cursor.fetchone()[0] or 0

    saldo = total_entradas - total_saidas
    print(f"\nTotal de Entradas: R$ {total_entradas:.2f}")
    print(f"Total de Saídas: R$ {total_saidas:.2f}")
    print(f"Saldo Final: R$ {saldo:.2f}")

    if saldo > 0:
        print("Situação: Lucro ✅")
    elif saldo < 0:
        print("Situação: Prejuízo ❌")
    else:
        print("Situação: Empate 😐")

# Exemplo de uso
while True:
    print("\n1. Adicionar Entrada")
    print("2. Adicionar Saída")
    print("3. Verificar Fluxo de Caixa")
    print("4. Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        desc = input("Descrição da entrada: ")
        valor = float(input("Valor: "))
        adicionar_entrada(desc, valor)
    elif opcao == '2':
        desc = input("Descrição da saída: ")
        valor = float(input("Valor: "))
        adicionar_saida(desc, valor)
    elif opcao == '3':
        calcular_fluxo()
    elif opcao == '4':
        break
    else:
        print("Opção inválida, tente novamente.")

cursor.close()
conn.close()