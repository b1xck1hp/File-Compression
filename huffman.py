import heapq
from collections import defaultdict


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(frequency):
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)

    return heap[0]


def build_huffman_codes(tree):
    codes = {}

    def generate_codes(node, current_code):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = current_code
        generate_codes(node.left, current_code + "0")
        generate_codes(node.right, current_code + "1")

    generate_codes(tree, "")
    return codes

def compress_file(file_path, compressed_file):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()

    # Calculate frequency of each character
    frequency = defaultdict(int)
    for char in data:
        frequency[char] += 1

    # Build Huffman tree and codes
    huffman_tree = build_huffman_tree(frequency)
    huffman_codes = build_huffman_codes(huffman_tree)

    # Encode the data
    encoded_data = "".join(huffman_codes[char] for char in data)

    # Pad encoded data to make it a multiple of 8
    extra_padding = 8 - len(encoded_data) % 8
    encoded_data += "0" * extra_padding

    # Store the padding info as 8 bits
    padded_info = f"{extra_padding:08b}"
    encoded_data = padded_info + encoded_data

    # Convert to bytes
    byte_array = bytearray()
    for i in range(0, len(encoded_data), 8):
        byte_array.append(int(encoded_data[i:i + 8], 2))

    # Write compressed data to file
    with open(compressed_file, 'wb') as f:
        f.write(byte_array)

    # Save Huffman codes to a file for decompression
    codes_file = compressed_file + ".codes"
    with open(codes_file, 'w', encoding='utf-8') as f:
        for char, code in huffman_codes.items():
            # Write each char and its code separated by a tab
            f.write(f"{char.encode('utf-8').hex()}\t{code}\n")

    print(f"File compressed successfully: {compressed_file}")


def decompress_file(file_path, decompressed_file):
    compressed_file = file_path
    codes_file = file_path + ".codes"

    # Load Huffman codes from the file
    huffman_codes = {}
    with open(codes_file, 'r', encoding='utf-8') as f:
        for line in f:
            char_hex, code = line.strip().split("\t", 1)
            char = bytes.fromhex(char_hex).decode('utf-8')  # Decode from hex
            huffman_codes[code] = char

    with open(compressed_file, 'rb') as f:
        byte_array = f.read()

    # Convert bytes back to binary string
    bit_string = "".join(f"{byte:08b}" for byte in byte_array)

    # Extract padding info
    extra_padding = int(bit_string[:8], 2)
    encoded_data = bit_string[8:-extra_padding]

    # Decode the data using Huffman codes
    with open(decompressed_file, 'w', encoding='utf-8') as f:
        current_code = ""
        for bit in encoded_data:
            current_code += bit
            if current_code in huffman_codes:
                f.write(huffman_codes[current_code])
                current_code = ""

    print(f"File decompressed successfully: {decompressed_file}")

def benchmark_file(file_path):
    import time

    start_time = time.time()
    compressed_file = file_path + ".huf"
    compress_file(file_path, compressed_file)
    end_time = time.time()
    print(f"Compression benchmark: {end_time - start_time:.2f} seconds")


def main():
    while True:
        print("\nChoose an option:")
        print("1. Compress a file")
        print("2. Decompress a file")
        print("3. Benchmark compression")
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "4":
            print("Exiting...")
            break

        file_path = input("Enter the file path: ")

        if choice == "1":
            compressed_file = input("Enter the name for the compressed file (including extension): ")
            compress_file(file_path, compressed_file)
        elif choice == "2":
            decompressed_file = input("Enter the name for the decompressed file (including extension): ")
            decompress_file(file_path, decompressed_file)
        elif choice == "3":
            benchmark_file(file_path)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
