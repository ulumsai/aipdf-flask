from flask import Flask, request, jsonify
from flask_cors import CORS

from . import core
from langchain_core.messages import AIMessage, HumanMessage
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()

app.config["FLASK_APP"] = os.getenv("FLASK_APP")
app.config["FLASK_ENV"] = os.getenv("FLASK_ENV")

state = {
    "chat_dialog_history":[],
    "embedding_model":"GooglePalm Embeddings",
    "llm_type":"Google",
    "error":False,
    "vectorstore":[],
    "messages":[],
}

def run_on_start():
    print('Process get vectore from document ...')
    text_chunks = []
    
    documents = []
    for filename in os.listdir("core/docs"):
        documents.append(filename)

    if documents is not None:
        for doc in documents:
            upload = core.uploadFile.UploadFile(doc)
            splits = upload.get_document_splits()
            text_chunks.extend(splits)

    model_name = state["embedding_model"]
    get_vectorstore_instance = core.ingest.GetVectorstore()
    state["vectorstore"] = get_vectorstore_instance.get_vectorstore(
        text_chunks, model_name
    )
    
    print('finish get vectore.')

run_on_start()  # Call the function on app startup

def process_prompt(input):
    langchain_local = core.langchain_local.LangchainLocal(state)
    response_generator = langchain_local.get_response(
        user_input=input,
        chat_history=state["chat_dialog_history"],
        vectorstore=state["vectorstore"],
    )
    
    response_list = []
    for response_chunk in response_generator:
        if response_chunk !="":
            response_list.append(response_chunk)
            
    state['chat_dialog_history'].append(HumanMessage(content=input))
    state['chat_dialog_history'].append(AIMessage(content=response_list))
    
    return response_list


@app.route('/')
def index():
    data = {
        "message": "Hello, wellcome to chatbot-ai-pdf",
    }
    return jsonify(data), 200

@app.route('/ask', methods=['POST'])
def process():
    input_data = request.json.get('question')
    if not input_data:
        return jsonify({"error": "No data provided"}), 400
    try:
        response_list = process_prompt(input_data)
        return jsonify({"message": response_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)