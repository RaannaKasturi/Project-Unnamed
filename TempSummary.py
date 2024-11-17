from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
from tools import extract_text_from_pdf

LANGUAGE = "english"
SENTENCES_COUNT = 15

def generate_textrank_summary(research_paper_text):
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    parser = PlaintextParser.from_string(research_paper_text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = TextRankSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    sentences = summarizer(parser.document, SENTENCES_COUNT)
    summary = ""
    for sentence in sentences:
        summary += str(sentence) + ""
    return summary

def generate_luhn_summary(research_paper_text):
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    parser = PlaintextParser.from_string(research_paper_text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = LuhnSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    sentences = summarizer(parser.document, SENTENCES_COUNT)
    summary = ""
    for sentence in sentences:
        summary += str(sentence) + ""
    return summary

def generate_lsa_summary(research_paper_text):
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    parser = PlaintextParser.from_string(research_paper_text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    sentences = summarizer(parser.document, SENTENCES_COUNT)
    summary = ""
    for sentence in sentences:
        summary += str(sentence) + ""
    return summary

def generate_temp_summary(pdf_path):
    research_paper_text, length_of_research_paper = extract_text_from_pdf(pdf_path)
    textrank_summary = generate_textrank_summary(research_paper_text)
    luhn_summary = generate_luhn_summary(research_paper_text)
    lsa_summary = generate_lsa_summary(research_paper_text)
    temp_summary = textrank_summary.replace("\n", "") + luhn_summary.replace("\n", "") + lsa_summary.replace("\n", "")
    return temp_summary, length_of_research_paper
