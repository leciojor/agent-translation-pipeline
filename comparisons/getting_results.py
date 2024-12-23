'''
Logic to retrieve results from the pipeline system with different configurations
'''

from backend.__main__ import agent_translation, system_translation
import csv
from tqdm import tqdm

def testing(tests, mode, lang):
    '''
    The results for each text/sentence are wrote in tsv files with the following format:

    SOURCE SENTENCE FIRST ENGLISH TRANSLATION FINAL REFINED TRANSLATION
    ...             ...                       ...
    ...             ...                       ...
    '''

    for test in tests:
        with open(f"data/cleaned/Lecio-{lang}-src.txt", 'r') as src:
            sentences = src.readlines()                
            with open(test["name"][:-4] + f"_{lang}" + ".tsv", "w",  newline='', encoding='utf-8') as translations:
                tsv_writer = csv.writer(translations, delimiter='\t')
                tsv_writer.writerow(['Source', 'First English Translation', 'Final Refined Translation'])

                for sentence in tqdm(sentences , desc=f"Execution for {lang} and {test['name']}"):
                    try:
                        if sentence:
                            if "nmt" in test:
                                final_output = mode(lang, test["model"], sentence, test["k_models"], test["k"], test["nmt"], verbose=False)
                            else: 
                                final_output = mode(lang, test["model"], sentence, test["k_models"], test["k"], verbose=False)

                            initial = final_output[0]
                            translation = final_output[1]['refined_translation']

                            tsv_writer.writerow([sentence[0:-1], initial, translation])
                    except Exception as e:
                        tsv_writer.writerow([sentence, f"Error: {e}", f"Error: {e}"])



def main():
    '''
    For more information on the configurations tested, please look at the slides
    '''
    options_llm_mode = [{"name": "comparisons/results/gpt4_22.tsv", "model":"", "k_models":2, "k":2}, {"name": "comparisons/results/gpt4_23.tsv", "k_models":2, "model":"", "k":3}, {"name": "comparisons/results/gpt4_14.tsv", "model":"", "k_models":1, "k":4}]
    options_nmt_mode = [{"name": "comparisons/results/nmtBing.tsv", "model":"", "k_models":1, "k":3, "nmt":"bing"}, {"name": "comparisons/results/nmtYandex.tsv", "model":"", "k_models":1, "k":3, "nmt":"yandex"}, {"name": "comparisons/results/nmtAlibaba.tsv", "k_models":1, "model":"", "k":3, "nmt":"alibaba"}]
    testing([options_llm_mode[0]], agent_translation, "german")
    # testing([options_nmt_mode[2]], system_translation, "german")


if __name__ == "__main__":
    main()