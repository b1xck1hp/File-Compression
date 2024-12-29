from huffman import *

import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from functools import partial
from tkinterdnd2 import DND_FILES, TkinterDnD

def compress_file_GUI(input_path, output_path):
    """Compress a file with GUI feedback."""
    try:
        if os.path.exists(output_path):
            if not messagebox.askyesno("File Exists", "Output file already exists. Overwrite?"):
                return
        
        print(f"Compressing: {input_path} -> {output_path}")
        compress_file(input_path, output_path)
        messagebox.showinfo("Success", f"File compressed successfully!\nSaved to: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Compression failed: {str(e)}")

def decompress_file_GUI(input_path, output_path):
    """Decompress a file with GUI feedback."""
    try:
        if os.path.exists(output_path):
            if not messagebox.askyesno("File Exists", "Output file already exists. Overwrite?"):
                return
        
        print(f"Decompressing: {input_path} -> {output_path}")
        decompress_file(input_path, output_path)
        messagebox.showinfo("Success", f"File decompressed successfully!\nSaved to: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Decompression failed: {str(e)}")

def browse_file(entry):
    file_path = filedialog.askopenfilename(
        filetypes=[("Supported Files", "*.txt *.bin *.huff"), ("All Files", "*.*")]
    )
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def browse_output_folder(entry):
    """Browse for output location and get filename."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        while True:
            output_file_name = simpledialog.askstring(
                "Output File Name",
                "Enter the output file name (with extension: .huff, .bin, or .txt):"
            )
            if output_file_name and output_file_name.endswith(('.huff', '.bin', '.txt')):
                output_path = os.path.join(folder_path, output_file_name)
                entry.delete(0, tk.END)
                entry.insert(0, output_path)
                break
            else:
                messagebox.showerror("Invalid File Name", "Please provide a valid file name with extension (.huff, .bin, or .txt).")

def run_action(action, input_entry, output_entry):
    input_path = input_entry.get()
    output_path = output_entry.get()

    if not input_path or not output_path:
        messagebox.showerror("Error", "Please specify both input and output paths.")
        return

    if action == "compress":
        compress_file_GUI(input_path, output_path)
    elif action == "decompress":
        decompress_file_GUI(input_path, output_path)

class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
        self.top = None

    def enter(self, event=None):
        x = y = 0
        x += self.widget.winfo_rootx() + 50
        y += self.widget.winfo_rooty() + 20
        self.top = tk.Toplevel(self.widget)
        self.top.overrideredirect(True)
        self.top.geometry("+%d+%d" % (x, y))
        label = tk.Label(self.top, text=self.text, justify=tk.LEFT,
                         relief=tk.SOLID, borderwidth=1,
                         font=("Arial", 9, "normal"))
        label.pack(ipadx=1)

    def close(self, event=None):
        if self.top:
            self.top.destroy()
            self.top = None

def handle_drop(event, input_entry):
    """Handle drag and drop file events"""
    file_path = event.data
    # Clean the file path
    file_path = file_path.strip('{}')
    if file_path.startswith('"') and file_path.endswith('"'):
        file_path = file_path[1:-1]
        
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def create_gui(parent=None):
    """Create and setup the Huffman compression GUI"""
    if parent is None:
        root = TkinterDnD.Tk()
        root.title("Huffman Compression Tool")
    else:
        root = parent

    # Create main frame with padding
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Enable drag and drop for the main frame
    try:
        main_frame.drop_target_register(DND_FILES)
        main_frame.dnd_bind('<<Drop>>', lambda e: handle_drop(e, input_entry))
    except Exception as e:
        print(f"TkinterDnD not initialized. Drag and drop will be disabled. Error: {e}")

    # Title and description
    title_frame = ttk.Frame(main_frame)
    title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 15))
    ttk.Label(title_frame, text="Huffman File Compression", 
              font=("Arial", 12, "bold")).pack()
    ttk.Label(title_frame, text="Compress and decompress files using Huffman coding\nDrag and drop files here", 
              font=("Arial", 9)).pack()

    # Input Section
    ttk.Label(main_frame, text="Input File:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    input_entry = ttk.Entry(main_frame, width=50)
    input_entry.grid(row=1, column=1, padx=10, pady=5)

    # Also enable drag and drop for the entry widget
    try:
        input_entry.drop_target_register(DND_FILES)
        input_entry.dnd_bind('<<Drop>>', lambda e: handle_drop(e, input_entry))
    except Exception as e:
        print(f"Could not enable drag and drop for entry: {e}")

    browse_input_btn = ttk.Button(main_frame, text="...", command=partial(browse_file, input_entry))
    browse_input_btn.grid(row=1, column=2, padx=5, pady=5)

    # Output Section
    ttk.Label(main_frame, text="Output File:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    output_entry = ttk.Entry(main_frame, width=50)
    output_entry.grid(row=2, column=1, padx=10, pady=5)
    browse_output_btn = ttk.Button(main_frame, text="...", command=partial(browse_output_folder, output_entry))
    browse_output_btn.grid(row=2, column=2, padx=5, pady=5)

    # Action Buttons
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=3, column=0, columnspan=3, pady=20)
    
    compress_btn = ttk.Button(button_frame, text="Compress", 
                            command=partial(run_action, "compress", input_entry, output_entry))
    compress_btn.pack(side=tk.LEFT, padx=10)
    
    decompress_btn = ttk.Button(button_frame, text="Decompress", 
                              command=partial(run_action, "decompress", input_entry, output_entry))
    decompress_btn.pack(side=tk.LEFT, padx=10)

    # Supervisor note
    supervisor_frame = ttk.Frame(main_frame)
    supervisor_frame.grid(row=4, column=0, columnspan=3, pady=(20, 5))
    ttk.Label(supervisor_frame, text="Project Supervised by: Eng Taghreed Salem",
             font=("Arial", 9, "italic")).pack(anchor="center")

    # Add tooltips
    CreateToolTip(compress_btn, "Compress a file using Huffman coding")
    CreateToolTip(decompress_btn, "Decompress a previously compressed file")
    CreateToolTip(browse_input_btn, "Select input file")
    CreateToolTip(browse_output_btn, "Choose output location and filename")

    if parent is None:
        root.mainloop()
    
    return main_frame

if __name__ == "__main__":
    create_gui()
