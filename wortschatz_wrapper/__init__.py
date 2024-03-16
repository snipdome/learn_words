
import codecs
import os, sys, io




# def get_ranked():
#     path = os.path.dirname(os.path.abspath(__file__))

#     with open(os.path.join(path, 'dutch10000-utf8.txt')) as word_list:
#         return word_list.read().splitlines()



class dictionary_reader():

    files = {
        'words': '-words.txt',
        'sentences': '-sentences.txt',
    }

    def __init__(self, dictionary_folder_path, read_words=True, read_sentences=True):
        self.dictionary_folder_path = dictionary_folder_path
        self.dictionary_name = dictionary_folder_path.split('/')[-1]
        self.language = self.dictionary_name.split('_')[0]
        
        self.read_words() if read_words else None
        self.read_sentences() if read_sentences else None

    def read_words(self):
        # files are UTF-8 encoded
        with codecs.open(self.dictionary_folder_path + '/' + self.dictionary_name + self.files['words'], 'r', 'utf-8') as f:
            lines = f.read().splitlines()
            word_lines = [line.split('\t') for line in lines]            
            # remove words whose letters are not in the english alphabet
            word_lines = [line for line in word_lines if line[1].isalpha() and len(line) ==3]
            _, words_list, words_count = [list(i) for i in zip(*word_lines)]
            # order of words by frequency
            words, counts = zip(*sorted(zip(words_list, words_count), key=lambda x: int(x[1]), reverse=True))
            self.words, self.counts = words, counts
            self.words_dict = [{'word': word, 'count': count} for word, count in zip(words, counts)]

    def read_sentences(self):
        with codecs.open(self.dictionary_folder_path + '/' + self.dictionary_name + self.files['sentences'], 'r', 'utf-8') as f:
            lines = f.read().splitlines()
            lines = [line.split('\t') for line in lines if len(line.split('\t')) == 2]
            sentences_list = [line[1] for line in lines]
            self.sentences = sentences_list
    
    def get_sentence(self, word, randomize_sentences=False):
        if randomize_sentences:
            import random
            new_sentence_list = self.sentences
            random.shuffle(new_sentence_list)
            for sentence in new_sentence_list:
                if word in sentence.split():
                    return sentence
        else:
            # return the first sentence that contains the word without scanning the whole list
            for sentence in self.sentences:
                if word in sentence.split():
                    return sentence