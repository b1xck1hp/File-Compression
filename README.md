# File Compression

A Python-based file compression application featuring multiple compression algorithms and a modern GUI interface. This project implements both Huffman coding for text compression and specialized PNG image compression techniques.

## Features

- Text file compression using Huffman coding algorithm
- PNG image compression with customizable quality settings
- Modern and intuitive GUI using CustomTkinter
- Real-time compression statistics
- Support for multiple file formats

## Team Members

- Mohamed Saied
- Amr Magdy
- Belel Mohamed

## Requirements

- Python 3.x
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/b1xck1hp/File-Compression.git
```

2. Navigate to the project directory:
```bash
cd File-Compression
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main application:
```bash
python main_app.py
```

### For Text Compression:
1. Select "Huffman Compression" from the main menu
2. Choose your input text file
3. Click "Compress" to start the compression process
4. View compression statistics and save the compressed file

### For Image Compression:
1. Select "PNG Compression" from the main menu
2. Load your PNG image
3. Adjust compression settings as needed
4. Preview and save the compressed image

## Project Structure

- `main_app.py`: Main application entry point and GUI framework
- `huffman.py`: Core Huffman compression algorithm implementation
- `huffman_GUI.py`: GUI interface for Huffman compression
- `png_compressor_gui.py`: GUI interface for PNG compression
- `requirements.txt`: List of Python dependencies
