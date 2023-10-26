from dotenv import load_dotenv
import streamlit as st

from langchain.callbacks.base import BaseCallbackHandler
from utilities.utils import (
    process_docx_report,
    process_pdf_report,
    num_tokens_from_string,
)

st.set_page_config(
    page_title='Investment Analyzer',
    page_icon='💰',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.title("Investment Analyzer 💰")


# Load environment variables from .env file
load_dotenv()

accepted_file_types = ["pdf", "docx"]

uploaded_files = st.file_uploader("Upload one or more files", accept_multiple_files=True, type=accepted_file_types)


if st.button("Run Analysis", use_container_width=True):
    if uploaded_files:
        tot_len = 0
        result = None
        for file in uploaded_files:
            file_extension = file.name.split(".")[-1].upper()
            st.markdown("----")
            st.markdown(f'File: **{file.name}**')
            res_box = st.empty()
            file_content = file.read()  # Read the content of the uploaded file
            if file_extension == 'PDF':
                result = process_pdf_report(file_content,file.name,res_box)

            elif file_extension == 'DOCX':
                result = process_docx_report(file_content,file.name)
            else:
                result = None
                raise ValueError("File type not supported!")
            st.markdown(result)