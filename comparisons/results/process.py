
import csv


def get_final_translations(tsv_file):
    '''
    Retrives last collum of tsv file (with the final translations)
    '''

    # Helper function to determine if a line is part of a complete TSV row
    def is_complete_row(line):
        return line.count("\t") == 2

    # Read and process the TSV file
    with open(tsv_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    fixed_lines = []
    current_row = ""

    for line in lines:
        line = line.strip()
        if is_complete_row(line):  # A complete row detected
            if current_row:  # If there's an existing row, append it first
                fixed_lines.append(current_row)
            current_row = line  # Start a new row
        else:  # Append the line to the current row
            current_row += " " + line

    # Append the last row if it exists
    if current_row:
        fixed_lines.append(current_row)

    # Write the fixed TSV content back to the file
    with open(tsv_file, "w", encoding="utf-8") as file:
        file.write("\n".join(fixed_lines) + "\n")
# get_final_translations("/Users/ui/agent-translation-pipeline/comparisons/results/gpt4_22_portuguese.tsv")
get_final_translations("/Users/ui/agent-translation-pipeline/comparisons/results/gpt4_22_german.tsv")
