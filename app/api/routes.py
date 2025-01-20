from fastapi import APIRouter

router = APIRouter()
vectorstore = None


@router.get("/")
async def root():
    return {"message": "Welcome to TalkToMyCV microservice!"}


@router.post("/upload")
async def upload_pdf(file: UploadFile):
    global vectorstore
    documents = load_pdf(file.file)
    vectorstore = create_vector_store(documents)
    return {"message": "PDF uploaded and processed successfully"}


@router.get("/query")
async def query_cv_endpoint(query: str):
    if vectorstore is None:
        return {"error": "Upload a PDF first"}
    response = query_cv(vectorstore, query)
    return {"response": response}
