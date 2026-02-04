import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import os

# ---------- Window ----------
root = tk.Tk()
root.title("Image Processor")
root.geometry("1200x700")  

# ---------- Globals ----------
original_img = None
current_file = None
history = []
redo_history = []

# ---------- Frames ----------
left_frame = tk.Frame(root, width=300)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

#  Image Display 
img_label = tk.Label(right_frame, bg="gray", width=600, height=500)
img_label.pack(fill=tk.BOTH, expand=True)

def show_image(img):
    img_pil = Image.fromarray(img)
    img_pil = img_pil.resize((600, 500))
    img_tk = ImageTk.PhotoImage(img_pil)
    img_label.config(image=img_tk)
    img_label.image = img_tk

#  File Menu 
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
 
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
 
def menu_open():
    global current_file, original_img, history, redo_history
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    if not file_path:
        return
    img = cv2.imread(file_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    original_img = img
    current_file = file_path
    history = [original_img.copy()]
    redo_history.clear()
    show_image(original_img)
 
def menu_save():
    global current_file, original_img
    if original_img is None:
        return
    if not current_file:
        menu_save_as()
        return
    save_img = cv2.cvtColor(original_img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(current_file, save_img)
    messagebox.showinfo("Saved", f"Image saved: {os.path.basename(current_file)}")
 
def menu_save_as():
    global current_file, original_img
    if original_img is None:
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
    if not file_path:
        return
    current_file = file_path
    save_img = cv2.cvtColor(original_img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(current_file, save_img)
    messagebox.showinfo("Saved", f"Image saved: {os.path.basename(current_file)}")
 
def menu_exit():
    root.destroy()
 
file_menu.add_command(label="Open", command=menu_open)
file_menu.add_command(label="Save", command=menu_save)
file_menu.add_command(label="Save As", command=menu_save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=menu_exit)

#  Edit Menu 


#  Image Processing Functions 
def convert_grayscale():
    global original_img, history, redo_history
    if original_img is None:
        messagebox.showerror("Error", "Please open an image first")
        return
    gray = cv2.cvtColor(original_img, cv2.COLOR_RGB2GRAY)
    gray_rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    original_img = gray_rgb
    history.append(original_img.copy())
    redo_history.clear()
    show_image(original_img)

def apply_blur(val):
    global original_img, history, redo_history
    if original_img is None:
        return
    k = int(val)
    if k % 2 == 0:
        k += 1
    if k < 1:
        k = 1
    blurred = cv2.GaussianBlur(original_img, (k, k), 0)
    original_img = blurred
    history.append(original_img.copy())
    redo_history.clear()
    show_image(original_img)

def edge_detection():
    global original_img, history, redo_history
    if original_img is None:
        messagebox.showerror("Error", "Please open an image first")
        return
    gray = cv2.cvtColor(original_img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    original_img = edges_rgb
    history.append(original_img.copy())
    redo_history.clear()
    show_image(original_img)

def adjust_brightness(val):
    global original_img, history, redo_history
    if original_img is None:
        return
    brightness = int(val)
    bright = cv2.convertScaleAbs(original_img, alpha=1, beta=brightness)
    original_img = bright
    history.append(original_img.copy())
    redo_history.clear()
    show_image(original_img)

def adjust_contrast(val):
    global original_img, history, redo_history
    if original_img is None:
        return
    contrast = float(val)
    contrast_img = cv2.convertScaleAbs(original_img, alpha=contrast, beta=0)
    original_img = contrast_img
    history.append(original_img.copy())
    redo_history.clear()
    show_image(original_img)

def resize_image(val):
    global original_img, history, redo_history
    if original_img is None:
        return
    scale = float(val)
    h, w = original_img.shape[:2]
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(original_img, (new_w, new_h))
    original_img = resized
    history.append(original_img.copy())
    redo_history.clear()
    show_image(original_img)

# rotate image
def rotate_image(angle):
    global original_img, history, redo_history
    if original_img is None:
        return
    if angle == 90:
        rotated = cv2.rotate(original_img, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        rotated = cv2.rotate(original_img, cv2.ROTATE_180)
    elif angle == 270:
        rotated = cv2.rotate(original_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        return
    original_img = rotated
    history.append(original_img.copy())
    redo_history.clear()
    show_image(original_img)
 
# flip image:
def flip_image(mode):
    global original_img, history, redo_history
    if original_img is None:
        return
    if mode == 'horizontal':
        flipped = cv2.flip(original_img, 1)
    elif mode == 'vertical':
        flipped = cv2.flip(original_img, 0)
    else:
        return
    original_img = flipped
    history.append(original_img.copy())
    redo_history.clear()
    show_image(original_img)
 
# Buttons
# Rotate buttons
rotate_frame = tk.Frame(left_frame)
rotate_frame.pack(pady=5)
tk.Button(rotate_frame, text="Rotate 90°", command=lambda: rotate_image(90), width=10).pack(side=tk.LEFT, padx=2)
tk.Button(rotate_frame, text="Rotate 180°", command=lambda: rotate_image(180), width=10).pack(side=tk.LEFT, padx=2)
tk.Button(rotate_frame, text="Rotate 270°", command=lambda: rotate_image(270), width=10).pack(side=tk.LEFT, padx=2)
 
# Flip buttons
flip_frame = tk.Frame(left_frame)
flip_frame.pack(pady=5)
tk.Button(flip_frame, text="Flip Horizontal", command=lambda: flip_image('horizontal'), width=15).pack(side=tk.LEFT, padx=2)
tk.Button(flip_frame, text="Flip Vertical", command=lambda: flip_image('vertical'), width=15).pack(side=tk.LEFT, padx=2)

tk.Button(left_frame, text="Open Image", command=menu_open, width=20).pack(pady=5)
tk.Button(left_frame, text="Grayscale", command=convert_grayscale, width=20).pack(pady=5)
tk.Button(left_frame, text="Edge Detection", command=edge_detection, width=20).pack(pady=5)


#  Sliders 
tk.Label(left_frame, text="Blur").pack(pady=(10,0))
tk.Scale(left_frame, from_=1, to=15, orient="horizontal", command=apply_blur, length=200).pack()

tk.Label(left_frame, text="Brightness").pack(pady=(10,0))
tk.Scale(left_frame, from_=-100, to=100, orient="horizontal", command=adjust_brightness, length=200).pack()

tk.Label(left_frame, text="Contrast").pack(pady=(10,0))
tk.Scale(left_frame, from_=0.5, to=3.0, resolution=0.1, orient="horizontal", command=adjust_contrast, length=200).pack()

tk.Label(left_frame, text="Resize / Scale").pack(pady=(10,0))
tk.Scale(left_frame, from_=0.1, to=3.0, resolution=0.1, orient="horizontal", command=resize_image, length=200).pack()

#  Main loop 
root.mainloop()
