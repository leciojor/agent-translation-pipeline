'''
Logic to collect automated metrics (BLEU and COMET)
'''
from sacrebleu.metrics import BLEU
import csv
import subprocess
import os

def get_bleu(tsv_file, lang):
    with open(f"data/cleaned/Lecio-English-{lang}-tgt.txt", "r") as references:
        refs = references.readlines()

    final_translations =  get_final_translations(tsv_file)
    bleu = BLEU()

    return bleu.corpus_score(final_translations, [refs])

def get_final_translations(tsv_file):
    '''
    Retrives last collum of tsv file (with the final translations)
    '''
    with open(tsv_file, 'r') as file:
        reader = csv.reader(file, delimiter='\t')  
        final_translations = [final[2] for final in reader if len(final) > 2] 

    return final_translations[1:]

def get_comet(tsv_file, lang):
    final_translations =  get_final_translations(tsv_file)
    with open('temp.txt', 'w') as temp:
        temp.writelines(f"{line}\n" for line in final_translations)

    subprocess.run(['comet-score', '-s',  f"data/cleaned/Lecio-{lang}-src.txt", '-t', 'temp.txt', '-r', f"data/cleaned/Lecio-English-{lang}-tgt.txt", '--gpus', '0'], stdout=open("comparisons/results/auto_evals/comet_" + tsv_file[20:-4] + ".txt", "w"))

    os.remove('temp.txt')



def main():
    options = [{"name": "comparisons/results/gpt4_22.tsv", "model":"", "k":2}, {"name": "comparisons/results/gpt4_23.tsv", "model":"", "k":3}, {"name": "comparisons/results/gpt4_14.tsv", "model":"", "k":4}, {"name": "comparisons/results/nmtBing.tsv", "model":"", "k":3, "nmt":"bing"}, {"name": "comparisons/results/nmtYandex.tsv", "model":"", "k":3, "nmt":"yandex"}, {"name": "comparisons/results/nmtAlibaba.tsv", "model":"", "k":3, "nmt":"alibaba"}]

    for lang in ['portuguese', "german"]:
        # for option in options:
        #     file_name = option["name"][:-4] + f"_{lang}" + ".tsv"
        #     bleu = get_bleu(file_name, lang)
        #     print(f"{lang} - BLEU SCORE FOR {option['name']}: {bleu}")

        #     with open("comparisons/results/auto_evals/BLEU_SCORES.txt", 'a') as file:
        #         file.write(f"{lang} - BLEU SCORE FOR {option}: \n {bleu} \n")
        for option in options:
            file_name = option["name"][:-4] + f"_{lang}" + ".tsv"
            print(f"Getting COMET for {option}")
            get_comet(file_name, lang)
        


if __name__ == "__main__":
    main()