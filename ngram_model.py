import math
import random
from collections import Counter

class Ngram:
    V = 65424
    START_CHAR = '\u0002'  # U+0002 \x02
    def __init__(self, model:Counter, part_dict:Counter, n, num_starts, k=1):
        self.model = model
        self.part_dict = part_dict
        self.n = n
        self.k = k
        self.num_starts = num_starts

    def get_probability(self, character, context):
        num_chars = self.n - 1

        if self.n == 1:
            numerator_key = tuple([character])
        else:
            numerator_key = tuple(context[(-num_chars):] + [character])

        if self.n == 1:
            # unigram model so denom is N
            denom_count = sum(self.part_dict.values())
        else:
            all_start = True
            denominator_key = tuple(context[(-num_chars):])
            for char in denominator_key:
                if char != self.START_CHAR:
                    all_start = False

            if all_start:
                denom_count = self.num_starts
            else:
                denom_count = self.part_dict[denominator_key]


        numer_count = self.model[numerator_key]
        # if denom_count == 0 or numer_count == 0:
        #     return 0, denom_count == 0


        # k-smoothing
        prob = (numer_count + self.k) / ((self.V * self.k) + denom_count)
        return prob


    def get_n(self):
        return self.n


    # def generate_char(self, context):
    #     num_chars = self.n - 1
    #     context = context[(-num_chars):]
    #     possible_chars = []
    #     max_prob = -math.inf
    #
    #     # TODO: bug to fix when counts are 0
    #     for tup, count in self.model.items():
    #         current_tup = list(tup)
    #         if context != current_tup[:-1]: continue
    #
    #         current_prob = self.get_probability(current_tup[-1], current_tup[:-1])
    #
    #         if abs(current_prob - max_prob) <= 0.00001:
    #             # same log_probability
    #             possible_chars += [current_tup[-1]]
    #         elif current_prob > max_prob:
    #             # log probability is greater
    #             possible_chars = [current_tup[-1]]
    #             max_prob = current_prob
    #
    #     return random.sample(possible_chars, 1)[0]