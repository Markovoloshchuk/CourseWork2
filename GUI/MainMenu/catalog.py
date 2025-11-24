import sys
import os
import tkinter as tk
from tkinter import ttk
import time

from Utils import tkinter_general

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)



class CatalogView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")

        self.is_loading = False  # Щоб не запускати завантаження двічі одночасно
        self.current_product_index = 0 # Лічильник товарів (для бази даних)
        self.grid_row = 0        # Поточний рядок сітки
        self.grid_col = 0        # Поточна колонка сітки

        self.create_widgets()

        self.load_more_products()
    
    def create_widgets(self):
        #Category Buttons Frame
        category_Frame = tk.Frame(self, bg="lightgray")
        category_Frame.pack(side=tk.TOP, fill=tk.X)

        models_button = tk.Button(category_Frame, text="Models", font=("Arial", 18, "bold"))
        models_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        fabrics_button = tk.Button(category_Frame, text="Fabrics", font=("Arial", 18, "bold"))
        fabrics_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        #Body Frame
        body_frame = tk.Frame(self, bg="white")
        body_frame.pack(fill=tk.BOTH, expand=True)

        #Search Frame
        search_Frame = tk.Frame(body_frame, bg="pink", width=250)
        search_Frame.pack(side=tk.LEFT, fill=tk.Y)
        search_Frame.pack_propagate(False)


        #Content Frame
        scroll_container = tk.Frame(body_frame, bg="white")
        scroll_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(scroll_container, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(scroll_container, orient=tk.VERTICAL, command=self.canvas.yview)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.configure(yscrollcommand=self.on_scroll)

        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.canvas_frame_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
    
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind('<Enter>', self._bind_mouse_wheel)
        self.canvas.bind('<Leave>', self._unbind_mouse_wheel)

        def on_canvas_resize(event):
            canvas_width = event.width
            self.canvas.itemconfig(self.canvas_frame_window, width=canvas_width)
        
        self.canvas.bind("<Configure>", on_canvas_resize)

    def _bind_mouse_wheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mouse_wheel(self, event):
        self.canvas.bind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        # Linux: Button-4 = Вгору, Button-5 = Вниз
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        # Windows/MacOS: Використовує delta
        elif event.delta:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.check_scroll_position()

    def on_scroll(self, *args):
        # Цей метод викликається самим канвасом при будь-якому русі
        self.scrollbar.set(*args) # Оновлюємо візуально повзунок
        self.check_scroll_position()

    def check_scroll_position(self):
        if self.is_loading:
            return

        # yview() повертає (top, bottom). bottom — це число від 0.0 до 1.0
        # 1.0 означає самий низ. 
        # Ми ставимо поріг 0.9 (90%), щоб почати вантажити трохи заздалегідь
        current_position = self.canvas.yview()[1]
        
        if current_position > 0.9:
            self.load_more_products()

    def load_more_products(self):
        self.is_loading = True
        print(f"Loading data... Offset: {self.current_product_index}")
        
        # Імітація запиту до бази даних (тут ви будете брати реальні дані)
        # Наприклад: new_products = database.get_products(limit=10, offset=self.current_product_index)
        new_products = [f"Product {i}" for i in range(self.current_product_index, self.current_product_index + 12)]
        
        if not new_products:
            self.is_loading = False
            return

        # Налаштування колонок (3 колонки)
        self.scrollable_frame.columnconfigure(0, weight=1)
        self.scrollable_frame.columnconfigure(1, weight=1)
        self.scrollable_frame.columnconfigure(2, weight=1)

        # Додавання карток
        for name in new_products:
            self.create_product_card(name)
            
        self.current_product_index += len(new_products)
        
        # Даємо Tkinter час оновити інтерфейс перед тим, як дозволити нове завантаження
        self.after(500, lambda: setattr(self, 'is_loading', False))

    def create_product_card(self, name):
        # Створення однієї картки
        card = tk.Frame(self.scrollable_frame, bg="#f0f0f0", bd=1, relief="solid")
        card.grid(row=self.grid_row, column=self.grid_col, padx=10, pady=40, sticky="nsew")
        
        tk.Label(card, text=name, font=("Arial", 12), bg="#f0f0f0").pack(pady=40)
        
        # Логіка сітки (Grid Logic)
        self.grid_col += 1
        if self.grid_col > 2: # Якщо 3 колонки заповнені (0, 1, 2)
            self.grid_col = 0
            self.grid_row += 1