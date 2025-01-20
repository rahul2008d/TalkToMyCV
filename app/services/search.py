from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def search_query(query: str, index_path: str = "vector_store/faiss_index") -> str:
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # Load FAISS vector store
    vector_store = FAISS.load_local(index_path, embeddings)

    # # Perform search query
    # results = vector_store.similarity_search(
    #     query, k=1
    # )  # Adjust k as needed for number of results
    # return results[0].page_content if results else "No relevant results found."
    # Initialize OpenAI chat model for answering queries
    chat_model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)

    # Create the ConversationalRetrievalChain with the vector store and chat model
    qa_chain = ConversationalRetrievalChain.from_llm(
        chat_model, vector_store.as_retriever()
    )

    # Retrieve relevant document from the vector store
    results = vector_store.similarity_search(
        query, k=1
    )  # Adjust k as needed for the number of documents to retrieve

    if not results:
        return "No relevant results found."

    # Extract the document content from the retrieved results
    retrieved_document_content = results[0].page_content

    # Construct the prompt
    prompt = f"""
    You are a helpful assistant that is specialized in interpreting resume content. Given the context below, answer the user's question as precisely and concisely as possible.

    Context: {retrieved_document_content}

    User's Question: {query}

    Answer:
    """

    # Get the response from the QA chain using the generated prompt
    response = chat_model.chat([{"role": "system", "content": prompt}])

    # Return the final answer from the response
    return response["choices"][0]["message"]["content"].strip()
