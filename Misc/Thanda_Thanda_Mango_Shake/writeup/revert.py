# hex_to_image.py

def hex_to_image(input_path, output_path):
    with open(input_path, 'r') as f:
        hex_data = f.read().strip()
    with open(output_path, 'wb') as img:
        img.write(bytes.fromhex(hex_data))
    print(f"[+] Image restored as {output_path}")

if __name__ == "__main__":
    hex_to_image("gannay.txt", "restored.png")
