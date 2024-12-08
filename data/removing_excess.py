

with open("cleaned/Lecio-german-src.txt", 'r') as german:
    lines = german.readlines()
    lines = lines[:100]
    with open("cleaned/Lecio-german-src.txt", 'w') as german_:
        german_.writelines(lines) 


with open("cleaned/Lecio-portuguese-src.txt", 'r') as portuguese:
    lines = portuguese.readlines()
    lines = lines[:100]
    with open("cleaned/Lecio-portuguese-src.txt", 'w') as portuguese_:
        portuguese_.writelines(lines) 

with open("cleaned/Lecio-English-german-tgt.txt", 'r') as german:
    lines = german.readlines()
    lines = lines[:100]
    with open("cleaned/Lecio-English-german-tgt.txt", 'w') as german_:
        german_.writelines(lines) 


with open("cleaned/Lecio-English-portuguese-tgt.txt", 'r') as portuguese:
    lines = portuguese.readlines()
    lines = lines[:100]
    with open("cleaned/Lecio-English-portuguese-tgt.txt", 'w') as portuguese_:
        portuguese_.writelines(lines) 

