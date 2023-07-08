import random
import string
import time

def generate_random_word(length):
    characters = string.ascii_lowercase
    return ''.join(random.choice(characters) for _ in range(length))

def main():
    target_word = input("Enter a word to generate: ")
    print(f"'{target_word}' contains {len(target_word)} characters.")
    print ("Generating...")
    start_time = time.time()
    generated_word = ''

    while generated_word != target_word:
        generated_word = generate_random_word(len(target_word))

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"The word '{target_word}' was generated in {elapsed_time:.4f} seconds.")

if __name__ == "__main__":
    main()
