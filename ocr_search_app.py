import streamlit as st
import easyocr
import numpy as np
from PIL import Image
from transformers import pipeline

# Load EasyOCR Reader for Hindi and English
reader = easyocr.Reader(['hi', 'en'])

# Force Huggingface Transformers to use PyTorch explicitly
qa_pipeline = pipeline('question-answering', model='distilbert-base-cased-distilled-squad', framework='pt')

# Function to perform OCR on the image
def ocr_image(uploaded_image):
    # Convert the uploaded image to a NumPy array
    image = Image.open(uploaded_image)
    image_np = np.array(image)

    # Perform OCR using EasyOCR
    result = reader.readtext(image_np, detail=0, paragraph=True)
    return " ".join(result)

# Function to search keywords in extracted text using the question-answering pipeline
def search_keywords(extracted_text, keyword):
    # We are using Huggingface's QA model for a text search
    search_result = qa_pipeline({
        'context': extracted_text,
        'question': f"Where is {keyword} mentioned in the text?"
    })

    return search_result['answer']

# Streamlit Web Interface
st.title(" OCR and Document Search Web Application ")
st.write("Upload an image containing text in Hindi and English, extract the text, and search for keywords.")

# Upload Image
uploaded_image = st.file_uploader("Upload an image file (JPG,JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_image:
    # Display the uploaded image
    st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

    # OCR Extraction
    st.write("Extracting text from the image...")
    extracted_text = ocr_image(uploaded_image)

    # Display the extracted text
    st.write("### Extracted Text")
    st.write(extracted_text)

    # Keyword Search using the QA model
    st.write("### Search in Extracted Text")
    keyword = st.text_input("Enter a keyword to search:")

    if keyword:
        search_result = search_keywords(extracted_text, keyword)
        st.write(f"Search Result: {search_result}")

# Add copyright message
st.write("© 2024 Made by PriyaSammal")