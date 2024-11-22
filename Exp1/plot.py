import matplotlib.pyplot as plt
import numpy as np

def relative_frequency(list_of_words):
    freq = {}
    for word in list_of_words:
        for letter in word.upper():
            if letter.isalpha():
                freq[letter] = freq.get(letter, 0) + 1
    total = sum(freq.values())
    for key in freq:
        freq[key] = (freq[key] / total) * 100
    return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))


def pad_frequencies(freq_dict, length=25):
    values = list(freq_dict.values())
    return values[:length] + [0] * (length - len(values))


with open("./Exp1/encrypted_words.txt") as f:
    content = f.read()
    words = content.split("\n")
    plaintext = words[0:25]
    monoalphabetic = words[25:50]
    playfair = words[50:75]
    hill = words[75:100]
    polyalphabetic = words[100:125]

freq_plaintext = relative_frequency(plaintext)
freq_monoalphabetic = relative_frequency(monoalphabetic)
freq_playfair = relative_frequency(playfair)
freq_hill = relative_frequency(hill)
freq_polyalphabetic = relative_frequency(polyalphabetic)

x = range(2, 27)  # 2 to 26 on x-axis

plt.figure(figsize=(12, 8))
plt.plot(x, pad_frequencies(freq_plaintext), label="Plaintext", linewidth=2)
plt.plot(
    x,
    pad_frequencies(freq_playfair),
    label="Playfair cipher",
    linestyle=":",
    linewidth=2,
)
plt.plot(
    x,
    pad_frequencies(freq_polyalphabetic),
    label="Vigenère cipher",
    linestyle="--",
    linewidth=2,
)
plt.plot(
    x, pad_frequencies(freq_hill), label="Hill cipher", linestyle="-.", linewidth=2
)
plt.plot(
    x,
    pad_frequencies(freq_monoalphabetic),
    label="Monoalphabetic cipher",
    linestyle=(0, (3, 1, 1, 1)),
    linewidth=2,
)

plt.axhline(y=32.5, color="gray", linestyle="-", linewidth=1)

plt.xlabel("Frequency ranked letters")
plt.ylabel("Relative Frequency of Occurrence (%)")
plt.title("Relative Frequency of Occurrence of Letters")
plt.legend()
plt.xlim(2, 26)

plt.grid(True, linestyle=":", alpha=0.7)
plt.show()