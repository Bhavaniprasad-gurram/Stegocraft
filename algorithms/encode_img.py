import os
import random
import zipfile
import tempfile
from datetime import datetime
from PIL import Image
from algorithms.crypto_utils import aes_encrypt, aes_decrypt


def encode_lsb_image(image_path, message):
    image = Image.open(image_path).convert("RGB")
    width, height = image.size

    key = str(random.randint(10000, 99999))

    # AES-encrypt the message before hiding
    encrypted_message = aes_encrypt(message, key)

    message_length = len(encrypted_message) * 8 + 5
    if message_length > (width * height * 3):
        raise ValueError("Text too long for chosen image.")

    with tempfile.TemporaryDirectory() as temp_dir:
        key_file_path = os.path.join(temp_dir, 'key_image.txt')
        with open(key_file_path, 'w') as file:
            file.write(str(key))

        pixels = image.load()
        for i in range(width):
            for j in range(height):
                r, g, b = pixels[i, j]
                pixels[i, j] = (r - (r % 2), g - (g % 2), b - (b % 2))

        binary_message = ""
        for char in encrypted_message:
            binary_char = bin(ord(char))[2:].zfill(8)
            binary_message += binary_char

        binary_message = key + binary_message

        counter = 0
        for i in range(width):
            for j in range(height):
                r, g, b = pixels[i, j]
                if counter < len(binary_message):
                    r += int(binary_message[counter])
                    if counter + 1 < len(binary_message):
                        g += int(binary_message[counter + 1])
                    if counter + 2 < len(binary_message):
                        b += int(binary_message[counter + 2])
                    counter += 3
                    pixels[i, j] = (r, g, b)
                else:
                    break

        encoded_img_path = os.path.join(temp_dir, 'encoded_image.png')
        image.save(encoded_img_path)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        zip_file_path = os.path.join(tempfile.gettempdir(), f'encoded_image_result_{timestamp}.zip')
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            zip_file.write(encoded_img_path, os.path.basename(encoded_img_path))
            zip_file.write(key_file_path, os.path.basename(key_file_path))

    return zip_file_path


def decode_lsb_image(image_path, key):
    image = Image.open(image_path).convert("RGB")
    pixels = image.load()

    binary_message = ""
    for i in range(image.width):
        for j in range(image.height):
            r, g, b = pixels[i, j]
            binary_message += str(r % 2)
            binary_message += str(g % 2)
            binary_message += str(b % 2)

    key_length = 5
    binary_message = binary_message[key_length:]

    encrypted_output = ""
    for i in range(0, len(binary_message), 8):
        binary_char = binary_message[i:i + 8]
        char_code = int(binary_char, 2)
        if char_code == 0:
            break
        encrypted_output += chr(char_code)

    encrypted_output = encrypted_output.rstrip("\0").rstrip()

    try:
        output = aes_decrypt(encrypted_output, str(key))
    except Exception:
        return encrypted_output  # fallback to raw if AES fails

    return output
