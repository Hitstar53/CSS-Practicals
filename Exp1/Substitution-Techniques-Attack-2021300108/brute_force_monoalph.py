from itertools import permutations


def is_valid_mapping(ciphertext, plaintext, mapping):
    reverse_mapping = {v: k for k, v in mapping.items()}
    for c, p in zip(ciphertext, plaintext):
        if p in reverse_mapping:
            if reverse_mapping[p] != c:
                return False
        else:
            reverse_mapping[p] = c
    return True


def monoalphabetic_bruteforce(
    ciphertext,
    target_plaintext,
    alphabet_subset,
    full_alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    limit=6,
):
    # Limit the alphabet subset to the first 'limit' letters
    limited_alphabet_subset = alphabet_subset[:limit]

    # Generate all possible permutations of the limited alphabet subset
    for perm in permutations(limited_alphabet_subset):
        # Create a mapping from the limited alphabet subset to the permutation
        mapping = {limited_alphabet_subset[i]: perm[i] for i in range(limit)}

        # Check if this mapping produces the target plaintext
        if is_valid_mapping(ciphertext.upper(), target_plaintext.upper(), mapping):
            plaintext_attempt = ciphertext.upper().translate(str.maketrans(mapping))
            if plaintext_attempt == target_plaintext.upper():
                # Create the full key based on the permutation
                full_key = "".join(perm) + full_alphabet[limit:]
                print(
                    f"Match found! Permutation: {''.join(perm)} -> Plaintext: {plaintext_attempt}"
                )
                print(f"Full key: {full_alphabet} -> {full_key}")
                return

    print("No matching permutation found.")


# Example usage
ciphertext = "FEFDUS"
target_plaintext = "ABACUS"
alphabet_subset = "ABCDEF"  # Subset of the alphabet to consider
monoalphabetic_bruteforce(ciphertext, target_plaintext, alphabet_subset, limit=6)