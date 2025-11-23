import sys
import os

from bson.binary import Binary

from Utils import mongodb_connection
from Utils import mongodb_functions

import tkinter as tk
from PIL import Image, ImageTk
import io
from tkinter import messagebox, filedialog, ttk


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# 1. Отримуємо документ
full_docs = list(mongodb_connection.model_images_collection.find({}))
print("Retrieving the images from MongoDB...")

images_path = list()

# Перевірка, чи документ знайдено
if full_docs:
    for doc in full_docs:
        if doc['filename']:
            print("Starting to save the images back to file...")
            image_data = doc['image_file']
            
            os.makedirs('Data/Images', exist_ok=True) 
            output_path = f"Data/Images/{doc['filename']}.jpg"
            images_path.append(output_path)
            
            with open(output_path, 'wb') as f:
                f.write(image_data)
            print(f"Image saved to {output_path}.")
else:
    print("Documents not found!")
    image_data = None # Щоб не було помилки далі


root = tk.Tk()
root.title("MongoDB Image Gallery")
root.geometry("1000x1000")

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

my_canvas = tk.Canvas(main_frame)
my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

my_canvas.configure(yscrollcommand=my_scrollbar.set)

scrollable_frame = tk.Frame(my_canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: my_canvas.configure(
        scrollregion=my_canvas.bbox("all")
    )
)

my_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Кількість стовпчиків, яку ви хочете
COLUMNS = 3 

if images_path:
    # enumerate дає нам і номер (i), і сам документ (doc)
    for i, doc in enumerate(images_path):
        
        # --- МАГІЯ GRID ---
        # Цілочисельне ділення (//) визначає номер рядка
        row_val = i // COLUMNS 
        # Остача від ділення (%) визначає номер стовпчика (0, 1 або 2)
        col_val = i % COLUMNS 

        # Створюємо картку
        card = tk.Frame(scrollable_frame, bd=2, relief=tk.RIDGE, padx=10, pady=10)
        
        # ЗАМІСТЬ pack ВИКОРИСТОВУЄМО grid
        # sticky="nsew" змушує картку розтягуватися, якщо є вільне місце
        card.grid(row=row_val, column=col_val, padx=10, pady=10, sticky="nsew")

        # --- ВНУТРІШНЄ НАПОВНЕННЯ (залишається як було) ---
        try:
            # Припустимо, doc - це шлях або байти. Тут ваша логіка відкриття:
            img = Image.open(doc) # Або io.BytesIO(doc['file'])
            img.thumbnail((200, 200)) # Трохи зменшимо для галереї

            tk_img = ImageTk.PhotoImage(img)
            
            # Всередині картки можна використовувати pack(), 
            # бо це окремий контейнер!
            lbl_preview = tk.Label(card, image=tk_img, bg="#ddd")
            lbl_preview.pack() # Тут pack() безпечний
            
            # Важливе збереження посилання
            lbl_preview.image = tk_img  # type: ignore
            
            file_name = os.path.basename(doc)
            if len(file_name) > 15:
                file_name = file_name[:12] + "..."

            # Підпис
            lbl_name = tk.Label(card, text=file_name)
            lbl_name.pack()

        except Exception as e:
            print(f"Error: {e}")

# Опціонально: налаштування ваги стовпчиків, щоб вони були однакової ширини
for x in range(COLUMNS):
    scrollable_frame.grid_columnconfigure(x, weight=1)

def _on_mousewheel(event):
    my_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

my_canvas.bind_all("<MouseWheel>", _on_mousewheel)        


root.mainloop()