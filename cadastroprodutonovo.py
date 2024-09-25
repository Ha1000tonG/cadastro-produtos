import sqlite3
import pandas as pd
from tkinter import ttk
import customtkinter
from tkinter import messagebox
from tkinter import *


# Função para conectar ao banco de dados
def conectar_bd():
    return sqlite3.connect("produtos.db")


# Função para criar a tabela se não existir
def criar_tabela():
    conexao = conectar_bd()
    with conexao:
        c = conexao.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                valor DECIMAL NOT NULL,
                tipo TEXT NOT NULL
            )
        """
        )
    conexao.close()


# Função para cadastrar produtos no banco de dados
def cadastrar_produto(descricao, quantidade, valor, tipo):
    conexao = conectar_bd()
    with conexao:
        c = conexao.cursor()
        c.execute(
            """
            INSERT INTO produtos (descricao, quantidade, valor, tipo)
            VALUES (?, ?, ?, ?)""",
            (descricao, quantidade, valor, tipo),
        )
    conexao.close()


# Função para selecionar produtos do banco de dados
def selecionar_produtos():
    conexao = conectar_bd()
    with conexao:
        c = conexao.cursor()
        c.execute("SELECT * FROM produtos")
        produtos = c.fetchall()
    conexao.close()
    return produtos


# Função para deletar um produto pelo ID
def deletar_produto(produto_id):
    conexao = conectar_bd()
    with conexao:
        c = conexao.cursor()
        c.execute("DELETE FROM produtos WHERE ID = ?", (produto_id,))
    conexao.close()


# Função para deletar todos os produtos
def deletar_todos_produtos():
    resposta = messagebox.askyesno(
        "Confirmação", "Tem certeza que deseja deletar todos os produtos?"
    )
    if resposta:
        conexao = conectar_bd()
        with conexao:
            c = conexao.cursor()
            c.execute("DELETE FROM produtos")
        conexao.close()
        messagebox.showinfo("Sucesso", "Todos os produtos foram deletados com sucesso!")
        mostrar_produtos()


# Função para exportar os dados para Excel
def exportar_para_excel():
    produtos = selecionar_produtos()
    df_produtos = pd.DataFrame(
        produtos, columns=["ID", "Descrição", "Quantidade", "Valor", "Tipo"]
    )
    df_produtos.to_excel("produtos.xlsx", index=False)
    messagebox.showinfo("Exportar para Excel", "Exportação realizada com sucesso!")


# Função para validar o formulário de cadastro
def validar_campos():
    if not entry_descricao.get():
        messagebox.showerror("Erro", "Preencha o campo Descrição")
        return False
    if not entry_quantidade.get().isdigit():
        messagebox.showerror("Erro", "Preencha o campo Quantidade corretamente")
        return False
    if not entry_valor.get().replace(".", "", 1).isdigit():
        messagebox.showerror("Erro", "Preencha o campo Valor corretamente")
        return False
    if not combobox_tipo.get():
        messagebox.showerror("Erro", "Selecione um Tipo")
        return False
    return True


# Função para cadastrar produto via interface
def cadastrar_produtos():
    if entry_descricao.get() == "":
        messagebox.showerror("Erro", "Preencher o campo Descrição")
    elif entry_quantidade.get() == "":
        messagebox.showerror("Erro", "Preencher o campo Quantidade")
    elif entry_valor.get() == "":
        messagebox.showerror("Erro", "Preencher o campo Valor")
    elif combobox_tipo.get() == "":
        messagebox.showerror("Erro", "Preencher o campo Tipo Unidade")
    else:
        # Conectar ao banco de dados
        conexao = sqlite3.connect("produtos.db")
        c = conexao.cursor()

        # Inserir dados no banco
        c.execute(
            "INSERT INTO produtos (descricao, quantidade, valor, tipo) VALUES (?, ?, ?, ?)",
            (
                entry_descricao.get(),
                entry_quantidade.get(),
                entry_valor.get(),
                combobox_tipo.get(),
            ),
        )

        conexao.commit()
        conexao.close()

        # Exibir mensagem de sucesso
        messagebox.showinfo("Cadastro de Produtos", "Cadastro realizado com sucesso!")

        # Limpar os campos de entrada
        entry_descricao.delete(0, "end")
        entry_quantidade.delete(0, "end")
        entry_valor.delete(0, "end")

        # Atualizar o Treeview
        mostrar_produtos()


# Função para limpar os campos do formulário
def limpar_campos():
    entry_descricao.delete(0, END)
    entry_quantidade.delete(0, END)
    entry_valor.delete(0, END)
    combobox_tipo.set("")


# Função para deletar produto via interface
def deletar():
    try:
        item_selecionado = tree.selection()[0]
        produto_id = tree.item(item_selecionado, "values")[
            0
        ]  # ID está oculto, mas ainda é necessário
        deletar_produto(produto_id)
        messagebox.showinfo("Sucesso", "Produto deletado com sucesso")
        mostrar_produtos()
    except IndexError:
        messagebox.showerror("Erro", "Selecione um produto para deletar")


# Função para mostrar os produtos no Treeview, ocultando o ID
def mostrar_produtos():
    global tree  # Declaração global para o Treeview

    # Limpa o conteúdo atual do frameDireita
    for widget in frameDireita.winfo_children():
        widget.destroy()

    lista_produtos = selecionar_produtos()  # Função que carrega os produtos do banco

    # Se a lista de produtos estiver vazia, vamos garantir que pelo menos o cabeçalho apareça
    if not lista_produtos:
        lista_produtos = []

    # Configura o estilo do Treeview para ajustar cores e design
    style = ttk.Style()
    style.theme_use("default")  # Use o tema padrão para customização
    style.configure(
        "Treeview",
        background="#2a2d2e",  # Cor de fundo para as linhas do Treeview
        foreground="white",  # Cor do texto
        fieldbackground="#2a2d2e",  # Cor de fundo das células
        rowheight=25,  # Altura das linhas
    )
    style.map(
        "Treeview",
        background=[("selected", "#22559b")],  # Cor ao selecionar um item
    )

    # Ajustar o tamanho do Treeview de acordo com a quantidade de produtos cadastrados
    tree = ttk.Treeview(
        frameDireita,
        columns=["Descrição", "Quantidade", "Valor", "Tipo"],
        show="headings",  # Remove a coluna vazia da esquerda
    )

    # Configura os cabeçalhos
    tree.heading("Descrição", text="Descrição")
    tree.heading("Quantidade", text="Quantidade")
    tree.heading("Valor", text="Valor")
    tree.heading("Tipo", text="Tipo")

    # Configura as colunas (largura e alinhamento)
    tree.column("Descrição", width=200, anchor="center")
    tree.column("Quantidade", width=100, anchor="center")
    tree.column("Valor", width=100, anchor="center")
    tree.column("Tipo", width=150, anchor="center")

    # Insere os dados no Treeview, sem o ID
    for produto in lista_produtos:
        # produto[1] = descrição, produto[2] = quantidade, produto[3] = valor, produto[4] = tipo
        tree.insert("", "end", values=(produto[1], produto[2], produto[3], produto[4]))

    # Scrollbar vertical
    vsb = customtkinter.CTkScrollbar(
        frameDireita, orientation="vertical", command=tree.yview
    )
    tree.configure(yscrollcommand=vsb.set)

    # Organiza o layout do Treeview e a scrollbar
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")

    # Expande o frame para garantir que o Treeview ocupe o espaço corretamente
    frameDireita.grid_rowconfigure(0, weight=1)
    frameDireita.grid_columnconfigure(0, weight=1)

    # Rolagem automática para o topo
    tree.yview_moveto(0)


# Interface gráfica
janela = customtkinter.CTk()
janela.title("Cadastro de Produtos")
janela.geometry("780x390")
janela.resizable(False, False)

frameBaixo = customtkinter.CTkFrame(janela, width=410, height=303)
frameBaixo.grid(row=0, column=0, pady=1, padx=1, sticky=NSEW)

frameDireita = customtkinter.CTkFrame(janela, width=588, height=303)
frameDireita.grid(row=0, column=1, pady=3, padx=1, sticky=NSEW)

# Labels e inputs
customtkinter.CTkLabel(frameBaixo, text="Descrição:").grid(
    row=0, column=0, padx=10, pady=10
)
entry_descricao = customtkinter.CTkEntry(frameBaixo, width=300)
entry_descricao.grid(row=0, column=1)

customtkinter.CTkLabel(frameBaixo, text="Quantidade:").grid(
    row=1, column=0, padx=10, pady=10
)
entry_quantidade = customtkinter.CTkEntry(frameBaixo, width=300)
entry_quantidade.grid(row=1, column=1)

customtkinter.CTkLabel(frameBaixo, text="Valor:").grid(
    row=2, column=0, padx=10, pady=10
)
entry_valor = customtkinter.CTkEntry(frameBaixo, width=300)
entry_valor.grid(row=2, column=1)

customtkinter.CTkLabel(frameBaixo, text="Tipo:").grid(row=3, column=0, padx=10, pady=10)
lista_tipos = ["Caixa", "Saco", "Unidade"]
combobox_tipo = customtkinter.CTkComboBox(frameBaixo, values=lista_tipos, width=300)
combobox_tipo.grid(row=3, column=1)

# Botões
customtkinter.CTkButton(
    frameBaixo, text="Cadastrar Produto", command=cadastrar_produtos
).grid(row=4, column=0, columnspan=2, padx=10, pady=10)
customtkinter.CTkButton(
    frameBaixo, text="Exportar para Excel", command=exportar_para_excel
).grid(row=5, column=0, columnspan=2, padx=10, pady=10)
customtkinter.CTkButton(frameBaixo, text="Deletar Produto", command=deletar).grid(
    row=6, column=0, columnspan=2, padx=10, pady=10
)
customtkinter.CTkButton(
    frameBaixo, text="Deletar Todos", command=deletar_todos_produtos, fg_color="red"
).grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Inicializar o banco de dados e carregar os produtos na interface
criar_tabela()
mostrar_produtos()

janela.mainloop()
