
from crewai import Task
from pydanticModels.JSONOutput import TranslationOutput, MQM


class Translation:

    def __init__(self, agent, sentence, lang) -> None:
        self.task = Task(description=f"Analyze the sentence provided: {sentence} and translate it from {lang} to english",
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
        self.task = Task(description=f"Evaluate the following translation from {lang} to english: {tgt}. Source Sentence: {src}.",
                expected_output="An MQM Score Card JSON file",
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
                        output_json=TranslationOutput
                        )