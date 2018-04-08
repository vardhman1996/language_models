import numpy as np
import pandas as pd

STOP_CHAR = '\u0003' # U+0003 \x03
START_CHAR = '\u0002' # U+0002 \x02
NUM_SENTENCES = 500
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
            if (i > NUM_SENTENCES): break
            sentence = sentence.lower()
            sentence_chars = [c for c in sentence]
            temp_sentence = sentence_chars + [STOP_CHAR]

            # list of all characters in this dataset for frequences
            # char_list += temp_sentence

            # list of char-split sentences to make ngrams
            sentence_list = sentence_list + [temp_sentence]

    return np.array(sentence_list)


def main():
    sentences_df = read_data(DATA, lang=['eng', 'cmn'])
    # print(sentences_df.loc[sentences_df['lang'] == sentences_df['lang'].unique()[0]])
    sentences_df.to_csv("data/languages.csv", sep="\t", index=False, header=None)
    sentence_list = get_sentences(sentences_df)

    print(sentence_list[:10])


    # freq_dist = nltk.FreqDist(char_list)
    # print([char for (char, count) in freq_dist.most_common()])


if __name__ == "__main__":
    main()