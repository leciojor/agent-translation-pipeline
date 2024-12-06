
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource



class MQMKnowledge:
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
    
    def __init__(self, lang):
        self.lang = lang


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
