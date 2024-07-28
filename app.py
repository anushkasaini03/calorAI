import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
    response = model.generate_content([input_prompt, image[0]])
    return response.text

# Function to setup input image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Set page config
st.set_page_config(page_title="CalorAI", layout="wide", initial_sidebar_state="expanded")

# Custom CSS (unchanged)
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 20px;
        border: none;
        padding: 10px 25px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 10px;
    }
    .uploadedFile {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stHeader {
        color: #2E8B57;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #e6f3ff;
    }
    </style>
    """, unsafe_allow_html=True)

# App layout (unchanged)
st.title("🍽️ CalorAI")
st.subheader("Intelligent Calorie and Nutrition Analysis")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📸 Upload Food Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

with col2:
    st.markdown("### 🔍 Nutrition Analysis")
    input_prompt = st.text_area("Customize your analysis prompt (optional):", 
                                value="""Analyze the food items in the image and provide the following details:

1. List each food item with its estimated calorie content.
2. Calculate the total calories for the entire meal.
3. Provide a breakdown of macronutrients (protein, carbs, fats) in percentages.
4. Assess the overall healthiness of the meal.
5. Suggest any improvements or alternatives for a more balanced diet.""",
                                height=200)
    
    analyze_button = st.button("Analyze Nutrition")

    if analyze_button and uploaded_file is not None:
        with st.spinner("🧠 AI is analyzing your meal..."):
            try:
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_prompt, image_data)
                st.success("Analysis complete!")
                st.markdown("### 📊 Nutrition Analysis Results")
                st.markdown(response)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    elif analyze_button and uploaded_file is None:
        st.warning("⚠️ Please upload an image before analyzing.")

# Sidebar (unchanged)
st.sidebar.title("About CalorAI")
st.sidebar.info("""
CalorAI uses advanced image recognition and AI to analyze your meals.
Simply upload a photo of your food to get detailed nutritional information and personalized advice.
""")

st.sidebar.title("💡 Tips for Best Results")
st.sidebar.markdown("""
- Use clear, well-lit images
- Include all food items in the frame
- Avoid blurry or dark photos
- Try different angles for complex meals
""")

st.sidebar.title("🔒 Privacy Note")
st.sidebar.info("Your images are processed securely and not stored after analysis.")

# Footer (unchanged)
st.markdown("---")
st.markdown("Developed with ❤️ by CalorAI | Powered by Gemini AI")
