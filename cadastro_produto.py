import sqlite3
import pandas as pd
from tkinter import ttk
import customtkinter
from tkinter import messagebox
from tkinter import *

# teste github

lista_tipos = ["Caixa", "Saco", "Unidade"]

janela = customtkinter.CTk()
janela.title("Cadastro de Produtos")
janela.geometry("980x320")
janela.resizable(width=FALSE, height=FALSE)

# dividindo a janela em quadros
frameBaixo = customtkinter.CTkFrame(janela, width=410, height=303)  # fg_color = "teal"
frameBaixo.grid(row=0, column=0, pady=1, padx=1, sticky=NSEW)

frameDireita = customtkinter.CTkFrame(janela, width=588, height=403)
frameDireita.grid(row=0, column=1, pady=3, padx=1, sticky=NSEW)

# conectando e criando o banco de dados
conexao = sqlite3.connect("produtos.db")
c = conexao.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS produtos(
    ID INTEGER PRIMARY KEY NOT NULL,
    descricao TEXT,
    quantidade INTEGER,
    valor DECIMAL,
    tipo TEXT
    )"""
)


def cadastrar_produtos():
    if entry_descricao.get() == "":
        messagebox.showerror("Erro", "Prencher o campo Descrição")
    elif entry_quantidade.get() == "":
        messagebox.showerror("Erro", "Prencher o campo Quantidade")
    elif entry_valor.get() == "":
        messagebox.showerror("Erro", "Prencher o campo Valor")
    elif combobox_tipo.get() == "":
        messagebox.showerror("Erro", "Prencher o campo Tipo Unidade")

    else:
        conexao = sqlite3.connect("produtos.db")
        c = conexao.cursor()
        c.execute(
            "INSERT INTO produtos VALUES (NULL, :descricao, :quantidade, :valor, :tipo)",
            {
                "descricao": entry_descricao.get(),
                "quantidade": entry_quantidade.get(),
                "valor": entry_valor.get(),
                "tipo": combobox_tipo.get(),
            },
        )

        messagebox.showinfo("Cadastro de Produtos", "Cadastro realizado com sucesso!")

        entry_descricao.delete(0, "end")
        entry_quantidade.delete(0, "end")
        entry_valor.delete(0, "end")
        # combobox_tipo.delete(0, "end")

        conexao.commit()

        for widget in frameDireita.winfo_children():
            widget.destroy()

        mostrar()


# função exportar banco de dados para excel
def exporta_produtos():
    conexao = sqlite3.connect(
        "produtos.db",
    )

    c = conexao.cursor()
    c.execute("SELECT * FROM produtos")
    produtos_cadastrados = c.fetchall()
    produtos_cadastrados = pd.DataFrame(
        produtos_cadastrados,
        columns=["ID", "Descricao", "Quantidade", "Valor", "Tipo"],
    )
    produtos_cadastrados.to_excel("produtos.xlsx", index=False)

    conexao.commit()
    conexao.close()

    messagebox.showinfo("Exportar para Excel", "Importação realizada com sucesso!")


# Deletar produto
def deletar_produto(i):
    conexao = sqlite3.connect("produtos.db")
    with conexao:
        c = conexao.cursor()
        query = "DELETE FROM produtos WHERE ID=?"
        c.execute(query, i)


# funcao deletar
def deletar():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario["values"]
        valor = treev_lista[0]

        deletar_produto([valor])
        print(valor)

        messagebox.showinfo("Sucesso", "Os dados foram deletados com sucesso")

        for widget in frameDireita.winfo_children():
            widget.destroy()

        mostrar()

    except IndexError:
        messagebox.showerror("Erro", "Seleciona um dos dados na tabela")


# Mostrar produto mo GRID
def selecionar_produto():
    conexao = sqlite3.connect("produtos.db")
    lista_form = []
    with conexao:
        c = conexao.cursor()
        c.execute("SELECT * FROM produtos")
        rows = c.fetchall()
        for row in rows:
            lista_form.append(row)
    return lista_form


listas = selecionar_produto()


# Função mostrar produto mo GRID
# criando um Treeview com barras de rolagem
def mostrar():
    list_header = ["ID", "Descricao", "Valor", "Quantidade", "Tipo"]

    df_list = selecionar_produto()

    global tree

    tree = ttk.Treeview(
        frameDireita,
        selectmode="extended",
        columns=list_header,
        show="headings",
    )
    # scrollbar vertical
    vsb = customtkinter.CTkScrollbar(
        frameDireita,
        orientation="vertical",
        command=tree.yview,
    )

    # scrollbar horizontal
    # hsb = ttk.Scrollbar(frameDireita, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set)  # , xscrollcommand=hsb.set

    style = ttk.Style(janela)
    style.theme_use("default")
    style.configure(
        "Treeview",
        background="#2a2d2e",
        foreground="white",
        rowheight=22,
        fieldbackground="#343638",
        bordercolor="#343638",
        borderwidth=0,
        font=("Roboto", 10),
    )
    style.map("Treeview", background=[("selected", "#22559b")])

    style.configure(
        "Treeview.Heading",
        background="#565b5e",
        foreground="white",
        relief="flat",
        font=("Roboto", 12),
    )
    style.map("Treeview.Heading", background=[("active", "#3484F0")])

    tree.grid(column=0, row=0, sticky="nsew")
    vsb.grid(column=1, row=0, sticky="ns")
    # hsb.grid(column=0, row=1, sticky="ew")
    frameDireita.grid_rowconfigure(0, weight=10)

    hd = ["nw", "nw", "nw", "nw", "nw", "center", "center"]
    h = [50, 300, 100, 100, 120, 50, 0]
    n = 0

    for col in list_header:
        # ajustando a largura das colunas e a posição do texto do cabeçalho
        tree.heading(col, text=col.title(), anchor=CENTER)
        tree.column(col, width=h[n], anchor=CENTER)
        n += 1

    for item in df_list:
        tree.insert("", "end", values=item)


mostrar()


# ///////////////////////////////////////////////////////////////////

label_descricao = customtkinter.CTkLabel(
    frameBaixo,
    text="Descrição:",
    width=50,
    font=("Roboto", 15),
)
label_descricao.grid(row=0, column=0, padx=0, pady=10)


label_quantidade = customtkinter.CTkLabel(
    frameBaixo,
    text="Quantidade:",
    font=("Roboto", 15),
)
label_quantidade.grid(row=1, column=0, padx=10, pady=10)


label_valor = customtkinter.CTkLabel(
    frameBaixo,
    text="Valor:",
    font=("Roboto", 15),
)
label_valor.grid(row=2, column=0, padx=10, pady=10)


label_tipo = customtkinter.CTkLabel(
    frameBaixo,
    text="Tipo:",
    font=("Roboto", 15),
)
label_tipo.grid(row=3, column=0, padx=10, pady=10)


entry_descricao = customtkinter.CTkEntry(
    frameBaixo,
    width=300,
    font=("Roboto", 15),
)
entry_descricao.grid(row=0, column=1, padx=10, pady=10)


entry_quantidade = customtkinter.CTkEntry(
    frameBaixo,
    width=300,
    font=("Roboto", 15),
)
entry_quantidade.grid(row=1, column=1, padx=10, pady=10)


entry_valor = customtkinter.CTkEntry(
    frameBaixo,
    width=300,
    font=("Roboto", 15),
)
entry_valor.grid(row=2, column=1, padx=10, pady=10)


combobox_tipo = customtkinter.CTkComboBox(
    frameBaixo, values=lista_tipos, width=300, font=("Roboto", 15)
)
combobox_tipo.grid(row=3, column=1, padx=10, pady=10)


botao_cadastrar = customtkinter.CTkButton(
    frameBaixo,
    text="Cadastrar Produto",
    command=cadastrar_produtos,
    width=200,
    font=("bold", 15),
)
botao_cadastrar.grid(row=4, column=0, columnspan=2, padx=10, pady=0, ipadx=80)


botao_exportar = customtkinter.CTkButton(
    frameBaixo,
    text="Exportar para Excel",
    command=exporta_produtos,
    width=200,
    font=("bold", 15),
)
botao_exportar.grid(row=5, column=0, columnspan=2, padx=10, pady=10, ipadx=80)


botao_deletar = customtkinter.CTkButton(
    frameBaixo,
    command=deletar,
    text="Deletar",
    width=100,
    fg_color="#bf521b",
    hover_color="#752a05",
    font=("bold", 15),
    # fg_color="transparent",
)
botao_deletar.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=80)

janela.mainloop()
