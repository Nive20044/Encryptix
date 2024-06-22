from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

# Database operations
def create_connection():
    return sql.connect('listOfTasks.db')

def create_table(conn):
    with conn:
        conn.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT)')

def insert_task(conn, task):
    with conn:
        conn.execute('INSERT INTO tasks VALUES (?)', (task,))

def delete_task_from_db(conn, task):
    with conn:
        conn.execute('DELETE FROM tasks WHERE title = ?', (task,))

def delete_all_tasks_from_db(conn):
    with conn:
        conn.execute('DELETE FROM tasks')

def retrieve_tasks(conn):
    with conn:
        return conn.execute('SELECT title FROM tasks').fetchall()

# Task operations
def add_task():
    task_string = task_field.get()
    if not task_string:
        messagebox.showinfo('Error', 'Field is Empty.')
    else:
        insert_task(the_connection, task_string)
        list_update()
        task_field.delete(0, 'end')

def list_update():
    task_listbox.delete(0, 'end')
    tasks = retrieve_tasks(the_connection)
    for task in tasks:
        task_listbox.insert('end', task[0])

def delete_task():
    try:
        selected_task = task_listbox.get(task_listbox.curselection())
        delete_task_from_db(the_connection, selected_task)
        list_update()
    except:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

def delete_all_tasks():
    if messagebox.askyesno('Delete All', 'Are you sure?'):
        delete_all_tasks_from_db(the_connection)
        list_update()

def close():
    the_connection.commit()
    the_connection.close()
    guiWindow.destroy()

if __name__ == "__main__":
    guiWindow = Tk()
    guiWindow.title("To-Do List")
    guiWindow.geometry("665x400+550+250")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#B5E5CF")
    
    # Establish database connection
    the_connection = create_connection()
    create_table(the_connection)

    functions_frame = Frame(guiWindow, bg="#8EE5EE")
    functions_frame.pack(side="top", expand=True, fill="both")

    task_label = Label(functions_frame, text="TO-DO-LIST \n Enter the Task Title:",
        font=("arial", "14", "bold"), bg="#8EE5EE", foreground="#FF6103")
    task_label.place(x=20, y=30)

    task_field = Entry(functions_frame, font=("Arial", "14"), width=42,
        foreground="white", background="black")
    task_field.place(x=180, y=30)

    add_button = Button(functions_frame, text="Add", width=15, bg='#D4AC0D',
        font=("arial", "14", "bold"), command=add_task)
    del_button = Button(functions_frame, text="Remove", width=15, bg='#D4AC0D',
        font=("arial", "14", "bold"), command=delete_task)
    del_all_button = Button(functions_frame, text="Delete All", width=15,
        font=("arial", "14", "bold"), bg='#D4AC0D', command=delete_all_tasks)
    exit_button = Button(functions_frame, text="Exit / Close", width=52,
        bg='#D4AC0D', font=("arial", "14", "bold"), command=close)
    
    add_button.place(x=18, y=80)
    del_button.place(x=240, y=80)
    del_all_button.place(x=460, y=80)
    exit_button.place(x=17, y=330)

    task_listbox = Listbox(functions_frame, width=70, height=9, font="bold",
        selectmode='SINGLE', background="BLACK", foreground="WHITE",
        selectbackground="#FF8C00", selectforeground="WHITE")
    task_listbox.place(x=17, y=140)

    list_update()
    guiWindow.mainloop()
