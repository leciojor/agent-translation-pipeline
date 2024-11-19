from filters import Filter
import os
import subprocess
from tqdm import tqdm
from argparse import ArgumentParser


def get_tmx_files_text(directory, limit=False):
    tmx_texts = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".tmx"):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    text = f.read()
                    if limit:
                        text = text[:round(len(text) * 0.6)]
                    tmx_texts.append(text)
    return tmx_texts

def forming_txt_files(texts, lang, eng='src', other='tgt', new=False):
    
    for pair in tqdm(texts, desc="Writing cleaned txt to text files", unit="pair"):
        eng = pair[0]
        o = pair[1]

        if new:
            with open(f"cleaned/Lecio-English-{eng}.txt", 'w') as f:
                pass
            with open(f"cleaned/Lecio-{lang}-{other}.txt", 'w') as f:
                pass

        with open(f"cleaned/Lecio-English-{eng}.txt", 'a') as f:
            f.write(eng + '\n')
        with open(f"cleaned/Lecio-{lang}-{other}.txt", 'a') as f:
            f.write(o + '\n')

def main(folder = 'portuguese'):
    tmx_texts = get_tmx_files_text(folder, limit=True)
    final_pairs_amount = 0
    for text in tmx_texts:
        filter = Filter(text)
        print("Pairs: ", filter.texts)
        filter.execute_all_filters()
        print("Filters run sucessfully")

        forming_txt_files(filter.texts, folder)

        final_pairs_amount += len(filter)

    return final_pairs_amount


if __name__ == "__main__":
    final_pairs_amount = main()
    print("FINAL PAIRS AMOUNT PORTUGUESE: ", final_pairs_amount)
    final_pairs_amount = main('german')
    print("FINAL PAIRS AMOUNT GERMAN: ", final_pairs_amount)

    parser = ArgumentParser()
    parser.add_argument('language', help='Language')
    args = parser.parse_args()
    lang = args.lang

    main(lang)

    

    