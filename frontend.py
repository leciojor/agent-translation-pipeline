'''
Streamlit frontend logic
'''

from backend.__main__ import agent_translation, system_translation
import streamlit as st
from streamlit import session_state as state
from backend.__main__ import agent_translation, system_translation

def restart():
    state['status'] = ("Fill the pipeline configurations and click START", "success")

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

    state['status'] = ("Agent pipeline finished the translation process", "success")

    st.text(f"""
    ------------------------------------------------------------------------------------------------------------------------------------------------
    
    {lang.upper()} SOURCE : {input}

    INITIAL ENGLISH TRANSLATION: {initial}

    FINAL ENGLISH TRANSLATION: {translation['refined_translation']}

    MQM SCOREBOARD: 

    {mqm_scoreboard}
        
    ------------------------------------------------------------------------------------------------------------------------------------------------
    """)

    if st.button("Restart"):
        restart()



def main():
    st.title("Portuguese/German to English LLM Translation Pipeline")
    st.text('ADD READ ME')

    if "status" not in state:
        state['status'] = ("Fill the pipeline configurations and click START", 'success')

    with st.empty():
        if state['status'][1] == 'success':
            st.success(state['status'][0])
        elif state['status'][1] == 'warning':
            st.warning(state['status'][0])
        elif state['status'][1] == 'error':
            st.error(state['status'][0])

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
            state['status'] = ("You cannot use the NMT mode without specifing the system you would like to use", "error")
            st.rerun()
        elif state['lang'] and state['input'] and state['model'] and state['mode'] and state['k']:
            state['status'] = ("RUNNING PIPELINE EXECUTION", "warning")
            st.spinner(text="In progress...")
            try:
                if state['model'] == "Gpt4o-mini":
                    exec_pipe(state['lang'], state['input'], "", state['mode'], state['executions'], state['k'], state['nmt'])
                else:
                    exec_pipe(state['lang'], state['input'], state["model"], state['mode'], state['executions'], state['k'], state['nmt'])
            except Exception as e:
                state['status'] = (state['status'], "error")

        else:
            state['status'] = ("Please fill all configurations before execution", "error")
            st.rerun()








if __name__ == "__main__":
    main()    