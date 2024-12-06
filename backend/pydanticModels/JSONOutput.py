from pydantic import BaseModel

class TranslationOutput(BaseModel):
    original_text: str
    translated_text: str

class MQM(BaseModel):
    language_pair: str
    total_errors_identified: int
    accuracy: dict[str, bool]
    fluency: dict[str, bool]
    terminology: dict[str, bool]
    locate_style: dict[str, bool]
    formatting: dict[str, bool]
    other: dict[str, bool]
    error_classification: str
    summary_and_comments: str

