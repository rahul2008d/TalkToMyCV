from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from transformers import pipeline


def create_vector_store(documents):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore


def query_cv(vectorstore, query: str):
    qa_chain = load_qa_chain(vectorstore, pipeline="text-davinci-003")
    return qa_chain.run(query)
