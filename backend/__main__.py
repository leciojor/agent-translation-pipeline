'''
Crew call logic
'''

from argparse import ArgumentParser
from backend.Agents import TranslationAgent, EvaluationAgent, RefinementAgent
from backend.Tasks import Translation, Evaluation, Refinement
from backend.Crews import Translation, Evaluation, Refinement
import translators as ts
import threading


def pipe1(translator, inputs, input, lang, final_output):
    task = Translation(translator.agent, input, lang)
    results = task.execute(inputs = inputs)
    #pipe2()
    return results

def pipe2(evaluator, translation, src, final_output):
    # task = Evaluation(evaluator.agent, src, translation)
    # inputs = {"Source Sentence": src, "Translation": translation}
    # results = task.execute(inputs = inputs)
    # return results
    pass
    '''TODO: add crew setup for pipe 2 '''

def agent_translation(lang, llm, input, k_models, k_iterations, final_output):
    translator = TranslationAgent(lang, llm)
    evaluator = EvaluationAgent(lang, llm)
    refiner = RefinementAgent(lang, llm)
    inputs = {"Source Sentence": input}
    

    # each pipe: translate -> evaluate -> refine (iterate k times)
    threads_pipelines = []
    for _ in range(k_models):
        threads_pipelines.append(threading.Thread(target = pipe1(translator, inputs, input, lang, final_output)))

    '''TODO: Add logic to get the final translation with the highest BLUE score'''

def system_translation(lang, llm, input, k_models, k_iterations, nmt, final_output):
    evaluator = EvaluationAgent(lang, llm)
    refiner = RefinementAgent(lang, llm)
    inputs = {"Source Sentence": input}
    if lang == 'portuguese':
        l = 'pt'
    elif lang == 'german':
        l = 'de'

    translation = ts.translate_text(input, translator=nmt, from_language=l, to_language='en')
    
    # each pipe: translate -> evaluate -> refine (iterate k times)
    threads_pipelines = []
    for _ in range(k_models):
        thread = threading.Thread(target = pipe2(evaluator, translation, input, final_output))
        threads_pipelines.append(thread)
        thread.start()

    for thread in threads_pipelines:
        thread.join()

    '''TODO: Add logic to get the final translation with the highest BLUE score'''


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("language", help="Language that will be translated to English")
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
    lang = args.language
    input = args.input
    model = args.models 
    mode = args.mode
    nmt = args.nmt_model
    k_models = args.k
    k = args.iterations

    final_output = """"""

    if mode == 'llm':
        agent_translation(lang, model, input, k_models, k, final_output)
    else:
        system_translation(lang, model, input, k_models, k, nmt, final_output)


    print(f"""
    ------------------------------------------------------------------------------------------------------------------------------------------------
    
    {lang.upper()} SOURCE : {input}

    ENGLISH TRANSLATION: {final_output}
          
    ------------------------------------------------------------------------------------------------------------------------------------------------
    """)