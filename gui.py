import tkinter as tk
from tkinter import filedialog
from app import main

def browse_input_folder():
    input_folder = filedialog.askdirectory()
    input_folder_var.set(input_folder)

def browse_output_folder():
    output_folder = filedialog.askdirectory()
    output_folder_var.set(output_folder)

def start_processing():
    main(input_folder_var.get(),
         output_folder_var.get(),
         float(offset_x_var.get()),
         float(offset_y_var.get()),
         float(face_percent_var.get()),
         int(resize_var.get()),
         float(threshold_var.get()),
         output_format_var.get())

root = tk.Tk()
root.title("Face Detection and Cropping")

input_folder_var = tk.StringVar()
output_folder_var = tk.StringVar()
offset_x_var = tk.StringVar(value="0.0")
offset_y_var = tk.StringVar(value="-15.0")
face_percent_var = tk.StringVar(value="40.0")
resize_var = tk.StringVar(value="512")
threshold_var = tk.StringVar(value="0.5")
output_format_var = tk.StringVar(value="jpg")

tk.Label(root, text="Input folder:").grid(row=0, column=0, sticky="e")
tk.Entry(root, textvariable=input_folder_var).grid(row=0, column=1)
tk.Button(root, text="Browse", command=browse_input_folder).grid(row=0, column=2)

tk.Label(root, text="Output folder:").grid(row=1, column=0, sticky="e")
tk.Entry(root, textvariable=output_folder_var).grid(row=1, column=1)
tk.Button(root, text="Browse", command=browse_output_folder).grid(row=1, column=2)

tk.Label(root, text="Offset X:").grid(row=2, column=0, sticky="e")
tk.Entry(root, textvariable=offset_x_var).grid(row=2, column=1)

tk.Label(root, text="Offset Y:").grid(row=3, column=0, sticky="e")
tk.Entry(root, textvariable=offset_y_var).grid(row=3, column=1)

tk.Label(root, text="Face Percent:").grid(row=4, column=0, sticky="e")
tk.Entry(root, textvariable=face_percent_var).grid(row=4, column=1)

tk.Label(root, text="Resize:").grid(row=5, column=0, sticky="e")
tk.Entry(root, textvariable=resize_var).grid(row=5, column=1)

tk.Label(root, text="Threshold:").grid(row=6, column=0, sticky="e")
tk.Entry(root, textvariable=threshold_var).grid(row=6, column=1)

tk.Label(root, text="Output Format:").grid(row=7, column=0, sticky="e")
tk.Entry(root, textvariable=output_format_var).grid(row=7, column=1)

tk.Button(root, text="Start Processing", command=start_processing).grid(row=8, column=1)

root.mainloop()
