# Resume Analyzer using NLP and Streamlit

This project is a web-based Resume Analyzer built using Natural Language Processing (NLP) techniques and the Streamlit framework. It helps identify how well a resume matches a given job description by comparing keyword overlap.

## Features

- Upload and parse resumes in PDF format
- Paste job descriptions directly into the interface
- Keyword extraction using spaCy (original + lemmatized forms)
- Calculates match score percentage
- Displays found and missing keywords
- Saves results to an Excel file (`results.xlsx`) for record-keeping

## Technologies Used
- Python 3
- Streamlit (GUI)
- spaCy (NLP processing)
- pdfplumber (PDF parsing)
- pandas (data handling and Excel export)
- openpyxl (Excel writing backend)

## Installation

### 1. Clone this repository:

- git clone https://github.com/vishal2k06/ResumeAnalyzer.git
- cd ResumeAnalyzer

### 2. Install dependencies:

- pip install -r requirements.txt
- python -m spacy download en_core_web_sm

### 3. Running the App

Start the StreamLit Server using:
  - streamlit run app.py

## Project Structure

ResumeAnalyzer:
  - app.py          
  - requirements.txt     
  - results.xlsx         
  - README.md

## How It Works

- Job description and resume text are both processed using spaCy.
- Keywords (nouns, verbs, proper nouns) are extracted in both original and lemmatized form.
- Resume is matched against job keywords, and a similarity score is calculated.
- Matching results and statistics are stored in results.xlsx.

## Use Cases

- Helps recruiters quickly assess resume relevance
- Assists students and job seekers in improving resume targeting
- Can be adapted into larger hiring platforms or screening tools

## License
  - This project is licensed under the MIT License. See the LICENSE file for details.
