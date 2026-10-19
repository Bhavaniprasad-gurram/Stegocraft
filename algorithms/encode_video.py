import wave
import numpy as np
import random
import zipfile
import os
import tempfile
from datetime import datetime
from algorithms.crypto_utils import aes_encrypt, aes_decrypt


def generate_key():
    """Generates a random 5-digit key for encoding message."""
    return random.randint(10000, 99999)


def encode_lsb_video(video_file_path, message):
    key = generate_key()

    # AES-encrypt the message before hiding
    encrypted_message = aes_encrypt(message, str(key))

    with tempfile.TemporaryDirectory() as temp_dir:
        key_file_path = os.path.join(temp_dir, 'key_video.txt')
        with open(key_file_path, 'w') as file:
            file.write(str(key))

        video_array = np.fromfile(video_file_path, dtype=np.uint8)
        message_binary = ''.join(format(ord(c), '08b') for c in encrypted_message)

        key_binary = format(key, '020b')
        message_binary = key_binary + message_binary
        message_binary += '00000000'

        if len(message_binary) > len(video_array):
            raise ValueError('Message is too long to fit in the video file')

        video_array_copy = video_array.copy()

        for i in range(len(message_binary)):
            video_array_copy[i] = (video_array_copy[i] & ~1) | int(message_binary[i])

        encoded_video_file_path = os.path.join(temp_dir, 'encoded_video.avi')
        with open(encoded_video_file_path, 'wb') as file:
            file.write(video_array_copy.tobytes())

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        zip_file_path = os.path.join(tempfile.gettempdir(), f'encoded_video_result_{timestamp}.zip')
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            zip_file.write(encoded_video_file_path, os.path.basename(encoded_video_file_path))
            zip_file.write(key_file_path, os.path.basename(key_file_path))

    return zip_file_path


def decode_lsb_video(encoded_video_file_path, key):
    with open(encoded_video_file_path, 'rb') as file:
        encoded_video_array = np.frombuffer(file.read(), dtype=np.uint8)

    key_binary = ''
    for byte in encoded_video_array[:20]:
        key_binary += str(byte & 1)

    extracted_key = int(key_binary, 2)

    if str(key) != str(extracted_key):
        return None

    message_binary = ''
    for byte in encoded_video_array[20:]:
        message_binary += str(byte & 1)

    encrypted_message = ''
    for i in range(0, len(message_binary), 8):
        byte = message_binary[i:i + 8]
        if byte == '00000000':
            break
        char = chr(int(byte, 2))
        encrypted_message += char

    try:
        message = aes_decrypt(encrypted_message.strip(), str(key))
    except Exception:
        return None

    return message