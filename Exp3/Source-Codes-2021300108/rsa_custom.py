import os
import math
import random

# Function to perform the Miller-Rabin primality test
def is_prime(n, k=5): 
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    # Miller-Rabin test
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Function to generate a random prime number
def generate_prime_number(bit_length):
    while True:
        # Generate a random number of the desired bit length
        prime_candidate = random.getrandbits(bit_length)
        # Ensure it's odd (even numbers can't be prime except 2)
        prime_candidate |= (1 << bit_length - 1) | 1
        if is_prime(prime_candidate):
            return prime_candidate

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

# Function to generate RSA keys using random large primes
def generate_rsa_keys(bit_length=1024):
    print("Generating prime numbers...")
    p = generate_prime_number(bit_length)
    q = generate_prime_number(bit_length)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  
    if math.gcd(e, phi) != 1:
        e = 17
        while math.gcd(e, phi) != 1:
            e += 1

    d = modinv(e, phi)
    return ((e, n), (d, n))

# Function to encrypt a message using the public key
def encrypt(message, public_key):
    e, n = public_key
    message_bytes = message.encode("utf-8")
    chunk_size = (n.bit_length() - 1) // 8 - 11
    chunks = [
        message_bytes[i : i + chunk_size]
        for i in range(0, len(message_bytes), chunk_size)
    ]

    encrypted_chunks = []
    for chunk in chunks:
        padded = os.urandom(11) + b"\x00" + chunk
        m = int.from_bytes(padded, "big")
        c = pow(m, e, n)
        encrypted_chunks.append(c)

    return encrypted_chunks

# Function to decrypt a message using the private key
def decrypt(cipher, private_key):
    d, n = private_key
    decrypted_chunks = []
    for c in cipher:
        m = pow(c, d, n)
        padded = m.to_bytes((m.bit_length() + 7) // 8, "big")
        chunk = padded[12:] 
        decrypted_chunks.append(chunk)

    return b"".join(decrypted_chunks).decode("utf-8")

# Main code to demonstrate RSA functionality
if __name__ == "__main__":
    print("Generating RSA keys...")
    public_key, private_key = generate_rsa_keys(
        512
    )  # Using 512-bit primes for demonstration
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")

    # Example message
    message = "Hello RSA"
    print(f"\nOriginal Message: {message}")

    # Encrypt the message
    encrypted_message = encrypt(message, public_key)
    print(f"Encrypted Message: {encrypted_message}")

    # Decrypt the message
    decrypted_message = decrypt(encrypted_message, private_key)
    print(f"Decrypted Message: {decrypted_message}")
