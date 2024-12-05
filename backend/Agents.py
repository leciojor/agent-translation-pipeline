from crewai import Agent, Tool
from crewai.knowledge import StringKnowledgeSource

class TranslationAgent:

    def __init__(self, lang, llm, verbose=True) -> None:
        if llm:
            self.agent  = Agent(
            role=f"{lang} to English translator",
            goal=f"Translate sentences in {lang} to English",
            backstory=f"You translate texts from {lang} to English",
            llm=llm,
            verbose=verbose,
        )
        else:
            self.agent  = Agent(
            role=f"{lang} to English translator",
            goal=f"Translate sentences in {lang} to English",
            backstory=f"You translate texts from {lang} to English",
            llm=llm,
            verbose=verbose,
        )

        

class EvaluationAgent:

    
    mqm_info = StringKnowledgeSource(
        content="""
            MQM (Multidimensional Quality Metrics) is a flexible framework for evaluating and annotating translation quality. 
            It provides a detailed categorization of errors based on their type and severity, 
            offering a structured way to identify and analyze issues in translations.
        """,
        metadata={}
    )


    def __init__(self, lang, llm, verbose=True) -> None:
        if llm:
            self.agent  = Agent(
            role="Machine translation evaluator.",
            goal=f"Evaluate a machine translated sentence from {lang} to english using Multidimensional Quality Metrics (MQM)",
            backstory=f"You evaluate machine translated sentences from {lang} to english using Multidimensional Quality Metrics (MQM)",
            knowledge_sources = [EvaluationAgent.mqm_info, self.get_mqm_template()],
            llm=llm,
            verbose=verbose,
        )
        else:
            self.agent  = Agent(
            role="Machine translation evaluator.",
            goal=f"Evaluate a machine translated sentence from {lang} to english",
            backstory=f"You evaluates machine translated sentences from {lang} to english",
            llm=llm,
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

        Total Segments Evaluated: [Number]
        Total Errors Identified: [Number]

        ------------------------------
        Error Breakdown by Type
        ------------------------------
        1. Accuracy:
        - Mistranslation: [check or not]
        - Omission: [check or not]
        - Addition: [check or not]
        - Untranslated: [check or not]

        2. Fluency:
        - Grammar: [check or not]
        - Punctuation: [check or not]
        - Spelling: [check or not]
        - Word Order: [check or not]
        - Register: [check or not]

        3. Terminology:
        - Inconsistent: [check or not]
        - Incorrect: [check or not]

        4. Locale/Style:
        - Style: [check or not]
        - Locale Conventions: [check or not]

        5. Formatting:
        - Tag Issues: [check or not]
        - Layout: [check or not]

        6. Other:
        - Non-linguistic Issues: [check or not]

        ------------------------------
        Error Breakdown by Severity
        ------------------------------
        1. Neutral: [check or not]
        2. Minor: [check or not]
        3. Major: [check or not]
        4. Critical: [check or not]

        ------------------------------
        Summary & Comments
        ------------------------------
        [Evaluator's general comments and observations about the quality of the translation.]

        ==============================
            END OF SCOREBOARD
        ==============================

    """,
    )
        return mqm_template




class RefinementAgent:

    mqm_info = StringKnowledgeSource(
        content="""
            MQM (Multidimensional Quality Metrics) is a flexible framework for evaluating and annotating translation quality. 
            It provides a detailed categorization of errors based on their type and severity, 
            offering a structured way to identify and analyze issues in translations.
        """,
        metadata={}
    )

    def __init__(self, llm, lang, verbose=True) -> None:
        if llm:
            self.agent  = Agent(
            role=f"Sentence Translation Refiner",
            goal=f"Refine sentence translations from {lang} to english based on MQM scorecard of the translation",
            backstory=f"You refine sentence translations from {lang} to english based on MQM scorecard of the translation",
            knowledge_sources = [RefinementAgent.mqm_info],
            llm=llm,
            verbose=verbose,
        )
        else:
            self.agent  = Agent(
            role=f"Sentence Translation Refiner",
            goal=f"Refine sentence translations from {lang} to english",
            backstory=f"You refine sentence translations from {lang} to english",
            llm=llm,
            verbose=verbose,
        )


