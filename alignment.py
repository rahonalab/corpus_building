import re
import string
import unicodedata
from difflib import get_close_matches
import sys

# Define the file paths
conllu_file_path = '/Users/gopal/Desktop/awesome-align-master/AnnConllu/100YearsSolitude_German.conllu'
alignment_file_path = '/Users/gopal/Desktop/awesome-align-master/examples/100YearsSolitude_English-German-word'
output_file_path = '/Users/gopal/Desktop/awesome-align-master/100YearsSolitude_German_with_alignment.conllu'
log_file_path = '/Users/gopal/Desktop/awesome-align-master/unaligned_words.log'
print_log_file_path = '/Users/gopal/Desktop/awesome-align-master/process_log.txt'

# Redirect print statements to a log file
sys.stdout = open(print_log_file_path, 'w', encoding='utf-8')

# Load the English-German alignment pairs
alignment_pairs = []
with open(alignment_file_path, 'r', encoding='utf-8') as alignment_file:
    for line in alignment_file:
        alignment_pairs.append([pair.split('<sep>') for pair in line.strip().split()])

# Initialize variables for processing the CoNLL-U file
output_lines = []
current_sentence_index = 0
unaligned_words = []

# Function to normalize and clean words for comparison
def normalize_word(word):
    return unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8').lower().strip(string.punctuation)

# Read the CoNLL-U file and process each token
with open(conllu_file_path, 'r', encoding='utf-8') as conllu_file:
    for line in conllu_file:
        if line.startswith("#") or line.strip() == "":
            # Add comments and blank lines as they are
            output_lines.append(line)
        else:
            # Process token lines
            columns = line.strip().split('\t')
            if len(columns) >= 2:
                german_word = columns[1]
                cleaned_german_word = normalize_word(german_word)

                print(f"Processing German word: {german_word} (cleaned: {cleaned_german_word}) in sentence {current_sentence_index}")

                # Find corresponding English word(s) for the current sentence
                if current_sentence_index < len(alignment_pairs):
                    sentence_pairs = alignment_pairs[current_sentence_index]

                    print(f"Current sentence pairs: {sentence_pairs}")

                    # Attempt exact matching
                    matching_indices = [
                        i for i, pair in enumerate(sentence_pairs)
                        if normalize_word(pair[1]) == cleaned_german_word
                    ]

                    if not matching_indices:
                        # Attempt fuzzy matching if no exact match
                        print(f"No exact match for: {german_word}. Attempting fuzzy matching...")
                        potential_matches = get_close_matches(
                            cleaned_german_word, [normalize_word(pair[1]) for pair in sentence_pairs], n=1, cutoff=0.7
                        )
                        print(f"Fuzzy match results: {potential_matches}")
                        if potential_matches:
                            closest_match = potential_matches[0]
                            matching_indices = [
                                i for i, pair in enumerate(sentence_pairs)
                                if normalize_word(pair[1]) == closest_match
                            ]

                    if matching_indices:
                        # Use the first matching pair
                        english_word = sentence_pairs.pop(matching_indices[0])[0]
                        print(f"Aligned: {german_word} -> {english_word}")

                        # Add alignment information to the Misc column
                        if len(columns) == 10:
                            if columns[9] == "_":
                                columns[9] = f"alignment={english_word}"
                            else:
                                columns[9] += f"|alignment={english_word}"
                    else:
                        # Log unaligned word
                        unaligned_words.append(german_word)
                        print(f"No match found for: {german_word} in sentence {current_sentence_index}")
                else:
                    # If sentence index exceeds alignment pairs, log the issue
                    print(f"Sentence index {current_sentence_index} exceeds alignment pairs.")
                    unaligned_words.append(german_word)

                output_lines.append('\t'.join(columns) + '\n')
            else:
                output_lines.append(line)

        # Increment sentence index after the end of a sentence
        if line.strip() == "":
            print("\n--- End of Sentence ---\n")
            current_sentence_index += 1

# Write the modified CoNLL-U file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.writelines(output_lines)

# Log unaligned words
if unaligned_words:
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        log_file.write("Unaligned Words:\n")
        for word in unaligned_words:
            log_file.write(word + '\n')

print(f"Annotated CoNLL-U file has been saved to {output_file_path}")
print(f"Unaligned words have been logged to {log_file_path}")

# Close the redirected stdout
sys.stdout.close()
