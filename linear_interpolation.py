from ngram_model import Ngram
import numpy as np
import math

class LinearInterpolation:
    START_CHAR = '\u0002'  # U+0002 \x02
    UNK_CHAR = '\u0001'
    def __init__(self, models, weights):
        self.models = models
        self.unigram = models[0] # unigram model
        self.weights = weights

    def set_seed(self, seed):
        np.random.seed(seed)

    def get_probability(self, character, context):
        character = self.check_unk(character)

        total_prob = 0
        for i, model in enumerate(self.models):
            model_context = [self.START_CHAR] * (model.get_n() - 1) + context
            total_prob += self.weights[i] * model.get_probability(character, model_context)
        return math.log(total_prob, 2)


    def check_unk(self, character):
        if (character,) not in self.unigram.model.keys():
            return self.UNK_CHAR
        return character

    # TODO: tooooo slow!!!!
    def generate_char(self, context):
        char_set = set(self.unigram.model.keys())
        char_set.remove((self.UNK_CHAR,))

        char_list = list(char_set)
        char_probs = np.zeros(len(char_list))

        for i, c in enumerate(char_list):
            char_probs[i] = 2 ** self.get_probability(c[0], context)

        s = np.sum(char_probs)

        char_probs = char_probs / np.sum(char_probs)
        character_list = []
        for c in char_list:
            character_list += c[0]
        gen_char = np.random.choice(character_list, 1, p=char_probs)

        print("sum_prob: ", s, "prob: ", self.get_probability(gen_char[0], context))

        return gen_char[0]