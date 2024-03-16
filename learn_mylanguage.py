import wortschatz_wrapper as wsw
from core import main_loop

# Where the dictionary is located
dictionary_folder_path = 'language_pack/en_example_2014_pack'

# Where the database of learned words is located. If it doesn't exist, it will be created
database_path = 'my_en_words.xlsx'


# Program start

dutch = wsw.dictionary_reader(dictionary_folder_path, read_words=True, read_sentences=True)

main_loop(database_path, dutch.words, dutch.sentences, n_words_per_cycle=6)