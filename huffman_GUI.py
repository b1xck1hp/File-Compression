from huffman import *

import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from functools import partial
from tkinterdnd2 import DND_FILES, TkinterDnD
import customtkinter

def calculate_compression_ratio(original_size, compressed_size):
    """Calculate the compression percentage"""
    ratio = ((original_size - compressed_size) / original_size) * 100
    return ratio

class CustomDialog(customtkinter.CTkToplevel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title(title)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        # Center the dialog
        self.geometry("400x250")
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (250 // 2)
        self.geometry(f"+{x}+{y}")
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        # Title
        self.title_label = customtkinter.CTkLabel(
            self,
            text="Enter Output Filename",
            font=customtkinter.CTkFont(size=16, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Filename frame
        self.filename_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.filename_frame.grid(row=1, column=0, sticky="ew", padx=20)
        self.filename_frame.grid_columnconfigure(0, weight=1)
        
        # Entry for filename
        self.entry = customtkinter.CTkEntry(self.filename_frame, placeholder_text="Enter filename without extension")
        self.entry.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Extension selection
        self.extension_label = customtkinter.CTkLabel(
            self,
            text="Select File Extension:",
            font=customtkinter.CTkFont(size=12)
        )
        self.extension_label.grid(row=2, column=0, padx=20, pady=(0, 5), sticky="w")
        
        # Extension options
        self.extensions = ['.txt', '.bin', '.huff']
        self.extension_var = customtkinter.StringVar(value=self.extensions[0])
        self.extension_menu = customtkinter.CTkOptionMenu(
            self,
            values=self.extensions,
            variable=self.extension_var,
            width=200
        )
        self.extension_menu.grid(row=2, column=0, padx=20, pady=(0, 20))
        
        # Buttons frame
        self.button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=3, column=0, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Buttons
        self.ok_button = customtkinter.CTkButton(
            self.button_frame,
            text="OK",
            command=self.ok_click,
            width=100
        )
        self.ok_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.cancel_button = customtkinter.CTkButton(
            self.button_frame,
            text="Cancel",
            command=self.cancel_click,
            width=100
        )
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.result = None
        self.entry.focus_set()
        self.bind("<Return>", lambda e: self.ok_click())
        self.bind("<Escape>", lambda e: self.cancel_click())
        
    def ok_click(self):
        filename = self.entry.get()
        if not filename:
            messagebox.showerror("Error", "Please enter a filename")
            return
        self.result = filename + self.extension_var.get()
        self.destroy()
        
    def cancel_click(self):
        self.destroy()

def get_output_filename(parent):
    dialog = CustomDialog(parent, "Output Filename")
    dialog.wait_window()
    return dialog.result

def compress_file_GUI(input_path, output_path):
    """Compress a file with GUI feedback."""
    try:
        if os.path.exists(output_path):
            if not messagebox.askyesno("File Exists", "Output file already exists. Overwrite?"):
                return
        
        original_size = os.path.getsize(input_path)
        print(f"Compressing: {input_path} -> {output_path}")
        compress_file(input_path, output_path)
        compressed_size = os.path.getsize(output_path)
        
        compression_ratio = calculate_compression_ratio(original_size, compressed_size)
        update_text_area(
            f"File compressed successfully!\n"
            f"Original size: {original_size:,} bytes\n"
            f"Compressed size: {compressed_size:,} bytes\n"
            f"Compression ratio: {compression_ratio:.2f}%\n"
            f"Saved to: {output_path}"
        )
    except Exception as e:
        update_text_area(f"Compression failed: {str(e)}")

def decompress_file_GUI(input_path, output_path):
    """Decompress a file with GUI feedback."""
    try:
        if os.path.exists(output_path):
            if not messagebox.askyesno("File Exists", "Output file already exists. Overwrite?"):
                return
        
        print(f"Decompressing: {input_path} -> {output_path}")
        decompress_file(input_path, output_path)
        update_text_area(f"File decompressed successfully!\nSaved to: {output_path}")
    except Exception as e:
        update_text_area(f"Decompression failed: {str(e)}")

def browse_file(entry):
    file_path = filedialog.askopenfilename(
        filetypes=[("Supported Files", "*.txt *.bin *.huff"), ("All Files", "*.*")]
    )
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def browse_output_folder(entry, parent):
    """Browse for output location and get filename."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_file_name = get_output_filename(parent)
        if output_file_name:
            full_path = os.path.join(folder_path, output_file_name)
            entry.delete(0, tk.END)
            entry.insert(0, full_path)

def run_action(action, input_entry, output_entry, parent):
    input_path = input_entry.get()
    output_path = output_entry.get()
    
    if not input_path or not output_path:
        messagebox.showerror("Error", "Please specify both input and output paths")
        return
        
    if action == "compress":
        compress_file_GUI(input_path, output_path)
    else:
        decompress_file_GUI(input_path, output_path)

def handle_drop(event, input_entry):
    """Handle drag and drop file events"""
    try:
        # Strip curly braces and quotes that Windows adds
        file_path = event.data.strip("{}")
        if file_path.startswith('"') and file_path.endswith('"'):
            file_path = file_path[1:-1]
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)
    except Exception as e:
        print(f"Error handling drop: {e}")

def update_text_area(message):
    """Update the text area with a message"""
    text_area.configure(state='normal')
    text_area.insert('end', message + '\n' + "-"*50 + '\n')
    text_area.see('end')  # Scroll to the bottom
    text_area.configure(state='disabled')

def create_gui(parent=None):
    """Create and setup the Huffman compression GUI"""
    if parent is None:
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        root = TkinterDnD.Tk()
        root.title("Huffman Compression Tool")
        root._configure_window_background()
    else:
        root = parent

    # Create main frame with padding
    main_frame = customtkinter.CTkFrame(root)
    main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    # Configure the window
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    # Configure grid weights for main_frame
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=3)
    main_frame.grid_columnconfigure(2, weight=1)
    for i in range(7):
        main_frame.grid_rowconfigure(i, weight=1)
    
    # Title and description
    title_label = customtkinter.CTkLabel(
        main_frame, 
        text="Huffman File Compression",
        font=customtkinter.CTkFont(size=24, weight="bold")
    )
    title_label.grid(row=0, column=0, columnspan=3, pady=(0, 5), sticky="ew")
    
    desc_label = customtkinter.CTkLabel(
        main_frame,
        text="Compress and decompress files using Huffman coding\nDrag and drop files here",
        font=customtkinter.CTkFont(size=14)
    )
    desc_label.grid(row=1, column=0, columnspan=3, pady=(0, 20), sticky="ew")

    # Input Section
    input_frame = customtkinter.CTkFrame(main_frame)
    input_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 10))
    input_frame.grid_columnconfigure(1, weight=1)  # Make entry expand
    
    customtkinter.CTkLabel(input_frame, text="Input File:").grid(row=0, column=0, padx=10, pady=5)
    input_entry = customtkinter.CTkEntry(input_frame)
    input_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    browse_input_btn = customtkinter.CTkButton(
        input_frame, 
        text="Browse",
        command=partial(browse_file, input_entry),
        width=100
    )
    browse_input_btn.grid(row=0, column=2, padx=10, pady=5)

    # Output Section
    output_frame = customtkinter.CTkFrame(main_frame)
    output_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 20))
    output_frame.grid_columnconfigure(1, weight=1)  # Make entry expand
    
    customtkinter.CTkLabel(output_frame, text="Output File:").grid(row=0, column=0, padx=10, pady=5)
    output_entry = customtkinter.CTkEntry(output_frame)
    output_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    browse_output_btn = customtkinter.CTkButton(
        output_frame,
        text="Browse",
        command=partial(browse_output_folder, output_entry, root),
        width=100
    )
    browse_output_btn.grid(row=0, column=2, padx=10, pady=5)

    # Action Buttons
    button_frame = customtkinter.CTkFrame(main_frame)
    button_frame.grid(row=4, column=0, columnspan=3, pady=(0, 20), sticky="ew")
    button_frame.grid_columnconfigure((0, 1), weight=1)  # Equal width for buttons
    
    compress_btn = customtkinter.CTkButton(
        button_frame,
        text="Compress",
        command=partial(run_action, "compress", input_entry, output_entry, root),
        width=150
    )
    compress_btn.grid(row=0, column=0, padx=10, sticky="ew")
    
    decompress_btn = customtkinter.CTkButton(
        button_frame,
        text="Decompress",
        command=partial(run_action, "decompress", input_entry, output_entry, root),
        width=150
    )
    decompress_btn.grid(row=0, column=1, padx=10, sticky="ew")

    # Text Area for logging
    global text_area
    text_area = customtkinter.CTkTextbox(main_frame)
    text_area.grid(row=5, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="nsew")
    text_area.configure(state='disabled')

    # Enable drag and drop
    try:
        input_entry.drop_target_register(DND_FILES)
        input_entry.dnd_bind('<<Drop>>', lambda e: handle_drop(e, input_entry))
    except Exception as e:
        print(f"TkinterDnD not initialized. Drag and drop will be disabled. Error: {e}")

    if parent is None:
        # Set minimum window size
        root.minsize(500, 600)
        
        # Center the window on the screen
        root.update_idletasks()
        width = 600
        height = 700
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        root.mainloop()
    
    return main_frame

if __name__ == "__main__":
    create_gui()
