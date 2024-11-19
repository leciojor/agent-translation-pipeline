import re
import html
from tqdm import tqdm
import string

class Filter:

    @staticmethod
    def check_all_non_alpha(pair):

        for c in pair[0]:

            if c.isalpha():
                return False
            
        return True

    
    #filter 1
    @staticmethod
    def remove_spurious(text):
        cleaned_text = text.replace('—', ' ')
        cleaned_text = re.sub(r"[^a-zA-Z0-9\s.,!?;:'\"çãõáàéíóúâêôÀÁÉÍÓÚÇÃÕÊÂÔ-]", '', cleaned_text)
    
        cleaned_text = cleaned_text.replace('\r', '').replace('\n', '').replace('\t', '')

        return cleaned_text

    @staticmethod
    def get_texts_pairs(text):
        segments = re.findall(r'<seg>(.*?)</seg>', text, re.DOTALL)
        pairs = []
        
        if len(segments) % 2 == 0:
            for i in range(0, len(segments), 2):
                seg_eng = Filter.remove_spurious(segments[i])
                seg_por = Filter.remove_spurious(segments[i+1])

                #filter 2
                if seg_eng and seg_por:
                    pairs.append((seg_eng, seg_por))

            return pairs

        else:
            print("Not all segments are matching")
            return []

    def __init__(self, text):
        self.raw = text
        self.texts = Filter.get_texts_pairs(self.raw)

    def __len__(self):
        return len(self.texts)
    
    def execute_all_filters(self):
        print("Changing filters")
        for i, pair in enumerate(tqdm(self.texts, desc="Processing text pairs", unit="pair")):
            text = html.unescape(pair[0])
            text = re.sub(r'[\x00-\x1F\x7F]', '', text)            
            text = re.sub(r'\s+', ' ', text).strip()            
            text = text.replace("“", '"').replace("”", '"')  
            text = text.replace("‘", '"').replace("’", '"') 
            text = text.strip()
            text = ' '.join(text.split())

            text_ = html.unescape(pair[1])
            text_ = re.sub(r'[\x00-\x1F\x7F]', '', text_)            
            text_ = re.sub(r'\s+', ' ', text_).strip()            
            text_ = text_.replace("“", '"').replace("”", '"')  
            text_ = text_.replace("‘", '"').replace("’", '"')  
            text_ = text_.strip()
            text_ = ' '.join(text_.split())

            self.texts[i] = (text, text_)   

        self.texts = set(self.texts)
        self.texts = list(self.texts)             
        print("Removing filters")

        copy_texts = self.texts.copy()
        for i, pair in enumerate(tqdm(self.texts, desc="Processing text pairs 2", unit="pair")):

            if pair[0].strip() == pair[1].strip():
                copy_texts.remove(pair)
            elif len(pair[0].split()) < 3 or len(pair[1].split()) < 3 or len(pair[0].split()) > 100 or len(pair[1].split()) > 100:
                copy_texts.remove(pair)
            elif len(pair[0].split()) > (len(pair[1].split()) * 1.3) or len(pair[1].split()) > (len(pair[0].split()) * 1.3):
                copy_texts.remove(pair)
            elif pair[0].isdigit() or pair[1].isdigit():
                copy_texts.remove(pair)
            elif Filter.check_all_non_alpha(pair):
                copy_texts.remove(pair)
            elif not pair[0].strip() or not pair[1].strip():
                copy_texts.remove(pair)
            elif re.search(r'<[^>]*>', pair[0]) or re.search(r'<[^>]*>', pair[1]):
                copy_texts.remove(pair)
            elif all(char in string.punctuation + string.whitespace for char in pair[0]) or all(char in string.punctuation + string.whitespace for char in pair[1]):
                copy_texts.remove(pair)
            elif all(char in string.punctuation for char in pair[0].strip()) or all(char in string.punctuation for char in pair[1].strip()):
                copy_texts.remove(pair)
            elif all(char in string.punctuation + string.whitespace or char.isdigit() for char in pair[0].strip()) or all(char in string.punctuation or char.isdigit() for char in pair[1].strip()):
                copy_texts.remove(pair)
            elif 'https' in pair[0] or 'https' in pair[1]:
                copy_texts.remove(pair)
            
            #domain exclusive removals
            elif 'bpt' in pair[0] or 'bpt' in pair[1]:
                copy_texts.remove(pair)
            elif 'ph x"' in pair[0] or 'ph x"' in pair[1]:
                copy_texts.remove(pair)
            elif 'type"x' in pair[0] or 'type"x' in pair[1]:
                copy_texts.remove(pair)
            elif 'a.m.;' in pair[0] or 'a.m.;' in pair[1]:
                copy_texts.remove(pair)
            elif 'p.m.' in pair[0] or 'p.m.' in pair[1]:
                copy_texts.remove(pair)
            elif pair[0] == 'Understanding the why of the gospel and the why of the priesthood will help us to see the divine purpose of all of this.':
                copy_texts.remove(pair)
            elif pair[0] == 'The desire to receive a patriarchal blessing should come from a desire to know and live Gods will for you.':
                copy_texts.remove(pair)
            elif pair[0] == 'But first, of course, we had to collect the worms.':
                copy_texts.remove(pair)
    


        self.texts = copy_texts
    

    #filters 3,4,5
    def normalization(self):

        for i, pair in enumerate(self.texts):
            text = html.unescape(pair[0])
            text = re.sub(r'[\x00-\x1F\x7F]', '', text)            
            text = re.sub(r'\s+', ' ', text).strip()            
            text = text.replace("“", '"').replace("”", '"')  
            text = text.replace("‘", '"').replace("’", '"') 
            text = text.strip()
            text = ' '.join(text.split())

            text_ = html.unescape(pair[1])
            text_ = re.sub(r'[\x00-\x1F\x7F]', '', text_)            
            text_ = re.sub(r'\s+', ' ', text_).strip()            
            text_ = text_.replace("“", '"').replace("”", '"')  
            text_ = text_.replace("‘", '"').replace("’", '"')  
            text_ = text_.strip()
            text_ = ' '.join(text_.split())

            self.texts[i] = (text, text_)                

    
    #filter 10
    def source_equal_target_removal(self):
        copy = self.texts.copy()
        for pair in self.texts:
            if pair[0].strip() == pair[1].strip():
                copy.remove(pair)

        self.texts = copy

    #filters 13, 14
    def short_long_removal(self):
        copy = self.texts.copy()
        for pair in self.texts:
            if len(pair[0].split()) < 4 or len(pair[1].split()) < 4 or len(pair[0].split()) > 99 or len(pair[1].split()) > 99:
                copy.remove(pair)
        
        self.texts = copy


    #filter 7
    def duplicates_remove(self):
        self.texts = set(self.texts)
        self.texts = list(self.texts)
    
    #filter 8
    def non_textual_removal(self):
        copy = self.texts.copy()
        #remove only numbers
        for pair in self.texts:
            if pair[0].isdigit() or pair[1].isdigit():
                copy.remove(pair)
        #remove only non alpha and numeric chars        
            elif Filter.check_all_non_alpha(pair):
                copy.remove(pair)
            elif 'https' in pair[0] or 'https' in pair[1]:
                copy.remove(pair)
        
        self.texts = copy


    #filter 16
    def remove_unbalanced(self):
        copy = self.texts.copy()
        for pair in self.texts:
            if len(pair[0].split()) > (len(pair[1].split()) * 1.2) or len(pair[1].split()) > (len(pair[0].split()) * 1.2):
                copy.remove(pair)

        self.texts = copy

    #filter 12
    def remove_pont_tags_white(self):
        copy = self.texts.copy()
        for pair in self.texts:
            if not pair[0].strip() or not pair[1].strip():
                copy.remove(pair)
            elif re.search(r'<[^>]*>', pair[0]) or re.search(r'<[^>]*>', pair[1]):
                copy.remove(pair)
            elif all(char in string.punctuation + string.whitespace for char in pair[0]) or all(char in string.punctuation + string.whitespace for char in pair[1]):
                copy.remove(pair)
            elif all(char in string.punctuation for char in pair[0].strip()) or all(char in string.punctuation for char in pair[1].strip()):
                copy.remove(pair)
            elif all(char in string.punctuation + string.whitespace or char.isdigit() for char in pair[0].strip()) or all(char in string.punctuation or char.isdigit() for char in pair[1].strip()):
                copy.remove(pair)

        self.texts = copy

    #filter 15
    def removing_missalignments(self):
        copy = self.texts.copy()
        for pair in self.texts:
            if pair[0] == 'Understanding the why of the gospel and the why of the priesthood will help us to see the divine purpose of all of this.':
                copy.remove(pair)
            if pair[0] == 'The desire to receive a patriarchal blessing should come from a desire to know and live Gods will for you.':
                copy.remove(pair)
            if pair[0] == 'But first, of course, we had to collect the worms.':
                copy.remove(pair)
    
        self.texts = copy





    
    