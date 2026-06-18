from openai import OpenAI
from datetime import datetime

# My API key is within openai_test_key.txt
# You can import the key this way, or just write something like OPENAI_KEY = "[your api key]"
with open("openai_test_key.txt", "r") as f:
    OPENAI_KEY = f.read()

client = OpenAI(api_key=OPENAI_KEY)


# Generates text of a given length (words) suitable for typing test
def generate_text(length):
    prompt = (
        "Generate random text optimized for a typing test. Use varied word lengths, but avoid strange punctuation/symbols."
        "Do not use common sentences such as \"the quick brown fox...\"."
        "Use varied subjects for the sentences to keep users engaged."
        f"Follow standard grammar rules and generate exactly {length} words."
    )
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output_text.strip()


# Gets input and returns a tuple of (text, time) with the typed text and time in seconds
def timed_input():
    start = datetime.now()
    text = input().strip()
    end = datetime.now()
    time = (end - start).total_seconds()
    return text, time


def typing_test():
    print("Once text is displayed, press enter to begin test.")
    print("-")
    length = 10
    text = generate_text(length)
    print(text)

    # We let the user wait until they are ready so that the start isn't sudden or reactionary
    input("(awaiting enter)...")
    typed_text, seconds = timed_input()

    # Calculating the actual accuracy is a much more advanced process
    # Reference "Levenshtein Distance Formula" if interested
    # So, we just check for equality
    if typed_text != text:
        print("You did not successfully match the given text.")


    # The standard method involves using characters, not words
    # One "word" means 5 characters
    words = len(text)/5
    wpm = (words/seconds) * 60
    print(f"Words per minute: {wpm}")

    # Prompt them to try again
    input("Press enter to try again.")
    typing_test()



typing_test()