import socket
import random
from Crypto.Cipher import AES
import os

# Diffie-Hellman parameters
P = 23  # A prime number
G = 5  # A primitive root modulo P


# Function to generate a private key
def generate_private_key():
    return random.randint(1, P - 1)


# Function to calculate public key
def calculate_public_key(private_key):
    return pow(G, private_key, P)


# Function to calculate the shared secret
def calculate_shared_secret(public_key, private_key):
    return pow(public_key, private_key, P)


# AES encryption
def aes_encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
    return cipher.nonce + ciphertext


# Menu
def menu():
    print("\n---- Sender Menu ----")
    print("1. Generate Key using Diffie-Hellman")
    print("2. Send a Message to the Receiver (using AES encryption)")
    print("3. Exit")


def sender_program():
    private_key = None
    shared_secret = None

    while True:
        menu()
        choice = int(input("Enter your choice: "))

        if choice == 1:
            private_key = generate_private_key()
            public_key = calculate_public_key(private_key)
            print(f"Your public key: {public_key}")

            # Send public key to the receiver and receive theirs
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("localhost", 3333))
                s.send(f"{public_key}".encode())
                receiver_public_key = int(s.recv(1024).decode())
                print(f"Receiver's public key: {receiver_public_key}")

            shared_secret = calculate_shared_secret(receiver_public_key, private_key)
            print(f"Shared secret key: {shared_secret}")

        elif choice == 2:
            if shared_secret is None:
                print("Generate the shared key first!")
                continue

            # Read the message from sender_input.txt
            with open("sender_input.txt", "r") as file:
                message = file.read()

            key = (
                str(shared_secret).zfill(16).encode()
            )  # Use the shared secret as the AES key
            encrypted_message = aes_encrypt(key, message)

            # Send the encrypted message to the receiver
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("localhost", 3333))
                s.send(encrypted_message)
            print("Encrypted message sent.")

        elif choice == 3:
            print("Exiting sender program.")
            break


if __name__ == "__main__":
    sender_program()
