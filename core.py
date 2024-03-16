import pandas as pd, openpyxl, os, sys, random
from termcolor import colored
from enum import Enum
import threading

'''
This program aims to create/update a python dictionary that contain the dutch word as key, and the value is another dictionary that contain:
- word meaning
- word type (verb, noun, etc)
- word example
- word comments
- verb conjugation
'''


def get_sentence(word, sentences, result, index, randomize_sentences=False):
    if randomize_sentences:
        import random
        new_sentence_list = sentences.copy()
        random.shuffle(new_sentence_list)
        for sentence in new_sentence_list:
            if word in sentence.split():
                result[index] = sentence
                return
    else:
        # return the first sentence that contains the word without scanning the whole list
        for sentence in sentences:
            if word in sentence.split():
                result[index] = sentence
                return

def main_loop(database_path, dictionary_words, dictionary_sentences=None, n_words_per_cycle=6):
    pd.set_option('display.max_colwidth', None)

    if not os.path.exists(database_path):
        print(f'Created new database at {database_path}')
        df = pd.DataFrame({'Word': '', 'Prec. article': '', 'Type': '', 'Meaning': '', 'Verb forms': '', 'Comments': '', 'Example': ''}, index=[0])
    else:
        print(f'Using existing database at {database_path}')
        df = pd.read_excel(database_path)
    df = df.astype(str)
    # As it got converted to string, now it may have nan values. Replace them with empty strings
    df = df.replace('nan', '')


    new_words = list(set(dictionary_words) - set(df['Word']))
    saved_words = list(df['Word'])


    class WorkMode(Enum):
        ASK_SAVED_WORDS = '[1] Be asked about learned words'
        ASK_NEW_WORDS = '[2] Be asked about new words'
        ASK_WORDS = '[3] Be asked about learned and new words'

    # define a lambda function to get the workmode from a number
    def get_workmode(x):
        for y in WorkMode:
            if y.value[1] == str(x):
                return y
        return None

    class WordDict(Enum):
        WORD = '[1] Prec. article'
        TYPE = '[2] Type'
        MEANING = '[3] Meaning'
        VERB_FORMS = '[4] Verb forms'
        COMMENTS = '[5] Comments'
        EXAMPLE = '[6] Example'
        SHOW_ALL = '[0] Show all'

    def get_worddict(x):
        for y in WordDict:
            if y.value[1] == str(x):
                return y
        return None


    proceed = True
    while proceed:
        print(f'What do you want to do?')
        for mode in WorkMode: print(mode.value)
        # get single input from user
        mode = input()
        if mode == '\x1b' or mode == '':
            break
        workmode = get_workmode(mode)
        if workmode == WorkMode.ASK_SAVED_WORDS:
            n_words = min(n_words_per_cycle, len(saved_words))
            if n_words == 0: print('No saved words to ask about.')
            words = random.sample(saved_words, n_words)
            if dictionary_sentences is not None:
                # open a thread for each word. Asynchronous. use threading
                example_sentences = [None for _ in range(n_words)]
                threads = [threading.Thread(target=get_sentence, args=(word, dictionary_sentences, example_sentences, i, True)) for i, word in enumerate(words)]
                for thread in threads: thread.start()
            keep_asking_words = True
            for i, word in enumerate(words):
                if not keep_asking_words: break
                keep_asking_info = True
                displayed_sentence = False
                while keep_asking_info:
                    print(f'What do you know about ', colored(word, 'green'), ' ?')
                    for field in WordDict: print(field.value)
                    if dictionary_sentences is not None and not displayed_sentence:
                        # join the thread
                        threads[i].join()
                        print('Here is an example: ', colored(example_sentences[i], 'green'))
                        displayed_sentence = True
                    choice = input()
                    if choice == '\x1b':
                        keep_asking_words = keep_asking_info = False
                    if choice == '':
                        keep_asking_info = False
                    else:
                        worddict = get_worddict(choice)
                        if worddict == WordDict.SHOW_ALL:
                            found_word = df[df['Word'] == word]
                            if not found_word.empty:
                                print(found_word)
                        else:
                            print(f'What do you know about ', colored(word, 'green'), ' regarding ', colored(worddict.value, 'green'), ' ?')
                            new_value = input()
                            if new_value == '\x1b' or new_value == '':
                                keep_asking_info = False
                            else:
                                word_position = df.index[df['Word'] == word].tolist()
                                # if len(word_position) != 1:
                                #     print(colored(f'Warning: No word found or found more than one word with the same name {word}.', 'red'))
                                if len(word_position) == 0:
                                    word_position = len(df)
                                    df.at[word_position, 'Word'] = word
                                    df.at[word_position, worddict.value[4:]] = new_value
                                elif len(word_position) == 1:
                                    df.at[word_position[0], worddict.value[4:]] = new_value
            # close the threads
            if dictionary_sentences is not None:
                for thread in threads: thread.join()
        elif workmode == WorkMode.ASK_NEW_WORDS:
            n_words = min(n_words_per_cycle, len(new_words))
            words = random.sample(new_words, n_words)
            keep_asking_words = True
            if dictionary_sentences is not None:
                # open a thread for each word. Asynchronous. use threading
                example_sentences = [None for _ in range(n_words)]
                threads = [threading.Thread(target=get_sentence, args=(word, dictionary_sentences, example_sentences, i, True)) for i, word in enumerate(words)]
                for thread in threads: thread.start()
            for i, word in enumerate(words):
                if not keep_asking_words: break
                keep_asking_info = True
                displayed_sentence = False
                while keep_asking_info:
                    print(f'What do you know about ', colored(word, 'green'), ' ?')
                    for field in WordDict: print(field.value)
                    if dictionary_sentences is not None and not displayed_sentence:
                        # join the thread
                        threads[i].join()
                        print('Here is an example: ', colored(example_sentences[i], 'green'))
                        displayed_sentence = True
                    choice = input()
                    if choice == '\x1b':
                        keep_asking_info = keep_asking_words = False
                    elif choice == '':
                        keep_asking_info = False
                    else:
                        worddict = get_worddict(choice)
                        print(f'What do you know about ', colored(word, 'green'), ' regarding ', colored(worddict.value, 'green'), ' ?')
                        new_value = input()
                        if new_value == '\x1b' or new_value == '':
                            keep_asking_info = False
                        else:
                            word_position = df.index[df['Word'] == word].tolist()
                            # if len(word_position) > 0:
                            #     print(colored(f'Warning: found more than one word with the same name {word}.', 'red'))
                            if len(word_position) == 0:
                                word_position = len(df)
                                df.at[word_position, 'Word'] = word
                                df.at[word_position, worddict.value[4:]] = new_value
                            elif len(word_position) == 1:
                                df.at[word_position[0], worddict.value[4:]] = new_value
            # close the threads
            if dictionary_sentences is not None:
                for thread in threads: thread.join()
        elif workmode == WorkMode.ASK_WORDS:
            n_words = min(n_words_per_cycle, len(dictionary_words))
            words = random.sample(dictionary_words, n_words)
            keep_asking_words = True
            if dictionary_sentences is not None:
                # open a thread for each word. Asynchronous. use threading
                example_sentences = [None for _ in range(n_words)]
                threads = [threading.Thread(target=get_sentence, args=(word, dictionary_sentences, example_sentences, i, True)) for i, word in enumerate(words)]
                for thread in threads: thread.start()
            for word in words:
                if not keep_asking_words: break
                keep_asking_info = True
                displayed_sentence = False
                while keep_asking_info:
                    print(f'What do you know about ', colored(word, 'green'), ' ?')
                    for field in WordDict: print(field.value)
                    if dictionary_sentences is not None and not displayed_sentence:
                        # join the thread
                        threads[i].join()
                        print('Here is an example: ', colored(example_sentences[i], 'green'))
                        displayed_sentence = True
                    choice = input()
                    if choice == '\x1b':
                        keep_asking_info = keep_asking_words = False
                    elif choice == '':
                        keep_asking_info = False
                    else:
                        worddict = get_worddict(choice)
                        if worddict == WordDict.SHOW_ALL:
                            found_word = df[df['Word'] == word]
                            if not found_word.empty:
                                print(found_word)
                        else:
                            print(f'What do you know about ', colored(word, 'green'), ' regarding ', colored(worddict.value, 'green'), ' ?')
                            new_value = input()
                            if new_value == '\x1b' or new_value == '':
                                keep_asking_info = False
                            else:
                                # Find the word in the database, and update the corresponding existing field, or create a new field
                                word_position = df.index[df['Word'] == word].tolist()
                                if len(word_position) == 0:
                                    word_position = len(df)
                                    df.at[word_position, 'Word'] = word
                                    df.at[word_position, worddict.value[4:]] = new_value
                                elif len(word_position) == 1:
                                    df.at[word_position[0], worddict.value[4:]] = new_value
                                # else:
                                #     print(colored(f'Warning: found more than one word with the same name {word}.', 'red'))
        else:
            print('Invalid input. Please try again.')
            continue

    # save the updated database
    df.to_excel(database_path, index=False)
