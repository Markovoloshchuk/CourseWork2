import sys
import os

from Utils import mongodb_connection
from Utils import mongodb_functions
from Utils import tkinter_general

import tkinter as tk
from tkinter import messagebox, filedialog, ttk

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

def open_collection_window():
    collection_window = tk.Tk()
    collection_window.title("Login")
    tkinter_general.center_window(collection_window, 1200, 800)
    collection_window.configure(bg="#e6ccff")

    collection_window.mainloop()