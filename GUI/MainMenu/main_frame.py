import sys, os, io
import tkinter as tk
from PIL import Image, ImageTk
import base64

from Utils import tkinter_general
from GUI.MainMenu.catalog import CatalogView
from GUI.MainMenu.account import AccountView
from GUI.MainMenu.info_frame import InfoFrameView

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)


# --- Фрейми-заглушки для прикладу (Створіть окремі файли для них пізніше) ---

# --- Головний клас ---
class MainFrameView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#e6ccff")
        self.controller = controller


        self.controller.title("Atelier")
        tkinter_general.center_window(self.controller, 1200, 800) 

        # 1. Створюємо загальний контейнер
        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True)

        self.editor_window = None

        # 2. Створюємо статичний Хедер (він створюється лише 1 раз)
        self.create_header()

        # 3. Створюємо контейнер для динамічного контенту (туди будемо пхати Catalog, Info...)
        self.content_area = tk.Frame(self.container, bg="white")
        self.content_area.pack(fill="both", expand=True)

        # 4. Завантажуємо стартову сторінку (наприклад, Каталог)
        self.switch_content(CatalogView)
    
    def load_logo_from_binary(self, path):
        """Читає бінарний файл без розширення і повертає ImageTk об'єкт"""
        if not os.path.exists(path):
            print(f"Логотип не знайдено за шляхом: {path}")
            return None
        
        try:
            # 1. Читаємо чисті байти
            with open(path, 'rb') as f:
                file_data = f.read()
            
            try:
                # Перевірка: якщо це Base64, воно має бути текстом
                image_bytes = base64.b64decode(file_data)
            except Exception:
                # Якщо помилка декодування (значить це вже була бінарна картинка),
                # то використовуємо дані як є
                image_bytes = file_data


            # 2. Перетворюємо байти у віртуальний файл
            data_stream = io.BytesIO(image_bytes)
            
            # 3. Відкриваємо як картинку PIL
            pil_image = Image.open(data_stream)

            width, height = pil_image.size
            
            new_width = int(width / 8)
            new_height = int(height / 8)
            
            # Змінюємо розмір (Image.LANCZOS робить картинку чіткою при зменшенні)
            pil_image = pil_image.resize((new_width, new_height), Image.LANCZOS) # type: ignore
            
            # Опціонально: ресайз логотипа, щоб не був гігантським
            # pil_image.thumbnail((150, 80)) 
            
            return ImageTk.PhotoImage(pil_image)
            
        except Exception as e:
            print(f"Помилка завантаження логотипа: {e}")
            return None

    def create_header(self):
        header_frame = tk.Frame(self.container, bg="#e6ccff", height=100)
        header_frame.pack(fill=tk.X, pady=0) # pady прибрали, щоб було щільно, або залиште за смаком

        # Логотип
        logo_path = os.path.join("Data/Images/Atelier_logo_small")
        
        self.logo_img = self.load_logo_from_binary(logo_path)

        if self.logo_img:
            # Якщо картинка завантажилась - показуємо її
            tk.Label(header_frame, image=self.logo_img, bg="#e6ccff").pack(side=tk.LEFT, padx=20, pady=5)
        else:
            # Якщо файлу немає або помилка - показуємо старий текст як запасний варіант
            tk.Label(header_frame, text="Atelier", font=("Arial", 24, "bold"), bg="#e6ccff", fg="purple").pack(side=tk.LEFT, padx=20, pady=5)
        # Кнопки навігації (Зверніть увагу на command)
        self.create_nav_button(header_frame, "Catalog", lambda: self.switch_content(CatalogView), side=tk.LEFT)
        self.create_nav_button(header_frame, "Info", lambda: self.switch_content(InfoFrameView), side=tk.LEFT)
        self.create_nav_button(header_frame, "Editor", command=self.open_editor, side=tk.LEFT)
        
        self.create_nav_button(header_frame, "Account", lambda: self.switch_content(AccountView), side=tk.RIGHT)
        self.create_nav_button(header_frame, "My Orders", lambda: print("Orders clicked"), side=tk.RIGHT)

    def create_nav_button(self, parent, text, command, side):
        """Допоміжний метод для створення кнопок, щоб не дублювати код"""
        btn = tk.Button(parent, text=text, font=("Arial", 14), bg="white", fg="black",
                        activebackground="#d1b3ff", activeforeground="black",
                        borderwidth=0, cursor="hand2",
                        command=command)
        btn.pack(side=side, padx=10, pady=10)

    def switch_content(self, frame_class):
        """
        Метод для заміни контенту в центральній частині.
        """
        # 1. Видаляємо все, що зараз є в content_area
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # 2. Створюємо новий фрейм
        # Передаємо self.content_area як parent, щоб він вклався в правильне місце
        new_frame = frame_class(self.content_area, self.controller)
        new_frame.pack(fill="both", expand=True)
        
        # Зберігаємо посилання на поточний фрейм, якщо треба
        self.current_content_frame = new_frame
    
    def open_editor(self):
        """Відкриває вікно редактора"""
        from GUI.Editor.editor_frame import EditorFrameView

        if self.editor_window is None or not self.editor_window.winfo_exists():
            self.editor_window = EditorFrameView() # Зберігаємо в self!
        else:
            self.editor_window.lift() # Піднімаємо наверх, якщо вже відкрито
            self.editor_window.focus_set()

