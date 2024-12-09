'''
Main logic to get the data from the tmx files and clean it
'''

from filters import Filter
import os
from tqdm import tqdm
from argparse import ArgumentParser


def get_tmx_files_text(directory, limit=False):
    tmx_texts = []
    for root, dirs, files in os.walk(f"data/{directory}"):
        for file in files:
            if file.endswith(".tmx"):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    text = f.read()
                    if limit:
                        text = text[:round(len(text) * 0.6)]
                    tmx_texts.append(text)
    return tmx_texts

def forming_txt_files(texts, lang, en_name='tgt', other='src'):
    
    for pair in tqdm(texts, desc="Writing cleaned txt to text files", unit="pair"):
        eng = pair[0]
        ot = pair[1]

        with open(f"./data/cleaned/Lecio-English-{lang}-{en_name}.txt", 'a') as f:
            f.write(eng + '\n')
        with open(f"./data/cleaned/Lecio-{lang}-{other}.txt", 'a') as f:
            f.write(ot + '\n')

def main(folder = 'portuguese', new=False, en_name='tgt', other='src'):
    tmx_texts = get_tmx_files_text(folder, limit=True)
    final_pairs_amount = 0
    os.makedirs("./data/cleaned", exist_ok=True)
    if new:
        with open(f"./data/cleaned/Lecio-English-{folder}-{en_name}.txt", 'w') as f:
            pass
        with open(f"./data/cleaned/Lecio-{folder}-{other}.txt", 'w') as f:
            pass
    
    for text in tmx_texts:
        filter = Filter(text)
        print("Pairs: ", filter.texts)
        filter.execute_all_filters()
        print("Filters run sucessfully")

        forming_txt_files(filter.texts, folder)

        final_pairs_amount += len(filter)

    return final_pairs_amount


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('language', help='Language to be cleaned')
    parser.add_argument('new_files', help='Boolean (True/False) variable. Adds new cleaned files instead of just appending lines to the current ones.')
    args = parser.parse_args()
    lang = args.language
    new = args.new_files

    
    if new:
        final_pairs_amount = main(lang, new=new)
    else:
        final_pairs_amount = main(lang)
    print(f"FINAL PAIRS AMOUNT {lang}: ", final_pairs_amount)

    

    