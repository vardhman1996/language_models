import nltk
import data_manipulation as dm
from collections import Counter
import pickle as pkl
import os
from ngram_model import Ngram

DATA = "data/languages.csv"
MODEL = "models/"


def make_ngrams(sentences, n=1):
    """
    make ngrams from the list of sentences passed and the n value
    :return: list of ngrams
    """
    ngrams = []

    # start symbol based on the n-gram
    start_sym_list = [dm.START_CHAR] * (n - 1)
    for sentence_char in sentences:
        sentence_char = start_sym_list + sentence_char
        ngrams += list(nltk.ngrams(sentence_char, n))
    return ngrams


def save_model(fdist, filename):
    with open(os.path.join(MODEL, filename), "wb") as model_file:
        pkl.dump(fdist, model_file)
    return 0


def main():
    # load and manipulate data
    sentences_df = dm.read_data(DATA, lang=['eng'])
    sentence_list = dm.get_sentences(sentences_df)

    n = 5 # make ngrams
    ngram_counts = make_ngrams(sentence_list, n=n)
    part_ngram_counts = make_ngrams(sentence_list, n=n-1)
    f_dist_ngram = Counter(ngram_counts)
    f_dist_part_ngram = Counter(part_ngram_counts)
    ngram_model = Ngram(f_dist_ngram, f_dist_part_ngram, n) # ngram model

    # save model
    save_model(ngram_model, "{0}gram_model.pkl".format(n))
    return 0


if __name__ == "__main__":
    main()