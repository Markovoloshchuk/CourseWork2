import sys
import os

from bson.binary import Binary

from Utils import mongodb_connection
from Utils import mongodb_functions

import tkinter as tk
from PIL import Image, ImageTk
import io
from tkinter import messagebox, filedialog

# ... Ваша логіка шляхів залишається без змін ...
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# 1. Отримуємо документ
full_doc = mongodb_connection.images_collection.find_one({"image_id": 1})
print("Retrieving the image from MongoDB...")

# Перевірка, чи документ знайдено
if full_doc:
    print("Starting to save the image back to file...")
    image_data = full_doc['image_file']
    
    # ВИПРАВЛЕННЯ 1: Використовуємо подвійні лапки для f-string, щоб не конфліктувати з ключем
    # Також переконайтесь, що папка Data/Images існує
    os.makedirs('Data/Images', exist_ok=True) 
    output_path = f"Data/Images/{full_doc['image_id']}.jpg"
    
    with open(output_path, 'wb') as f:
        f.write(image_data)
    print(f"Image saved to {output_path}.")
else:
    print("Document not found!")
    image_data = None # Щоб не було помилки далі

# --- TKINTER ЧАСТИНА ---

current_file_path = None

def select_file():
    """Відкриває вікно вибору файлу"""
    global current_file_path
    
    # 1. Відкриваємо провідник
    file_path = filedialog.askopenfilename(
        title="Оберіть зображення",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    
    if file_path:
        current_file_path = file_path
        
        # --- ДОДАНО: Оновлюємо текст лейбла, щоб бачити назву файлу ---
        lbl_path_text.config(text=f"Обрано: {os.path.basename(file_path)}")
        
        show_preview(file_path)

def show_preview(path):
    """Показує зменшену копію картинки у вікні"""
    try:
        img = Image.open(path)
        img.thumbnail((300, 300))
        
        tk_img = ImageTk.PhotoImage(img)
        lbl_preview.config(image=tk_img, text="")
        
        
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося відкрити картинку: {e}")

def upload_to_db():
    """Читає файл з диску і відправляє в MongoDB"""
    if not current_file_path:
        messagebox.showwarning("Увага", "Спочатку оберіть файл!")
        return

    try:
        # 1. Читаємо файл як байти (Binary)
        with open(current_file_path, 'rb') as f:
            image_bytes = f.read()

        # 2. Готуємо документ
        # Можете додати сюди введення ID вручну, якщо хочете
        doc = {
            "image_id": mongodb_functions.get_next_sequence("image_id"),
            "filename": os.path.basename(current_file_path),
            "image_file": Binary(image_bytes), # Важливий момент конвертації
        }

        # 3. Вставляємо в базу
        mongodb_connection.images_collection.insert_one(doc)
        
        messagebox.showinfo("Успіх", "Зображення завантажено в базу!")
        
        # Очищення полів після завантаження
        lbl_path_text.config(text="Файл не обрано")
        lbl_preview.config(image='', text="Місце для прев'ю")
        entry_desc.delete(0, tk.END)
        
    except Exception as e:
        messagebox.showerror("Помилка завантаження", str(e))


root = tk.Tk()
root.title("MongoDB Image Uploader")
root.geometry("1000x1000")

# Кнопка вибору
btn_select = tk.Button(root, text="📂 Обрати файл", command=select_file, height=2)
btn_select.pack(pady=10)

# Текст з назвою файлу
lbl_path_text = tk.Label(root, text="Файл не обрано", fg="blue")
lbl_path_text.pack()

# Область прев'ю
lbl_preview = tk.Label(root, text="Місце для прев'ю", bg="#ddd", padx=5, pady=5)
lbl_preview.pack(pady=10)

# Поле для опису (опціонально)
tk.Label(root, text="Додати опис:").pack()
entry_desc = tk.Entry(root, width=40)
entry_desc.pack()

# Кнопка завантаження
btn_upload = tk.Button(root, text="☁️ Завантажити в БД", command=upload_to_db, bg="green", fg="white", font=("Arial", 12, "bold"))
btn_upload.pack(pady=20, fill=tk.X, padx=20)

root.mainloop()