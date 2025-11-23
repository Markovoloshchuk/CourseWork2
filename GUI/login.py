import sys
import os


from Utils import mongodb_connection
from Utils import mongodb_functions
from Utils import tkinter_general
from GUI import collection

import tkinter as tk
from tkinter import messagebox, filedialog, ttk


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

def open_login_window():
    def handle_login():
        entered_login = login_Entry.get()
        entered_password = password_Entry.get()
        
        if mongodb_functions.verify_password(entered_login, entered_password):
            messagebox.showinfo("Успіх", "Вхід успішний!")
            login_window.destroy()
            collection.open_collection_window()
        else:
            messagebox.showerror("Помилка", "Невірний логін або пароль.")

    def on_focus_out(event):
        password = password_Entry.get()
        if not password:
             return 

        if mongodb_functions.is_password_valid(password):
            hint_Label.config(fg="white") 
            enter_Button.config(state="normal", bg="#b366ff")
        else:
            hint_Label.config(fg="red")
            enter_Button.config(state="disabled", bg="grey")

    def on_focus_in(event):
        hint_Label.config(fg="white")
    
    login_window = tk.Tk()
    login_window.title("Login")
    tkinter_general.center_window(login_window, 500, 700)
    login_window.configure(bg="#e6ccff")
    login_window.resizable(False, False)

    title_Label = tk.Label(login_window, text="Login Screen", font=("Arial", 16), bg="#e6ccff", fg="purple").pack(pady=20)

    login_input_Frame = tk.Frame(login_window, width=400, height=600, bg="white")
    login_input_Frame.propagate(False)
    login_Label = tk.Label(login_input_Frame, text="Login", bg="white", font=("Arial", 12))
    login_Entry = tk.Entry(login_input_Frame, font=("Arial", 12))
    password_Label = tk.Label(login_input_Frame, text="Password", bg="white", font=("Arial", 12))

    password_Entry = tk.Entry(login_input_Frame, show="*", font=("Arial", 12))
    password_Entry.bind("<FocusOut>", on_focus_out)
    password_Entry.bind("<FocusIn>", on_focus_in)

    hint_Label = tk.Label(login_input_Frame, text="*password must contain at least 8 characters, one small and one capital letter, one digit", bg="white", font=("Arial", 8), fg="white", justify="left", wraplength=300)
    enter_Button = tk.Button(login_input_Frame, text="Enter", justify=tk.CENTER, width=20, font=("Arial", 14), bg="#b366ff", fg="white", activebackground="#cc80ff", activeforeground="white", command=handle_login)
    forgotPassword_Button = tk.Button(login_input_Frame, text="Forgot Password?", justify=tk.CENTER, width=20, font=("Arial", 10), bg="white", fg="#a6a6a6", borderwidth=0, highlightthickness=0, activebackground="white", activeforeground="#737373")

    login_input_Frame.pack()
    login_Label.pack(anchor='w', padx=20, pady=(20, 0))
    login_Entry.pack(padx=20, pady=(0, 20), fill=tk.X)
    password_Label.pack(anchor='w', padx=20, pady=(0, 0))
    password_Entry.pack(padx=20, pady=(0, 0), fill=tk.X)
    hint_Label.pack(anchor='w', padx=20, pady=(0, 20))
    enter_Button.pack()
    forgotPassword_Button.pack(pady=(10, 0))

    def keep_focus(event):
        event.widget.focus_set()
        return "break"
    
    login_Entry.bind("<Button-1>", keep_focus)
    password_Entry.bind("<Button-1>", keep_focus)

    def dismiss_focus(event):
        login_window.focus_set()

    login_input_Frame.bind("<Button-1>", dismiss_focus) 
    login_window.bind("<Button-1>", dismiss_focus)
    
    login_Label.bind("<Button-1>", dismiss_focus)
    password_Label.bind("<Button-1>", dismiss_focus)
    hint_Label.bind("<Button-1>", dismiss_focus)

    login_window.mainloop()