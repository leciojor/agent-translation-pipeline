'''
Streamlit frontend logic
'''

from backend.__main__ import agent_translation, system_translation
import streamlit as st
from streamlit import session_state as state
from backend.__main__ import agent_translation, system_translation

def exec_pipe(lang, input, model, mode, parallel_executions, k_iterations, nmt):
    if mode == 'llm':
        final_output = agent_translation(lang, model, input, parallel_executions, k_iterations)
    else:
        final_output = system_translation(lang, model, input, parallel_executions, k_iterations, nmt)

    translation = final_output[0]
    mqm_scoreboard = final_output[1]

    state['status'] = st.success("Agent pipeline finished the translation process")

    if st.button("Restart"):
        st.text(f"""
    ------------------------------------------------------------------------------------------------------------------------------------------------
    
    {lang.upper()} SOURCE : {input}

    ENGLISH TRANSLATION: {translation['refined_translation']}

    MQM SCOREBOARD: 

    {mqm_scoreboard}
          
    ------------------------------------------------------------------------------------------------------------------------------------------------
    """)


def main():
    st.title("English to Portuguese/German LLM Translation Pipeline")
    st.text('ADD READ ME')

    if "status" not in state:
        state['status'] = st.success("Fill the pipeline configurations and click START")

    with st.empty():
        state['status']

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
    
    if state['mode'] == 'nmt':
        state['nmt'] = st.selectbox("Machine Translation System", ["yandex", "bing", "alibaba"])

    state['lang'] = st.selectbox("Source Language", ["portuguese", "english"])
    state['input'] = st.text_input("TRANSLATE: ")

    if st.button("START PIPELINE EXECUTION"):
        if state['mode'] == 'nmt' and not state['nmt']:
            state['status'] = st.error("You cannot use the ")
        elif state['lang'] and state['input'] and state['model'] and state['mode'] and state['k'] and state['done']:
            state['status'] = st.error("RUNNING PIPELINE EXECUTION")
            st.spinner(text="In progress...")
            try:
                exec_pipe(state['lang'], state['input'], state['model'], state['mode'], state['executions'], state['k'], state['nmt'])
            except Exception as e:
                state['status'] = st.error(state['status'])

        else:
            state['status'] = st.error("Please fill all configurations before execution")








if __name__ == "__main__":
    main()    