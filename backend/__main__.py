'''
Crew call logic
'''
import json

from argparse import ArgumentParser
from Agents import TranslationAgent, EvaluationAgent, RefinementAgent
from Tasks import Translation, Evaluation, Refinement
import translators as ts
import threading
from crewai import Crew


def get_best_output(final_outputs):
    return final_outputs[0]

def pipe1(translator, input, lang, final_outputs, evaluator, refiner):
    print("Executing pipe 1")
    translation = Translation(translator.agent, input, lang)
    crew = Crew(agents=[translator.agent], tasks=[translation.task])
    output = crew.kickoff()
    text = output.raw

    if text[0] == '`':
        translation_result = text[7:-4]
    else:
        translation_result = text

    translation_result = json.loads(translation_result)
    pipe2(evaluator, refiner, lang, translation_result['translated_text'], translation_result['original_text'], final_outputs)
    

def pipe2(evaluator, refiner, lang, translation, src, final_outputs):
    print("Executing pipe 2")
    evaluation = Evaluation(evaluator.agent, lang, src, translation)
    refinement = Refinement(refiner.agent, lang, src, translation)
    crew = Crew(agents=[evaluator.agent, refiner.agent], tasks=[evaluation.task, refinement.task])
    output = crew.kickoff()

    final_outputs.append(output)
    

def agent_translation(lang, llm, input, k_models, k_iterations):
    translator = TranslationAgent(lang, llm)
    evaluator = EvaluationAgent(lang, llm)
    refiner = RefinementAgent(lang, llm)
    final_outputs = []

    # each pipe: translate -> evaluate -> refine (iterate k times)
    threads_pipelines = []
    for _ in range(k_models):
        threads_pipelines.append(threading.Thread(target = pipe1(translator, input, lang, final_outputs, evaluator, refiner)))

    '''TODO: Add logic to get the final translation with the highest BLUE score'''
    
    final_output = get_best_output(final_outputs)

    return final_output

def system_translation(lang, llm, input, k_models, k_iterations, nmt):
    evaluator = EvaluationAgent(lang, llm)
    refiner = RefinementAgent(lang, llm)
    final_outputs = []
    if lang == 'portuguese':
        l = 'pt'
    elif lang == 'german':
        l = 'de'

    translation = ts.translate_text(input, translator=nmt, from_language=l, to_language='en')
    print(f"{nmt} initialy translated to {translation}")

    # each pipe: translate -> evaluate -> refine (iterate k times)
    threads_pipelines = []
    for _ in range(k_models):
        thread = threading.Thread(target = pipe2(evaluator, refiner, lang, translation, input, final_outputs))
        threads_pipelines.append(thread)
        thread.start()

    for thread in threads_pipelines:
        thread.join()

    '''TODO: Add logic to get the final translation with the highest BLUE score'''

    final_output = get_best_output(final_outputs)

    return final_output


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("language", help="Language that will be translated to English (portuguese/english)")
    parser.add_argument("input", help="Sentence to be translated")
    parser.add_argument("model", help="Base LLM for agents")
    parser.add_argument("mode", help="Pipeline mode (llm/nmt)")
    parser.add_argument("k", type=int, help="Amount of parallel executions")
    parser.add_argument("iterations", type=int, help="Amount of refinement iterations for each execution")
    parser.add_argument(
        "--nmt_model", 
        help="Specify the NMT model to use for system translation",
        required=False
    )
    
    args = parser.parse_args()
    lang = args.language.lower()
    input = args.input
    model = args.model 
    mode = args.mode
    nmt = args.nmt_model
    k_models = args.k
    k = args.iterations

    print()
    print(f"Starting pipeline translation from {lang} to english")
    if mode == 'llm':
        final_output = agent_translation(lang, model, input, k_models, k)
    else:
        final_output = system_translation(lang, model, input, k_models, k, nmt)


    print(f"""
    ------------------------------------------------------------------------------------------------------------------------------------------------
    
    {lang.upper()} SOURCE : {input}

    ENGLISH TRANSLATION: {final_output}
          
    ------------------------------------------------------------------------------------------------------------------------------------------------
    """)