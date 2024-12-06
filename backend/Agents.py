from crewai import Agent, LLM
from langchain_ollama import ChatOllama
from knowledgeModels.MQM import MQMKnowledge
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
            memory=False
        )
        else:
            self.agent  = Agent(
            role=f"{lang} to English translator",
            goal=f"Translate sentences in {lang} to English",
            backstory=f"You translate texts from {lang} to English",            
            verbose=verbose,
            memory=False
        )

        

class EvaluationAgent:


    def __init__(self, lang, llm, verbose=True) -> None:
        self.knowledge = MQMKnowledge(lang)
        self.lang = lang
        if llm:
            self.agent  = Agent(
            role="Machine translation evaluator",
            goal=f"Evaluate a machine translated sentence from {lang} to english using Multidimensional Quality Metrics (MQM)",
            backstory=f"You evaluate machine translated sentences from {lang} to english using Multidimensional Quality Metrics (MQM)",
            knowledge_sources = [self.knowledge.mqm_info, self.knowledge.get_mqm_template()],
            llm=LLM(
                model=llm,
                base_url=os.environ['OLLAMA_HOST'], temperature=0.1, context=os.environ['CONTEXT']),
            verbose=verbose,
            memory=False
        )
        else:
            self.agent  = Agent(
            role="Machine translation evaluator",
            goal=f"Evaluate a machine translated sentence from {lang} to english",
            backstory=f"You evaluates machine translated sentences from {lang} to english",
            verbose=verbose,
            memory=False
        )
            




class RefinementAgent:

    def __init__(self, lang, llm, verbose=True) -> None:
        self.knowledge = MQMKnowledge(lang)
        if llm:
            self.agent  = Agent(
            role=f"Sentence Translation Refiner",
            goal=f"Refine sentence translations from {lang} to english based on MQM scorecard of the translation",
            backstory=f"You refine sentence translations from {lang} to english based on MQM scorecard of the translation",
            knowledge_sources = [self.knowledge.mqm_info],
            llm=LLM(
                model=llm,
                base_url=os.environ['OLLAMA_HOST'], temperature=0.1, context=os.environ['CONTEXT']),
            verbose=verbose,
            memory=False
        )
        else:
            self.agent  = Agent(
            role=f"Sentence Translation Refiner",
            goal=f"Refine sentence translations from {lang} to english",
            backstory=f"You refine sentence translations from {lang} to english",
            verbose=verbose,
            memory=False
        )
            
class BestOutputAgent:

    def __init__(self, lang, llm, verbose=True) -> None:
        self.knowledge = MQMKnowledge(lang)
        if llm:
            self.agent  = Agent(
            role=f"Best translation manager",
            goal=f"Define what is the best translation between all the translations available from {lang} to english based on the MQM scoreboard of each",
            backstory=f"You define what is the best translation between all the translations available from {lang} to english based on the MQM scoreboard of each",
            knowledge_sources = [self.knowledge.mqm_info],
            llm=LLM(
                model=llm,
                base_url=os.environ['OLLAMA_HOST'], temperature=0.1, context=os.environ['CONTEXT']),
            verbose=verbose,
            memory=False
        )
        else:
            self.agent  = Agent(
            role=f"Best translation manager",
            goal=f"Define what is the best translation between all the translations available from {lang} to english based on the MQM scoreboard of each",
            backstory=f"You define what is the best translation between all the translations available from {lang} to english based on the MQM scoreboard of each",
            knowledge_sources = [RefinementAgent.mqm_info],
            verbose=verbose,
            memory=False
        )



