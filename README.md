# Streamlit Investment Analyzer App README

## Overview

The Streamlit Investment Analyzer App is a tool designed to assist investment bankers in the analysis of investment documents. It empowers you to effortlessly upload and analyze PDF and DOCX files containing investment strategies, performance metrics, and other financial information. The app utilizes the power of OpenAI's GPT-3.5 Turbo model to generate insightful questions for managing partners, facilitating a more profound examination of investment strategies.

## Features

- **Document Analysis**: Upload one or more PDF and DOCX files that contain investment-related information.

- **Intelligent Question Generation**: Automatically generate insightful questions based on the content of the uploaded documents. These questions can help you delve deeper into the investment strategy, risk factors, benefits, and more.

- **Categorization of Questions**: Questions are categorized under themes or concepts identified in the documents, making it easier to address specific aspects of the analysis.

- **Objective and Critical Inquiry**: The questions aim to encourage critical examination of the documents, challenging assumptions and scrutinizing the reliability and sustainability of the described investment strategies.

- **Wide Layout**: The app is designed with a wide layout to provide ample space for document analysis and question generation.

## How to Use

1. **Upload Investment Documents**: Start by uploading one or more investment documents in PDF or DOCX format. Simply use the file uploader, and the app will process the content.

2. **Generate Questions**: Click the "Run Analysis" button. The app will analyze the documents and generate insightful questions based on the content.

3. **Review and Use Questions**: The generated questions will be displayed, categorized under relevant themes or concepts. You can use these questions to engage in deeper discussions with managing partners and further assess the investment strategies.

## Environment Setup

Before running the Streamlit app, make sure to set up your environment:

1. Create a `.env` file and set your OpenAI API key as `OPENAI_API_KEY` for GPT-3.5 Turbo.

2. Install the required Python packages using `pip install -r requirements.txt`.

## Customization

You can customize the app by modifying the Streamlit code in `app.py`. Adjust the system prompt and other settings in the `process_content_and_get_gpt_response` function within the `utils.py` file to fine-tune the question generation process.