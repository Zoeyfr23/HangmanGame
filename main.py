# Hanged Man Functions

#building the game board
def build_board():
    word = input("Please enter a word: ")
    underscores = "_ " * len(word)
    print(underscores.strip())


# version 1 of validating the input
def validate_character(input_str):
    if not input_str:
        return "Invalid input"

    if len(input_str) > 1:
        if input_str.isalpha():
            return "E1"
        elif not all(char.isalpha() for char in input_str):
            return "E3"

    if len(input_str) == 1:
        if input_str.isalpha():
            return input_str.lower()
        else:
            return "E2"

    return "Invalid input"


#updated version 2 of validating the input
def is_valid_input(letter_guessed):
    # Check if the input is a single alphabetical letter
    return len(letter_guessed) == 1 and letter_guessed.isalpha()


#updated version 3 of validating the input
def check_valid_input(letter_guessed, old_letters_guessed):
    letter_guessed = letter_guessed.lower()
    old_letters_guessed = [letter.lower() for letter in old_letters_guessed]

    if len(letter_guessed) != 1 or not letter_guessed.isalpha():
        return False

    if letter_guessed in old_letters_guessed:
        return False

    return True

#updating the guessed letters list
def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed.append(letter_guessed.lower())
        return True
    else:
        old_letters_guessed.sort()
        print("X")
        print(" -> ".join(old_letters_guessed))
        return False


#shows what letters where found and what missing- and where
def show_hidden_word(secret_word, old_letters_guessed):
    hidden_word = ''

    for letter in secret_word:
        if letter in old_letters_guessed:
            hidden_word += letter + ' '
        else:
            hidden_word += '_ '

    return hidden_word.strip()


#checking winning of the game (True if so, False otherwise)
def check_win(secret_word, old_letters_guessed):
    for letter in secret_word:
        if letter not in old_letters_guessed:
            return False

    return True


#prints hangman state
def print_hangman(num_of_tries, color="white"):
    color_codes = {
        "white": "\033[0m",
        "red": "\033[91m",
        "magenta": "\033[95m"
    }
    print(f"{color_codes[color]}{HANGMAN_PHOTOS[num_of_tries]}\033[0m")



#choose word from the file
def choose_word(file_path, index):
    with open(file_path, 'r') as file:
        words = file.read().split()

    unique_words = len(set(words))

    word_index = (index - 1) % len(words)
    secret_word = words[word_index]

    return unique_words, secret_word


# Get valid index input from the user
def get_valid_index(words_count):
    while True:
        index_input = input(f"Please enter an index between 1 and {words_count}: ")
        if index_input.isdigit():
            index = int(index_input)
            if 1 <= index <= words_count:
                return index
            else:
                print(f"Index out of range. Enter a number between 1 and {words_count}.")
        else:
            print("Invalid input. Please enter a valid number.")




#prints open screen
def open_screen():
    return  """Welcome to the game Hangman 
     _    _                                         
    | |  | |                                        
    | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
    |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
    | |  | | (_| | | | | (_| | | | | | | (_| | | | |
    |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                         __/ |                      
                         |___/ """

#hangman photos
def hangman_photos():
    return {
        1: "   x-------x",
        2: """        x-------x
        |
        |
        |
        |
        |""",
        3: """        x-------x
        |       |
        |       0
        |
        |
        |""",
        4: """        x-------x
        |       |
        |       0
        |       |
        |
        |""",
        5: """        x-------x
        |       |
        |       0
        |      /|\\
        |
        |""",
        6: """        x-------x
        |       |
        |       0
        |      /|\\
        |      /
        |""",
        7: """        x-------x
        |        |
        |        0
        |       /|\\
        |       / \\
        |"""
    }


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    MAX_TRIES = 6
    HANGMAN_ASCII_ART = open_screen()
    HANGMAN_PHOTOS = hangman_photos()
    guessed_letters = []
    hangman_state = 1

    # Print the opening screen
    print(HANGMAN_ASCII_ART)

    # Player enters text file path + index
    file_path = input("Please enter text file path: ")

    # Count the unique words in the file
    with open(file_path, 'r') as file:
        words = file.read().split()
    unique_words_count = len(set(words))

    # Get a valid index input from the user
    index_file = get_valid_index(unique_words_count)

    # Save the secret word
    unique_words, secret_word = choose_word(file_path, index_file)

    # Print hangman and lines for the secret word
    print_hangman(hangman_state)
    print(show_hidden_word(secret_word, guessed_letters))

    while hangman_state <= MAX_TRIES:
        letter = input("Guess a letter: ").lower()

        if check_valid_input(letter, guessed_letters):
            guessed_letters.append(letter)

            if letter not in secret_word:
                hangman_state += 1
                print("):")
                print_hangman(hangman_state)

            if check_win(secret_word, guessed_letters):
                print(show_hidden_word(secret_word, guessed_letters))
                print_hangman(hangman_state, color="magenta")
                print("\033[95mWIN!\033[0m")
                break
        else:
            try_update_letter_guessed(letter, guessed_letters)

        print(show_hidden_word(secret_word, guessed_letters))

    else:
        print_hangman(7, color="red")
        print("\033[91mLOSE! The word was:\033[0m", secret_word)

