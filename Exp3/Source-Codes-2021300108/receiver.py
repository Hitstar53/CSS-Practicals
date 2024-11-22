import os
import rsa_custom as rsa
import socket
import pickle
import monoalph as mono

# Receiver class to handle operations
class Receiver:
    def __init__(self, thirdparty_host, thirdparty_port, my_port):
        self.thirdparty_host = thirdparty_host
        self.thirdparty_port = thirdparty_port
        self.my_port = my_port
        self.private_key = None
        self.symmetric_key = None
        self.pub_key, self.private_key = rsa.generate_rsa_keys()
        with open("../Input-Output-2021300108/keys.txt", "a") as f:
            f.write(f"Public Key:\n{self.pub_key}\n")
            f.write(f"Secret Key:\n{self.private_key}\n\n")

    # Register identity with the third party
    def register_identity(self, identity):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.thirdparty_host, self.thirdparty_port))
            message = {"type": "register", "identity": identity, "public_key": self.pub_key}
            s.sendall(pickle.dumps(message))
            response = s.recv(1024).decode()
            print(response)
            with open("../Input-Output-2021300108/receiver.txt", "w") as f:
                f.write(f"Identity: {identity}\n")
                f.write(f"Response: {response}\n")
            s.close()

    # Receive symmetric key (encrypted) from sender
    def receive_symmetric_key(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", self.my_port))
            s.listen(1)
            print("Waiting for symmetric key from sender...")
            conn, addr = s.accept()
            with conn:
                encrypted_symmetric_key = pickle.loads(conn.recv(4096))
                self.symmetric_key = rsa.decrypt(encrypted_symmetric_key, self.private_key)
                print("Symmetric Key received and decrypted")
                with open("../Input-Output-2021300108/receiver.txt", "a") as f:
                    f.write(f"Decrypted Symmetric Key: {self.symmetric_key}\n")

    # Continuously listen for a message from the sender
    def listen_for_message(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", self.my_port))
            s.listen(1)
            print("Waiting for message from sender...")
            conn, addr = s.accept()
            with conn:
                encrypted_message = conn.recv(1024).decode()
                decrypted_message = mono.monoalphabetic_cipher(
                    encrypted_message, self.symmetric_key, mode="decrypt")
                print("Decrypted message received:", decrypted_message)
                with open("../Input-Output-2021300108/receiver.txt", "a") as f:
                    f.write(f"Decrypted Message: {decrypted_message}\n")


# Main Menu for Receiver
def receiver_menu():
    receiver = Receiver("localhost", 4444, 3333)
    identity = input("Enter your identity: ")

    while True:
        print("\n---- Receiver Menu ----")
        print("1. Register Identity with Third Party")
        print("2. Wait for Symmetric Key from Sender")
        print("3. Wait for Message from Sender")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            receiver.register_identity(identity)
        elif choice == "2":
            receiver.receive_symmetric_key()
        elif choice == "3":
            receiver.listen_for_message()
        elif choice == "4":
            print("Exiting Receiver Program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    receiver_menu()
