
from sacrebleu.metrics import BLEU


def get_bleu():
    bleu = BLEU()

    return bleu.corpus_score([], [//refs])


def get_comet():
    pass



def main():
    options = [{"name": "comparisons/results/gpt4_22.tsv", "model":"", "k":2}, {"name": "comparisons/results/gpt4_23.tsv", "model":"", "k":3}, {"name": "comparisons/results/gpt4_24.tsv", "model":"", "k":4}, {"name": "comparisons/results/nmtBing.tsv", "model":"", "k":3, "nmt":"bing"}, {"name": "comparisons/results/nmtYandex.tsv", "model":"", "k":3, "nmt":"yandex"}, {"name": "comparisons/results/nmtAlibaba.tsv", "model":"", "k":3, "nmt":"alibaba"}]

    for option in options:
        bleu = get_bleu()
        print(f"BLEU SCORE FOR {option['name']}")
        comet = get_comet()
        print(f"COMET SCORE FOR {option['comet']}")


if __name__ == "__main__":
    main()