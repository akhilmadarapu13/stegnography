import cv2
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Generate AES key from password
def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Encrypt message using AES
def encrypt_message(message: str, password: str) -> bytes:
    salt = os.urandom(16)
    key = generate_key(password, salt)
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    message_bytes = message.encode()
    pad_length = 16 - len(message_bytes) % 16
    message_bytes += bytes([pad_length]) * pad_length

    ciphertext = encryptor.update(message_bytes) + encryptor.finalize()
    return salt + iv + ciphertext

# Decrypt message using AES
def decrypt_message(encrypted_message: bytes, password: str) -> str:
    salt = encrypted_message[:16]
    iv = encrypted_message[16:32]
    ciphertext = encrypted_message[32:]

    key = generate_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_bytes = decryptor.update(ciphertext) + decryptor.finalize()
    pad_length = decrypted_bytes[-1]
    return decrypted_bytes[:-pad_length].decode()

# Hide encrypted message in image
def hide_message(image_path: str, message: str, password: str, output_path: str):
    encrypted_message = encrypt_message(message, password)
    encoded_message = base64.b64encode(encrypted_message).decode() + "@@END@@"

    img = cv2.imread(image_path)
    index = 0

    for char in encoded_message:
        if index >= img.shape[0] * img.shape[1]:
            raise ValueError("Message too large to hide in image")
        img[index // img.shape[1], index % img.shape[1], 0] = ord(char)
        index += 1

    cv2.imwrite(output_path, img)

# Extract encrypted message from image
def extract_message(image_path: str, password: str):
    img = cv2.imread(image_path)
    chars = []
    index = 0

    while index < img.shape[0] * img.shape[1]:
        char = chr(img[index // img.shape[1], index % img.shape[1], 0])
        chars.append(char)
        if ''.join(chars[-7:]) == "@@END@@":
            break
        index += 1

    if index >= img.shape[0] * img.shape[1]:
        raise ValueError("No hidden message found or message incomplete")

    encoded_message = ''.join(chars[:-7])
    encrypted_message = base64.b64decode(encoded_message)
    return decrypt_message(encrypted_message, password)

if __name__ == "__main__":
    while True:
        print("\n1. Encrypt Image")
        print("2. Decrypt Image")
        print("3. Exit")
        option = input("Choose an option (1/2/3): ")

        if option == '1':
            image_path = input("Enter the image path: ")
            message = input("Enter the message to hide: ")
            password = input("Enter the password: ")
            output_path = "encryptedImage.png"

            try:
                hide_message(image_path, message, password, output_path)
                print(f"✅ Encrypted image saved at {output_path}")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif option == '2':
            image_path = input("Enter the encrypted image path: ")
            password = input("Enter the password for decryption: ")

            try:
                decrypted_message = extract_message(image_path, password)
                print(f"✅ Decrypted message: {decrypted_message}")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif option == '3':
            print("Exiting...")
            break

        else:
            print("Invalid option. Please try again.")
