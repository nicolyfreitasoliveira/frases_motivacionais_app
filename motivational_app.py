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
    cursor.execute("SELECT id, text FROM quotes")
    quotes = cursor.fetchall()
    conn.close()
    if quotes:
        return random.choice(quotes)
    else:
        return (None, "✨ Adicione uma frase motivacional para começar!")

def add_quote():
    new_quote = simpledialog.askstring("Adicionar Frase", "Digite a nova frase motivacional:")
    if new_quote:
        conn = sqlite3.connect("quotes.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO quotes (text) VALUES (?)", (new_quote,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Frase adicionada com sucesso! 🌟")

def edit_quote():
    global current_quote_id
    if current_quote_id is None:
        messagebox.showwarning("Aviso", "Não há frase selecionada para editar.")
        return

    new_text = simpledialog.askstring("Editar Frase", "Edite a frase:", initialvalue=quote_label.cget("text"))
    if new_text:
        conn = sqlite3.connect("quotes.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE quotes SET text = ? WHERE id = ?", (new_text, current_quote_id))
        conn.commit()
        conn.close()
        quote_label.config(text=new_text)
        messagebox.showinfo("Sucesso", "Frase atualizada com sucesso! ✏️")

# 🆕 NOVO: Ver histórico completo
def show_history():
    """Abre uma nova janela mostrando todas as frases salvas no banco."""
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, text FROM quotes ORDER BY id DESC")
    quotes = cursor.fetchall()
    conn.close()

    history_window = tk.Toplevel(root)
    history_window.title("📜 Histórico de Frases")
    history_window.geometry("500x400")
    history_window.configure(bg="#f7f6f3" if not dark_mode else "#1e1e1e")

    title = tk.Label(history_window, text="📜 Suas Frases Motivacionais", 
                     font=("Arial Rounded MT Bold", 16),
                     bg=history_window["bg"], fg="#333" if not dark_mode else "#f1f1f1")
    title.pack(pady=10)

    if not quotes:
        msg = tk.Label(history_window, text="✨ Nenhuma frase adicionada ainda!",
                       bg=history_window["bg"], fg="#777", font=("Arial", 12))
        msg.pack(pady=20)
        return

    frame = tk.Frame(history_window, bg=history_window["bg"])
    frame.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(frame, font=("Georgia", 12), height=15, width=50, 
                         yscrollcommand=scrollbar.set,
                         bg="white" if not dark_mode else "#2b2b2b",
                         fg="#333" if not dark_mode else "#f1f1f1",
                         selectbackground="#ffcc66")
    for i, (id, text) in enumerate(quotes, 1):
        listbox.insert("end", f"{i}. {text}")
    listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    scrollbar.config(command=listbox.yview)

# ------------------------------
# Interface
# ------------------------------
def update_quote():
    global current_quote_id
    current_quote_id, text = get_random_quote()
    quote_label.config(text=text)

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def apply_theme():
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

    for b in [add_button, edit_button, next_button, theme_button, history_button]:
        b.config(bg=colors["button_bg"], fg=colors["text"], activebackground=colors["button_hover"])

def on_enter(e):
    e.widget.config(bg="#ffd27f")

def on_leave(e):
    apply_theme()

# ------------------------------
# Janela Principal
# ------------------------------
create_db()
root = tk.Tk()
root.title("💫 Frases Motivacionais do Dia 💫")
root.geometry("620x460")
root.eval('tk::PlaceWindow . center')

dark_mode = False
current_quote_id, initial_text = get_random_quote()

# ------------------------------
# Elementos da Tela
# ------------------------------
title_label = tk.Label(root, text="✨ Inspire-se!", font=("Arial Rounded MT Bold", 22, "bold"))
title_label.pack(pady=20)

quote_label = tk.Label(
    root,
    text=initial_text,
    wraplength=500,
    justify="center",
    font=("Georgia", 16, "italic"),
    relief="groove",
    bd=3,
    padx=20,
    pady=20
)
quote_label.pack(pady=20)

top_frame = tk.Frame(root, bg=root["bg"])
top_frame.pack(fill="x", pady=(10, 0))

theme_button = tk.Button(
    top_frame,
    text="🌙 Tema Escuro",
    command=toggle_theme,
    font=("Arial", 11, "bold"),
    padx=10,
    pady=5,
    cursor="hand2"
)
theme_button.pack(side="right", padx=15)

# 🆕 Frame principal para os botões centrais
button_frame = tk.Frame(root, bg=root["bg"])
button_frame.pack(pady=20)

add_button = tk.Button(button_frame, text="➕ Adicionar", command=add_quote, font=("Arial", 12, "bold"), padx=15, pady=8, cursor="hand2")
edit_button = tk.Button(button_frame, text="✏️ Editar", command=edit_quote, font=("Arial", 12, "bold"), padx=15, pady=8, cursor="hand2")
next_button = tk.Button(button_frame, text="🔄 Nova", command=update_quote, font=("Arial", 12, "bold"), padx=15, pady=8, cursor="hand2")
history_button = tk.Button(button_frame, text="📜 Histórico", command=show_history, font=("Arial", 12, "bold"), padx=15, pady=8, cursor="hand2")

add_button.pack(side="left", padx=8)
edit_button.pack(side="left", padx=8)
next_button.pack(side="left", padx=8)
history_button.pack(side="left", padx=8)

footer = tk.Label(root, text="✨ Desenvolvido por Nicoly Freitas Oliveira ✨", font=("Arial", 10))
footer.pack(side="bottom", pady=10)

apply_theme()
root.mainloop()
