def rail_fence_decrypt(ciphertext, num_rails):
    rails = [""] * num_rails
    index = 0
    pattern = [0] * len(ciphertext)

    rail = 0
    direction = 1
    for i in range(len(ciphertext)):
        pattern[i] = rail
        rail += direction
        if rail == 0 or rail == num_rails - 1:
            direction *= -1

    for rail_num in range(num_rails):
        for i in range(len(ciphertext)):
            if pattern[i] == rail_num:
                rails[rail_num] += ciphertext[index]
                index += 1

    result = ""
    rail = 0
    direction = 1
    for i in range(len(ciphertext)):
        result += rails[rail][0]
        rails[rail] = rails[rail][1:]
        rail += direction
        if rail == 0 or rail == num_rails - 1:
            direction *= -1

    return result


def rail_fence_bruteforce(ciphertext):
    for num_rails in range(2, len(ciphertext)):
        decrypted_text = rail_fence_decrypt(ciphertext, num_rails)
        print(f"Attempt with {num_rails} rails: {decrypted_text}")


if __name__ == "__main__":
    ciphertext = "HOLELWRDLO"
    rail_fence_bruteforce(ciphertext)
