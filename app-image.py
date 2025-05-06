import streamlit as st
from openai import OpenAI
from PIL import Image
import fitz  # PyMuPDF
import os
import docx
import pandas as pd
import base64
import io

st.set_page_config(page_title="OpenAI Assistant", layout="wide")
st.title("🤖 OpenAI Assistant: Prompt + Files + GPT-4 Vision")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = st.text_area("📝 Enter your prompt", height=150)
uploaded_image = st.file_uploader("🖼️ Upload an image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
uploaded_file = st.file_uploader("📄 Upload a file (PDF, TXT, DOCX, XLSX)", type=["pdf", "txt", "docx", "xlsx"])
file_text = ""
image_bytes = None

def extract_file_text(file):
    text = ""
    if file.type == "application/pdf":
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    elif file.type == "text/plain":
        text = file.read().decode("utf-8")
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(file)
        text = df.to_string(index=False)
    return text

def encode_image_to_base64(image_bytes, mime_type="image/png"):
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"

if uploaded_image:
    image_bytes = uploaded_image.read()
    image_display = Image.open(io.BytesIO(image_bytes))
    st.image(image_display, caption="🖼️ Uploaded Image", use_container_width=True)

if uploaded_file:
    file_text = extract_file_text(uploaded_file)
    st.text_area("📄 Extracted File Content", value=file_text, height=200)

if st.button("🚀 Submit to OpenAI"):
    try:
        if uploaded_image and image_bytes:
            mime_type = uploaded_image.type or "image/png"
            image_base64_url = encode_image_to_base64(image_bytes, mime_type)
            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt + "\n\n" + file_text},
                    {"type": "image_url", "image_url": {
                        "url": image_base64_url,
                        "detail": "high"
                    }}
                ]
            }]
            model = "gpt-4-turbo"  # vision-capable
        else:
            messages = [{"role": "user", "content": prompt + "\n\n" + file_text}]
            model = "gpt-4"

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1000
        )

        st.markdown("### 🤖 Response:")
        st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"❌ Error: {e}")
