import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import os

# Configure Streamlit page
st.set_page_config(page_title="Image to GPT-4", layout="wide")
st.title("🖼️ Upload an Image for GPT-4 Vision")

# Load OpenAI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Upload image
uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Prompt
prompt = st.text_area("Enter your prompt to describe the image", "What is in this image?")

def encode_image_to_base64(image_file):
    encoded = base64.b64encode(image_file.read()).decode("utf-8")
    mime = image_file.type or "image/jpeg"
    return f"data:{mime};base64,{encoded}"

# Display uploaded image
if uploaded_image:
    image_display = Image.open(uploaded_image)
    st.image(image_display, caption="Uploaded Image", use_container_width=True)

# Submit button
if st.button("Send to OpenAI"):
    if uploaded_image and prompt:
        try:
            image_url = encode_image_to_base64(uploaded_image)
            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {
                        "url": image_url,
                        "detail": "high"
                    }}
                ]
            }]

            response = client.chat.completions.create(
                model="gpt-4o",  # or gpt-4-turbo with vision, depending on your access
                messages=messages,
                max_tokens=1000
            )

            st.markdown("### 🧠 GPT-4 Response:")
            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("Please upload an image and enter a prompt.")

