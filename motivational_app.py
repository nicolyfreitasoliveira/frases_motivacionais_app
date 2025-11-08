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

def show_history():
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, text FROM quotes ORDER BY id DESC")
    quotes = cursor.fetchall()
    conn.close()

    history_window = tk.Toplevel(root)
    history_window.title("📜 Histórico de Frases")
    history_window.geometry("500x400")
    history_window.configure(bg="#f3e8ff" if not dark_mode else "#1b1b1b")

    title = tk.Label(history_window, text="📜 Suas Frases Motivacionais",
                     font=("Arial Rounded MT Bold", 16),
                     bg=history_window["bg"],
                     fg="#3b0764" if not dark_mode else "#e9d8fd")
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
                         selectbackground="#a855f7")
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
            "bg": "#121212",
            "text": "#fdfdfd",
            "button_bg": "#7c3aed",
            "button_hover": "#8b5cf6",
            "quote_bg": "#1e1e1e",
        }
        theme_button.config(text="☀️", bg=colors["bg"], fg="#e9d8fd", highlightbackground="#7c3aed")
    else:
        colors = {
            "bg": "#fdf6e3",
            "text": "#333",
            "button_bg": "#f59e0b",
            "button_hover": "#fbbf24",
            "quote_bg": "#fffdf6",
        }
        theme_button.config(text="🌙", bg=colors["bg"], fg="#3b0764", highlightbackground="#f59e0b")

    root.configure(bg=colors["bg"])
    title_label.config(bg=colors["bg"], fg=colors["text"])
    quote_label.config(bg=colors["quote_bg"], fg=colors["text"])
    footer.config(bg=colors["bg"], fg=colors["text"])
    button_frame.config(bg=colors["bg"])
    top_frame.config(bg=colors["bg"])

    for b in [add_button, edit_button, next_button, history_button]:
        b.config(bg=colors["button_bg"], fg="white", activebackground=colors["button_hover"], relief="flat")

def create_round_button(parent, text, command):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 12, "bold"),
        padx=15,
        pady=8,
        cursor="hand2",
        bd=0,
        relief="flat",
        bg="#f59e0b",
        fg="white",
        activebackground="#fbbf24",
        activeforeground="#000",
        highlightthickness=0
    )
    btn.configure(borderwidth=0)
    btn.pack(side="left", padx=10)
    btn.bind("<Enter>", lambda e: e.widget.config(bg="#fbbf24"))
    btn.bind("<Leave>", lambda e: apply_theme())
    return btn

# ------------------------------
# Janela Principal
# ------------------------------
create_db()
root = tk.Tk()
root.title("🌟 Frases Motivacionais do Dia 🌟")
root.geometry("640x480")
root.eval('tk::PlaceWindow . center')

dark_mode = False
current_quote_id, initial_text = get_random_quote()

# ------------------------------
# Layout
# ------------------------------
top_frame = tk.Frame(root, bg=root["bg"])
top_frame.pack(fill="x", pady=(10, 0))

theme_button = tk.Button(
    top_frame,
    text="🌙",
    command=toggle_theme,
    font=("Arial", 13, "bold"),
    padx=8,
    pady=5,
    cursor="hand2",
    bd=1,
    relief="groove",
    highlightthickness=1
)
theme_button.pack(side="right", padx=15)

title_label = tk.Label(root, text="💫 Inspire-se!", font=("Arial Rounded MT Bold", 24, "bold"))
title_label.pack(pady=20)

quote_label = tk.Label(
    root,
    text=initial_text,
    wraplength=520,
    justify="center",
    font=("Georgia", 16, "italic"),
    relief="groove",
    bd=3,
    padx=20,
    pady=20
)
quote_label.pack(pady=20)

button_frame = tk.Frame(root, bg=root["bg"])
button_frame.pack(pady=20)

add_button = create_round_button(button_frame, "➕ Adicionar", add_quote)
edit_button = create_round_button(button_frame, "✏️ Editar", edit_quote)
next_button = create_round_button(button_frame, "🔄 Nova", update_quote)
history_button = create_round_button(button_frame, "📜 Histórico", show_history)

footer = tk.Label(root, text="✨ Desenvolvido por Nicoly Freitas Oliveira ✨", font=("Arial", 10))
footer.pack(side="bottom", pady=10)

apply_theme()
root.mainloop()
