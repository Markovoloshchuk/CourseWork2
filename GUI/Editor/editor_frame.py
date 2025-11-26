import sys
import os
import tkinter as tk

# Імпортуємо базовий клас таблиці
from GUI.Editor.base_info_editor_frame import BaseInfoEditorView

# Імпортуємо класи-форми (вони будуть використовуватися і для створення, і для редагування)
from GUI.Editor.model_info_creator import ModelInfoCreatorFrame
from GUI.Editor.fabric_info_creator import FabricInfoCreatorFrame
from GUI.Editor.tailor_info_creator import TailorInfoCreatorFrame

from Utils import tkinter_general

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)


class EditorFrameView(tk.Toplevel):
    def __init__(self):
        super().__init__()
        
        self.title("Atelier Editor")
        tkinter_general.center_window(self, 1000, 800) # Трохи ширше для таблиць
        self.configure()

        # 1. Створюємо загальний контейнер
        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True)

        self.create_sidebar()

        self.content_area = tk.Frame(self.container, bg="white")
        self.content_area.pack(fill="both", expand=True)

    def create_sidebar(self):
        sidebar_frame = tk.Frame(self.container, bg="#e6ccff", width=200)
        sidebar_frame.pack(fill=tk.Y, side=tk.LEFT, pady=0)
        sidebar_frame.pack_propagate(False) # Фіксуємо ширину сайдбару

        tk.Label(sidebar_frame, text="Atelier Editor", font=("Arial", 16, "bold"), 
                bg="#e6ccff", fg="purple").pack(side=tk.TOP, padx=10, pady=20)

        # --- Розділ CREATOR (Створення нових) ---
        tk.Label(sidebar_frame, text="CREATE NEW", font=("Arial", 10, "bold"), bg="#e6ccff", fg="#555").pack(anchor="w", padx=10, pady=(10,0))
        self.create_nav_button(sidebar_frame, "➕ New Model", lambda: self.open_creator(ModelInfoCreatorFrame))
        self.create_nav_button(sidebar_frame, "➕ New Fabric", lambda: self.open_creator(FabricInfoCreatorFrame))
        self.create_nav_button(sidebar_frame, "➕ New Tailor", lambda: self.open_creator(TailorInfoCreatorFrame))

        # --- Розділ EDITOR (Редагування списків) ---
        tk.Label(sidebar_frame, text="MANAGE LISTS", font=("Arial", 10, "bold"), bg="#e6ccff", fg="#555").pack(anchor="w", padx=10, pady=(20,0))
        
        # Тут ми викликаємо спеціальні методи, які налаштують таблицю
        self.create_nav_button(sidebar_frame, "📝 Manage Models", self.show_model_table)
        self.create_nav_button(sidebar_frame, "📝 Manage Fabrics", self.show_fabric_table)
        self.create_nav_button(sidebar_frame, "📝 Manage Tailors", self.show_tailor_table)

    def create_nav_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, font=("Arial", 12), bg="#e6ccff", fg="black",
                        activebackground="#d1b3ff", activeforeground="black",
                        borderwidth=0, highlightthickness=0, cursor="hand2", anchor="w",
                        command=command)
        btn.pack(side=tk.TOP, fill=tk.X, padx=10, pady=2)

    def clear_content(self):
        """Очищає праву частину вікна"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # --- Методи для відкриття форм створення (як було раніше) ---
    def open_creator(self, frame_class):
        self.clear_content()
        # Тут ми створюємо CreatorFrame прямо в content_area (не як вікно, а як фрейм)
        new_frame = frame_class(self.content_area, self)
        new_frame.pack(fill="both", expand=True)

    # --- НОВІ Методи для відкриття ТАБЛИЦЬ редагування ---
    
    def show_model_table(self):
        self.clear_content()
        # Створюємо таблицю (BaseInfoEditorView)
        editor = BaseInfoEditorView(
            parent=self.content_area,
            controller=self,
            collection_name="models",           # База даних
            creator_class=ModelInfoCreatorFrame, # Клас, який відкриється у Popup при натисканні Edit
            headers=[                           # Стовпці таблиці
                ("_id", "ID"), 
                ("model_name", "Name"), 
                ("price", "Price"), 
                ("in_stock", "In Stock")
            ]
        )
        editor.pack(fill="both", expand=True)

    def show_fabric_table(self):
        self.clear_content()
        editor = BaseInfoEditorView(
            parent=self.content_area,
            controller=self,
            collection_name="fabrics",
            creator_class=FabricInfoCreatorFrame, # Відкриється вікно тканини
            headers=[
                ("_id", "ID"), 
                ("fabric_name", "Name"), 
                ("fabric_color", "Color"), 
                ("price_per_meter", "Price/m")
            ]
        )
        editor.pack(fill="both", expand=True)

    def show_tailor_table(self):
        self.clear_content()
        editor = BaseInfoEditorView(
            parent=self.content_area,
            controller=self,
            collection_name="tailors",
            creator_class=TailorInfoCreatorFrame, # Відкриється вікно кравця
            headers=[
                ("_id", "ID"), 
                ("name", "Full Name"), 
                ("number", "Phone")
            ]
        )
        editor.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = EditorFrameView()
    app.mainloop()