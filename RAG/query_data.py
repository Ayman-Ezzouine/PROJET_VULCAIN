import argparse
import logging
from logging.handlers import RotatingFileHandler
from langchain.vectorstores.chroma import Chroma
from langchain_community.vectorstores import PGVector
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"
CONNECTION_STRING = "postgresql+psycopg2://postgres:avignon84@localhost:5432/postgres"
COLLECTION_NAME = 'mes_documents'
PROMPT_TEMPLATE = """
Réponds à la question en français et en te basant sur le contexte ci-dessus:

{context}

---

Réponds à la question en français et en te basant sur le contexte ci-dessus: {question}
"""
logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

def call_api(prompt, options, context):
    # The 'options' parameter contains additional configuration for the API call.
    config = options.get('config', {})
    additional_option = config.get('additionalOption', None)

    # The 'context' parameter provides info about which vars were used to create the final prompt.
    user_variable = context.get('vars', {}).get('userVariable', None)

    # The prompt is the final prompt string after the variables have been processed.
    # Custom logic to process the prompt goes here.
    # For instance, you might call an external API or run some computations.Z
    output = query_rag(prompt)

    # The result should be a dictionary with at least an 'output' field.
    result = {
        "output": output,
    }

    # Assuming some_error_condition and token_usage_calculated are defined somewhere
    some_error_condition = False  # Set this based on actual error conditions
    token_usage_calculated = False  # Set this based on actual token usage calculation

    if some_error_condition:
        result['error'] = "An error occurred during processing"

    if token_usage_calculated:
        # If you want to report token usage, you can set the 'tokenUsage' field.
        token_count = 0  # Replace with actual token count
        prompt_token_count = 0  # Replace with actual prompt token count
        completion_token_count = 0  # Replace with actual completion token count
        result['tokenUsage'] = {"total": token_count, "prompt": prompt_token_count, "completion": completion_token_count}

    return result

def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    logger.info('here is the query : ' + query_text)
    query_rag(query_text)


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    # dbvector = PGVector(connection_string=CONNECTION_STRING, embedding_function=embedding_function,collection_name=COLLECTION_NAME )
    logging.info(f"Generated prompt: {query_text}")
    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=2)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = Ollama(model="mistral")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return formatted_response


if __name__ == "__main__":
    main()
