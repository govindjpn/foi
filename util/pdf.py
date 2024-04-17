from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter

import pandas as pd 
import pickle
import os
import util.log as log 


def get_pdf_text(pdf_file): 
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages :
        text += page.extract_text()
    #log.log_write(text)
    log.log_write(f"get_pdf_text:: {pdf_file.name} #pages = {len(pdf_reader.pages)}")
    return text, len(pdf_reader.pages)

def get_text_chunks (raw_text) :  
    text_splitter  = CharacterTextSplitter(
            separator = "\n",
            chunk_size = 1000,
            chunk_overlap = 200,
            length_function = len
    )
    chunks = text_splitter.split_text(raw_text)
    log.log_write(f"get_text_chunks:: {len(raw_text)}")
    return chunks 

def pdf2chunks (pdf_file) : 
    ## get PDF text  
    raw_text, page_count = get_pdf_text(pdf_file)
    ## divide text to chunks 
    text_chunks = get_text_chunks(raw_text)
    return page_count, text_chunks

def get_test_pdf_chunks():
    return pdf2chunks("test-1.pdf")

