# Random Word Generator with Word Validation

This Python script generates random strings and identifies legitimate English words within those strings. It measures the execution time and provides statistics on the number of words produced and the percentage of legitimate English words found.

## Usage

1. Ensure you have the required Python packages installed (`enchant`, `colorama`).
2. Run the script using a Python interpreter.
3. Enter the desired number of seconds to run the script when prompted.
4. The script will generate random strings and display them, highlighting legitimate English words in green.
5. After the specified duration, the script will provide statistics on the generated words and the percentage of legitimate English words found.

## Requirements

- Python 3.x
- `enchant` library (to check for legitimate English words)
- `colorama` library (to display colored output)

## How it Works

1. The script uses the `random` module to generate random strings and the `time` module to measure the execution time.
2. The `generate_random_string(length)` function generates a random string of the specified length using lowercase and uppercase letters, as well as spaces.
3. The `find_words_in_string(s)` function:
   - Uses the `enchant` library to create an English dictionary object.
   - Extracts words from a given string using regular expressions.
   - Checks each word against the dictionary and filters out non-English words or single-character words.
   - Returns a list of legitimate English words.
4. The `main()` function:
   - Prompts the user to enter the number of seconds to run the script.
   - Sets the end time for the script execution based on the user's input.
   - Initializes variables to keep track of the word statistics.
   - Generates random strings and identifies legitimate words until the time limit is reached.
   - Displays the strings, highlighting legitimate words in green using the `colorama` library.
   - Calculates and outputs statistics, including the total words produced, total legitimate English words found, and the percentage of legitimate words.
   - Outputs the list of legitimate words encountered during the execution.

## Note

- The script uses a basic English dictionary to identify legitimate English words. Depending on your requirements, you may need to adjust or use more comprehensive word lists.
- The execution time of the script is determined by the user's input. Keep in mind that longer durations may lead to more statistically significant results.
- This script is primarily intended for demonstration and educational purposes, and the word validation is based on simple criteria. It may not capture all legitimate English words or handle complex language structures efficiently.