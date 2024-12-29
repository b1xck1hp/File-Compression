import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import os
from tkinterdnd2 import DND_FILES, TkinterDnD

class CreateToolTip:
    """Create a tooltip for a given widget"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = ttk.Label(self.tooltip, text=self.text, background="#ffffe0", 
                         relief="solid", borderwidth=1)
        label.pack()

    def leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class ImageCompressorGUI:
    def __init__(self, root):
        self.root = root
        
        # Enable drag and drop
        try:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.handle_drop)
        except:
            print("TkinterDnD not initialized. Drag and drop will be disabled.")
        
        # Set title only if root is a Tk window
        if isinstance(self.root, tk.Tk):
            self.root.title("PNG Image Compressor")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill="both", expand=True)

        # Title and description
        self.title_frame = ttk.Frame(self.main_frame)
        self.title_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(self.title_frame, text="PNG Image Compressor", 
                 font=("Arial", 12, "bold")).pack()
        ttk.Label(self.title_frame, text="Compress and decompress PNG images with quality control", 
                 font=("Arial", 9)).pack()

        # Left panel for controls
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(side="left", fill="y", padx=(0, 10))

        # Right panel for preview
        self.preview_frame = ttk.LabelFrame(self.main_frame, text="Preview", padding=10)
        self.preview_frame.pack(side="right", fill="both", expand=True)
        
        self.preview_label = ttk.Label(self.preview_frame, text="No image selected")
        self.preview_label.pack(expand=True)

        # Mode selection
        self.mode_frame = ttk.LabelFrame(self.control_frame, text="Mode", padding=10)
        self.mode_frame.pack(fill="x", padx=5, pady=5)
        
        self.mode_var = tk.StringVar(value="compress")
        self.compress_radio = ttk.Radiobutton(self.mode_frame, text="Compress", 
                                            variable=self.mode_var, value="compress",
                                            command=self.update_mode)
        self.compress_radio.pack(side="left", padx=5)
        
        tooltip_compress = CreateToolTip(self.compress_radio, "Convert PNG to compressed JPEG")
        
        self.decompress_radio = ttk.Radiobutton(self.mode_frame, text="Decompress", 
                                              variable=self.mode_var, value="decompress",
                                              command=self.update_mode)
        self.decompress_radio.pack(side="left", padx=5)
        
        tooltip_decompress = CreateToolTip(self.decompress_radio, "Convert JPEG back to PNG")

        # Input file
        self.input_frame = ttk.LabelFrame(self.control_frame, text="Input Image", padding=10)
        self.input_frame.pack(fill="x", padx=5, pady=5)
        
        self.input_path = tk.StringVar()
        self.input_entry = ttk.Entry(self.input_frame, textvariable=self.input_path, width=50)
        self.input_entry.pack(side="left", padx=5)
        
        self.browse_btn = ttk.Button(self.input_frame, text="Browse", command=self.browse_input)
        self.browse_btn.pack(side="left", padx=5)

        # Output file
        self.output_frame = ttk.LabelFrame(self.control_frame, text="Output Image", padding=10)
        self.output_frame.pack(fill="x", padx=5, pady=5)
        
        self.output_path = tk.StringVar()
        self.output_entry = ttk.Entry(self.output_frame, textvariable=self.output_path, width=50)
        self.output_entry.pack(side="left", padx=5)
        
        self.save_btn = ttk.Button(self.output_frame, text="Save As", command=self.browse_output)
        self.save_btn.pack(side="left", padx=5)

        # Quality slider
        self.quality_frame = ttk.LabelFrame(self.control_frame, text="Compression Quality", padding=10)
        self.quality_frame.pack(fill="x", padx=5, pady=5)
        
        self.quality_var = tk.IntVar(value=85)
        self.quality_slider = ttk.Scale(self.quality_frame, from_=0, to=100, 
                                      orient="horizontal", variable=self.quality_var)
        self.quality_slider.pack(fill="x", padx=5)
        
        self.quality_label = ttk.Label(self.quality_frame, text="85%")
        self.quality_label.pack()
        self.quality_slider.configure(command=self.update_quality_label)

        # Supervisor note
        self.supervisor_frame = ttk.Frame(self.control_frame)
        self.supervisor_frame.pack(fill="x", padx=5, pady=(20, 5))
        self.supervisor_label = ttk.Label(self.supervisor_frame, 
                                        text="Project Supervised by: Eng Taghreed Salem",
                                        font=("Arial", 9, "italic"))
        self.supervisor_label.pack(anchor="center")

        # Progress bar
        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(self.control_frame, variable=self.progress_var, length=200)
        self.progress_bar.pack_forget()

        # Compress button
        self.compress_btn = ttk.Button(self.control_frame, text="Compress Image", command=self.compress_image)
        self.compress_btn.pack(pady=20)

        # Status
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(self.control_frame, textvariable=self.status_var, wraplength=400)
        self.status_label.pack(pady=10)

    def update_quality_label(self, value):
        self.quality_label.configure(text=f"{int(float(value))}%")

    def browse_input(self):
        if self.mode_var.get() == "compress":
            filetypes = [("PNG files", "*.png"), ("All files", "*.*")]
        else:
            filetypes = [("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")]
            
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.input_path.set(filename)
            self.update_preview(filename)
            # Auto-set output filename
            base_name = os.path.splitext(filename)[0]
            if self.mode_var.get() == "compress":
                output_name = base_name + "_compressed.jpg"
            else:
                output_name = base_name + "_decompressed.png"
            self.output_path.set(output_name)

    def update_preview(self, image_path=None):
        """Update the preview panel with the selected image"""
        if image_path is None:
            image_path = self.input_path.get()
        try:
            # Open and resize image for preview
            image = Image.open(image_path)
            # Calculate aspect ratio
            aspect_ratio = image.width / image.height
            preview_width = 300
            preview_height = int(preview_width / aspect_ratio)
            
            # Resize image maintaining aspect ratio
            image = image.resize((preview_width, preview_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Update preview label
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo  # Keep a reference
        except Exception as e:
            self.preview_label.configure(text="Error loading preview")

    def browse_output(self):
        if self.mode_var.get() == "compress":
            defaultext = ".jpg"
            filetypes = [("JPEG files", "*.jpg"), ("All files", "*.*")]
        else:
            defaultext = ".png"
            filetypes = [("PNG files", "*.png"), ("All files", "*.*")]
            
        filename = filedialog.asksaveasfilename(
            defaultextension=defaultext,
            filetypes=filetypes)
        if filename:
            self.output_path.set(filename)

    def update_mode(self):
        mode = self.mode_var.get()
        if mode == "compress":
            self.compress_btn.configure(text="Compress Image")
            self.quality_frame.pack(fill="x", padx=5, pady=5)
        else:
            self.compress_btn.configure(text="Decompress Image")
            self.quality_frame.pack_forget()
        
        # Clear the paths when switching modes
        self.input_path.set("")
        self.output_path.set("")
        self.status_var.set("")
        self.preview_label.configure(text="No image selected")

    def handle_drop(self, event):
        """Handle drag and drop file events"""
        file_path = event.data
        # Clean the file path (remove curly braces and extra quotes if present)
        file_path = file_path.strip('{}')
        if file_path.startswith('"') and file_path.endswith('"'):
            file_path = file_path[1:-1]
            
        # Check if it's a valid image file
        if self.mode_var.get() == "compress" and not file_path.lower().endswith(('.png')):
            messagebox.showerror("Error", "Please drop a PNG file for compression")
            return
        elif self.mode_var.get() == "decompress" and not file_path.lower().endswith(('.jpg', '.jpeg')):
            messagebox.showerror("Error", "Please drop a JPEG file for decompression")
            return
            
        self.input_path.set(file_path)
        self.update_preview()

    def compress_image(self):
        input_path = self.input_path.get()
        output_path = self.output_path.get()
        mode = self.mode_var.get()

        if not input_path or not output_path:
            self.status_var.set("Please select input and output files.")
            return

        if os.path.exists(output_path):
            if not messagebox.askyesno("File Exists", "Output file already exists. Overwrite?"):
                return

        try:
            # Configure progress bar
            self.progress_var.set(0)
            self.progress_bar.pack(fill="x", padx=5, pady=5)
            self.root.update()

            # Open the image
            img = Image.open(input_path)
            
            if mode == "compress":
                quality = self.quality_var.get()
                # Convert PNG to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                    
                # Save with compression
                img.save(output_path, 'JPEG', quality=quality, optimize=True)
            else:
                # For decompression, just save as PNG
                img.save(output_path, 'PNG')
            
            # Calculate size results
            original_size = os.path.getsize(input_path)
            new_size = os.path.getsize(output_path)
            size_ratio = (1 - new_size / original_size) * 100
            
            action = "Compression" if mode == "compress" else "Decompression"
            ratio_text = f"Compression ratio: {size_ratio:.2f}%" if mode == "compress" else f"Size change: {-size_ratio:.2f}%"
            
            self.status_var.set(
                f"{action} successful!\n"
                f"Original size: {original_size/1024:.2f} KB\n"
                f"New size: {new_size/1024:.2f} KB\n"
                f"{ratio_text}"
            )
            
            # Update preview with the new image
            self.update_preview(output_path)
            
        except Exception as e:
            self.status_var.set(f"Error during {mode}: {str(e)}")
        finally:
            self.progress_bar.pack_forget()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageCompressorGUI(root)
    root.mainloop()
