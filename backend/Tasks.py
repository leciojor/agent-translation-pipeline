
from crewai import Task


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
                        agent=agent
                        )


class Evaluation:

    def __init__(self, agent, lang, src, tgt) -> None:
        self.task = Task(description=f"Evaluate the following translation from {lang} to english: {tgt}. Source Sentence: {src}.",
                expected_output="An MQM Score Card",
                agent=agent
        )


class Refinement:

    def __init__(self, agent, lang, src, tgt) -> None:
        self.task = Task(description=f"Refine the following translation from {lang} to english: source sentence - {src}, translation - {tgt}",
                        expected_output="JSON object with 'original_text' and 'translated_text'.",
                        metadata={
                                "output_format": {
                                "type": "json",
                                "fields": {
                                        "original_translated_text": "string",
                                        "refined_translation": "string"
                        }
                        }
                        },
                        agent=agent
                        )