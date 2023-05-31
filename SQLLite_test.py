import tkinter as tk
from tkinter import ttk
import sqlite3

root = tk.Tk()
root.title("Book Store")


def fetch_data():
    try:
        conn = sqlite3.connect('studentdb')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS student
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT,
                    studentname TEXT,
                    studentsurname TEXT,
                        project_points REAL,
                        l1_points REAL,
                        l2_points REAL,
                        l3_points REAL,
                        finalgrade REAL
                    )''')
        cursor.execute("SELECT * FROM student")
        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


treeview = ttk.Treeview(root)
treeview["columns"] = (
    "id", "email", "studentname", "studentsurname", "project_points", "l1_points", "l2_points", "l3_points",
    "finalgrade")
treeview.column("#0", width=0)
treeview.heading("id", text="ID")
treeview.heading("studentname", text="Imie")
treeview.heading("studentsurname", text="Nazwisko")
treeview.heading("project_points", text="Punkty z projektu")
treeview.heading("l1_points", text="Punkty z listy 1")
treeview.heading("l2_points", text="Punkty z listy 2")
treeview.heading("l3_points", text="Punkty z listy 3")
treeview.heading("finalgrade", text="Finalowa ocena")
treeview.pack()


def load_data():
    data = fetch_data()
    treeview.delete(*treeview.get_children())
    for row in data:
        treeview.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))


def open_new_student_window():
    new_window = tk.Toplevel(root)
    new_window.title("Dodaj nowego studenta")
    email_label = ttk.Label(new_window, text="Email")
    email_label.pack()
    email_entry = ttk.Entry(new_window)
    email_entry.pack()
    name_label = ttk.Label(new_window, text="Imie")
    name_label.pack()
    name_entry = ttk.Entry(new_window)
    name_entry.pack()
    surname_label = ttk.Label(new_window, text="Nazwisko")
    surname_label.pack()
    surname_entry = ttk.Entry(new_window)
    surname_entry.pack()
    project_label = ttk.Label(new_window, text="Punkty z projektu")
    project_label.pack()
    project_entry = ttk.Entry(new_window)
    project_entry.pack()
    l1_label = ttk.Label(new_window, text="Punkty z listy 1")
    l1_label.pack()
    l1_entry = ttk.Entry(new_window)
    l1_entry.pack()
    l2_label = ttk.Label(new_window, text="Punkty z listy 2")
    l2_label.pack()
    l2_entry = ttk.Entry(new_window)
    l2_entry.pack()
    l3_label = ttk.Label(new_window, text="Punkty z listy 3")
    l3_label.pack()
    l3_entry = ttk.Entry(new_window)
    l3_entry.pack()
    grade_label = ttk.Label(new_window, text="Finałowa ocena")
    grade_label.pack()
    grade_entry = ttk.Entry(new_window)
    grade_entry.pack()

    def add_new():
        # Pobranie wartości z widgetów
        new_email = email_entry.get()
        new_name = name_entry.get()
        new_surname = surname_entry.get()
        new_project = project_entry.get()
        new_l1 = l1_entry.get()
        new_l2 = l2_entry.get()
        new_l3 = l3_entry.get()
        new_grade = grade_entry.get()
        try:
            conn = sqlite3.connect('studentdb')
            cursor = conn.cursor()
            sql = "INSERT INTO student (email ,studentname ,studentsurname ,project_points ,l1_points ,l2_points ,l3_points ,finalgrade) VALUES (?,?,?,?,?,?,?,?)"
            params = (new_email, new_name, new_surname, new_project, new_l1, new_l2, new_l3, new_grade)
            cursor.execute(sql, params)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        load_data()
        new_window.destroy()

    add_button = ttk.Button(new_window, text="Dodaj", command=add_new)
    add_button.pack()


add_new_book_button = tk.Button(root, text="Dodaj nowego studenta", command=open_new_student_window)
add_new_book_button.pack(side="left")


def open_details_window(event):
    def deleteStudent():
        # Usuwanie:
        student_id = (id_entry.get())
        try:
            conn = sqlite3.connect('studentdb')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM student WHERE id=?", (student_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        load_data()
        details_window.destroy()

    def update_student():
        new_email = email_entry.get()
        new_name = name_entry.get()
        new_surname = surname_entry.get()
        new_project = project_entry.get()
        new_l1 = l1_entry.get()
        new_l2 = l2_entry.get()
        new_l3 = l3_entry.get()
        new_grade = grade_entry.get()
        same_id = int(id_entry.get())
        try:
            conn = sqlite3.connect('studentdb')
            mycursor = conn.cursor()

            mycursor.execute("UPDATE student SET email=?, studentname=?, studentsurname=?, project_points=?,l1_points=? ,"
                         "l2_points=? ,l3_points=? ,finalgrade=? WHERE id=?",
                         (new_email, new_name, new_surname, new_project, new_l1, new_l2, new_l3, new_grade, same_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
        finally:
            if mycursor:
                mycursor.close()
            if conn:
                conn.close()
        load_data()

    # Pobranie zaznaczonego elementu
    selected_item = treeview.focus()
    if selected_item:
        # Pobranie danych z zaznaczonego elementu
        item_data = treeview.item(selected_item)
        item_values = item_data["values"]
    # Tworzenie nowego okna
    details_window = tk.Toplevel(root)
    details_window.title("Szczegóły")
    # Tworzenie i wyświetlanie widgetów opartych na danych z zaznaczonego elementu
    id_label = ttk.Label(details_window, text="ID:")
    id_label.pack()
    id_entry = ttk.Entry(details_window)
    id_entry.insert(0, item_values[0])
    id_entry.config(state="disabled")  # Uniemożliwienie zmiany id
    id_entry.pack()

    email_label = ttk.Label(details_window, text="Email:")
    email_label.pack()
    email_entry = ttk.Entry(details_window)
    email_entry.insert(0, item_values[1])
    email_entry.pack()

    name_label = ttk.Label(details_window, text="Imie:")
    name_label.pack()
    name_entry = ttk.Entry(details_window)
    name_entry.insert(0, item_values[2])
    name_entry.pack()

    surname_label = ttk.Label(details_window, text="Nazwisko")
    surname_label.pack()
    surname_entry = ttk.Entry(details_window)
    surname_entry.insert(0, item_values[3])
    surname_entry.pack()

    project_label = ttk.Label(details_window, text="Punkty z projektu")
    project_label.pack()
    project_entry = ttk.Entry(details_window)
    project_entry.insert(0, item_values[4])
    project_entry.pack()

    l1_label = ttk.Label(details_window, text="Punkty z listy 1")
    l1_label.pack()
    l1_entry = ttk.Entry(details_window)
    l1_entry.insert(0, item_values[5])
    l1_entry.pack()

    l2_label = ttk.Label(details_window, text="Punky z listy 2")
    l2_label.pack()
    l2_entry = ttk.Entry(details_window)
    l2_entry.insert(0, item_values[6])
    l2_entry.pack()

    l3_label = ttk.Label(details_window, text="Punky z listy 3")
    l3_label.pack()
    l3_entry = ttk.Entry(details_window)
    l3_entry.insert(0, item_values[7])
    l3_entry.pack()

    grade_label = ttk.Label(details_window, text="Ocena")
    grade_label.pack()
    grade_entry = ttk.Entry(details_window)
    grade_entry.insert(0, item_values[8])
    grade_entry.pack()

    delete_button = tk.Button(details_window, text="Usun studenta", command=deleteStudent)
    delete_button.pack()

    update_button = ttk.Button(details_window, text="Zaktualizuj studenta", command=update_student)
    update_button.pack()


treeview.bind("<Double-1>", open_details_window)

load_data()
root.mainloop()
