import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import random

# Funções do Banco de Dados

def create_db():
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_random_quote():
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT text FROM quotes")
    quotes = cursor.fetchall()
    conn.close()
    if quotes:
        return random.choice(quotes)[0]
    else:
        return "✨ Adicione uma frase motivacional para começar!"

def add_quote():
    new_quote = simpledialog.askstring("Adicionar Frase", "Digite a nova frase motivacional:")
    if new_quote:
        conn = sqlite3.connect("quotes.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO quotes (text) VALUES (?)", (new_quote,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Frase adicionada com sucesso! 🌟")

# Funções da Interface
def update_quote():
    quote_label.config(text=get_random_quote())

# Configuração da Janela Principal

create_db()
root = tk.Tk()
root.title(" Frases Motivacionais do Dia ")
root.geometry("600x400")
root.configure(bg="#f7f6f3")

# Centralizar na tela
root.eval('tk::PlaceWindow . center')

# Estilo e Layout

title_label = tk.Label(
    root,
    text="💫 Inspire-se!",
    font=("Arial Rounded MT Bold", 22, "bold"),
    bg="#f7f6f3",
    fg="#333"
)
title_label.pack(pady=20)

quote_label = tk.Label(
    root,
    text=get_random_quote(),
    wraplength=500,
    justify="center",
    font=("Georgia", 16, "italic"),
    bg="white",
    fg="#555",
    relief="groove",
    bd=3,
    padx=20,
    pady=20
)
quote_label.pack(pady=20)

# Botões

button_frame = tk.Frame(root, bg="#f7f6f3")
button_frame.pack(pady=10)

def on_enter(e):  # Efeito hover
    e.widget.config(bg="#ffd27f")

def on_leave(e):
    e.widget.config(bg="#ffcc66")

add_button = tk.Button(
    button_frame,
    text="➕ Adicionar Frase",
    command=add_quote,
    bg="#ffcc66",
    fg="#333",
    font=("Arial", 12, "bold"),
    relief="raised",
    padx=20,
    pady=8,
    borderwidth=3,
    cursor="hand2"
)
add_button.bind("<Enter>", on_enter)
add_button.bind("<Leave>", on_leave)
add_button.pack(side="left", padx=10)

next_button = tk.Button(
    button_frame,
    text="🔄 Nova Frase",
    command=update_quote,
    bg="#b0e0a8",
    fg="#333",
    font=("Arial", 12, "bold"),
    relief="raised",
    padx=20,
    pady=8,
    borderwidth=3,
    cursor="hand2"
)
next_button.pack(side="left", padx=10)

# Rodapé
footer = tk.Label(
    root,
    text="✨ Desenvolvido por Nicoly Oliveira ✨",
    bg="#f7f6f3",
    fg="#777",
    font=("Arial", 10)
)
footer.pack(side="bottom", pady=10)

# Iniciar o App

root.mainloop()
