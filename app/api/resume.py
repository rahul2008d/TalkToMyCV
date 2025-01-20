from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.vectorize import vectorize_and_store_pdf
from app.services.search import search_query
import shutil

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
        # Save the uploaded file
        file_location = f"uploads/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Vectorize the PDF and store it
        vectorize_and_store_pdf(file_location)

        return {
            "message": f"File {file.filename} uploaded and vectorized successfully."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route to submit query and get response from the indexed data
@router.post("/ask_question")
async def ask_question(query: str):
    try:
        # Perform search based on the query
        response = search_query(query)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
