from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os
from predict import load_model, process_image

app = FastAPI()

# Load the trained model
model = load_model("ML_Model\Model\model.h5")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file:
        return JSONResponse(status_code=400, content={"message": "No file provided"})
    
    # Pastikan direktori temp ada
    temp_dir = "./temp"
    os.makedirs(temp_dir, exist_ok=True)

    # Save the uploaded file temporarily
    image_path = os.path.join(temp_dir, file.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process the image and make predictions
    results = process_image(image_path, model)

    # Clean up: Remove the temporary file after processing
    os.remove(image_path)

    return {"predictions": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
