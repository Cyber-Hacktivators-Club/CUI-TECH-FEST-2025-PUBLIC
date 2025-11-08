# read_image_hex.py

def image_to_hex(input_path, output_path):
    with open(input_path, 'rb') as img:
        data = img.read()
        hex_data = data.hex()
    with open(output_path, 'w') as f:
        f.write(hex_data)
    print(f"[+] Hex dump saved to {output_path}")

if __name__ == "__main__":
    image_to_hex("ganna.jpg", "output.txt")
