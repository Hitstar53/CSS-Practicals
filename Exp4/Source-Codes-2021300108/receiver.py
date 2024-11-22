import socket
import random
from Crypto.Cipher import AES

P = 23
G = 5


# Function to generate a private key
def generate_private_key():
    return random.randint(1, P - 1)


# Function to calculate public key
def calculate_public_key(private_key):
    return pow(G, private_key, P)


# Function to calculate the shared secret
def calculate_shared_secret(public_key, private_key):
    return pow(public_key, private_key, P)


# AES decryption
def aes_decrypt(key, ciphertext):
    nonce = ciphertext[:16]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext[16:])
    return plaintext.decode()


# Menu
def menu():
    print("\n---- Receiver Menu ----")
    print("1. Wait for key exchange (Diffie-Hellman)")
    print("2. Wait for encrypted message")
    print("3. Exit")


def receiver_program():
    private_key = generate_private_key()
    public_key = calculate_public_key(private_key)
    shared_secret = None

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("localhost", 3333))
        server_socket.listen(5)
        print("Receiver is waiting for connections...")

        while True:
            menu()
            choice = int(input("Enter your choice: "))

            if choice == 1:
                # Handle public key exchange
                client_socket, _ = server_socket.accept()
                with client_socket:
                    sender_public_key = int(client_socket.recv(1024).decode())
                    client_socket.send(f"{public_key}".encode())
                    shared_secret = calculate_shared_secret(
                        sender_public_key, private_key
                    )
                    print(f"Shared secret key established: {shared_secret}")

            elif choice == 2:
                if shared_secret is None:
                    print("You must exchange the key first!")
                    continue

                # Receive the encrypted message
                client_socket, _ = server_socket.accept()
                with client_socket:
                    encrypted_message = client_socket.recv(1024)

                # Decrypt the message using the shared key
                key = str(shared_secret).zfill(16).encode()
                decrypted_message = aes_decrypt(key, encrypted_message)

                # Write the decrypted message to receiver_output.txt
                with open("receiver_output.txt", "w") as file:
                    file.write(decrypted_message)

                print("Decrypted message received and written to receiver_output.txt")

            elif choice == 3:
                print("Exiting receiver program.")
                break


if __name__ == "__main__":
    receiver_program()
