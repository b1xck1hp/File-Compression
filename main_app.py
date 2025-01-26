import tkinter as tk
import customtkinter
import webbrowser
from huffman_GUI import create_gui as create_huffman_gui
from png_compressor_gui import ImageCompressorGUI
from tkinterdnd2 import DND_FILES, TkinterDnD

class HyperlinkLabel(customtkinter.CTkLabel):
    def __init__(self, *args, **kwargs):
        self.link = kwargs.pop("link", "")
        super().__init__(*args, **kwargs)
        self.configure(cursor="hand2", text_color="#4D9FFF")
        self.bind("<Button-1>", self._open_link)
        self.bind("<Enter>", lambda e: self.configure(text_color="#89C4FF"))
        self.bind("<Leave>", lambda e: self.configure(text_color="#4D9FFF"))

    def _open_link(self, event):
        webbrowser.open_new_tab(self.link)

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("File Compression Suite")
        
        # Set appearance mode and theme
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        
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
        
        # Configure root window
        self.root.configure(bg="#2b2b2b")
        
        # Create main frame
        self.main_frame = customtkinter.CTkFrame(root)
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Create notebook for tabs
        self.notebook = customtkinter.CTkTabview(self.main_frame)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        self.huffman_tab = self.notebook.add("Text Compression")
        self.png_tab = self.notebook.add("Image Compression")
        self.about_tab = self.notebook.add("About")

        # Initialize Huffman GUI in its tab
        create_huffman_gui(self.huffman_tab)
        
        # Initialize PNG Compressor GUI in its tab
        self.png_app = ImageCompressorGUI(self.png_tab)

        # Add About section
        self.create_about_frame()

    def create_about_frame(self):
        # Create a frame for the content
        content_frame = customtkinter.CTkFrame(self.about_tab)
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        title_label = customtkinter.CTkLabel(
            content_frame, 
            text="File Compression Suite",
            font=customtkinter.CTkFont(size=24, weight="bold")
        )
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

        desc_label = customtkinter.CTkLabel(
            content_frame, 
            text=description,
            font=customtkinter.CTkFont(size=14),
            wraplength=500,
            justify='left'
        )
        desc_label.pack(pady=10)

        # Project Team
        team_title = customtkinter.CTkLabel(
            content_frame,
            text="Project Team",
            font=customtkinter.CTkFont(size=18, weight="bold")
        )
        team_title.pack(pady=(20, 10))
        
        # Team members with hyperlinks
        team_members = [
            ("Mohamed Saied", "https://www.linkedin.com/in/mohammedsaieedd/"),
            ("Amr Magdy", "https://www.linkedin.com/in/amr-magdy-7b1b1a1b5/"),
            ("Belal Mohamed", "https://www.linkedin.com/")
        ]
        
        team_frame = customtkinter.CTkFrame(content_frame, fg_color="transparent")
        team_frame.pack(pady=10)
        
        for name, link in team_members:
            member_label = HyperlinkLabel(
                team_frame,
                text=f"• {name}",
                font=customtkinter.CTkFont(size=14),
                link=link
            )
            member_label.pack(pady=2)

        # Version info
        version_label = customtkinter.CTkLabel(
            content_frame,
            text="Version 1.0.0",
            font=customtkinter.CTkFont(size=12)
        )
        version_label.pack(pady=(20, 0))

def main():
    root = TkinterDnD.Tk()
    app = MainApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()
