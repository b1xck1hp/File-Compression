import tkinter as tk
import customtkinter
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from tkinterdnd2 import DND_FILES, TkinterDnD

class ImageCompressorGUI:
    def __init__(self, root):
        self.root = root
        
        # Enable drag and drop
        try:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.handle_drop)
        except:
            print("TkinterDnD not initialized. Drag and drop will be disabled.")
        
        # Create main frame
        self.main_frame = customtkinter.CTkFrame(root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title and description
        self.title_label = customtkinter.CTkLabel(
            self.main_frame,
            text="PNG Image Compressor",
            font=customtkinter.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(0, 5))
        
        self.desc_label = customtkinter.CTkLabel(
            self.main_frame,
            text="Compress and decompress PNG images with quality control",
            font=customtkinter.CTkFont(size=14)
        )
        self.desc_label.pack(pady=(0, 20))

        # Create horizontal layout
        self.content_frame = customtkinter.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True)
        
        # Left panel for controls
        self.control_frame = customtkinter.CTkFrame(self.content_frame)
        self.control_frame.pack(side="left", fill="both", padx=(0, 10), pady=10)

        # Right panel for preview
        self.preview_frame = customtkinter.CTkFrame(self.content_frame)
        self.preview_frame.pack(side="right", fill="both", expand=True, pady=10)
        
        self.preview_label = customtkinter.CTkLabel(
            self.preview_frame,
            text="No image selected",
            font=customtkinter.CTkFont(size=14)
        )
        self.preview_label.pack(expand=True)

        # Mode selection
        self.mode_frame = customtkinter.CTkFrame(self.control_frame)
        self.mode_frame.pack(fill="x", padx=10, pady=10)
        
        self.mode_label = customtkinter.CTkLabel(
            self.mode_frame,
            text="Mode:",
            font=customtkinter.CTkFont(size=14, weight="bold")
        )
        self.mode_label.pack(pady=(0, 5))
        
        self.mode_var = customtkinter.StringVar(value="compress")
        self.compress_radio = customtkinter.CTkRadioButton(
            self.mode_frame,
            text="Compress",
            variable=self.mode_var,
            value="compress",
            command=self.update_mode
        )
        self.compress_radio.pack(side="left", padx=10)
        
        self.decompress_radio = customtkinter.CTkRadioButton(
            self.mode_frame,
            text="Decompress",
            variable=self.mode_var,
            value="decompress",
            command=self.update_mode
        )
        self.decompress_radio.pack(side="left", padx=10)

        # Input file
        self.input_frame = customtkinter.CTkFrame(self.control_frame)
        self.input_frame.pack(fill="x", padx=10, pady=10)
        
        self.input_label = customtkinter.CTkLabel(
            self.input_frame,
            text="Input Image:",
            font=customtkinter.CTkFont(size=14, weight="bold")
        )
        self.input_label.pack(pady=(0, 5))
        
        self.input_path = tk.StringVar()
        self.input_entry = customtkinter.CTkEntry(
            self.input_frame,
            textvariable=self.input_path,
            width=300
        )
        self.input_entry.pack(side="left", padx=5)
        
        self.browse_btn = customtkinter.CTkButton(
            self.input_frame,
            text="Browse",
            command=self.browse_input,
            width=100
        )
        self.browse_btn.pack(side="left", padx=5)

        # Output file
        self.output_frame = customtkinter.CTkFrame(self.control_frame)
        self.output_frame.pack(fill="x", padx=10, pady=10)
        
        self.output_label = customtkinter.CTkLabel(
            self.output_frame,
            text="Output Image:",
            font=customtkinter.CTkFont(size=14, weight="bold")
        )
        self.output_label.pack(pady=(0, 5))
        
        self.output_path = tk.StringVar()
        self.output_entry = customtkinter.CTkEntry(
            self.output_frame,
            textvariable=self.output_path,
            width=300
        )
        self.output_entry.pack(side="left", padx=5)
        
        self.save_btn = customtkinter.CTkButton(
            self.output_frame,
            text="Save As",
            command=self.browse_output,
            width=100
        )
        self.save_btn.pack(side="left", padx=5)

        # Quality slider
        self.quality_frame = customtkinter.CTkFrame(self.control_frame)
        self.quality_frame.pack(fill="x", padx=10, pady=10)
        
        self.quality_label = customtkinter.CTkLabel(
            self.quality_frame,
            text="Compression Quality:",
            font=customtkinter.CTkFont(size=14, weight="bold")
        )
        self.quality_label.pack(pady=(0, 5))
        
        self.quality_var = tk.IntVar(value=85)
        self.quality_slider = customtkinter.CTkSlider(
            self.quality_frame,
            from_=0,
            to=100,
            variable=self.quality_var,
            command=self.update_quality_label
        )
        self.quality_slider.pack(fill="x", padx=5)
        
        self.quality_value_label = customtkinter.CTkLabel(
            self.quality_frame,
            text="85%",
            font=customtkinter.CTkFont(size=12)
        )
        self.quality_value_label.pack()

        # Compress button
        self.compress_btn = customtkinter.CTkButton(
            self.control_frame,
            text="Compress Image",
            command=self.compress_image,
            font=customtkinter.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.compress_btn.pack(pady=20)

        # Status
        self.status_var = tk.StringVar()
        self.status_label = customtkinter.CTkLabel(
            self.control_frame,
            textvariable=self.status_var,
            wraplength=400,
            font=customtkinter.CTkFont(size=12)
        )
        self.status_label.pack(pady=10)

    def update_quality_label(self, value):
        self.quality_value_label.configure(text=f"{int(float(value))}%")

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
            
        if not image_path:
            self.preview_label.configure(image=None, text="No image selected")
            return
            
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
            self.preview_label.configure(image=photo, text="")
            self.preview_label.image = photo  # Keep a reference
        except Exception as e:
            self.preview_label.configure(image=None, text=f"Error loading preview: {str(e)}")

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
            self.quality_frame.pack(fill="x", padx=10, pady=10)
        else:
            self.compress_btn.configure(text="Decompress Image")
            self.quality_frame.pack_forget()
        
        # Clear paths
        self.input_path.set("")
        self.output_path.set("")
        self.preview_label.configure(image=None, text="No image selected")

    def handle_drop(self, event):
        file_path = event.data.strip("{}")
        if file_path.startswith('"') and file_path.endswith('"'):
            file_path = file_path[1:-1]
        
        # Check if the dropped file matches the current mode
        if self.mode_var.get() == "compress" and file_path.lower().endswith('.png'):
            self.input_path.set(file_path)
            self.update_preview(file_path)
            base_name = os.path.splitext(file_path)[0]
            self.output_path.set(base_name + "_compressed.jpg")
        elif self.mode_var.get() == "decompress" and file_path.lower().endswith(('.jpg', '.jpeg')):
            self.input_path.set(file_path)
            self.update_preview(file_path)
            base_name = os.path.splitext(file_path)[0]
            self.output_path.set(base_name + "_decompressed.png")
        else:
            messagebox.showerror("Invalid File", 
                               "Please drop a PNG file for compression or a JPEG file for decompression")

    def compress_image(self):
        input_path = self.input_path.get()
        output_path = self.output_path.get()
        
        if not input_path or not output_path:
            messagebox.showerror("Error", "Please select input and output files")
            return
            
        try:
            if self.mode_var.get() == "compress":
                # Open the PNG image
                with Image.open(input_path) as img:
                    # Convert to RGB if necessary
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    # Save as JPEG with specified quality
                    img.save(output_path, 'JPEG', quality=self.quality_var.get())
                self.status_var.set(f"Image compressed successfully!\nSaved to: {output_path}")
                # Update preview with compressed image
                self.update_preview(output_path)
            else:
                # Open the JPEG image
                with Image.open(input_path) as img:
                    # Save as PNG
                    img.save(output_path, 'PNG')
                self.status_var.set(f"Image decompressed successfully!\nSaved to: {output_path}")
                # Update preview with decompressed image
                self.update_preview(output_path)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error processing image: {str(e)}")
            self.status_var.set("Error processing image")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
    app = ImageCompressorGUI(root)
    root.mainloop()
