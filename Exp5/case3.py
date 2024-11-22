from sha512 import sha512

def send(message: str , seed: str):
    message_seed = message + seed
    hash_message = sha512(message_seed)
    print("Sending message:" , message)
    print("Hash :" , hash_message)
    return message + hash_message

def receive(message_recv: str, seed: str):
    hash_message = message_recv[-128:]
    message = message_recv[:-128]
    expected_hash_message = sha512(message + seed)
    try:
        assert expected_hash_message == hash_message
        print(f"Message hashes matching\nMessage : {message}\nHash : {hash_message}")
        return message
    except AssertionError:
        print("Message hashes not matching! Message corrupted")
        return None

print("Case 1")
seed_test = "hellothisishatim"
sent1 = send("Hatim" , seed_test)
recvd1 = receive(sent1 , seed_test)

print()
print("nodonattack")
sent2 = send("Sawai" , seed_test)
sent2 = sent2[:34] + "05" + sent2[36:]
recvd2 = receive(sent2 , seed_test)
assert recvd2 is None
