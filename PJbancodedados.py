import sqlite3


conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL CHECK (quantidade >= 0),
        preco REAL NOT NULL CHECK (preco >= 0)
    )
''')

def adicionar_produto():
    nome = input("Nome do produto: ")
    quantidade = int(input("Quantidade: "))
    preco = float(input("Preço: "))
    cursor.execute('INSERT INTO Produtos (nome, quantidade, preco) VALUES (?, ?, ?)', (nome, quantidade, preco))
    conn.commit()
    print("Produto adicionado com sucesso!")

def listar_produtos():
    cursor.execute('SELECT * FROM Produtos')
    produtos = cursor.fetchall()
    print("Produtos em estoque:")
    for produto in produtos:
        print(f"ID: {produto[0]}, Nome: {produto[1]}, Quantidade: {produto[2]}, Preço: {produto[3]:.2f}")

def atualizar_produto():
    id_produto = int(input("ID do produto a ser atualizado: "))
    quantidade = int(input("Nova quantidade (deixe em branco para não alterar): ") or "0")
    preco = float(input("Novo preço (deixe em branco para não alterar): ") or "0")
    if quantidade > 0:
        cursor.execute('UPDATE Produtos SET quantidade = ? WHERE id = ?', (quantidade, id_produto))
    if preco > 0:
        cursor.execute('UPDATE Produtos SET preco = ? WHERE id = ?', (preco, id_produto))
    conn.commit()
    print("Produto atualizado com sucesso!")

def remover_produto():
    id_produto = int(input("ID do produto a ser removido: "))
    cursor.execute('DELETE FROM Produtos WHERE id = ?', (id_produto,))
    conn.commit()
    print("Produto removido com sucesso!")

def buscar_produto():
    busca = input("Buscar produto por ID ou nome: ")
    if busca.isdigit():
        cursor.execute('SELECT * FROM Produtos WHERE id = ?', (int(busca),))
    else:
        cursor.execute('SELECT * FROM Produtos WHERE nome LIKE ?', ('%' + busca + '%',))
    produtos = cursor.fetchall()
    print("Produtos encontrados:")
    for produto in produtos:
        print(f"ID: {produto[0]}, Nome: {produto[1]}, Quantidade: {produto[2]}, Preço: {produto[3]:.2f}")

def calcular_valor_total():
    cursor.execute('SELECT SUM(quantidade * preco) FROM Produtos')
    total = cursor.fetchone()[0]
    print(f"Valor total do estoque: {total:.2f}")

def vender_produto():
    id_produto = int(input("ID do produto a ser vendido: "))
    quantidade_vendida = int(input("Quantidade vendida: "))
    cursor.execute('SELECT quantidade, preco FROM Produtos WHERE id = ?', (id_produto,))
    produto = cursor.fetchone()
    if produto and produto[0] >= quantidade_vendida:
        valor_venda = quantidade_vendida * produto[1]
        cursor.execute('UPDATE Produtos SET quantidade = ? WHERE id = ?', (produto[0] - quantidade_vendida, id_produto))
        conn.commit()
        print(f"Venda realizada com sucesso! Valor da venda: {valor_venda:.2f}")
    else:
        print("Erro: quantidade insuficiente em estoque.")

while True:
    print("\nSistema de Controle de Estoque")
    print("1. Adicionar Produto")
    print("2. Listar Produtos")
    print("3. Atualizar Produto")
    print("4. Remover Produto")
    print("5. Buscar Produto")
    print("6. Calcular Valor Total do Estoque")
    print("7. Vender Produto")
    print("0. Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        adicionar_produto()
    elif opcao == '2':
        listar_produtos()
    elif opcao == '3':
        atualizar_produto()
    elif opcao == '4':
        remover_produto()
    elif opcao == '5':
        buscar_produto()
    elif opcao == '6':
        calcular_valor_total()
    elif opcao == '7':
        vender_produto()
    elif opcao == '0':
        break
    else:
        print("Opção inválida. Tente novamente.")  

if __name__ == "__main__":
    main()
