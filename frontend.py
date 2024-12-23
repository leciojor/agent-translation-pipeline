'''
Streamlit frontend logic
'''

import json
from backend.__main__ import agent_translation, system_translation
import streamlit as st
from streamlit import session_state as state
from backend.__main__ import agent_translation, system_translation

def format_output(str):
    return '\n'.join(str[i:i+55] for i in range(0, len(str), 55))

def format_mqm(mqm):
    mqm = json.loads(mqm)
    final_txt = """"""
    for key in mqm:
        final_txt += f"{key.upper()}: {format_output(str(mqm[key]))} \n"

    return final_txt

def restart():
    state['lang'] = ""
    state['input'] = ""
    state['model'] = ""
    state['mode'] = ""
    state['executions'] = None
    state['k'] = None
    state['nmt'] = ""

def exec_pipe(lang, input, model, mode, parallel_executions, k_iterations, nmt):
    if mode == 'llm':
        final_output = agent_translation(lang, model, input, parallel_executions, k_iterations)
    else:
        final_output = system_translation(lang, model, input, parallel_executions, k_iterations, nmt)

    initial = final_output[0]
    translation = final_output[1]
    mqm_scoreboard = final_output[2]


    st.text(f"""
    ------------------------------------------------------------------------------------------------------------------------------------------------
    
    {lang.upper()} SOURCE : {format_output(input)}

    INITIAL ENGLISH TRANSLATION: {format_output(initial)}

    FINAL ENGLISH TRANSLATION: {format_output(translation['refined_translation'])}

    MQM SCOREBOARD FROM FINAL ENGLISH TRANSLATION: 

    {format_mqm(mqm_scoreboard)}
        
    ------------------------------------------------------------------------------------------------------------------------------------------------
    """)

    if st.button("Restart"):
        restart()



def main():
    st.title("Portuguese/German to English LLM Translation Pipeline")
    
    st.success("Fill the pipeline configurations and click START")


    if 'lang' not in state:
        state['lang'] = ""
    if 'input' not in state:
        state['input'] = ""
    if 'model' not in state:
        state['model'] = ""
    if 'mode' not in state:
        state['mode'] = ""
    if 'executions' not in state:
        state['executions'] = None
    if 'k' not in state:
        state['k'] = None
    if 'nmt' not in state:
        state['nmt'] = ""
    
    

    state['lang'] = st.selectbox("Source Language", ["portuguese", "german"])
    state['input'] = st.text_input("INPUT: ")
    state['model'] = st.selectbox("BASE LLM", ["ollama/wizardlm2", "ollama/llama2", "Gpt4o-mini"])
    state['mode'] = st.selectbox("Pipeline mode", ["llm", "nmt"])
    state['executions'] = st.number_input("Enter the amount of parallel executions", value=1, format="%d")
    state['k'] = st.number_input("Enter the amount of refinement iterations for each paralel execution", value=1, format="%d")

    if state['mode'] == 'nmt':
        state['nmt'] = st.selectbox("Machine Translation System", ["yandex", "bing", "alibaba"])

    if st.button("START PIPELINE EXECUTION"):
        if state['mode'] == 'nmt' and not state['nmt']:
            st.error("You cannot use the NMT mode without specifing the system you would like to use", "error")
            st.rerun()
        elif state['lang'] and state['input'] and state['model'] and state['mode'] and state['k']:
            with st.spinner(text="In progress..."):    
                st.warning("PIPELINE IS RUNNING...")
                try:
                    if state['model'] == "Gpt4o-mini":
                        exec_pipe(state['lang'], state['input'], "", state['mode'], state['executions'], state['k'], state['nmt'])
                    else:
                        exec_pipe(state['lang'], state['input'], state["model"], state['mode'], state['executions'], state['k'], state['nmt'])
                except Exception as e:
                    st.error(e)

        else:
            st.error("Please fill all configurations before execution")
            st.rerun()








if __name__ == "__main__":
    main()    