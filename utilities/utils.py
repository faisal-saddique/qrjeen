import openai
from langchain.document_loaders import Docx2txtLoader
from typing import List
from langchain.document_loaders import PyMuPDFLoader
import tempfile
import tiktoken
import re
from langchain.docstore.document import Document
from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def process_content_and_get_gpt_response(content, container):

    tokens = num_tokens_from_string(content)
    container.info(f"No. of Tokens in file: {tokens}")
    if tokens > 9500:
        # Consider the first 7500 tokens of content
        container.info("Chunking to put it under the limit.")
        content = content[:7500]
        
    SYSTEM_PROMPT = """You are an Investment Banker tasked with the responsibility of analyzing a set of merged investment
documents. These documents cover various investment strategies, supported by performance metrics.
Your objective is to analyze these documents and subsequently formulate questions that can be directed
at the managing partner to critically examine the topic in depth.

TASK
Scrutinize the attached investment documents and formulate penetrating questions aimed at the
managing partner based on your analysis.

INSTRUCTION
Reading & Comprehending: Scan through the merged investment documents. As you do so, focus on
identifying core themes, key terms, and underlying concepts that stand out.
Document Reference: Clearly state the name of each document within the merged file as you go through
them. This will help in attributing the questions or insights to specific documents.
Structured Output: Present your findings under the following headers:
Core Themes & Concepts Identified: Identify and summarize at least 5 overarching themes and core
concepts from the documents.
Investment Strategy: Outline at least 5 specifics of the investment strategies that each document
elaborates on.
Potential Risks: Enumerate at least 3 very novel risks involved, as presented in the documents or inferred
from the information given.
Expected Benefits: Describe the expected benefits as portrayed or implied in the documents.
Insightful Questions for Managing Partner: Generate a list of insightful questions that should probe
deeper into the strategy's design, the decision-making process that led to it, associated risk factors, and
other relevant topics. This part is more open-ended.
Depth & Objectivity: As you generate these questions, aim for a level of depth and objectivity that
encourages a comprehensive response from the managing partner. The goal is to create questions that
elicit detailed explanations and thus reveal the managing partner's level of expertise and depth of
understanding.

POINTS OF CLARIFICATION
Structure: Make an effort to categorize your questions under the themes or concepts you've identified.
This will make it easier for the managing partner to address them.
Relevance: Ensure that each question you generate is intrinsically tied to the subject matter presented in
the investment documents.
Inquisitive Depth: Aim to formulate questions that press for nuanced answers, thereby allowing a deeper
delve into the managing partner's expertise, decision-making skills, and depth of understanding about
the investment strategies.
Critical Inquiry: Your questions should aim to critically examine the contents of the document,
challenging assumptions and scrutinizing the reliability and sustainability of the described investment
strategies.

ADDITIONAL INSTRUCTIONS
Remember, the overarching goal is for you to autonomously identify salient points and key insights from
the supportive documents. Leverage these insights to formulate questions that not only enable a richer,
more nuanced exploration of the investment strategy at hand but also critically evaluate the veracity,
robustness, and sustainability of these strategies. Aim to formulate questions that compel the managing
partner to validate or reconsider the assumptions, methodologies, and outcomes discussed in the
documents."""

    report = []
    for resp in openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": content
            }
        ],
        temperature=1,
        max_tokens=9500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stream=True
    ):
        # join method to concatenate the elements of the list 
        # into a single string, 
        # then strip out any empty strings
        if "content" in resp.choices[0].delta:
            # container.text += resp.choices[0].delta.content
            # container.markdown(resp.choices[0].delta.content)

            report.append(resp.choices[0].delta.content)
            result = "".join(report)
            # result = result.replace("\n", "")       
            container.markdown(result)

def process_docx_report(content, filename, container):
    # Assuming the content is in bytes format, save it temporarily
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    loader = Docx2txtLoader(file_path=temp_file_path)
    data = loader.load()
    # data = [re.sub(r"\n\s*\n", "\n\n", obj.page_content) for obj in data]
    # for d in data:
    #     d.page_content = re.sub(r"\n\s*\n", "\n\n", d.page_content)
    #     d.metadata["source"] = filename
    return process_content_and_get_gpt_response("\n\n".join([doc.page_content for doc in data]),container=container)

def num_tokens_from_string(content: str) -> int:

    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(content))
    return num_tokens


def process_pdf_report(content, filename, container):
    # Assuming the content is in bytes format, save it temporarily
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    pdf_loader = PyMuPDFLoader(temp_file_path)
    pdf_data = pdf_loader.load()  # Load PDF file

    # for doc in pdf_data:
    #     # Merge hyphenated words
    #     doc.page_content = re.sub(r"(\w+)-\n(\w+)", r"\1\2", doc.page_content)
    #     # Fix newlines in the middle of sentences
    #     doc.page_content = re.sub(
    #         r"(?<!\n\s)\n(?!\s\n)", " ", doc.page_content.strip())
    #     # Remove multiple newlines
    #     doc.page_content = re.sub(r"\n\s*\n", "\n\n", doc.page_content)

    #     doc.metadata["source"] = filename

    return process_content_and_get_gpt_response("\n\n".join([doc.page_content for doc in pdf_data]),container=container)
