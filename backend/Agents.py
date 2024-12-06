from crewai import Agent, LLM
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from langchain_ollama import ChatOllama
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
                base_url=os.environ['OLLAMA_HOST'], temperature=0.1),
            verbose=verbose,
        )
        else:
            self.agent  = Agent(
            role=f"{lang} to English translator",
            goal=f"Translate sentences in {lang} to English",
            backstory=f"You translate texts from {lang} to English",            
            verbose=verbose,
        )

        

class EvaluationAgent:

    
    mqm_info = StringKnowledgeSource(
        content="""
            MQM (Multidimensional Quality Metrics) is a flexible framework for evaluating and annotating translation quality. 
            It provides a detailed categorization of errors based on their type and severity, 
            offering a structured way to identify and analyze issues in translations.
        """,
        metadata={
            "domain": "translation_quality",
            "framework": "MQM",
            "source": "internal_documentation",
        }
    )


    def __init__(self, lang, llm, verbose=True) -> None:
        self.lang = lang
        if llm:
            self.agent  = Agent(
            role="Machine translation evaluator",
            goal=f"Evaluate a machine translated sentence from {lang} to english using Multidimensional Quality Metrics (MQM)",
            backstory=f"You evaluate machine translated sentences from {lang} to english using Multidimensional Quality Metrics (MQM)",
            knowledge_sources = [EvaluationAgent.mqm_info, self.get_mqm_template()],
            llm=LLM(
                model=llm,
                base_url=os.environ['OLLAMA_HOST']),
            verbose=verbose,
        )
        else:
            self.agent  = Agent(
            role="Machine translation evaluator",
            goal=f"Evaluate a machine translated sentence from {lang} to english",
            backstory=f"You evaluates machine translated sentences from {lang} to english",
            llm=LLM(
                model=llm,
                base_url=os.environ['OLLAMA_HOST']),
            verbose=verbose,
        )
            
    def get_mqm_template(self):
        mqm_template = StringKnowledgeSource(
        content=f"""
        ==============================
                MQM Scoreboard
        ==============================

        Language Pair: [{self.lang} -> English]
        ==============================

        Total Errors Identified: [Number]

        ------------------------------
        Error Breakdown by Type
        ------------------------------
        1. Accuracy:
        - Mistranslation: [boolean]
        - Omission: [boolean]
        - Addition: [boolean]
        - Untranslated: [boolean]

        2. Fluency:
        - Grammar: [boolean]
        - Punctuation: [boolean]
        - Spelling: [boolean]
        - Word Order: [boolean]
        - Register: [boolean]

        3. Terminology:
        - Inconsistent: [boolean]
        - Incorrect: [boolean]

        4. Locale/Style:
        - Style: [boolean]
        - Locale Conventions: [boolean]

        5. Formatting:
        - Tag Issues: [boolean]
        - Layout: [boolean]

        6. Other:
        - Non-linguistic Issues: [boolean]

        ------------------------------
        Error Classification
        ------------------------------
        [Neutral or Minor or Major or Critical]

        ------------------------------
        Summary & Comments
        ------------------------------
        [Evaluator's general comments and observations about the quality of the translation.]

        ==============================
            END OF SCOREBOARD
        ==============================

    """,
        metadata={
            "domain": "translation_quality",
            "framework": "MQM",
            "source": "internal_documentation"
        }
    )
        return mqm_template




class RefinementAgent:

    mqm_info = StringKnowledgeSource(
        content="""
            MQM (Multidimensional Quality Metrics) is a flexible framework for evaluating and annotating translation quality. 
            It provides a detailed categorization of errors based on their type and severity, 
            offering a structured way to identify and analyze issues in translations.
        """,
        metadata={
            "domain": "translation_quality",
            "framework": "MQM",
            "source": "internal_documentation",
        }
    )

    def __init__(self, lang, llm, verbose=True) -> None:
        if llm:
            self.agent  = Agent(
            role=f"Sentence Translation Refiner",
            goal=f"Refine sentence translations from {lang} to english based on MQM scorecard of the translation",
            backstory=f"You refine sentence translations from {lang} to english based on MQM scorecard of the translation",
            knowledge_sources = [RefinementAgent.mqm_info],
            llm=LLM(
                model=llm,
                base_url=os.environ['OLLAMA_HOST']),
            verbose=verbose,
        )
        else:
            self.agent  = Agent(
            role=f"Sentence Translation Refiner",
            goal=f"Refine sentence translations from {lang} to english",
            backstory=f"You refine sentence translations from {lang} to english",
            llm=LLM(
                model=llm,
                base_url=os.environ['OLLAMA_HOST']),
            verbose=verbose,
        )


