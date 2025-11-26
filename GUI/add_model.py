import tkinter as tk
from tkinter import messagebox, filedialog
import os
import base64  # Модуль для конвертації в текст
from PIL import Image, ImageTk

SAVE_DIR = "Local_Storage"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

current_file_path = None

def select_file():
    global current_file_path
    file_path = filedialog.askopenfilename(
        title="Оберіть зображення",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    if file_path:
        current_file_path = file_path
        lbl_path_text.config(text=f"Обрано: {os.path.basename(file_path)}")
        show_preview(file_path)

def show_preview(path):
    try:
        img = Image.open(path)
        img.thumbnail((300, 300))
        tk_img = ImageTk.PhotoImage(img)
        lbl_preview.config(image=tk_img, text="")
        lbl_preview.image = tk_img 
    except Exception as e:
        lbl_preview.config(text=f"Помилка прев'ю: {e}", image="")

def save_as_base64_text():
    """Читає картинку, кодує в Base64 (текст) і зберігає"""
    global current_file_path

    if not current_file_path:
        messagebox.showwarning("Увага", "Спочатку оберіть файл!")
        return

    try:
        filename = os.path.basename(current_file_path)
        name_without_ext = os.path.splitext(filename)[0]
        
        # Шлях до нового текстового файлу
        output_path = os.path.join(SAVE_DIR, name_without_ext) 

        # 1. Читаємо оригінал як байти
        with open(current_file_path, 'rb') as f_in:
            image_bytes = f_in.read()

        # 2. Конвертуємо байти в текст (Base64)
        base64_bytes = base64.b64encode(image_bytes)
        base64_string = base64_bytes.decode('utf-8') # Перетворюємо в звичайний рядок

        # 3. Записуємо ТЕКСТ у файл
        with open(output_path, 'w', encoding='utf-8') as f_out:
            f_out.write(base64_string)
        
        messagebox.showinfo("Успіх", f"Картинку перетворено в код!\nЗбережено: {output_path}")
        
        # Скидання
        lbl_path_text.config(text="Файл не обрано")
        lbl_preview.config(image='', text="Місце для прев'ю")
        lbl_preview.image = None
        current_file_path = None
        
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося зберегти: {e}")

# --- GUI ---
root = tk.Tk()
root.title("Img to Base64 Converter")
root.geometry("500x600")

tk.Label(root, text="Конвертер Картинка -> Текстовий Код", font=("Arial", 14, "bold"), pady=10).pack()
tk.Button(root, text="📂 Обрати картинку", command=select_file, height=2).pack(pady=10)
lbl_path_text = tk.Label(root, text="...", fg="blue")
lbl_path_text.pack()
lbl_preview = tk.Label(root, text="Прев'ю", bg="#ddd", height=15)
lbl_preview.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)
# Кнопка тепер викликає save_as_base64_text
tk.Button(root, text="💾 Зберегти як Текст (Base64)", command=save_as_base64_text, bg="orange", fg="black", font=("Arial", 12, "bold")).pack(pady=20, fill=tk.X, padx=20)

root.mainloop()