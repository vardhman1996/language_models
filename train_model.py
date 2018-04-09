import nltk
import data_manipulation as dm
from collections import Counter
import pickle as pkl
import os
from ngram_model import Ngram
from linear_interpolation import LinearInterpolation

DATA = "data/test.csv"
MODEL = "models/"
N = 5
UNK_CHAR = '\u0001'
WEIGHTS = [0.01, 0.04, 0.15, 0.3, 0.5]


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


def get_unk_chars(unigram):
    unigram_counts = Counter(unigram)
    unk_chars = []
    for k, v in unigram_counts.items():
        if v == 1:
            unk_chars += [k[0]]
    return unk_chars

def replace_unks(old_sentences, unk_chars):
    new_sentences = []
    for sentence in old_sentences:
        for i, char in enumerate(sentence):
            if char in unk_chars:
                sentence[i] = UNK_CHAR
        new_sentences += [sentence]
    return new_sentences


def save_model(fdist, filename):
    with open(os.path.join(MODEL, filename), "wb") as model_file:
        pkl.dump(fdist, model_file)
    return 0


def main():
    # load and manipulate data
    sentences_df = dm.read_data(DATA, lang=['eng', 'cmn'])
    sentence_list = dm.get_sentences(sentences_df)

    # unigram = make_ngrams(sentence_list, n=1)
    # unk_chars = get_unk_chars(unigram)
    #
    # sentence_list = replace_unks(sentence_list, unk_chars)

    unigram = make_ngrams(sentence_list, n=1)
    f_dist_unigram = Counter(unigram)

    unigram_model = Ngram(f_dist_unigram, f_dist_unigram, 1)
    models = [unigram_model]

    f_dist_part_ngram = f_dist_unigram
    for i in range(2, N + 1, 1):
        ngram = make_ngrams(sentence_list, i)
        f_dist_ngram = Counter(ngram)


        ngram_model = Ngram(f_dist_ngram, f_dist_part_ngram, i)
        models += [ngram_model]

        f_dist_part_ngram = f_dist_ngram

    lin_interpolation = LinearInterpolation(models, WEIGHTS)


    # n = 3 # make ngrams
    # ngram_counts = make_ngrams(sentence_list, n=n)
    # part_ngram_counts = make_ngrams(sentence_list, n=n-1)
    # f_dist_ngram = Counter(ngram_counts)
    # f_dist_part_ngram = Counter(part_ngram_counts)
    # ngram_model = Ngram(f_dist_ngram, f_dist_part_ngram, n) # ngram model

    # save model
    save_model(lin_interpolation, "lin_interpolate_model.pkl")
    return 0


if __name__ == "__main__":
    main()