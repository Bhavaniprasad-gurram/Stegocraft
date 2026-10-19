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


def encode_lsb_audio(audio_file_path, message):
    key = generate_key()

    # AES-encrypt the message before hiding it
    encrypted_message = aes_encrypt(message, str(key))

    with tempfile.TemporaryDirectory() as temp_dir:
        key_file_path = os.path.join(temp_dir, 'key.txt')
        with open(key_file_path, 'w') as file:
            file.write(str(key))

        audio = wave.open(audio_file_path, 'r')
        params = audio.getparams()
        frames = audio.readframes(audio.getnframes())

        audio_array = np.frombuffer(frames, dtype=np.int16)
        message_binary = ''.join(format(ord(c), '08b') for c in encrypted_message)

        key_binary = format(key, '020b')
        message_binary = key_binary + message_binary
        message_binary += '00000000'

        if len(message_binary) > len(audio_array):
            raise ValueError('Message is too long to fit in the audio file')

        audio_array_copy = audio_array.copy()
        audio_array_copy.setflags(write=True)

        for i in range(len(message_binary)):
            audio_array_copy[i] &= ~1
            audio_array_copy[i] |= int(message_binary[i])

        encoded_frames = audio_array_copy.tobytes()

        encoded_audio_path = os.path.join(temp_dir, 'encoded_audio.wav')
        encoded_audio = wave.open(encoded_audio_path, 'w')
        encoded_audio.setparams(params)
        encoded_audio.writeframes(encoded_frames)
        encoded_audio.close()

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        zip_file_path = os.path.join(tempfile.gettempdir(), f'encoded_result_{timestamp}.zip')
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            zip_file.write(encoded_audio_path, os.path.basename(encoded_audio_path))
            zip_file.write(key_file_path, os.path.basename(key_file_path))

    return zip_file_path


def decode_lsb_audio(encoded_audio_file_path, key):
    encoded_audio = wave.open(encoded_audio_file_path, 'r')
    frames = encoded_audio.readframes(encoded_audio.getnframes())
    encoded_audio_array = np.frombuffer(frames, dtype=np.int16)

    key_binary = ''
    for sample in encoded_audio_array[:20]:
        key_binary += str(sample & 1)

    extracted_key = int(key_binary, 2)

    if str(key) != str(extracted_key):
        return None

    message_binary = ''
    for sample in encoded_audio_array[20:]:
        message_binary += str(sample & 1)

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
