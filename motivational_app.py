import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import random

# ------------------------------
# Banco de Dados
# ------------------------------
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

# ------------------------------
# Interface
# ------------------------------
def update_quote():
    quote_label.config(text=get_random_quote())

def toggle_theme():
    """Alterna entre tema claro e escuro."""
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def apply_theme():
    """Aplica as cores de acordo com o modo atual."""
    if dark_mode:
        colors = {
            "bg": "#1e1e1e",
            "text": "#f1f1f1",
            "button_bg": "#3a3a3a",
            "button_hover": "#555",
            "quote_bg": "#2b2b2b",
        }
        theme_button.config(text="☀️ Tema Claro")
    else:
        colors = {
            "bg": "#f7f6f3",
            "text": "#333",
            "button_bg": "#ffcc66",
            "button_hover": "#ffd27f",
            "quote_bg": "white",
        }
        theme_button.config(text="🌙 Tema Escuro")

    root.configure(bg=colors["bg"])
    title_label.config(bg=colors["bg"], fg=colors["text"])
    quote_label.config(bg=colors["quote_bg"], fg=colors["text"])
    footer.config(bg=colors["bg"], fg=colors["text"])
    button_frame.config(bg=colors["bg"])

    for b in [add_button, next_button, theme_button]:
        b.config(bg=colors["button_bg"], fg=colors["text"], activebackground=colors["button_hover"])

def on_enter(e):
    e.widget.config(bg="#ffd27f")

def on_leave(e):
    apply_theme()  # volta à cor correta conforme o modo

# ------------------------------
# Janela Principal
# ------------------------------
create_db()
root = tk.Tk()
root.title("💫 Frases Motivacionais do Dia 💫")
root.geometry("600x420")
root.eval('tk::PlaceWindow . center')

dark_mode = False  # tema começa claro

# ------------------------------
# Elementos da Tela
# ------------------------------
title_label = tk.Label(root, text="✨ Inspire-se!", font=("Arial Rounded MT Bold", 22, "bold"))
title_label.pack(pady=20)

quote_label = tk.Label(
    root,
    text=get_random_quote(),
    wraplength=500,
    justify="center",
    font=("Georgia", 16, "italic"),
    relief="groove",
    bd=3,
    padx=20,
    pady=20
)
quote_label.pack(pady=20)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="➕ Adicionar Frase", command=add_quote, font=("Arial", 12, "bold"), padx=20, pady=8, cursor="hand2")
next_button = tk.Button(button_frame, text="🔄 Nova Frase", command=update_quote, font=("Arial", 12, "bold"), padx=20, pady=8, cursor="hand2")
theme_button = tk.Button(button_frame, text="🌙 Tema Escuro", command=toggle_theme, font=("Arial", 12, "bold"), padx=20, pady=8, cursor="hand2")

add_button.pack(side="left", padx=8)
next_button.pack(side="left", padx=8)
theme_button.pack(side="left", padx=8)

footer = tk.Label(root, text="✨ Desenvolvido por Nicoly Freitas Oliveira ✨", font=("Arial", 10))
footer.pack(side="bottom", pady=10)

# Aplica o tema inicial
apply_theme()

root.mainloop()