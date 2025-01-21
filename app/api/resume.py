from fastapi import APIRouter, File, Body, UploadFile, HTTPException
from app.services.vectorize import vectorize_and_store_pdf
from app.services.search import search_query
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
async def upload_pdf(file: UploadFile = File(...)):

    try:
        # Path for saving the uploaded file
        uploads_directory = "uploads"

        # Check if the "uploads" folder exists, if not, create it
        if not os.path.exists(uploads_directory):
            os.makedirs(uploads_directory)

        # Save the uploaded file
        file_location = os.path.join(uploads_directory, file.filename)

        try:
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

        # Vectorize the PDF and store it
        vectorize_and_store_pdf(file_location)

        return {
            "message": f"File {file.filename} uploaded and vectorized successfully."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route to submit query and get response from the indexed data
@router.post("/ask_question")
async def ask_question(query: str = Body(...)):
    try:
        # Perform search based on the query
        response = search_query(query)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
