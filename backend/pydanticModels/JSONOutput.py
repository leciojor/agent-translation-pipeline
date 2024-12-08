'''
Pydantic logic to define the agents output structure
'''


from pydantic import BaseModel

class TranslationOutput(BaseModel):
    original_text: str
    translated_text: str

class BestTranslation(BaseModel):
    best_translation_number: int

class RefinementOutput(BaseModel):
    original_translated_text: str
    refined_translation: str

class MQM(BaseModel):
    language_pair: str
    accuracy: dict[str, bool]
    fluency: dict[str, bool]
    terminology: dict[str, bool]
    locate_style: dict[str, bool]
    formatting: dict[str, bool]
    other: dict[str, bool]
    error_classification: str
    summary_and_comments: str

