
from langchain_community.vectorstores import PGVector
from get_embedding_function import get_embedding_function

CONNECTION_STRING = "postgresql+psycopg2://postgres:avignon84@localhost:5432/postgres"
COLLECTION_NAME = 'mes_documents'

def retrieve_documents(question: str) -> str:
    embedding_function = get_embedding_function()
    dbvector = PGVector(connection_string=CONNECTION_STRING, embedding_function=embedding_function,collection_name=COLLECTION_NAME )
      # Récupérer l'objet HuggingFaceBgeEmbeddings à partir de la fonction d'embedding
    embeddings = embedding_function

    
    similar_documents = dbvector.similarity_search_with_score(question,k=2)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in similar_documents])
    
    return context_text

def get_var(var_name, prompt, other_vars):
    question = other_vars['query']
    print(question)
    
    context = retrieve_documents(question)
    return {
        'output': context
    }