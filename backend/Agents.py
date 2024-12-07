from crewai import Agent, LLM

import os
from dotenv import load_dotenv

load_dotenv()

class TranslationAgent:

    def __init__(self, lang, llm, verbose=True) -> None:
        if llm:
            self.agent  = Agent(
            role=f"{lang} to English translator",
            goal=f"Translate sentences in {lang} to English",
            backstory=f"You translate texts from {lang} to English",
            llm=LLM(
                model=llm,
                base_url=os.environ['OLLAMA_HOST'], temperature=0.1, context=os.environ['CONTEXT']),
            verbose=verbose,
            memory=True
        )
        else:
            self.agent  = Agent(
            role=f"{lang} to English translator",
            goal=f"Translate sentences in {lang} to English",
            backstory=f"You translate texts from {lang} to English",            
            verbose=verbose,
            memory=True
        )

        

class EvaluationAgent:


    def __init__(self, lang, llm, verbose=True) -> None:
        if llm:
            self.agent  = Agent(
            role="Machine translation evaluator",
            goal=f"Evaluate a machine translated sentence from {lang} to english using Multidimensional Quality Metrics (MQM)",
            backstory=f"You evaluate machine translated sentences from {lang} to english using Multidimensional Quality Metrics (MQM)",
            llm=LLM(
                model=llm,
                base_url=os.environ['OLLAMA_HOST'], temperature=0.1, context=os.environ['CONTEXT']),
            verbose=verbose,
            memory=True
        )
        else:
            self.agent  = Agent(
            role="Machine translation evaluator",
            goal=f"Evaluate a machine translated sentence from {lang} to english",
            backstory=f"You evaluates machine translated sentences from {lang} to english",
            verbose=verbose,
            memory=True
        )
            


class RefinementAgent:

    
    def __init__(self, lang, llm, verbose=True) -> None:
        self.lang = lang
        if llm:
            self.agent  = Agent(
            role=f"Sentence Translation Refiner",
            goal=f"Refine sentence translations from {lang} to english based on MQM scorecard of the translation",
            backstory=f"You refine sentence translations from {lang} to english based on MQM scorecard of the translation",
            llm=LLM(
                model=llm,
                base_url=os.environ['OLLAMA_HOST'], temperature=0.1, context=os.environ['CONTEXT']),
            verbose=verbose,
            memory=True
        )
        else:
            self.agent  = Agent(
            role=f"Sentence Translation Refiner",
            goal=f"Refine sentence translations from {lang} to english",
            backstory=f"You refine sentence translations from {lang} to english",
            verbose=verbose,
            memory=True
        )
            
class BestOutputAgent:

    def __init__(self, lang, llm, verbose=True) -> None:
        if llm:
            self.agent  = Agent(
            role=f"Best translation manager",
            goal=f"Define what is the best translation between all the translations available from {lang} to english based on the MQM scoreboard of each",
            backstory=f"You define what is the best translation between all the translations available from {lang} to english based on the MQM scoreboard of each",
            llm=LLM(
                model=llm,
                base_url=os.environ['OLLAMA_HOST'], temperature=0.1, context=os.environ['CONTEXT']),
            verbose=verbose,
            memory=True
        )
        else:
            self.agent  = Agent(
            role=f"Best translation manager",
            goal=f"Define what is the best translation between all the translations available from {lang} to english based on the MQM scoreboard of each",
            backstory=f"You define what is the best translation between all the translations available from {lang} to english based on the MQM scoreboard of each",
            verbose=verbose,
            memory=True
        )



