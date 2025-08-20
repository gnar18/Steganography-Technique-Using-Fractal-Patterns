import numpy as np
import cv2

def generate_fractal(width, height, scale=0.005, seed=1234):
    np.random.seed(seed)
    fractal = np.zeros((width, height), dtype=np.uint8)
    for x in range(width):
        for y in range(height):
            zx, zy = x * scale - 2, y * scale - 1.5
            c_x, c_y = zx, zy
            iteration = 255
            while zx*zx + zy*zy < 4 and iteration > 0:
                zx, zy = zx*zx - zy*zy + c_x, 2*zx*zy + c_y
                iteration -= 1
            fractal[x, y] = iteration
    return fractal

def hide_text(image_path, secret_message, output_path, key=1234):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Image not found!")

    h, w, _ = img.shape
    fractal = generate_fractal(w, h, seed=key)

    binary_msg = ''.join(format(ord(c), '08b') for c in secret_message)
    idx = 0

    for x in range(w):
        for y in range(h):
            if fractal[x, y] % 2 == 0 and idx < len(binary_msg):
                img[y, x, 0] = (img[y, x, 0] & 0b11111110) | int(binary_msg[idx])
                idx += 1

    cv2.imwrite(output_path, img)
    print(f"✅ Message hidden successfully in {output_path}")

def extract_text(image_path, key=1234, msg_length=100):
    """Extract the hidden message from an image."""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Image not found!")

    h, w, _ = img.shape
    fractal = generate_fractal(w, h, seed=key)
    
    binary_msg = ""
    idx = 0
    for x in range(w):
        for y in range(h):
            if fractal[x, y] % 2 == 0 and idx < msg_length * 8:
                binary_msg += str(img[y, x, 0] & 1)
                idx += 1

    message = ''.join(chr(int(binary_msg[i:i+8], 2)) for i in range(0, len(binary_msg), 8))
    return message

if __name__ == "__main__":
    print("🔐 Fractal Steganography Tool")
    choice = input("Do you want to (H)ide or (E)xtract a message? ").strip().upper()

    if choice == "H":
        hide_text(
            image_path=input("Input image path: ").strip(),
            secret_message=input("Secret message: ").strip(),
            output_path=input("Output image filename: ").strip(),
            key=int(input("Secret key (number): ").strip())
        )
    elif choice == "E":
        msg = extract_text(
            image_path=input("Stego image path: ").strip(),
            key=int(input("Secret key (number): ").strip()),
            msg_length=int(input("Expected message length: ").strip())
        )
        print("📜 Extracted Message:", msg)
    else:
        print("❌ Invalid choice. Enter H or E.")

