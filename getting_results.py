'''
Evaluation and collection of metrics for different pipeline setups
'''

from backend.__main__ import agent_translation, system_translation
import csv
from tqdm import tqdm

def testing(tests, mode):
    langs = ["portuguese", "german"]

    for lang in langs:
        for test in tests:
            with open(f"data/cleaned/Lecio-{lang}-src.txt", 'r') as src:
                sentences = src.readlines()                
                with open(test["name"] + f"_{lang}", "w",  newline='', encoding='utf-8') as translations:
                    tsv_writer = csv.writer(translations, delimiter='\t')
                    tsv_writer.writerow(['Source', 'First English Translation', 'Final Refined Translation'])

                    for sentence in tqdm(sentences , desc=f"Execution for {lang} and {test['name']}"):
                        try:
                            if sentence:
                                if "nmt" in test:
                                    final_output = mode(lang, test["model"], sentence, 2, test["k"], test["nmt"], verbose=False)
                                else: 
                                    final_output = mode(lang, test["model"], sentence, 2, test["k"], verbose=False)

                                initial = final_output[0]
                                translation = final_output[1]['refined_translation']

                                tsv_writer.writerow([sentence, initial, translation])
                        except Exception as e:
                            tsv_writer.writerow([sentence, f"Error: {e}", f"Error: {e}"])



def main():
    options_llm_mode = [{"name": "comparisons/results/gpt4_22.tsv", "model":"", "k":2}, {"name": "comparisons/results/gpt4_23.tsv", "model":"", "k":3}, {"name": "comparisons/results/gpt4_24.tsv", "model":"", "k":4}]
    options_nmt_mode = [{"name": "comparisons/results/nmtBing.tsv", "model":"", "k":3, "nmt":"bing"}, {"name": "comparisons/results/nmtYandex.tsv", "model":"", "k":3, "nmt":"yandex"}, {"name": "comparisons/results/nmtAlibaba.tsv", "model":"", "k":3, "nmt":"alibaba"}]
    testing([options_llm_mode[0]], agent_translation)
    # testing([options_nmt_mode[0]], system_translation)


if __name__ == "__main__":
    main()