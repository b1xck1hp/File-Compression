import tkinter as tk
from tkinter import ttk
from huffman_GUI import create_gui as create_huffman_gui
from png_compressor_gui import ImageCompressorGUI
from tkinterdnd2 import DND_FILES, TkinterDnD

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("File Compression Suite")
        
        # Enable drag and drop for root window
        try:
            self.root.drop_target_register(DND_FILES)
        except Exception as e:
            print(f"Could not enable drag and drop for root window: {e}")
        
        # Center window on screen
        window_width = 1000
        window_height = 700
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Create Huffman compression tab
        self.huffman_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.huffman_frame, text='Text Compression (Huffman)')
        
        # Create PNG compression tab
        self.png_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.png_frame, text='Image Compression (PNG)')

        # Initialize Huffman GUI in its tab
        create_huffman_gui(self.huffman_frame)
        
        # Initialize PNG Compressor GUI in its tab
        self.png_app = ImageCompressorGUI(self.png_frame)

        # Add About section
        self.create_about_frame()

    def create_about_frame(self):
        about_frame = ttk.Frame(self.notebook)
        self.notebook.add(about_frame, text='About')

        # Add some padding
        about_frame.grid_columnconfigure(0, weight=1)
        about_frame.grid_rowconfigure(0, weight=1)

        # Create a frame for the content
        content_frame = ttk.Frame(about_frame, padding=20)
        content_frame.grid(row=0, column=0)

        # Title
        title_label = ttk.Label(content_frame, 
                              text="File Compression Suite", 
                              font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(0, 20))

        # Description
        description = """This application provides two different compression methods:

1. Text Compression (Huffman):
   - Compresses text files using Huffman coding
   - Optimal for text-based files
   - Lossless compression
   - Files are saved with .huff extension

2. Image Compression (PNG):
   - Converts PNG images to compressed JPEG
   - Adjustable compression quality
   - Lossy compression
   - Supports preview functionality
   - Maintains aspect ratio

Choose the appropriate tab based on your compression needs."""

        desc_label = ttk.Label(content_frame, 
                             text=description,
                             wraplength=500,
                             justify='left')
        desc_label.pack(pady=10)

        # Project Team
        ttk.Label(content_frame,
                 text="Project Team",
                 font=('Helvetica', 12, 'bold')).pack(pady=(20, 10))
        
        team_members = """• Mohamed Saied
• Belal Mahmoud
• Mobark Yehia
• Amr Magdy"""
        
        team_label = ttk.Label(content_frame,
                             text=team_members,
                             justify='left',
                             font=('Helvetica', 10))
        team_label.pack()

        # Supervisor
        ttk.Label(content_frame,
                 text="Project Supervisor",
                 font=('Helvetica', 12, 'bold')).pack(pady=(20, 10))
        
        supervisor_label = ttk.Label(content_frame,
                                   text="Eng Taghreed Salem",
                                   font=('Helvetica', 10, 'italic'))
        supervisor_label.pack()

        # Version info
        version_label = ttk.Label(content_frame,
                                text="Version 1.0.0",
                                font=('Helvetica', 10))
        version_label.pack(pady=(20, 0))

def main():
    root = TkinterDnD.Tk()
    app = MainApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()
