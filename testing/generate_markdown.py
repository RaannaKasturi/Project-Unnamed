from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from llama_cpp import Llama

def load_llm_model():
    try:
        llm = Llama(
            model_path="Llama-3.2-1B-Instruct-Q8_0.gguf",
            n_gpu_layers = -1,
            n_ctx=100000,
            n_batch=4096,
        )
        print("LLM model loaded successfully")
        return llm
    except Exception as e:
        print(f"Error loading LLM model: {e}")
        raise

def get_text_from_pdf(file):
    loader = PyPDFLoader(file)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
    texts = text_splitter.split_documents(pages)
    final_text = ""
    for text in texts:
        if text.page_content.startswith("REFERENCES"):
            break
        else:
            final_text = final_text + text.page_content
    research_paper = ""
    for text in final_text:
        if text.startswith(("REFERENCES", "REFERENCESREFERENCES", "REFERENCESREFERENCESREFERENCES")):
            break
        else:
            research_paper = research_paper + text
    return research_paper[:10000]

def generate_prompt(research_paper):
    prompt = f'''
    As a text script expert, please help me to write a short text script with the topic \\"{research_paper}\\".Your output should only and strictly use the following template:\\n# {{Title}}\\n## {{Subtitle01}}\\n- {{Emoji01}} Bulletpoint01\\n- {{Emoji02}} Bulletpoint02\\n## {{Subtitle02}}\\n- {{Emoji03}} Bulletpoint03\\n- {{Emoji04}} Bulletpoint04\\n\\nSummarize the giving topic to generate a mind map (as many subtitles as possible, with a minimum of three subtitles) structure markdown.\\n Do not include anything in the response, that is not the part of mindmap.\\n  Importantly your output must use language \\"English\\""
    '''
    return prompt

def generate_mindmap_structure(llm, prompt):
    response = llm.create_chat_completion(
        messages = [
            {'role':'system',
            'content': 'You are a helpful research assistant for generating well-formatted mindmaps in MarkDown format from scientific research papers.'},
            {'role':'user',
            'content': prompt}
        ],
        temperature=0.7,
        top_k=200,
        top_p=3.0,
    )
    mindmap_data = response['choices'][0]['message']['content']
    return mindmap_data

def generate_markdown(llm, file):
    final_text = get_text_from_pdf(file)
    prompt = generate_prompt(final_text)
    mindmap_markdown = generate_mindmap_structure(llm, prompt)
    if "**" in mindmap_markdown:
        mindmap_markdown = mindmap_markdown.replace("- **", "### ")
        mindmap_markdown = mindmap_markdown.replace("**", "")
    else:
        pass
    return mindmap_markdown

def sanitize_markdown(llm, mindmap_markdown):
    prompt = f'''
    As an experienced coder and programmer, help me convert the text \\"{mindmap_markdown}\\" into a well-formatted markdown. Your output should only and strictly use the following template:\\n# {{Title}}\\n## {{Subtitle01}}\\n- {{Emoji01}} Bulletpoint01\\n- {{Emoji02}} Bulletpoint02\\n## {{Subtitle02}}\\n- {{Emoji03}} Bulletpoint03\\n- {{Emoji04}} Bulletpoint04\\n\\nDo not include anything in the response, that is not the part of mindmap."
    '''
    sanitized_markdown = generate_mindmap_structure(llm, prompt)
    return sanitized_markdown