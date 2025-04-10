from PIL import Image
import numpy as np

def text_to_binary(text):
    """Convert text to a binary string"""
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary_string):
    """Convert binary string to text"""
    chars = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def encode_text(image_path, output_path, secret_text):
    """Hides text inside an image using LSB encoding"""
    img = Image.open(image_path)
    img = img.convert("RGB")  
    pixels = np.array(img)

    binary_text = text_to_binary(secret_text) + '1111111111111110'  
    text_index = 0

    for row in pixels:
        for pixel in row:
            for channel in range(3):  
                if text_index < len(binary_text):
                    pixel[channel] = (pixel[channel] & 0xFE) | int(binary_text[text_index])
                    text_index += 1

    encoded_img = Image.fromarray(pixels)
    encoded_img.save(output_path)
    print(f"Text encoded successfully in {output_path}")

def decode_text(image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = np.array(img)

    binary_text = ""
    for row in pixels:
        for pixel in row:
            for channel in range(3): 
                binary_text += str(pixel[channel] & 1)
                if binary_text[-16:] == "1111111111111110":  
                    return binary_to_text(binary_text[:-16])

    return "No hidden message found!"


input_image = "input.png"  
output_image = "output.png"
secret_message = "Hello, this is a secret!"


encode_text(input_image, output_image, secret_message)


decoded_message = decode_text(output_image)
print(f"Decoded Message: {decoded_message}")
