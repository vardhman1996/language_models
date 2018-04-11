from ngram_model import Ngram
import numpy as np
import math
import time
from multiprocessing import Pool
import multiprocessing as mp
import os

class LinearInterpolation:
    START_CHAR = '\u0002'  # U+0002 \x02
    UNK_CHAR = '\u0001'
    V = 65424
    def __init__(self, models, weights):
        self.models = models
        self.unigram = models[0] # unigram model
        self.weights = weights


    def set_seed(self, seed):
        np.random.seed(seed)


    def get_probability(self, character, context):
        # character = self.check_unk(character)
        prob_list = []
        not_zero_denom = []
        total_prob = 0

        for i, model in enumerate(self.models):
            model_context = [self.START_CHAR] * (model.get_n() - 1) + context
            total_prob += self.weights[i] * model.get_probability(character, model_context)
            prob_list.append(model.get_probability(character, model_context))
        # print(prob_list)
            # prob, denom = model.get_probability(character, model_context)
            # if not denom:
            #     not_zero_denom.append(i)
            # prob_list.append(prob)
        # total_prob = self.redistribute_prob(prob_list, not_zero_denom)
        return math.log(total_prob, 2)


    # def redistribute_prob(self, prob, zero_denom):
    #     weights = np.array(self.weights)
    #     weights = weights / np.sum(weights[zero_denom])
    #     total_prob = 0
    #     for i, p in enumerate(prob):
    #             total_prob += weights[i] * p
    #     return total_prob

    #
    # def check_unk(self, character):
    #     if (character,) not in self.unigram.model.keys():
    #         return self.UNK_CHAR
    #     return character

    # TODO: too slow!!!!
    def generate_char(self, context):
        char_set = set(self.unigram.model.keys())
        # char_set.remove((self.UNK_CHAR,))

        char_list = list(char_set)
        myfunc.model = self
        myfunc.context = context

        with Pool(10) as p:
            char_probs = list(p.map(myfunc, char_list))

        s = np.sum(char_probs)
        char_probs = char_probs / np.sum(char_probs)
        character_list = []
        for c in char_list:
            character_list += c[0]
        gen_char = np.random.choice(character_list, 1, p=char_probs)

        print("sum_prob: ", s, "prob: ", self.get_probability(gen_char[0], context), "char_set size: ", len(char_set))
        return gen_char[0]

def myfunc(c):
    return 2 ** myfunc.model.get_probability(c[0], myfunc.context)
