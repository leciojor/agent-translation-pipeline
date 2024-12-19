### AGENT TRANSLATION PIPELINE  ###

# Steps To Execute the Pipeline Logic:

* install the dependencies from requirements.txt
* add one .env file to the root folder with the following format:

```bash
OPENAI_API_KEY= <your-openai-key>

OPENAI_MODEL_NAME=gpt-4o-mini 

OLLAMA_HOST=http://127.0.0.1:11434

CONTEXT=32000
```

* then, in case you would like to run the pipeline logic with the intuitiveness of the front end, run the following command from the root directory:

```bash
streamlit run frontend.py
```

* otherwise, you can run the logic directly from the terminal with the following command:

```bash
python -m backend <source-language (portuguese/german)> <input-to-translate-to-english> <llm-base-model *leave it with empty string if the desired model it gpt4o-mini> <pipeline mode (nmt/llm)>  <amount-of-paralel-executions (integer)>  <amout-of-refinement-operations (integer)> <nmt-system (just for nmt mode)>
```
*If you want to use one of the available ollama models, you will need to make sure that ollama is running in your machine and that the respective model was downloaded locally

*The pipeline mode refers to what the system will use to do the initial translation from the pipeline. In case you would like an LLM to do that, chose "llm". If you would like another neural translation system to do that translation, chose "nmt" and select the system you would like to be used.

*The whole code in /backend is documented in case you would like to see how the main logic works (pipeline architecture, agents/tasks/crews definitions, etc)

*I strongly recommend using the streamlit frontend for executing the logic

![image](https://github.com/user-attachments/assets/a672926a-e587-4b49-a2d6-32ef7c98b211)

![image](https://github.com/user-attachments/assets/bc480a1e-4851-45cd-abae-7e3068312227)


