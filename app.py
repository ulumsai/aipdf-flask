from flask import Flask, request, jsonify
from flask_cors import CORS

# from . import core
import core
from langchain_core.messages import AIMessage, HumanMessage
import os
from dotenv import load_dotenv
import mimetypes

import logging
from datetime import datetime

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

# Configure logging
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

log_filename = os.path.join(log_dir, datetime.now().strftime('app_%Y-%m-%d.log'))
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
file_handler.setFormatter(formatter)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

app.logger.info('Flask application startup')
## end logging

def run_on_start():
    print('Process get vectore from document ...')
    text_chunks = []

    documents = []
    for filename in os.listdir("core/docs"):
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type == 'application/pdf':
            app.logger.info(f'processed file : {filename}')
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
    # .. save ke elasticsearch

    print('finish get vectore.')

run_on_start()  # Call the function on app startup

def process_prompt(input):
    langchain_local = core.langchain_local.LangchainLocal(state)
    
    ## load vectorstore from elasticsearch
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
    app.logger.info('App Accessed')
    data = {
        "message": "Hello, wellcome to chatbot-ai-pdf",
    }
    return jsonify(data), 200

@app.route('/ask', methods=['POST'])
def process():
    input_data = request.json.get('question')
    app.logger.info(f'Received request data: {input_data}')
    
    if not input_data:
        error_msg = "No data provided"
        app.logger.warning(error_msg)
        return jsonify({"error": error_msg}), 400
    
    try:
         # Process the request and log the response
        response_list = process_prompt(input_data)
        app.logger.info(f'Response data: {response_list}')
        return jsonify({"message": response_list}), 200
    except Exception as e:
        error_msg = str(e)
        app.logger.error(f'Error occurred: {error_msg}')
        return jsonify({"error": error_msg}), 500
    
if __name__ == '__main__':
    app.run(debug=os.getenv("FLASK_DEBUG"))