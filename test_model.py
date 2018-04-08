from collections import Counter
import pickle as pkl
import os
import ngram_model as nm
import argparse
import random

STOP_CHAR = '\u0003' # U+0003 \x03
START_CHAR = '\u0002' # U+0002 \x02
MODELS = "models/"

def load_model(n):
    filename = None
    for files in os.listdir(MODELS):
        if files.startswith(str(n)):
            filename = files

    if filename is None:
        return None

    with open(os.path.join(MODELS, filename), 'rb') as model_file:
        model = pkl.load(model_file)
    return model


def main():
    model = load_model(5)

    parser = argparse.ArgumentParser(description='Language model')
    parser.add_argument('-s', '--seed', type=int, default=1)
    args = parser.parse_args()
    seed = args.seed
    random.seed(seed)

    while(1):
        print("hello")
        user_input = input()
        user_input_chars = [c for c in user_input]

        context = [START_CHAR] * (model.get_n() - 1)

        i = 0
        while i < len(user_input_chars):
            print("context: ", context, "i: ", i)
            if user_input_chars[i] == 'o':
                next_char = user_input_chars[i + 1]
                if next_char == STOP_CHAR:
                    break
                context += [next_char]
                print()
                i += 1
            elif user_input_chars[i] == 'q':
                next_char = user_input_chars[i + 1]
                log_prob = model.get_probability(next_char, context)
                print(log_prob)
                i += 1
            elif user_input_chars[i] == 'g':
                inferred_chars = model.generate_char(context)
                print(inferred_chars)
            elif user_input_chars[i] == 'x':
                exit(1)
            i+=1
    return 0

if __name__ == "__main__":
    main()