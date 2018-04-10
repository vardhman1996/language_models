from collections import Counter
import pickle as pkl
import os
# import ngram_model as nm
import linear_interpolation as li
import argparse
import random

STOP_CHAR = '\u0003' # U+0003 \x03
START_CHAR = '\u0002' # U+0002 \x02
MODEL = "models/lin_interpolate_model.pkl"

def load_model():
    # filename = None
    # for files in os.listdir(MODELS):
    #     if files.startswith(str(n)):
    #         filename = files
    #
    # if filename is None:
    #     return None

    with open(MODEL, 'rb') as model_file:
        model = pkl.load(model_file)
    return model


def main():
    lin_model = load_model()

    parser = argparse.ArgumentParser(description='Language model')
    parser.add_argument('-s', '--seed', type=int, default=1)
    args = parser.parse_args()
    seed = args.seed
    lin_model.set_seed(seed)

    while(1):
        # print("hello")
        user_input = input().lower() #TODO: should this be lower case? train is on lower case
        user_input_chars = [c for c in user_input]

        context = []
        output = []
        i = 0
        while i < len(user_input_chars):
            # print("context: ", context, "i: ", i)
            if user_input_chars[i] == 'o':
                next_char = user_input_chars[i + 1]
                if next_char == STOP_CHAR:
                    break
                checked_char = lin_model.check_unk(next_char)
                log_prob = lin_model.get_probability(checked_char, context)
                print("P({0}|{1}) = {2} MLE char".format(next_char, ''.join(context), log_prob))
                context += [next_char]
                i += 1

            elif user_input_chars[i] == 'q':
                next_char = user_input_chars[i + 1]
                next_char = lin_model.check_unk(next_char)
                log_prob = lin_model.get_probability(next_char, context)
                print(log_prob)
                i += 1

            elif user_input_chars[i] == 'g':
                inferred_char = lin_model.generate_char(context)
                context += [inferred_char]
                output += [inferred_char]
                # print(inferred_char)
            elif user_input_chars[i] == 'x':
                exit(1)
            i+=1
        print(''.join(output))
    return 0

if __name__ == "__main__":
    main()