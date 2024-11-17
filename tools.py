from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import torch
from llama_cpp import Llama
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    all_text = " ".join([page.page_content for page in pages])
    start_index = all_text.find("ABSTRACT")
    end_index = all_text.find("REFERENCES")
    if start_index != -1 and end_index != -1 and start_index < end_index:
        relevant_text = all_text[start_index:end_index]
    else:
        relevant_text = all_text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
    text_list = text_splitter.split_text(relevant_text)
    research_paper_text = "".join(text_list)
    length_of_research_paper = len(research_paper_text)
    return research_paper_text, length_of_research_paper

def load_llm_model():
    if torch.cuda.is_available():
        print("CUDA is available. Using GPU for LLM model.")
    else:
        print("CUDA is not available. Using CPU for LLM model.")
    try:
        llm = Llama(
            model_path="Llama-3.2-1B-Instruct-Q8_0.gguf",
            n_gpu_layers=-1,
            n_ctx=70000,
            n_batch=1024*16,
            verbose=False,
            seed=-1,
        )
        print("LLM model loaded successfully")
        return llm
    except Exception as e:
        print(f"Error loading LLM model: {e}")
        raise

def retrieve_doi_id(doi_link):
    if doi_link.startswith("10."):
        doi_id = doi_link
    elif doi_link:
        doi_id = "10." + doi_link.split("10.")[1]
    else:
        doi_id = doi_link
    return doi_id