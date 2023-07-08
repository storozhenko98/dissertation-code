import random
import time
import enchant
import re
from colorama import Fore, Style, init

init(autoreset=True)

def generate_random_string(length):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '
    return ''.join(random.choice(characters) for i in range(length))

def find_words_in_string(s):
    d = enchant.Dict("en_US")
    words = re.findall(r'\b\w+\b', s)
    return [word for word in words if d.check(word) and len(word) > 1]

def main():
    try:
        seconds = int(input("Enter the number of seconds to run the script: "))
    except ValueError:
        print("Please enter a valid number")
        return

    end_time = time.time() + seconds
    
    total_words = 0
    legit_words = 0
    legit_words_list = []

    while time.time() < end_time:
        random_string = generate_random_string(100)
        words = find_words_in_string(random_string)
        
        total_words += len(re.findall(r'\b\w+\b', random_string))
        legit_words += len(words)
        legit_words_list.extend(words)
        
        output_string = random_string
        for word in words:
            colored_word = f"{Fore.GREEN}{word}{Style.RESET_ALL}"
            output_string = output_string.replace(word, colored_word, 1)
            
        print(output_string)
        time.sleep(0.001)  # Sleep for half a second

    # Output stats
    print(f"\nTotal words produced: {total_words}")
    print(f"Total legitimate English words: {legit_words}")
    
    if total_words > 0:
        percentage = (legit_words / total_words) * 100
        print(f"Percentage of legitimate English words: {percentage:.2f}%")
    else:
        print("No words were generated.")
    
    # Output legitimate words
    if legit_words_list:
        print(f"Legitimate words encountered: {', '.join(legit_words_list)}")
    else:
        print("No legitimate words encountered.")

if __name__ == "__main__":
    main()
