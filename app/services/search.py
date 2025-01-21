from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv
from functools import lru_cache
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Constants
INDEX_PATH = "vector_store/faiss_index"
ANSWER_PROMPT_TEMPLATE = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. Be as verbose and educational in your response as possible. 

Context: {context}
Question: "{question}"
Answer:
"""


# Initialize OpenAI Embeddings and Chat Model
def initialize_resources():
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vector_store = FAISS.load_local(
        INDEX_PATH, embeddings, allow_dangerous_deserialization=True
    )
    chat_model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)
    return embeddings, vector_store, chat_model


# Cache for Reusable Resources
@lru_cache(maxsize=1)
def get_qa_chain():
    _, vector_store, chat_model = initialize_resources()

    answer_prompt = ChatPromptTemplate.from_template(ANSWER_PROMPT_TEMPLATE)

    qa_chain = (
        {"context": vector_store.as_retriever(), "question": RunnablePassthrough()}
        | answer_prompt
        | chat_model
        | StrOutputParser()
    )

    return qa_chain


# Function to Handle User Query
def search_query(query: str) -> str:
    # Retrieve QA Chain
    qa_chain = get_qa_chain()

    # Get Response from QA Chain
    response = qa_chain.invoke(query)

    # Return Final Answer
    return response
