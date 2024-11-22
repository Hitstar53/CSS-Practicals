import socket
import pickle

# Dictionary to store public keys for each user (identity)
registered_keys = {}

def register_key(identity, public_key):
    registered_keys[identity] = public_key
    print(f"Registered {identity}'s public key.")


def get_public_key(identity):
    return registered_keys.get(identity)


def third_party_service():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 4444))
    server_socket.listen(5)
    print("Third Party Entity is running...")

    while True:
        client_socket, _ = server_socket.accept()
        request = client_socket.recv(1024)
        data = pickle.loads(request)

        if data["type"] == "register":
            register_key(data["identity"], data["public_key"])
            client_socket.send(b"Registration Successful")
        elif data["type"] == "get_key":
            public_key = get_public_key(data["identity"])
            client_socket.send(pickle.dumps(public_key))
        client_socket.close()

    server_socket.close()

if __name__ == "__main__":
    third_party_service()
