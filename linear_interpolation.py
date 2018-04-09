from ngram_model import Ngram
import math

class LinearInterpolation:
    START_CHAR = '\u0002'  # U+0002 \x02
    def __init__(self, models, weights):
        self.models = models
        self.weights = weights

    def get_probability(self, character, context):
        total_prob = 0
        for i, model in enumerate(self.models):
            model_context = [self.START_CHAR] * (model.get_n() - 1) + context
            total_prob += self.weights[i] * model.get_probability(character, model_context)
        return math.log(total_prob, 2)

