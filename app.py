import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf


# gemini function

def get_gemini_response(input, api_key):
    if not api_key:
        raise ValueError("API key is required")
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        raise ValueError(f"Invalid API key, details: {e}")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input, generation_config=genai.GenerationConfig(
        response_mime_type="application/json"),
    )
    return response.text

# convert pdf to text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


input_prompt = """

### As a skilled Application Tracking System (ATS) with advanced knowledge in technology and data science, your role is to meticulously evaluate a candidate's resume based on the provided job description. 

### Your evaluation will involve analyzing the resume for relevant skills, experiences, and qualifications that align with the job requirements. Look for key buzzwords and specific criteria outlined in the job description to determine the candidate's suitability for the position.

### Provide a detailed assessment of how well the resume matches the job requirements, highlighting strengths, weaknesses, and any potential areas of concern. Offer constructive feedback on how the candidate can enhance their resume to better align with the job description and improve their chances of securing the position.

### Your evaluation should be thorough, precise, and objective, ensuring that the most qualified candidates are accurately identified based on their resume content in relation to the job criteria.

### Remember to utilize your expertise in technology and data science to conduct a comprehensive evaluation that optimizes the recruitment process for the hiring company. Your insights will play a crucial role in determining the candidate's compatibility with the job role.
resume={text}
jd={jd}
### Evaluation Output:
result = {{
    "overall_score": int =1-100,  # Điểm tổng thể (%)
    "company_name": "ZSOLUTIONAI",
    "position_score": int =1-100,
    "experience_score": int =1-100,
    "skills_score": int 1-100,
    "orientation_score": int =1-100,
    "other_factors_score": int =1-100,
    "matched_skills": List[str],
    "missing_skills": List[str],
}}
"""

# stramlit

# require the api_key as input by user

st.title("DDS Smart ATS")
api_key = st.text_input("Enter your API key")

st.text("Imporve your ATS resume score Match")
jd = st.text_area("Paste job description here")
uploaded_file = st.file_uploader(
    "Upload your resume", type="pdf", help="Please upload the pdf")

submit = st.button('Check Your Score')
if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(
            input_prompt.format(text=text, jd=jd), api_key)
        # display response in json format with st.json
        st.json(response)
