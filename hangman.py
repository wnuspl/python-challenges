from openai import OpenAI

# My API key is within openai_test_key.txt
# You can import the key this way, or just write something like OPENAI_KEY = "[your api key]"
with open("openai_test_key.txt", "r") as f:
    OPENAI_KEY = f.read()

client = OpenAI(api_key=OPENAI_KEY)


# Used for choosing word
MIN_DIFFICULTY = 1
MAX_DIFFICULTY = 5


# Generates a random word with the specified difficulty using AI
def random_word(difficulty=1):
    prompt = (
        "Generate a random word to be used in a hangman-style game"
        f"If difficulty of {MIN_DIFFICULTY} means that almost everyone knows this word and {MAX_DIFFICULTY} means that no one knows this word, generate a word of difficulty {difficulty}."
        "Respond with only a single word, all lowercase, no punctuation"
    )
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    return response.output_text.strip().lower()


# Prompts the user to choose a difficulty
def get_difficulty():
    prompt = f"Please provide a difficulty ({MIN_DIFFICULTY}-{MAX_DIFFICULTY}): "
    difficulty = -1
    valid_difficulty_chosen = False
    while not valid_difficulty_chosen:
        candidate = input(prompt).strip()
        if candidate.isdigit() and MAX_DIFFICULTY >= int(candidate) >= MIN_DIFFICULTY:
            valid_difficulty_chosen = True
            difficulty = int(candidate)
    return difficulty

# Creates brief definition for the provided word using AI
def get_definition(word):
    prompt = (
        f"Provide a single sentence definition of the word \"{word}\" using simple language in the format of {word}: definition"
    )
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    return response.output_text.strip().lower()



# We wrap the game into a function so that we can easily restart once they finish
def play():
    # Prompt user to select difficulty
    difficulty = get_difficulty()

    # Choose a word
    print("Choosing word...")
    word = random_word(difficulty)
    print("I chose a word!")

    guessed_letters = []
    guessed = False
    while not guessed:

        # we build display to show all the guessed letters and blanks
        display = ""
        missing = 0
        for letter in word:
            if letter in guessed_letters:
                display += letter
            else:
                display += "_"
                missing += 1

        # When missing == 0, the player has guessed all the letters, so we know the word!
        if missing == 0:
            print(f"You guessed the word in {len(guessed_letters)} guesses!")
            print(f"The word was {word}.")
            print(get_definition(word))
            break


        # If they didn't win, we show the current state
        print(display)
        incorrect = [letter for letter in guessed_letters if letter not in word]
        print("Incorrect guesses:", ", ".join(incorrect))

        # Continue to get another non-guessed letter
        valid_guess = False
        while not valid_guess:
            prompt = "Guess a letter: "
            letter = (input(prompt)).strip()[0].lower()
            if letter.isalpha() and letter not in guessed_letters:
                valid_guess = True
                guessed_letters.append(letter)


    # (This is outside the loop)
    # Prompt the user to play again
    input("Press enter to play again")
    play()

play()
