import requests
import time
from requests.exceptions import RequestException


def check_word_frequency(word):
    # Google Books Ngram Viewer API URL
    url = f"https://books.google.com/ngrams/json?content={word}&year_start=1800&year_end=2019&corpus=26&smoothing=3"

    try:
        # Fetch data from the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        # Extract frequency information
        if data:
            timeseries = data[0].get("timeseries", [])
            if timeseries:
                total_count = sum(timeseries)
                if total_count > 0:
                    # Check if the word appears frequently enough
                    if (
                        max(timeseries) / total_count >= 0.01
                    ):  # Adjust this threshold as needed
                        return True
    except RequestException as e:
        print("Error fetching data:", e)
    except Exception as e:
        print("Error processing word:", word)
        print("Error:", e)
    return False


def filter_words(words, output_file_path):
    # Check if the output file exists and load existing filtered words
    existing_words = set()
    try:
        with open(output_file_path, "r") as output_file:
            existing_words = set(output_file.read().splitlines())
    except FileNotFoundError:
        pass

    for i, word in enumerate(words):
        if word in existing_words:
            print(f"Word '{word}' already exists in the output file, skipping...")
            continue
        if check_word_frequency(word):
            # Save the word to the file
            save_to_file([word], output_file_path)
        # Print progress percentage
        progress = (i + 1) / len(words) * 100
        print(f"Progress: {progress:.2f}% completed", end="\r")
        time.sleep(1)  # Add a delay of 1 second between requests
    print("\n")  # Print newline after progress completion


def read_word_list(file_path):
    with open(file_path, "r") as file:
        word_list = [line.strip() for line in file]
    return word_list


def save_to_file(words, file_path):
    with open(
        file_path, "a"
    ) as file:  # Use "a" to append to the file instead of overwriting
        for word in words:
            file.write(word + "\n")
            print(f"Word '{word}' saved to:", file_path)


# File paths
input_file_path = "word_list.txt"
output_file_path = "filtered_word_list.txt"

# Read the word list from the file
word_list = read_word_list(input_file_path)

# Filter the words
filter_words(word_list, output_file_path)

print("All words processed and saved to:", output_file_path)
