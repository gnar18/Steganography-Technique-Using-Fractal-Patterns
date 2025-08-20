import numpy as np
import cv2
import random


# Generate a fractal pattern using Mandelbrot set
def generate_fractal(width, height, scale=0.005, seed=1234):
    np.random.seed(seed)
    fractal = np.zeros((width, height), dtype=np.uint8)
    for x in range(width):
        for y in range(height):
            zx, zy = x * scale - 2, y * scale - 1.5
            c_x, c_y = zx, zy
            iteration = 255
            while zx*zx + zy*zy < 4 and iteration > 0:
                temp = zx * zx - zy * zy + c_x
                zy, zx = 2.0 * zx * zy + c_y, temp
                iteration -= 1
            fractal[x, y] = iteration
    return fractal


# Embed text within the fractal pattern in an image
def hide_text(image_path, secret_message, output_path, key=1234):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    h, w, _ = img.shape
    fractal = generate_fractal(w, h, seed=key)
    
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message)
    idx = 0

    for x in range(w):
        for y in range(h):
            if fractal[x, y] % 2 == 0 and idx < len(binary_message):  # Hide in even fractal pixels
                img[y, x, 0] = (img[y, x, 0] & 0b11111110) | int(binary_message[idx])
                idx += 1

    cv2.imwrite(output_path, img)
    print("✅ Message hidden successfully in:", output_path)


# Extract text from the image
def extract_text(image_path, key=1234, message_length=100):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    h, w, _ = img.shape
    fractal = generate_fractal(w, h, seed=key)
    
    binary_message = ""
    idx = 0
    
    for x in range(w):
        for y in range(h):
            if fractal[x, y] % 2 == 0 and idx < message_length * 8:
                binary_message += str(img[y, x, 0] & 1)
                idx += 1

    secret_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    return secret_message


# ----------------- MAIN -----------------
if __name__ == "__main__":
    print("🔐 Fractal Steganography Tool")
    choice = input("Do you want to (H)ide or (E)xtract a message? ").strip().upper()

    if choice == "H":
        image_path = input("Enter path of input image: ").strip()
        secret_message = input("Enter the secret message to hide: ").strip()
        output_path = input("Enter output image filename (e.g., hidden.png): ").strip()
        key = int(input("Enter secret key (number): ").strip())

        hide_text(image_path, secret_message, output_path, key)

    elif choice == "E":
        image_path = input("Enter path of stego image: ").strip()
        key = int(input("Enter secret key (number): ").strip())
        message_length = int(input("Enter expected message length (number of characters): ").strip())

        retrieved_text = extract_text(image_path, key, message_length)
        print("📜 Extracted Message:", retrieved_text)

    else:
        print("❌ Invalid choice. Please enter H or E.")
