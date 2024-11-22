import caesar as c
import hill as h
import playfair as pf
import monoalph as mono
import polyalph as poly

words = [
    "HELLO", "WORLD", "CRYPTOGRAPHY", "SECURITY", "ENCRYPTION",
    "DECRYPTION", "COMPUTER", "SCIENCE", "ALGORITHM", "PROGRAMMING",
    "SOFTWARE", "HARDWARE", "NETWORK", "DATABASE", "INFORMATION",
    "TECHNOLOGY", "INTERNET", "COMMUNICATION", "APPLICATION", "DEVELOPMENT", 
    "DISTRIBUTION", "OPERATING", "SYSTEM", "MOBILE", "WEB"
]

# create file encrypted_words.txt using all techniques
with open("./Exp1/encrypted_words.txt", "w") as f:
    for word in words:
        f.write(word + "\n")
    # f.write("\n")

    # Caesar
    for word in words:
        encrypted = c.caesar_cipher(word, 5)
        f.write(encrypted + "\n")
    # f.write("\n")
    
    # monoalphabetic
    for word in words:
        encrypted = mono.monoalphabetic_cipher(word, "QWERTYUIOPASDFGHJKLZXCVBNM", "encrypt")
        f.write(encrypted + "\n")
    # f.write("\n")
    
    # Hill
    for word in words:
        encrypted = h.hill_encrypt(word, [[17, 17], [21, 18]])
        f.write(encrypted + "\n")
    # f.write("\n")
    
    # Playfair
    for word in words:
        encrypted = pf.playfair_encrypt(word, pf.generate_playfair_key("PRIVATEKEY"))
        f.write(encrypted + "\n")
    # f.write("\n")
    
    # Polyalphabetic
    for word in words:
        encrypted = poly.vigenere_encrypt(word, "PKEY")
        f.write(encrypted + "\n")
    # f.write("\n")
    
    f.close()