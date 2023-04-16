import os
import tkinter as tk
from tkinter import ttk, filedialog
from app import main, convert_to_srgb
from PIL import Image, ImageTk
import glob

# Load image previews
def load_image_previews(folder, frame, columns=6):
    for widget in frame.winfo_children():
        widget.destroy()

    files = glob.glob(os.path.join(folder, "*.jpg")) + glob.glob(os.path.join(folder, "*.jpeg")) + glob.glob(os.path.join(folder, "*.png"))
    for i, file in enumerate(files):
        img = Image.open(file)
        img = convert_to_srgb(img)  # convert to sRGB color space
        img.thumbnail((100, 100), Image.LANCZOS)

        # Add black background to maintain aspect ratio
        img_bg = Image.new('RGBA', (100, 100), (0, 0, 0, 255))
        img_bg.paste(img, (int((100 - img.width) / 2), int((100 - img.height) / 2)))

        img = ImageTk.PhotoImage(img_bg)
        img_label = ttk.Label(frame, image=img)
        img_label.image = img
        img_label.grid(row=i // columns, column=i % columns, padx=5, pady=5)

def start_processing():
    main(input_folder_var.get(),
         output_folder_var.get(),
         float(offset_x_var.get()),
         float(offset_y_var.get()),
         float(face_percent_var.get()),
         int(resize_var.get()),
         float(threshold_var.get()),
         output_format_var.get())

# Start processing and show output image previews
def start_processing_and_show_output():
    start_processing()
    load_image_previews(output_folder_var.get(), output_preview_frame)

root = tk.Tk()
root.title("Face Detection and Cropping")

# Maximize window
root.state("zoomed")
# Set window background color
root.configure(bg="#222")
style = ttk.Style()
style.theme_use("clam")
style.configure(".", background="#222", foreground="#ccc")
style.map(".", background=[("selected", "#222"), ("active", "#333")])
style.configure("TEntry", fieldbackground="#222", foreground="#ccc", insertcolor="#ccc")
style.configure("TButton", background="#222", foreground="#ccc")

main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew")

controls_frame = ttk.Frame(main_frame)
controls_frame.grid(row=0, column=0, padx=20, pady=20, sticky="n")

# Default input and output folders
input_folder_default = os.path.join(os.getcwd(), "_INPUT")
output_folder_default = os.path.join(os.getcwd(), "_OUTPUT")

input_folder_var = tk.StringVar(value=input_folder_default)
output_folder_var = tk.StringVar(value=output_folder_default)
offset_x_var = tk.StringVar(value="0.0")
offset_y_var = tk.StringVar(value="-15.0")
face_percent_var = tk.StringVar(value="40.0")
resize_var = tk.StringVar(value="512")
threshold_var = tk.StringVar(value="0.5")
output_format_var = tk.StringVar(value="jpg")

# Input folder
ttk.Label(controls_frame, text="Input folder:").grid(row=0, column=0, sticky="e", padx=(0, 10))
input_folder_entry = ttk.Entry(controls_frame, textvariable=input_folder_var)
input_folder_entry.grid(row=0, column=1)
ttk.Button(controls_frame, text="Browse", command=lambda: load_image_previews(filedialog.askdirectory(), input_preview_frame)).grid(row=0, column=2)

# Output folder
ttk.Label(controls_frame, text="Output folder:").grid(row=1, column=0, sticky="e", padx=(0, 10))
output_folder_entry = ttk.Entry(controls_frame, textvariable=output_folder_var)
output_folder_entry.grid(row=1, column=1)
ttk.Button(controls_frame, text="Browse", command=lambda: load_image_previews(filedialog.askdirectory(), output_preview_frame)).grid(row=1, column=2)

# Additional parameters
params = [
    ("Offset X:", offset_x_var),
    ("Offset Y:", offset_y_var),
    ("Face Percent:", face_percent_var),
    ("Resize:", resize_var),
    ("Threshold:", threshold_var),
    ("Output Format:", output_format_var),
]

for i, (text, var) in enumerate(params):
    ttk.Label(controls_frame, text=text).grid(row=i + 2, column=0, sticky="e", padx=(0, 10))
    ttk.Entry(controls_frame, textvariable=var).grid(row=i + 2, column=1)

# Start processing button
ttk.Button(controls_frame, text="Start Processing", command=start_processing_and_show_output).grid(row=8, column=1)

# Image previews
preview_container = ttk.Frame(main_frame)
preview_container.grid(row=0, column=1, pady=10)

input_preview_frame = ttk.Frame(preview_container, relief="groove", borderwidth=2)
input_preview_frame.grid(row=0, column=0, padx=(0, 10))
ttk.Label(input_preview_frame, text="Input Image Previews").grid(row=0, columnspan=6)
load_image_previews(input_folder_var.get(), input_preview_frame)

output_preview_frame = ttk.Frame(preview_container, relief="groove", borderwidth=2)
output_preview_frame.grid(row=0, column=1)
ttk.Label(output_preview_frame, text="Output Image Previews").grid(row=0, columnspan=6)

root.mainloop()

