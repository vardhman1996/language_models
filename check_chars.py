import pandas as pd
import pickle as pkl
import codecs

DATA = "data/sentences.csv"
num = 6445797
dx = 64457

def read_data(datafile, lang=None):
    """
    read csv data from datafile and extract the languages passed
    :return:
    """
    sent_df = pd.read_csv(datafile, sep="\t", encoding="utf-8", names=['num', 'lang', 'sent'])

    if lang is not None:
        sent_df = sent_df.loc[sent_df['lang'].isin(lang)]

    return sent_df


def get_sentences(sentences_df):
    """
    break each sentence into characters
    :return: list of characters, list of sentence list
    """
    i = 0
    capital_set = set()
    lower_set = set()

    for sentence in sentences_df['sent'].values:
        if i % dx == 0: print((100*i)/num, "% done", i)
        i += 1

        for c in sentence:
            capital_set.add(c)
            lower_set.add(c.lower())

    return capital_set, lower_set



def break_sentences(data):
    i = 0
    capital_set = set()
    lower_set = set()
    for sentence in data:
        i += 1
        if i % 5000 == 0:
            print("Done: ", i)
        # sentence = sentence  # all sentences are lower cased
        for c in sentence:
            capital_set.add(c)
            lower_set.add(c.lower())


        # list of char-split sentences to make ngrams

    return capital_set, lower_set



def get_wili_data():
    DATA_TRAIN = "data/wili-2018/x_train.txt"
    DATA_TEST = "data/wili-2018/x_test.txt"

    data_train = codecs.open(DATA_TRAIN, encoding='utf-8')
    data_test = codecs.open(DATA_TEST, encoding='utf-8')

    capital_set, lower_set = break_sentences(data_train)

    c_set, l_set = break_sentences(data_test)

    for c in c_set:
        capital_set.add(c)

    for l in l_set:
        lower_set.add(l)

    print("Cap: ", len(capital_set), "Lower: ", len(lower_set))

def main():
    # sentences_df = read_data(DATA)
    # capital_set, lower_set = get_sentences(sentences_df)
    # with open("models/capital.pkl", 'wb') as cap_file:
    #     pkl.dump(capital_set, cap_file)
    #
    # with open("models/lower.pkl", 'wb') as low_file:
    #     pkl.dump(lower_set, low_file)
    get_wili_data()


if __name__ == "__main__":
    main()