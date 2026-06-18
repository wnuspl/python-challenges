import random

with open("sample.txt", "r", encoding="utf-8") as f:
    input_text = f.read()

# Return a dictionary with keys of words in the text and the value as their percentage
def build_frequency_dict(text):
    freq = {}
    word_list = text.split()
    for word in word_list:
        # freq.get(word, 0) is a useful syntax that lets us either get the value or set it to 0 if it doesn't exist
        freq[word] = freq.get(word, 0) + 1

    # divide by total words to get fractional frequencies
    for word in freq.keys():
        freq[word] = freq[word] / len(word_list)

    return freq


# Creates a list from a frequency dictionary (see above) containing only the weights
def build_weights(frequency_dict):
    weights = []
    for word in frequency_dict.keys():
        weights.append(frequency_dict[word])

    return weights



def generate_text(text, length):
    freq = build_frequency_dict(text)
    words = list(freq.keys())
    weights = build_weights(freq)

    # Useful function in the random library will give us a list of random words chosen from words.
    # Uses the weights we provide to bias certain indices
    generated = random.choices(words, weights=weights, k=length)
    return " ".join(generated)


print(generate_text(input_text, 20))