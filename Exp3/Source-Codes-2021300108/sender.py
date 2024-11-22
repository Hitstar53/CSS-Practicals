import os
import rsa_custom as rsa
import socket
import pickle
import monoalph as mono

# Sender class to handle operations
class Sender:
    def __init__(self, thirdparty_host, thirdparty_port, receiver_host, receiver_port):
        self.thirdparty_host = thirdparty_host
        self.thirdparty_port = thirdparty_port
        self.receiver_host = receiver_host
        self.receiver_port = receiver_port
        self.public_key = None
        self.pub_key, self.priv_key = rsa.generate_rsa_keys()
        self.secret_key = mono.generate_cipher_alphabet()

        with open("../Input-Output-2021300108/keys.txt", "a") as f:
            f.write(f"Public Key:\n{self.pub_key}\n")
            f.write(f"Secret Key:\n{self.priv_key}\n\n")

    # Register identity with the third party
    def register_identity(self, identity):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.thirdparty_host, self.thirdparty_port))
            message = {"type": "register", "identity": identity, "public_key": self.pub_key}
            s.sendall(pickle.dumps(message))
            response = s.recv(1024).decode()
            print(response)
            # write the secret key to sender.txt
            with open("../Input-Output-2021300108/sender.txt", "w") as f:
                f.write(f"Identity: {identity}\n")
                f.write(f"Response: {response}\n")
                f.write(f"Secret Key: {self.secret_key}\n\n")
            s.close()

    # Request public key of the receiver from the third party
    def request_public_key(self, receiver_identity):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.thirdparty_host, self.thirdparty_port))
            message = {"type": "get_key", "identity": receiver_identity}
            s.sendall(pickle.dumps(message))
            self.public_key = pickle.loads(s.recv(1024))
            print(f"Received {receiver_identity}'s Public Key")
            s.close()

    # Send the symmetric key to the receiver using asymmetric encryption
    def send_symmetric_key(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.receiver_host, self.receiver_port))
            # Encrypt symmetric key using receiver's public key
            # print("Sending key:", self.secret_key)
            encrypted_secret_key = rsa.encrypt(self.secret_key, self.public_key)
            data = pickle.dumps(encrypted_secret_key)
            s.sendall(data)
            print("Symmetric key sent to the receiver.")

    # Send a large message to the receiver using the symmetric key (assuming a simple encryption)
    def send_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.receiver_host, self.receiver_port))
            encrypted_message = mono.monoalphabetic_cipher(message, self.secret_key)
            s.sendall(encrypted_message.encode())
            with open("../Input-Output-2021300108/sender.txt", "a") as f:
                f.write(f"Encrypted Message: {encrypted_message}\n")
            print("Encrypted message sent to the receiver.")

# Main Menu for Sender
def sender_menu():
    sender = Sender("localhost", 4444, "localhost", 3333)
    identity = input("Enter your identity: ")

    while True:
        print("\n---- Sender Menu ----")
        print("1. Register Identity with Third Party")
        print("2. Send Symmetric Key to Receiver")
        print("3. Send Message to Receiver")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            sender.register_identity(identity)
        elif choice == "2":
            receiver_identity = input("Enter Receiver's Identity: ")
            sender.request_public_key(receiver_identity)
            sender.send_symmetric_key()
        elif choice == "3":
            # message = input("Enter message to send: ")
            # read message from input.txt
            with open("../Input-Output-2021300108/input.txt", "r") as f:
                message = f.read()
            sender.send_message(message)
        elif choice == "4":
            print("Exiting Sender Program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    sender_menu()
