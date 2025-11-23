import sys
import os
import tkinter as tk
from tkinter import messagebox

from Utils import mongodb_functions
from Utils import tkinter_general
from GUI.Authentication import login

class ForgotPasswordView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#e6ccff")
        self.controller = controller

        # Налаштування вікна
        self.controller.title("Restore Password")
        self.controller.resizable(False, False)
        tkinter_general.center_window(self.controller, 500, 500)
        
        # Змінна для збереження логіна, який ми перевірили на 1 етапі
        self.target_login = None

        self.create_widgets()
        self.setup_bindings()
        
        # Запускаємо одразу перший етап
        self.show_stage1()

    def create_widgets(self):
        # 1. Заголовок (спільний, кріпиться до self)
        self.title_Label = tk.Label(self, text="Restore Password Screen", font=("Arial", 16), bg="#e6ccff", fg="purple")
        self.title_Label.pack(pady=20)

        # ==========================================
        # ЕТАП 1: ВВЕДЕННЯ ЛОГІНУ
        # ==========================================
        self.stage1_frame = tk.Frame(self, width=400, height=400, bg="white")
        self.stage1_frame.pack_propagate(False) 

        self.login_Label = tk.Label(self.stage1_frame, text="Enter your Login", bg="white", font=("Arial", 12))
        self.login_Entry = tk.Entry(self.stage1_frame, font=("Arial", 12))

        self.login_Button = tk.Button(self.stage1_frame, text="Next", justify=tk.CENTER,
                                      width=20, font=("Arial", 14), bg="#b366ff", fg="white", 
                                      activebackground="#cc80ff", activeforeground="white",
                                      command=self.handle_stage1_submit)
        
        # Кнопка "Go back" на 1 етапі -> Повертає в меню Логіну
        self.back_to_menu_Button = tk.Button(self.stage1_frame, text="Go back to Login", justify=tk.CENTER, 
                                             font=("Arial", 12), bg="white", fg="#a6a6a6", 
                                             borderwidth=0, highlightthickness=0, 
                                             activebackground="white", activeforeground="#737373",
                                             command=self.go_back_to_login_view)

        # Розміщення елементів 1 етапу
        self.login_Label.pack(anchor='w', padx=20, pady=(40, 0))
        self.login_Entry.pack(padx=20, pady=(0, 20), fill=tk.X)
        self.login_Button.pack(pady=20)
        self.back_to_menu_Button.pack(pady=10)

        # ==========================================
        # ЕТАП 2: ВВЕДЕННЯ НОВОГО ПАРОЛЮ
        # ==========================================
        self.stage2_frame = tk.Frame(self, width=400, height=400, bg="white")
        self.stage2_frame.pack_propagate(False)

        self.user_info_Label = tk.Label(self.stage2_frame, text="", bg="white", fg="purple", font=("Arial", 10))
        self.user_info_Label.pack(pady=(20, 10))

        self.password_Label = tk.Label(self.stage2_frame, text="New password", bg="white", font=("Arial", 12))
        self.password_Entry = tk.Entry(self.stage2_frame, show="*", font=("Arial", 12))
        self.format_check_hint_Label = tk.Label(self.stage2_frame, 
                                text="*password must contain at least 8 characters, one small and one capital letter, one digit", 
                                bg="white", font=("Arial", 8), fg="white", 
                                justify="left", wraplength=300)

        self.repeat_password_Label = tk.Label(self.stage2_frame, text="Repeat password", bg="white", font=("Arial", 12))
        self.repeat_password_Entry = tk.Entry(self.stage2_frame, show="*", font=("Arial", 12))
        self.match_check_hint_Label = tk.Label(self.stage2_frame, 
                                text="*passwords do not match!", bg="white", font=("Arial", 8), fg="white", 
                                justify="left", wraplength=300)

        self.enter_Button = tk.Button(self.stage2_frame, text="Change Password", justify=tk.CENTER, 
                                    width=20, font=("Arial", 14), bg="#b366ff", fg="white", 
                                    activebackground="#cc80ff", activeforeground="white", 
                                    command=self.handle_stage2_submit)
        
        # Кнопка "Go back" на 2 етапі -> Повертає до вводу логіну (Етап 1)
        self.back_to_login_entrance_Button = tk.Button(self.stage2_frame, text="Go back", justify=tk.CENTER, 
                                    font=("Arial", 12), bg="white", fg="#a6a6a6", 
                                    borderwidth=0, highlightthickness=0, 
                                    activebackground="white", activeforeground="#737373",
                                    command=self.show_stage1)

        # Розміщення елементів 2 етапу
        self.password_Label.pack(anchor='w', padx=20, pady=(0, 0))
        self.password_Entry.pack(padx=20, pady=(0, 0), fill=tk.X)
        self.format_check_hint_Label.pack(anchor='w', padx=20, pady=(0, 20))

        self.repeat_password_Label.pack(anchor='w', padx=20, pady=(0, 0))
        self.repeat_password_Entry.pack(padx=20, pady=(0, 0), fill=tk.X)
        self.match_check_hint_Label.pack(anchor='w', padx=20, pady=(0, 20))

        self.enter_Button.pack()
        self.back_to_login_entrance_Button.pack(pady=10)

    def setup_bindings(self):
        # Validation binds
        self.password_Entry.bind("<FocusOut>", self.check_password_format)
        self.password_Entry.bind("<FocusIn>", self.reset_format_hint)
        
        self.repeat_password_Entry.bind("<FocusOut>", self.check_password_match)
        self.repeat_password_Entry.bind("<FocusIn>", self.reset_match_hint)

        # Focus management
        self.login_Entry.bind("<Button-1>", self.keep_focus)
        self.password_Entry.bind("<Button-1>", self.keep_focus)
        self.repeat_password_Entry.bind("<Button-1>", self.keep_focus)

        # Dismiss focus binds
        # Біндимо на обидва фрейми, бо в різні моменти часу активний лише один з них
        self.stage1_frame.bind("<Button-1>", self.dismiss_focus)
        self.stage2_frame.bind("<Button-1>", self.dismiss_focus)
        
        self.bind("<Button-1>", self.dismiss_focus) 
        
        self.login_Label.bind("<Button-1>", self.dismiss_focus)
        self.password_Label.bind("<Button-1>", self.dismiss_focus)
        self.repeat_password_Label.bind("<Button-1>", self.dismiss_focus)
        self.format_check_hint_Label.bind("<Button-1>", self.dismiss_focus)
        self.match_check_hint_Label.bind("<Button-1>", self.dismiss_focus)

    # ==========================================
    # ЛОГІКА ПЕРЕМИКАННЯ ЕТАПІВ
    # ==========================================

    def show_stage1(self):
        """Ховаємо 2-й етап, показуємо 1-й"""
        self.stage2_frame.pack_forget()
        self.stage1_frame.pack()

    def show_stage2(self):
        """Ховаємо 1-й етап, показуємо 2-й"""
        self.stage1_frame.pack_forget()
        self.stage2_frame.pack()
        
        # Очищуємо поля паролів при вході
        self.password_Entry.delete(0, tk.END)
        self.repeat_password_Entry.delete(0, tk.END)
        self.user_info_Label.config(text=f"Recovering password for: {self.target_login}")

    # ==========================================
    # ЛОГІКА ОБРОБКИ ДІЙ
    # ==========================================

    def handle_stage1_submit(self):
        """Перевіряємо логін"""
        login_val = self.login_Entry.get()

        if not login_val:
            messagebox.showwarning("Warning", "Please enter a login first.")
            return

        if not mongodb_functions.get_user(login_val):
            return
        
        self.target_login = login_val
        self.show_stage2() # Переходимо далі

    def handle_stage2_submit(self):
        """Зберігаємо новий пароль"""
        new_pass = self.password_Entry.get()
        repeat_pass = self.repeat_password_Entry.get()

        if not mongodb_functions.is_password_valid(new_pass):
            messagebox.showerror("Error", "Password is too weak.")
            return

        if new_pass != repeat_pass:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        
        # Оновлення в БД (розкоментуйте, коли буде функція)
        if mongodb_functions.uptade_password(self.target_login, new_pass):
            messagebox.showinfo("Success", "Password changed!")
            self.go_back_to_login_view()

    def go_back_to_login_view(self):
        
        self.controller.switch_frame(login.LoginView)

    # ==========================================
    # ДОПОМІЖНІ ФУНКЦІЇ (Validation & Focus)
    # ==========================================

    def check_password_format(self, event):
        pwd = self.password_Entry.get()
        if pwd and mongodb_functions.is_password_valid(pwd):
            self.format_check_hint_Label.config(fg="white") # або green
        else:
            self.format_check_hint_Label.config(fg="red")

    def reset_format_hint(self, event):
        self.format_check_hint_Label.config(fg="white")

    def check_password_match(self, event):
        if self.password_Entry.get() != self.repeat_password_Entry.get():
            self.match_check_hint_Label.config(fg="red")
        else:
            self.match_check_hint_Label.config(fg="white") # або green

    def reset_match_hint(self, event):
        self.match_check_hint_Label.config(fg="white")

    def keep_focus(self, event):
        event.widget.focus_set()
        return "break"

    def dismiss_focus(self, event):
        self.controller.focus_set()