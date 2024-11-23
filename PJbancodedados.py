import sqlite3

class BancoDeDados:
    def __init__(self, banco):
        self.banco = banco
        self.conexao = sqlite3.connect(banco)
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Produtos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco REAL NOT NULL
            );
        ''')
        self.conexao.commit()

    def adicionar_produto(self, nome, quantidade, preco):
        self.cursor.execute('''
            INSERT INTO Produtos (nome, quantidade, preco)
            VALUES (?, ?, ?);
        ''', (nome, quantidade, preco))
        self.conexao.commit()

    def listar_produtos(self):
        self.cursor.execute('''
            SELECT * FROM Produtos;
        ''')
        return self.cursor.fetchall()

    def atualizar_produto(self, id_produto, quantidade=None, preco=None):
        if quantidade is not None:
            self.cursor.execute('''
                UPDATE Produtos SET quantidade = ?
                WHERE id = ?;
            ''', (quantidade, id_produto))
        if preco is not None:
            self.cursor.execute('''
                UPDATE Produtos SET preco = ?
                WHERE id = ?;
            ''', (preco, id_produto))
        self.conexao.commit()

    def remover_produto(self, id_produto):
        self.cursor.execute('''
            DELETE FROM Produtos
            WHERE id = ?;
        ''', (id_produto,))
        self.conexao.commit()

    def buscar_produto(self, id_produto=None, nome_produto=None):
        if id_produto is not None:
            self.cursor.execute('''
                SELECT * FROM Produtos
                WHERE id = ?;
            ''', (id_produto,))
        elif nome_produto is not None:
            self.cursor.execute('''
                SELECT * FROM Produtos
                WHERE nome LIKE ?;
            ''', (f'%{nome_produto}%',))
        return self.cursor.fetchall()

    def calcular_valor_total(self):
        self.cursor.execute('''
            SELECT SUM(quantidade * preco) FROM Produtos;
        ''')
        return self.cursor.fetchone()[0]
    
import sqlite3

def main():
    banco_de_dados = BancoDeDados('estoque.db')

    while True:
        print("\n**Sistema de Controle de Estoque**")
        print("1. Adicionar Produto")
        print("2. Listar Produtos")
        print("3. Atualizar Produto")
        print("4. Remover Produto")
        print("5. Buscar Produto")
        print("6. Calcular Valor Total")
        print("7. Sair")

        opcao = int(input("Digite a opção: "))

        if opcao == 1:
            nome = input("Digite o nome do produto: ")
            quantidade = int(input("Digite a quantidade do produto: "))
            preco = float(input("Digite o preço do produto: "))
            banco_de_dados.adicionar_produto(nome, quantidade, preco)
        elif opcao == 2:
            produtos = banco_de_dados.listar_produtos()
            for produto in produtos:
                print(f"ID: {produto[0]}, Nome: {produto[1]}, Quantidade: {produto[2]}, Preço: {produto[3]}")
        elif opcao == 3:
            id_produto = int(input("Digite o ID do produto: "))
            quantidade = int(input("Digite a nova quantidade do produto: "))
            preco = float(input("Digite o novo preço do produto: "))
            banco_de_dados.atualizar_produto(id_produto, quantidade, preco)
        elif opcao == 4:
            id_produto = int(input("Digite o ID do produto: "))
            banco_de_dados.remover_produto(id_produto)
        elif opcao == 5:
            id_produto = int(input("Digite o ID do produto: "))
            produto = banco_de_dados.buscar_produto(id_produto)
            if produto:
                print(f"ID: {produto[0][0]}, Nome: {produto[0][1]}, Quantidade: {produto[0][2]}, Preço: {produto[0][3]}")
            else:
                print("Produto não encontrado")
        elif opcao == 6:
            valor_total = banco_de_dados.calcular_valor_total()
            print(f"Valor Total: {valor_total:.2f}")
        elif opcao == 7:
            break
        else:
            print("Opção inválida") 

    banco_de_dados.conexao.close()

if __name__ == '__main__':
    main()