import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from pyzbar.pyzbar import decode
import cv2

# Load the UPC type CSV
upc_data = pd.read_csv("upc_type.csv")

# Ensure the UPC codes in the CSV are strings and remove any extra whitespace
upc_data['upc'] = upc_data['upc'].astype(str).str.strip()

# Encode the 'type' column (food or beverage) into numeric values
label_encoder = LabelEncoder()
upc_data['encoded_type'] = label_encoder.fit_transform(upc_data['type'])

# Prepare the UPC dictionary for quick lookup
upc_dict = dict(zip(upc_data['upc'], upc_data['type']))

# Function to load the trained model
def load_model(model_path="ML_Model\Model\model.h5"):
    return tf.keras.models.load_model(model_path)

# Function to preprocess and predict the product type based on UPC
def predict_product_type(upc_code, model):
    # Encode the UPC code (convert to numeric representation)
    upc_code_numeric = pd.Series(upc_code).astype('category').cat.codes[0]

    # Predict the product type using the trained model
    prediction = model.predict(np.array([upc_code_numeric]))
    predicted_class = np.round(prediction[0][0])

    # Map prediction to type
    predicted_type = "Makanan Ringan" if predicted_class == 0 else "Minuman"
    
    # Menghitung confidence
    confidence = np.max(prediction) * 100  # Confidence dalam persen

    return predicted_type, confidence

# Function to process the uploaded image and make predictions
def process_image(image_path, model):
    # Load the image
    frame = cv2.imread(image_path)

    # Decode the UPC barcode from the image
    barcodes = decode(frame)

    results = []

    for barcode in barcodes:
        # Get the barcode data (UPC code) as a string
        upc_code = barcode.data.decode('utf-8').strip()
        print(f"Detected UPC code: {upc_code}")

        # Check if the UPC code is in the dictionary
        if upc_code in upc_dict:
            product_type = upc_dict[upc_code]
            predicted_type, confidence = predict_product_type(upc_code, model)

            # Hanya menyimpan hasil jika kategori valid (makanan ringan/minuman)
            if product_type in ["food", "beverage"]:
                results.append({
                    "predicted_class_upc": upc_code,
                    "confidence": f"{confidence:.2f}%",
                    "kategori": predicted_type
                })
    
    # Mengembalikan hasil valid atau daftar kosong
    return results if results else []
