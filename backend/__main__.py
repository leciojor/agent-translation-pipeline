'''
Crew call logic
'''
import json
from argparse import ArgumentParser
from Agents import TranslationAgent, EvaluationAgent, RefinementAgent, BestOutputAgent
from Tasks import Translation, Evaluation, Refinement, GettingBestOutput
import translators as ts
import threading
from crewai import Crew


def get_best_output(final_outputs, lang, llm, src):
    print('Getting Best Output')
    agent = BestOutputAgent(lang, llm).agent
    task = GettingBestOutput(agent, lang, src, final_outputs).task
    crew = Crew(agents=[agent], tasks=[task])
    output = crew.kickoff()
    final_result = json.loads(output.json)

    return final_outputs[final_result['best_translation_number']-1]

def pipe1(translator, input, lang, final_outputs, evaluator, refiner, k_iterations):
    print("Executing pipe 1")
    translation = Translation(translator.agent, input, lang)
    crew = Crew(agents=[translator.agent], tasks=[translation.task])
    output = crew.kickoff()
    translation_result = json.loads(output.json)

    pipe2(evaluator, refiner, lang, translation_result['translated_text'], translation_result['original_text'], final_outputs, k_iterations)
    

def pipe2(evaluator, refiner, lang, translation, src, final_outputs, k_iterations):
    print("Executing pipe 2")

    for _ in range(k_iterations):
        evaluation = Evaluation(evaluator.agent, lang, src, translation)
        refinement = Refinement(refiner.agent, lang, src, translation)
        crew = Crew(agents=[evaluator.agent, refiner.agent], tasks=[evaluation.task, refinement.task])
        output = crew.kickoff()
        tasks_outputs = output.tasks_output
        mqm_scoreboard = tasks_outputs[0].json
        output = json.loads(output.json)
        translation = output['refined_translation']

    final_outputs.append((output, mqm_scoreboard))
    

def agent_translation(lang, llm, input, k_models, k_iterations):
    translator = TranslationAgent(lang, llm)
    evaluator = EvaluationAgent(lang, llm)
    refiner = RefinementAgent(lang, llm)
    final_outputs = []

    # each pipe: translate -> evaluate -> refine (iterate k times)
    threads_pipelines = []
    for _ in range(k_models):
        threads_pipelines.append(threading.Thread(target = pipe1(translator, input, lang, final_outputs, evaluator, refiner, k_iterations)))

    
    final_output = get_best_output(final_outputs, lang, llm, input)

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
        thread = threading.Thread(target = pipe2(evaluator, refiner, lang, translation, input, final_outputs, k_iterations))
        threads_pipelines.append(thread)
        thread.start()

    for thread in threads_pipelines:
        thread.join()

    final_output = get_best_output(final_outputs, lang, llm, input)

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

    translation = final_output[0]
    mqm_scoreboard = final_output[1]

    print(f"""
    ------------------------------------------------------------------------------------------------------------------------------------------------
    
    {lang.upper()} SOURCE : {input}

    ENGLISH TRANSLATION: {translation['refined_translation']}

    MQM SCOREBOARD: 

    {mqm_scoreboard}
          
    ------------------------------------------------------------------------------------------------------------------------------------------------
    """)