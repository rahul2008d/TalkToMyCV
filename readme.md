# TalkToMyCV - FastAPI Backend with RAG

**Copyright (c) Rahul Datta**
[Click here to talk to my CV](https://portfolio.funcodingwithrahul.com/ai-document-query)

A powerful **API service** designed to process and analyze CVs (in PDF format) and provide intelligent responses to user queries. This API utilizes **Retrieval-Augmented Generation (RAG)** with **LangChain** and **FAISS** for efficient document retrieval and intelligent question answering.

---

## 🚀 **Project Overview**

TalkToMyCV is a **FastAPI-based backend** that processes PDF CVs uploaded by users and allows them to ask questions regarding the information in the CVs. The application leverages **RAG** to provide accurate and context-aware responses by first retrieving relevant information from the CV and then generating an answer based on the context.

- **Backend**: FastAPI (with Uvicorn)
- **Purpose**: Process CVs (PDFs), extract data, and answer questions with advanced retrieval and generation techniques.
- **Tech**: LangChain for RAG, FAISS for efficient document retrieval
- **Deployment**: Dockerized for easy cloud integration

---

## 🧑‍💻 **Key Features**

### 1. **PDF Upload & Processing**

- API endpoint to upload CVs in **PDF format**.
- Extract text and relevant information from the uploaded CV.

### 2. **Retrieval-Augmented Generation (RAG)**

- **LangChain** is used to combine document retrieval with generative AI models for answering questions.
- **FAISS** is used for efficient **vector-based** similarity search, ensuring fast retrieval of relevant content from the CVs.

### 3. **Question Answering System**

- Ability to ask questions about the CV’s content.
- Intelligent response generation using a combination of **retrieval** and **generation** techniques, ensuring context-aware answers.

### 4. **Scalable and Extensible**

- The API is designed to scale easily and integrate with other services and frontend projects.
- Future enhancements could include integrating **Machine Learning** models for more advanced processing.

### 5. **Dockerized for Deployment**

- The project is fully Dockerized, making it ready for cloud deployment with minimal configuration.

---

## 🔧 **Tech Stack**

- **Backend**:
  - **FastAPI** for efficient handling of requests and fast responses.
  - **Uvicorn** for serving the FastAPI app in a production-ready environment.
- **Document Processing**:

  - Utilizes libraries like **PyMuPDF** for PDF text extraction.

- **Retrieval-Augmented Generation (RAG)**:
  - **LangChain** for the seamless integration of document retrieval and generative models.
  - **FAISS** for efficient similarity-based document retrieval.
- **Deployment Tools**:
  - **Docker** for containerization and easy deployment across various platforms.
  - **Poetry** for Python dependency management.

---

## 🎯 **Installation & Setup**

### Prerequisites

- Python 3.8+
- Docker (for containerized deployment)
- FAISS and LangChain libraries

### Steps to Run Locally

1. **Clone the repository:**

   ```bash
   - git clone https://github.com/rahuldatta/talktomycv.git
   - cd talktomycv
   - poetry install
   - poetry add langchain faiss-cpu
   - uvicorn app.main:app --reload
   ```

## 📑 API Endpoints

### **`POST /upload-pdf/`**

- **Method**: `POST`
- **Description**: Upload a PDF CV for processing. The PDF will be extracted and stored for future query processing.

#### Request Body:

```json
{
  "file": "PDF file (multipart/form-data)"
}
```

### **`POST /ask-question/`**

- **Method**: `POST`
- **Description**: Ask a question based on the uploaded PDF. The system will retrieve relevant content from the PDF and generate an answer.

#### Request Body:

```json
{
  "question": "What is the candidate's experience?"
}


{
  "answer": "The candidate has 5 years of experience in software development, specializing in web applications."
}
```

This will render the request body and response in a clean and readable format when viewed in Markdown-supported environments.
