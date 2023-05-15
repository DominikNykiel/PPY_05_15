import tkinter as tk
from tkinter import ttk
import sqlite3

root = tk.Tk()
root.title("Book Store")


def fetch_data():
    conn = sqlite3.connect('bookstore.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  author TEXT,
                  price REAL,
                  category TEXT)''')
    c.execute("SELECT * FROM books")
    result = c.fetchall()
    c.close()
    conn.close()
    return result


treeview = ttk.Treeview(root)
treeview["columns"] = ("id", "title", "author", "price", "category")
treeview.column("#0", width=0)
treeview.heading("id", text="ID")
treeview.heading("title", text="Tytuł")
treeview.heading("author", text="Autor")
treeview.heading("price", text="Cena")
treeview.heading("category", text="Kategoria")
treeview.pack()


def load_data():
    data = fetch_data()
    treeview.delete(*treeview.get_children())
    for row in data:
        treeview.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))


def open_new_book_window():
    new_window = tk.Toplevel(root)
    new_window.title("Dodaj nową książkę")
    title_label = ttk.Label(new_window, text="Tytuł:")
    title_label.pack()
    title_entry = ttk.Entry(new_window)
    title_entry.pack()
    author_label = ttk.Label(new_window, text="Autor:")
    author_label.pack()
    author_entry = ttk.Entry(new_window)
    author_entry.pack()
    price_label = ttk.Label(new_window, text="Cena:")
    price_label.pack()
    price_entry = ttk.Entry(new_window)
    price_entry.pack()
    category_label = ttk.Label(new_window, text="Kategoria:")
    category_label.pack()
    category_entry = ttk.Entry(new_window)
    category_entry.pack()

    def add_new():
        # Pobranie wartości z widgetów
        new_title = title_entry.get()
        new_author = author_entry.get()
        new_price = price_entry.get()
        new_category = category_entry.get()
        conn = sqlite3.connect('bookstore.db')
        c = conn.cursor()
        sql = "INSERT INTO books (title, author, price, category) VALUES (?, ?, ?, ?)"
        params = (new_title, new_author, new_price, new_category)
        c.execute(sql, params)
        conn.commit()
        c.close()
        conn.close()
        load_data()
        new_window.destroy()

    add_button = ttk.Button(new_window, text="Dodaj", command=add_new)
    add_button.pack()


add_new_book_button = tk.Button(root, text="Dodaj nową książkę", command=open_new_book_window)
add_new_book_button.pack(side="left")




load_data()
root.mainloop()
print(fetch_data())
