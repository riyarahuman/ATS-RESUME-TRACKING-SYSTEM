import io
import base64
import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Updated to use Gemini 1.5
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  # 🔄 Switched to the latest model
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

# ✅ Proper PDF processing (handles multiple pages)
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())  # Convert PDF to images

        pdf_parts = []
        for img in images:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format="PNG")
            img_data = base64.b64encode(img_byte_arr.getvalue()).decode()
            pdf_parts.append({"mime_type": "image/png", "data": img_data})

        return pdf_parts
    else:
        st.error("No file uploaded. Please upload a PDF.")
        return None

# ✅ Streamlit UI
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# User inputs
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

# Buttons
submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improve My Skills")
submit3 = st.button("Percentage Match")

# ✅ Your Exact AI Prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager in the field of Data Science, Full Stack Web Development, 
Big Data Engineering, DevOps, and Data Analysis. Your task is to review the provided resume against the job description for these profiles. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
Based on the resume provided, identify key areas for improvement in skills, certifications, and experience 
to enhance alignment with the desired job role.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science, Full Stack Web Development, 
Big Data Engineering, DevOps, and Data Analysis. Your task is to evaluate the resume against the provided job description. 
Give me the percentage of match if the resume aligns with the job description. 
First, the output should show the percentage match, then list the missing keywords, and finally provide your overall thoughts.
"""

# ✅ Handle button clicks and responses
if uploaded_file is not None:
    st.success("PDF uploaded successfully!")
    pdf_content = input_pdf_setup(uploaded_file)  # Convert PDF to images

    if pdf_content:  # Ensures valid PDF processing
        if submit1:
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            st.subheader("Resume Evaluation:")
            st.write(response)

        if submit2:
            response = get_gemini_response(input_prompt2, pdf_content, input_text)
            st.subheader("Skill Improvement Suggestions:")
            st.write(response)

        if submit3:
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            st.subheader("ATS Match Analysis:")
            st.write(response)
else:
    st.warning("Please upload a resume to proceed.")
