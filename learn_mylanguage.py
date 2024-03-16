import wortschatz_wrapper as wsw
from core import main_loop

###  Configuration

# Where the dictionary is located
dictionary_folder_path = 'language_pack/en_example_2014_pack'

# n of most frequent words to be used
n_words = 10000

# Where the database of learned words is located. If it doesn't exist, it will be created
database_path = 'my_en_words.xlsx'



###  Program start

dictionary_wrapper = wsw.dictionary_reader(dictionary_folder_path, read_words=True, read_sentences=True)

# restrict the words to the 'n_words' most frequent words
dictionary_wrapper.words = dictionary_wrapper.words[:n_words]

main_loop(database_path, dictionary_wrapper.words, dictionary_wrapper.sentences, n_words_per_cycle=6)