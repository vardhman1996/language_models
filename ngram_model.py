import math
import random
from collections import Counter

class Ngram:
    def __init__(self, model:Counter, part_dict:Counter, n, k=1):
        self.model = model
        self.part_dict = part_dict
        self.n = n
        self.k = k

    def get_probability(self, character, context):
        numerator_key = tuple(context + [character])
        denominator_key = tuple(context)

        numer_count = self.model[numerator_key]
        denom_count = self.part_dict[denominator_key]

        prob = (numer_count + self.k)/ (len(self.model.keys()) * self.k + denom_count)
        return math.log(prob, 2)

    def get_n(self):
        return self.n

    def generate_char(self, context):
        num_chars = self.n - 1
        context = context[(-num_chars):]
        possible_chars = []
        max_prob = -math.inf

        for tup, count in self.model.items():
            current_tup = list(tup)
            if context != current_tup[:-1]: continue

            current_prob = self.get_probability(current_tup[-1], current_tup[:-1])

            if abs(current_prob - max_prob) <= 0.001:
                # same log_probability
                possible_chars += [current_tup[-1]]
            elif current_prob > max_prob:
                # log probability is greater
                possible_chars = [current_tup[-1]]
                max_prob = current_prob

        return possible_chars