import os
MAX_TRIES = 6

def print_start():
    """Prints the opening screen of the game.
    :return: None
    """
    HANGMAN_ASCII_ART = """Welcome to the game Hangman
      _    _                                         
     | |  | |                                        
     | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
     |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
     | |  | | (_| | | | | (_| | | | | | | (_| | | | |
     |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                          __/ |                      
                         |___/\n"""
    print(HANGMAN_ASCII_ART, MAX_TRIES)

def choose_word(file_path, index):
    """Chooses a word from a text file based on the given index.
    :param file_path: The path to the text file containing a list of words separated by spaces.
    :type file_path: str
    :param index: The position of the word to be chosen from the file.
    :type index: int
    :return: The word at the specified index.
    :rtype: str
    """
    # Read words from the text file
    with open(file_path, 'r') as file:
        words = file.read().split()
    # Get the word at the specified index (circular counting)
    chosen_word_index = (index - 1) % len(words)
    chosen_word = words[chosen_word_index]
    return chosen_word



def print_hangman(num_of_tries):
    """Prints the hangman image corresponding to the number of incorrect guesses.
    :param num_of_tries: The number of incorrect guesses made by the player.
    :type num_of_tries: int
    :return: None
    """
    HANGMAN_PHOTOS = {0: "      x-------x",
                      1: """        x-------x
        |
        |
        |
        |
        |
    """,
                      2: """        x-------x
        |       |
        |       0
        |
        |
        |""",
                      3: """        x-------x
        |       |
        |       0
        |       |
        |
        |
    """,
                      4: """        x-------x
        |       |
        |       0
        |      /|\\
        |
        |""",
                      5: """        x-------x
        |       |
        |       0
        |      /|\\
        |      /
        |""",
                      6: """        x-------x
        |       |
        |       0
        |      /|\\
        |      / \\
        |"""}
    print(HANGMAN_PHOTOS[num_of_tries])

def show_hidden_word(secret_word, old_letters_guessed):
    """Reveals the guessed letters in the secret word and hides the remaining letters with underscores.
    :param secret_word: The secret word that the player needs to guess.
    :type secret_word: str
    :param old_letters_guessed: List of letters that have been guessed so far.
    :type old_letters_guessed: list
    :return: A string representing the hidden word with guessed letters revealed and others as underscores.
    :rtype: str
    """
    returned_word = ""
    for letter in secret_word:
        if (letter in old_letters_guessed):
            returned_word += letter + " "
        else:
            returned_word += "_ "
    return returned_word


def check_valid_input(letter_guessed, old_letters_guessed):
    """Checks if the input character is valid and hasn't been guessed before.
    :param letter_guessed: The input character to be validated.
    :type letter_guessed: str
    :param old_letters_guessed: List of characters that have been guessed before.
    :type old_letters_guessed: list
    :return: True if the input character is a single alphabetical letter and hasn't been guessed before, False otherwise.
    :rtype: bool
    """
    if ((len(letter_guessed) > 1) or (not letter_guessed.isalpha())):
        return False
    else:
        if (letter_guessed.lower() in old_letters_guessed):
            return False
    return True

def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """Tries to update the list of guessed letters with the input character.
    :param letter_guessed: The input character to be added to the list of guessed letters.
    :type letter_guessed: str
    :param old_letters_guessed: List of characters that have been guessed before.
    :type old_letters_guessed: list
    :return: True if the input character is successfully added to the list of guessed letters, False otherwise.
    :rtype: bool
    """
    if check_valid_input(letter_guessed,old_letters_guessed):
        old_letters_guessed += letter_guessed
        return True
    else:
        print("X")
        old_letters_guessed = set(old_letters_guessed)
        print(' -> '.join(sorted(old_letters_guessed)))
        return False

def check_win(secret_word, old_letters_guessed):
    """Checks if all the letters in the secret word have been guessed and the player won.
    :param secret_word: The word to be guessed.
    :type secret_word: str
    :param old_letters_guessed: List of previously guessed letters.
    :type old_letters_guessed: list
    :return: True if all the letters in the secret word have been guessed, False otherwise.
    :rtype: bool
    """
    for letter in secret_word:
        if (letter not in old_letters_guessed):
            return False
    return True

def hangman(secret_word):
    num_of_tries = 0
    old_letters_guessed = []
    #Print the first drawing in the game
    print_hangman(num_of_tries)

    while num_of_tries < MAX_TRIES:
        print("Secret word:", show_hidden_word(secret_word, old_letters_guessed))
        guess = input("Guess a letter: ").lower()

        if not try_update_letter_guessed(guess, old_letters_guessed):
            continue

        # Check if the guessed letter is in the secret word
        if guess in secret_word:
            old_letters_guessed.append(guess)
        else:
            num_of_tries += 1
            print(":(")
            print_hangman(num_of_tries)

        # Check if the player has won
        if check_win(secret_word, old_letters_guessed):
            print("WIN")
            break

    #Chack if the player reached the max tries
    if num_of_tries == MAX_TRIES:
        print("LOSE")


def main():
    print_start()
    #Ask the user for input of the file path and word index.
    words_file_path = input("Please enter the file path containing words: ")
    normalized_file_path = os.path.normpath(words_file_path)
    index = int(input("Please enter the index of the word in the file: "))

    secret_word = choose_word(normalized_file_path,index)
    hangman(secret_word)



if __name__ == '__main__':
    main()
