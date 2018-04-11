import nltk
import data_manipulation as dm
from collections import Counter
import pickle as pkl
import os
from ngram_model import Ngram
from linear_interpolation import LinearInterpolation

DATA = "data/sentences.csv"
MODEL = "models/"
N = 5
UNK_CHAR = '\u0001'
WEIGHTS = [0.01, 0.04, 0.15, 0.3, 0.5]
LOAD_WILI = True


def make_ngrams(sentences, n=1):
    """
    make ngrams from the list of sentences passed and the n value
    :return: list of ngrams
    """
    ngrams = []
    i = 0
    # start symbol based on the n-gram
    start_sym_list = [dm.START_CHAR] * (n - 1)
    for sentence_char in sentences:
        if i % 10000 == 0: print("Done: ", i, " n: ", n)
        i += 1
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
    sentences_df = dm.read_data(DATA)
    sentence_list = dm.get_sentences(sentences_df)

    print("sentence_list len: ", len(sentence_list), "unique lang", len(set(sentences_df['lang'].values)))

    # load wili data
    if LOAD_WILI:
        sentences_wili = dm.get_wili_data()
        sentence_list += sentences_wili

    # unking
    # print("Unking characters")
    # unigram = make_ngrams(sentence_list, n=1)
    # unk_chars = get_unk_chars(unigram)
    # print("Num chars unked: ", len(unk_chars))
    # sentence_list = replace_unks(sentence_list, unk_chars)
    # print("Unking over")

    print("Ngrams generation started")
    unigram = make_ngrams(sentence_list, n=1)
    f_dist_unigram = Counter(unigram)

    unigram_model = Ngram(f_dist_unigram, f_dist_unigram, 1, len(sentence_list))
    # unigram_model.model[(UNK_CHAR,)] = max(1, unigram_model.model[UNK_CHAR] )

    models = [unigram_model]
    f_dist_part_ngram = f_dist_unigram
    for i in range(2, N + 1, 1):
        ngram = make_ngrams(sentence_list, i)
        f_dist_ngram = Counter(ngram)
        ngram_model = Ngram(f_dist_ngram, f_dist_part_ngram, n=i, num_starts=len(sentence_list), k=0.001)
        models += [ngram_model]
        f_dist_part_ngram = f_dist_ngram

    lin_interpolation = LinearInterpolation(models, WEIGHTS)
    # save model
    save_model(lin_interpolation, "lin_interpolate_model_no_unk.pkl")
    return 0


if __name__ == "__main__":
    main()