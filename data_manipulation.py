import pandas as pd
import codecs
import numpy as np

STOP_CHAR = '\u0003' # U+0003 \x03
START_CHAR = '\u0002' # U+0002 \x02
NUM_SENTENCES = 5000
DATA = "data/sentences.csv"


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
    # char_list = []
    sentence_list = []

    # get all unique languages
    languages = sentences_df['lang'].unique()

    for lang in languages:
        data_df = sentences_df.loc[sentences_df['lang'] == lang]
        data = data_df['sent'].values
        i = 0
        for sentence in data:
            i += 1
            if (i > NUM_SENTENCES):
                print("Tatoeba DATA done")
                break
            sentence = sentence.lower() # all sentences are lower cased
            sentence_chars = [c for c in sentence]
            temp_sentence = sentence_chars + [STOP_CHAR]

            # list of char-split sentences to make ngrams
            sentence_list = sentence_list + [temp_sentence]

    return sentence_list


def break_sentences(data):
    i = 0
    sentence_list = []
    for sentence in data:
        i += 1
        if i % 5000 == 0:
            print("Done: ", i)
        sentence = sentence.lower()  # all sentences are lower cased
        sentence_chars = [c for c in sentence]
        temp_sentence = sentence_chars + [STOP_CHAR]

        # list of char-split sentences to make ngrams
        sentence_list = sentence_list + [temp_sentence]

    return sentence_list



def get_wili_data():
    DATA_TRAIN = "data/wili-2018/x_train.txt"
    DATA_TEST = "data/wili-2018/x_test.txt"

    data_train = codecs.open(DATA_TRAIN, encoding='utf-8')
    # data_test = codecs.open(DATA_TEST, encoding='utf-8')

    sentences_train = break_sentences(data_train)
    print("Length train: ", len(sentences_train))

    # sentences_test = break_sentences(data_test)
    # print("Length test: ", len(sentences_test))

    return sentences_train


# def main():
#     sentences_df = read_data(DATA, lang=['eng', 'cmn'])
#     # print(sentences_df.loc[sentences_df['lang'] == sentences_df['lang'].unique()[0]])
#     sentences_df.to_csv("data/languages.csv", sep="\t", index=False, header=None)
#     sentence_list = get_sentences(sentences_df)
#
#     print(sentence_list[:10])
#
#
#     # freq_dist = nltk.FreqDist(char_list)
#     # print([char for (char, count) in freq_dist.most_common()])
#
#
# if __name__ == "__main__":
#     main()