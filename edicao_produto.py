# edicao_produto.py

import sqlite3
from tkinter import messagebox


# Função para conectar ao banco de dados
def conectar_bd():
    return sqlite3.connect("produtos.db")


# Função para preencher os campos com os dados do produto selecionado para edição
def preencher_campos_para_edicao(
    tree,
    entry_descricao,
    entry_quantidade,
    entry_valor,
    combobox_tipo,
    btn_salvar_edicao,
):
    try:
        item_selecionado = tree.selection()[0]  # Pega o item selecionado no Treeview
        produto = selecionar_produto_por_id(item_selecionado)  # Busca o produto pelo ID

        # Preenche os campos de entrada com os valores do produto selecionado
        entry_descricao.delete(0, "end")
        entry_descricao.insert("end", produto[1])
        entry_quantidade.delete(0, "end")
        entry_quantidade.insert("end", produto[2])
        entry_valor.delete(0, "end")
        entry_valor.insert("end", produto[3])
        combobox_tipo.set(produto[4])

        # Habilita o botão de salvar edição
        btn_salvar_edicao.configure(state="normal")

    except IndexError:
        messagebox.showerror("Erro", "Selecione um produto para editar")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado ao preencher campos: {e}")


# Função para buscar um produto específico por ID
def selecionar_produto_por_id(produto_id):
    conexao = conectar_bd()
    with conexao:
        c = conexao.cursor()
        c.execute("SELECT * FROM produtos WHERE ID = ?", (produto_id,))
        produto = c.fetchone()
    conexao.close()
    return produto


# Função para salvar as alterações feitas no produto
def salvar_edicao(
    tree,
    entry_descricao,
    entry_quantidade,
    entry_valor,
    combobox_tipo,
    btn_salvar_edicao,
    validar_campos,
    mostrar_produtos,
):
    try:
        item_selecionado = tree.selection()[0]  # Pega o item selecionado no Treeview
        produto_id = item_selecionado  # O ID do produto está no Treeview como iid

        # Verifica se os campos estão válidos antes de prosseguir
        if not validar_campos():
            return  # Interrompe a execução se a validação falhar

        # Atualizar o produto no banco de dados
        conexao = conectar_bd()
        with conexao:
            c = conexao.cursor()
            c.execute(
                """
                UPDATE produtos
                SET descricao = ?, quantidade = ?, valor = ?, tipo = ?
                WHERE ID = ?
                """,
                (
                    entry_descricao.get(),
                    entry_quantidade.get(),
                    entry_valor.get(),
                    combobox_tipo.get(),
                    produto_id,
                ),
            )
        conexao.close()

        # Exibir mensagem de sucesso
        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")

        # Limpar os campos de entrada
        entry_descricao.delete(0, "end")
        entry_quantidade.delete(0, "end")
        entry_valor.delete(0, "end")
        combobox_tipo.set("")

        # Desabilitar o botão de salvar edição até que outro item seja selecionado
        btn_salvar_edicao.configure(state="disabled")

        # Atualizar o Treeview
        mostrar_produtos()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar edição: {e}")
