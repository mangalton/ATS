import streamlit as st
import os 
import google.generativeai as genai
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,content,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([input,content,prompt])
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page= reader.pages[page]
        text+=str(page.extract_text())
    return text

##Prompt Template
input_prompts=f"""
Hey Act like a Skilled or very experience ATS(Application Tracking System) with a deep understanding of tech field.
Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide best assistance for improving the resumes. 
Assign the percentage Matching based on Job Description (JD) and the missing keywords with high accuracy 
resume: {{text}}
description:{{jd}}

I want the response in one single string having the structure
{{"JD Match:"%","MissingKeywords:[],"Profile Summary":""}}
"""

##streamlit app
st.title("ATS Resume Expert")
st.text("Application Tracking System")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume", type ="pdf", help="Please upload the pdf")

submit= st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompts,text,jd)
        st.subheader(response)