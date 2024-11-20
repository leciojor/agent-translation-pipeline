from crewai import Agent
from tools.Translate import Translate

class TranslationAgent:

    def __init__(self, input, lang, llm, verbose=True) -> None:
        self.agent  = Agent(
        role=f"{lang} to English translator",
        goal=f"Translate the following text from {lang} into English.\{lang}: {input}.\nEnglish:",
        backstory=f"I translate texts from {lang} to English",
        llm=llm,
        verbose=verbose,
    )
        

class EvaluationAgent:

    def __init__(self, text_to_evalute, lang, llm, verbose=True) -> None:
        self.agent  == Agent(
        role="You are a machine translation evaluator.",
        goal="",
        backstory="",
        llm=llm,
        verbose=verbose,
    )

class RefinementAgent:

    def __init__(self, llm, verbose=True) -> None:
        self.agent  == Agent(
        role="",
        goal="",
        backstory="",
        llm=llm,
        verbose=verbose,
    )