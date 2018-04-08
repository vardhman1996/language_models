
class Ngram:
    def __init__(self, model, part_dict):
        self.model = model
        self.part_dict = part_dict

    def get_probability(self, character, context, k=1):
        numerator_key = tuple(context + [character])
        denominator_key = tuple(context)

        numer_count = self.model[numerator_key]
        denom_count = self.part_dict[denominator_key]

        prob = (numer_count + k)/ (len(self.model.keys()) * k + denom_count)
        return prob