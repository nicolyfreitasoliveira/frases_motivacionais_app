#!/usr/bin/env python3
"""
App de Frases Motivacionais (Tkinter + SQLite)
Arquivo: motivational_app.py
Como usar: python3 motivational_app.py
Dependências: apenas bibliotecas padrão do Python (tkinter, sqlite3)
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import sqlite3
import os
from datetime import date
import random

DB_FILE = "quotes.db"
SAMPLE_QUOTES = [
    ("O único lugar onde o sucesso vem antes do trabalho é no dicionário.", "Vidal Sassoon"),
    ("Acredite que você pode — assim você já está no meio do caminho.", "Theodore Roosevelt"),
    ("Pequenos progressos diários resultam em grandes conquistas.", "Desconhecido"),
    ("Você é mais forte do que pensa e será mais feliz do que imagina.", "Desconhecido"),
    ("A jornada de mil milhas começa com um único passo.", "Lao-Tsé"),
]



def init_db(db_path=DB_FILE):
    create = not os.path.exists(db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            author TEXT,
            created_at TEXT DEFAULT (DATE('now'))
        )
        """
    )
    conn.commit()

    # Seed with sample quotes if empty
    cur.execute("SELECT COUNT(*) FROM quotes")
    count = cur.fetchone()[0]
    if count == 0:
        cur.executemany("INSERT INTO quotes (text, author) VALUES (?, ?)", SAMPLE_QUOTES)
        conn.commit()
    return conn


def get_all_quotes(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, text, author FROM quotes ORDER BY id")
    return cur.fetchall()


def add_quote(conn, text, author):
    cur = conn.cursor()
    cur.execute("INSERT INTO quotes (text, author) VALUES (?, ?)", (text.strip(), author.strip()))
    conn.commit()
    return cur.lastrowid


def update_quote(conn, qid, text, author):
    cur = conn.cursor()
    cur.execute("UPDATE quotes SET text = ?, author = ? WHERE id = ?", (text.strip(), author.strip(), qid))
    conn.commit()


def delete_quote(conn, qid):
    cur = conn.cursor()
    cur.execute("DELETE FROM quotes WHERE id = ?", (qid,))
    conn.commit()


def search_quotes(conn, term):
    cur = conn.cursor()
    like = f"%{term}%"
    cur.execute("SELECT id, text, author FROM quotes WHERE text LIKE ? OR author LIKE ? ORDER BY id", (like, like))
    return cur.fetchall()



class QuotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Frases Motivacionais do Dia")
        self.conn = init_db()

        # Top frame: quote of the day
        top = tk.Frame(root, padx=10, pady=10)
        top.pack(fill=tk.X)

        self.qod_var = tk.StringVar()
        self.qod_author_var = tk.StringVar()

        lbl_title = tk.Label(top, text="Frase do Dia", font=(None, 16, "bold"))
        lbl_title.pack(anchor=tk.W)

        self.lbl_quote = tk.Label(top, textvariable=self.qod_var, wraplength=600, justify=tk.LEFT, font=(None, 12))
        self.lbl_quote.pack(anchor=tk.W, pady=(6,0))

        self.lbl_author = tk.Label(top, textvariable=self.qod_author_var, font=(None, 10, "italic"))
        self.lbl_author.pack(anchor=tk.W, pady=(2,6))

        btn_frame = tk.Frame(top)
        btn_frame.pack(anchor=tk.W, pady=(0,8))

        tk.Button(btn_frame, text="Nova frase aleatória", command=self.show_random).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Atualizar Frase do Dia", command=self.show_qod).pack(side=tk.LEFT, padx=(6,0))

        mid = tk.Frame(root, padx=10, pady=6)
        mid.pack(fill=tk.X)

        tk.Label(mid, text="Pesquisar:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(mid)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6,6))
        tk.Button(mid, text="Buscar", command=self.do_search).pack(side=tk.LEFT)
        tk.Button(mid, text="Mostrar tudo", command=self.reload_list).pack(side=tk.LEFT, padx=(6,0))

        #botoes

        bottom = tk.Frame(root, padx=10, pady=6)
        bottom.pack(fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(bottom, activestyle='none')
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind('<Double-1>', self.on_edit)

        scrollbar = tk.Scrollbar(bottom, orient=tk.VERTICAL)
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        action_frame = tk.Frame(bottom)
        action_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(8,0))

        tk.Button(action_frame, text="Adicionar", width=15, command=self.on_add).pack(pady=(0,6))
        tk.Button(action_frame, text="Editar", width=15, command=self.on_edit).pack(pady=(0,6))
        tk.Button(action_frame, text="Excluir", width=15, command=self.on_delete).pack(pady=(0,6))
        tk.Button(action_frame, text="Exportar CSV", width=15, command=self.export_csv).pack(pady=(10,6))
        tk.Button(action_frame, text="Importar CSV", width=15, command=self.import_csv).pack(pady=(0,6))

        self.reload_list()
        self.show_qod()

    def show_qod(self):
        quotes = get_all_quotes(self.conn)
        if not quotes:
            self.qod_var.set("Ainda não há frases no banco de dados.")
            self.qod_author_var.set("")
            return

        today = date.today().isoformat()  # YYYY-MM-DD
        idx = hash(today) % len(quotes)
        q = quotes[idx]
        self.qod_var.set(q[1])
        self.qod_author_var.set(f"— {q[2] if q[2] else 'Desconhecido'}")

    def show_random(self):
        quotes = get_all_quotes(self.conn)
        if not quotes:
            messagebox.showinfo("Vazio", "Não há frases no banco de dados.")
            return
        q = random.choice(quotes)
        self.qod_var.set(q[1])
        self.qod_author_var.set(f"— {q[2] if q[2] else 'Desconhecido'}")


    def reload_list(self):
        self.listbox.delete(0, tk.END)
        self.quotes_cache = get_all_quotes(self.conn)
        for q in self.quotes_cache:
            display = f"{q[0]} — {truncate(q[1], 60)} {('— ' + q[2]) if q[2] else ''}"
            self.listbox.insert(tk.END, display)

    def do_search(self):
        term = self.search_entry.get().strip()
        if term == "":
            self.reload_list()
            return
        results = search_quotes(self.conn, term)
        self.listbox.delete(0, tk.END)
        for q in results:
            display = f"{q[0]} — {truncate(q[1], 60)} {('— ' + q[2]) if q[2] else ''}"
            self.listbox.insert(tk.END, display)
        self.quotes_cache = results

    def get_selected_id(self):
        sel = self.listbox.curselection()
        if not sel:
            return None
        idx = sel[0]
        if idx >= len(self.quotes_cache):
            return None
        return self.quotes_cache[idx][0]


    def on_add(self):
        dlg = QuoteDialog(self.root, "Adicionar Frase")
        if dlg.ok:
            text, author = dlg.text, dlg.author
            if not text.strip():
                messagebox.showwarning("Inválido", "A frase não pode ser vazia.")
                return
            add_quote(self.conn, text, author)
            self.reload_list()
            messagebox.showinfo("OK", "Frase adicionada com sucesso.")

    def on_edit(self, event=None):
        qid = self.get_selected_id()
        if qid is None:
            messagebox.showwarning("Seleção", "Selecione uma frase para editar (duplo-clique também funciona).")
            return

        cur = self.conn.cursor()
        cur.execute("SELECT text, author FROM quotes WHERE id = ?", (qid,))
        row = cur.fetchone()
        if not row:
            messagebox.showerror("Erro", "Frase não encontrada no banco de dados.")
            self.reload_list()
            return
        dlg = QuoteDialog(self.root, "Editar Frase", text=row[0], author=row[1])
        if dlg.ok:
            update_quote(self.conn, qid, dlg.text, dlg.author)
            self.reload_list()
            messagebox.showinfo("OK", "Frase atualizada.")

    def on_delete(self):
        qid = self.get_selected_id()
        if qid is None:
            messagebox.showwarning("Seleção", "Selecione uma frase para excluir.")
            return
        if not messagebox.askyesno("Confirmação", "Deseja realmente excluir esta frase?"):
            return
        delete_quote(self.conn, qid)
        self.reload_list()
        messagebox.showinfo("OK", "Frase excluída.")

    #importar arquivos
    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV', '*.csv')])
        if not path:
            return
        cur = self.conn.cursor()
        cur.execute("SELECT text, author, created_at FROM quotes ORDER BY id")
        rows = cur.fetchall()
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write('text,author,created_at\n')
                for r in rows:
                    text = r[0].replace('"', '""')
                    author = (r[1] or '').replace('"', '""')
                    f.write(f'"{text}","{author}","{r[2]}"\n')
            messagebox.showinfo("Exportado", f"Exportado {len(rows)} frases para {path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar: {e}")

    def import_csv(self):
        path = filedialog.askopenfilename(filetypes=[('CSV', '*.csv')])
        if not path:
            return
        try:
            count = 0
            with open(path, 'r', encoding='utf-8') as f:
                header = f.readline()
                for line in f:
                    # naive CSV parse: assume line is "text","author",... 
                    parts = parse_csv_line(line)
                    if not parts:
                        continue
                    text = parts[0]
                    author = parts[1] if len(parts) > 1 else ''
                    add_quote(self.conn, text, author)
                    count += 1
            self.reload_list()
            messagebox.showinfo("Importado", f"Importadas {count} frases de {path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao importar: {e}")


def truncate(s, n):
    return (s[:n-3] + '...') if len(s) > n else s


def parse_csv_line(line):
    parts = []
    cur = ''
    in_quotes = False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '"':
            if in_quotes and i + 1 < len(line) and line[i+1] == '"':
                cur += '"'
                i += 2
                continue
            in_quotes = not in_quotes
            i += 1
            continue
        if ch == ',' and not in_quotes:
            parts.append(cur)
            cur = ''
            i += 1
            continue
        if ch in "\r\n" and not in_quotes:
            break
        cur += ch
        i += 1
    if cur != '':
        parts.append(cur)
    return parts


class QuoteDialog(simpledialog.Dialog):
    def __init__(self, parent, title, text='', author=''):
        self._init_text = text
        self._init_author = author
        self.text = ''
        self.author = ''
        self.ok = False
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Frase:").grid(row=0, column=0, sticky=tk.W)
        self.txt = tk.Text(master, width=60, height=6)
        self.txt.grid(row=1, column=0, columnspan=2)
        self.txt.insert('1.0', self._init_text)

        tk.Label(master, text="Autor:").grid(row=2, column=0, sticky=tk.W, pady=(6,0))
        self.author_entry = tk.Entry(master, width=40)
        self.author_entry.grid(row=3, column=0, sticky=tk.W)
        self.author_entry.insert(0, self._init_author or '')
        return self.txt

    def apply(self):
        self.text = self.txt.get('1.0', tk.END).strip()
        self.author = self.author_entry.get().strip()
        self.ok = True

    #main
if __name__ == '__main__':
    root = tk.Tk()
    app = QuotesApp(root)
    root.geometry('800x500')
    root.mainloop()
