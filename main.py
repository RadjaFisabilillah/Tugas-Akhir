import tkinter as tk
from tkinter import filedialog, colorchooser, ttk
from PIL import Image, ImageOps, ImageTk, ImageFilter
import time

class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.loading_label = tk.Label(root, text="Loading", font=("Helvetica", 24), bg="white")
        self.loading_label.pack(pady=20)
        
        self.author_label = tk.Label(root, text="Dibuat oleh Radja", font=("Helvetica", 14), bg="white")
        self.author_label.pack(pady=10)
        
        self.root.update()
        
    def animate(self):
        dots = ""
        counter = 0
        start_time = time.time()
        
        while time.time() - start_time < 5:  
            dots = "." * (counter % 4)
            self.loading_label.config(text=f"Loading{dots}")
            self.root.update()
            time.sleep(0.5)
            counter += 1
        
        self.loading_label.destroy()
        self.author_label.destroy()

root = tk.Tk()
root.geometry("1000x600")
root.title("Alat Lukis Gambar")
root.config(bg="white")

loading_screen = LoadingScreen(root)
loading_screen.animate()

pen_color = "black"
pen_size = 5
file_path = ""
is_drawing = False

def add_image():
    global file_path
    file_path = filedialog.askopenfilename(
        initialdir="C:/KULIAH/Praktikum DKP/Tugas Akhir_Alat Edit Gambar/Gambar"
    )
    if file_path:
        image = Image.open(file_path)
        image = image.resize((canvas.winfo_width(), canvas.winfo_height()), Image.LANCZOS)
        canvas.image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, image=canvas.image, anchor="nw")

def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title="Pilih Warna Kuas")[1]

def change_size(size):
    global pen_size
    pen_size = size

def draw(event):
    x1, y1 = (event.x - pen_size), (event.y - pen_size)
    x2, y2 = (event.x + pen_size), (event.y + pen_size)
    canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline='')

def clear_canvas():
    canvas.delete("all")
    if canvas.image:
        canvas.create_image(0, 0, image=canvas.image, anchor="nw")

def apply_filter(filter):
    if file_path:
        image = Image.open(file_path)
        image = image.resize((canvas.winfo_width(), canvas.winfo_height()), Image.LANCZOS)
        if filter == "Hitam dan Putih":
            image = ImageOps.grayscale(image)
        elif filter == "Buram":
            image = image.filter(ImageFilter.BLUR)
        elif filter == "Timbul":
            image = image.filter(ImageFilter.EMBOSS)
        elif filter == "Pertajam":
            image = image.filter(ImageFilter.SHARPEN)
        elif filter == "Perhalus":
            image = image.filter(ImageFilter.SMOOTH)
        canvas.image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, image=canvas.image, anchor="nw")

def update_drawing_state_label():
    if is_drawing:
        drawing_state_label.config(text="Mode Menggambar: AKTIF", bg="#77DD77")
    else:
        drawing_state_label.config(text="Mode Menggambar: NON-AKTIF", bg="#FF6961")

def start_drawing():
    global is_drawing
    is_drawing = True
    update_drawing_state_label()
    canvas.bind("<B1-Motion>", draw)

def stop_drawing():
    global is_drawing
    is_drawing = False
    update_drawing_state_label()
    canvas.unbind("<B1-Motion>")

left_frame = tk.Frame(root, width=200, height=600, bg="#BEB7A4")
left_frame.pack(side="left", fill="y")

canvas_frame = tk.Frame(root, bg="white")
canvas_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(canvas_frame, width=750, height=600, bg="white", scrollregion=(0, 0, 750, 600))
hbar = tk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
hbar.pack(side="bottom", fill="x")
vbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
vbar.pack(side="right", fill="y")
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side="left", fill="both", expand=True)

image_button = tk.Button(left_frame, text="Tambahkan Gambar", bg="#114B5F", command=add_image)
image_button.pack(pady=15)

color_button = tk.Button(left_frame, text="Ubah Warna Kuas", command=change_color, bg="#114B5F")
color_button.pack(pady=5)

pen_size_frame = tk.Frame(left_frame, bg="#114B5F")
pen_size_frame.pack(pady=5)

pen_size_1 = tk.Radiobutton(pen_size_frame, text="Kecil", value=3, command=lambda: change_size(3), bg="#BEB7A4")
pen_size_1.pack(side="left")

pen_size_2 = tk.Radiobutton(pen_size_frame, text="Sedang", value=5, command=lambda: change_size(5), bg="#BEB7A4")
pen_size_2.pack(side="left")
pen_size_2.select()

pen_size_3 = tk.Radiobutton(pen_size_frame, text="Besar", value=7, command=lambda: change_size(7), bg="#BEB7A4")
pen_size_3.pack(side="left")

clear_button = tk.Button(left_frame, text="Bersihkan", command=clear_canvas, bg="#AD88C6")
clear_button.pack(pady=10)

filter_label = tk.Label(left_frame, text="Pilih Filter:", bg="#BEB7A4")
filter_label.pack()

filter_combobox = ttk.Combobox(left_frame, values=["Hitam dan Putih", "Buram", "Timbul", "Pertajam", "Perhalus"])
filter_combobox.pack()
filter_combobox.bind("<<ComboboxSelected>>", lambda event: apply_filter(filter_combobox.get()))

start_button = tk.Button(left_frame, text="Mulai Menggambar", command=start_drawing, bg="#77DD77")
start_button.pack(pady=10)

stop_button = tk.Button(left_frame, text="Berhenti Menggambar", command=stop_drawing, bg="#FF6961")
stop_button.pack(pady=10)

drawing_state_label = tk.Label(left_frame, text="Mode Menggambar: NON-AKTIF", bg="#FF6961", font=("Helvetica", 12))
drawing_state_label.pack(pady=10)

root.mainloop()
