from fastapi import APIRouter, File, Body, UploadFile, HTTPException, Request
from app.services.vectorize import vectorize_and_store_pdf
from app.services.search import search_query
from app.utils.limiter import limiter
import shutil
import os

router = APIRouter()


# Health check route
@router.get("/health")
async def health_check():
    try:
        # Return a simple health check response
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Health check failed")


# Route to upload PDF, vectorize and store it
@router.post("/upload_pdf")
async def upload_pdf(request: Request, file: UploadFile = File(...)):

    user_id = request.state.user_id  # Retrieve user_id
    uploads_directory = f"tmp/uploads/{user_id}"
    index_directory = f"tmp/vector_store/{user_id}"

    try:
        os.makedirs(uploads_directory, exist_ok=True)
        os.makedirs(index_directory, exist_ok=True)

        # Save the uploaded file
        file_location = os.path.join(uploads_directory, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Vectorize and store the PDF
        vectorize_and_store_pdf(file_location, index_directory)

        return {
            "message": f"File {file.filename} uploaded and vectorized successfully."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route to submit query and get response from the indexed data
@router.post("/ask_question")
@limiter.limit("4/minute")
async def ask_question(request: Request, query: str = Body(...)):
    try:
        user_id = request.state.user_id  # Retrieve user_id
        user_index_path = f"tmp/vector_store/{user_id}"
        default_index_path = "vector_store/default"

        if os.path.exists(user_index_path):
            index_path = user_index_path
            using_default = False
        else:
            index_path = default_index_path
            using_default = True

        # Check if the default index exists
        if not os.path.exists(index_path):
            raise HTTPException(
                status_code=500,
                detail="No valid vector database found. Please contact support.",
            )

        # Perform search based on the query
        response = search_query(query, index_path)

        return {
            "answer": response,
            "source": "default" if using_default else "user",
            "message": (
                "Answered from default knowledge base."
                if using_default
                else "Answered from your uploaded data."
            ),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
