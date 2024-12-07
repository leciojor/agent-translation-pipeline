
from crewai import Task
from pydanticModels.JSONOutput import TranslationOutput, MQM, RefinementOutput, BestTranslation


class Translation:

    def __init__(self, agent, sentence, lang) -> None:
        self.task = Task(description=f'Analyze the sentence provided: "{sentence}" and translate it from {lang} to english',
                        expected_output="JSON object with 'original_text' and 'translated_text'.",
                        metadata={
                                "output_format": {
                                "type": "json",
                                "fields": {
                                        "original_text": "string",
                                        "translated_text": "string"
                        }
                        }
                        },
                        agent=agent,
                        output_json=TranslationOutput
                        )


class Evaluation:

    def __init__(self, agent, lang, src, tgt) -> None:
        self.task = Task(description=f'Evaluate the following translation from {lang} to english using the MQM scorecard: "{tgt}". Source Sentence: "{src}".',
                expected_output="An MQM Score Card JSON file based on the translation",
                metadata={
                        "output_format": {
                        "type": "json",
                        "fields": {
                            "accuracy": "dict[str, bool]",
                            "fluency": "dict[str, bool]",
                            "terminology": "dict[str, bool]",
                            "locate_style": "dict[str, bool]",
                            "formatting": "dict[str, bool]",
                            "error_classification": "[str]",
                            "summary_and_comments": "str"
                }
                }
                },
                agent=agent,
                output_json=MQM
        )


class Refinement:

    def __init__(self, agent, lang, src, tgt) -> None:
        self.task = Task(description=f"""Refine the following translation from {lang} to english: source sentence - {src}, translation - {tgt}
                        based on the MQM scorecard information of the translation""",
                        expected_output="JSON object with 'original_translated_text' and 'refined_translation'.",
                        metadata={
                                "output_format": {
                                "type": "json",
                                "fields": {
                                        "original_translated_text": "string",
                                        "refined_translation": "string"
                        }
                        }
                        },
                        agent=agent,
                        output_json=RefinementOutput
                        )
        
class GettingBestOutput:

    def format_translations(translations, src):
        txt = f"""Source Sentence: {src} \n"""
        count = 1
        for t in translations:
            output = t[0]    
            mqm = t[1]
            txt += f"TRANSLATION number {count}: {output}\n"
            txt += f"""MQM Scoreboard: 
            {mqm}\n"""
            txt += "\n"
            count += 1
        
        return txt

        
    def __init__(self, agent, lang, src, translations) -> None:
        self.task = Task(description=f"""Get the best translation from {lang} to English between the following translations and their respectives mqm scorecards:
                          
                        {GettingBestOutput.format_translations(translations, src)}""",
                        expected_output="JSON object with 'best_translation_number'",
                        metadata={
                                "output_format": {
                                "type": "json",
                                "fields": {
                                        "best_translation_number": "int"
                        }
                        }
                        },
                        agent=agent,
                        output_json=BestTranslation
                        )