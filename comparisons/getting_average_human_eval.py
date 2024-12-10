'''
Logic to get average human evaluation score for different pipeline configurations
'''

import csv
import os


def get_average(lang_dir):

    
    for filename in os.listdir(lang_dir):
        print(f"getting average human evaluations for {filename}")
        sum_1 = 0
        sum_2 = 0
        count = 0 
        results_file = os.path.join(lang_dir, filename)

        with open(results_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')  

            for row in reader:
                sum_1 += int(row['First English Translation'])
                sum_2 += int(row['Final Refined Translation'])
                count += 1

        # Calculate the averages
        avg_1 = sum_1 / count if count > 0 else 0
        avg_2 = sum_2 / count if count > 0 else 0

        # Output the results
        print(f"Average for First English Translation: {avg_1}")
        print(f"Average for Final Refined Translation: {avg_2}")



if __name__ == "__main__":
    #portuguese evals
    get_average("results/human_evals/portuguese")

    # german evals
    get_average("results/human_evals/german")
