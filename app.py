from functools import partial
import subprocess
from tools import load_llm_model
import gradio as gr
from generateSummary import summarize
import torch

theme = gr.themes.Soft(
    primary_hue="purple",
    secondary_hue="cyan",
    neutral_hue="slate",
    font=[
        gr.themes.GoogleFont('Syne'), 
        gr.themes.GoogleFont('Poppins'), 
        gr.themes.GoogleFont('Poppins'), 
        gr.themes.GoogleFont('Poppins')
    ],
)

def clear_everything(pdf_file, summary_output, info):
    pdf_file = None
    summary_output = None
    info = None
    return pdf_file, summary_output, info

# if torch.cuda.is_available():
#     print("GPU is available. Installing GPU version of llama-cpp-python...")
#     try:
#         subprocess.run("cmake --version", shell=True)
#     except:
#         try:
#             subprocess.run("sudo apt install cmake", shell=True)
#             subprocess.run("sudo apt install gcc-11 g++-11", shell=True)
#             subprocess.run("sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 60 --slave /usr/bin/g++ g++ /usr/bin/g++-11", shell=True)
#         except:
#             subprocess.run("apt install cmake", shell=True)
#             subprocess.run("apt install gcc-11 g++-11", shell=True)
#             subprocess.run("update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 60 --slave /usr/bin/g++ g++ /usr/bin/g++-11", shell=True)
#     subprocess.run("gcc --version", shell=True)
#     subprocess.run("g++ --version", shell=True)
#     subprocess.run('CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 pip install llama-cpp-python --force-reinstall --no-cache-dir', shell=True)

print("Loading LLM model...")
llm = load_llm_model()
print("Loaded LLM model Successfully...")

summarize_with_llm = partial(summarize, llm)

with gr.Blocks(theme=theme, title="Hybrid PDF Summarizer", fill_height=True) as app:
    gr.HTML(
        value ='''
        <h1 style="text-align: center;">Hybrid PDF Summarizer</h1><br><p style="text-align: center;">This app uses a hybrid approach to summarize PDF documents completely based on CPU.</p><br><p style="text-align: center;">The app uses traditional methodologies such as TextRank, LSA, Luhn algorithms as well as quantized large language model (LLM) to generate summaries of the PDF document.</p><br><p style="text-align: center;">The summarization process can take some time depending on the size of the PDF document and the complexity of the content.</p>
        ''')
    with gr.Column():
        with gr.Row():
            pdf_file = gr.File(label="Upload PDF", file_types=['.pdf'])
            with gr.Column():
                with gr.Row():
                    summarize_btn = gr.Button(value="Summarize")
                    clear_btn = gr.Button(value="Clear")
                info = gr.Textbox(label="Summarization Info", placeholder="Details regarding summarization will be shown here", interactive=False)
        summary_output = gr.TextArea(label="PDF Summary", placeholder="The summary will be displayed here", interactive=False, show_copy_button=True)

    summarize_btn.click(
        summarize_with_llm,
        inputs=pdf_file,
        outputs=[summary_output, info],
        concurrency_limit=5,
        scroll_to_output=True,
        api_name="summarize",
        show_progress="full",
        max_batch_size=10,
    )
    clear_btn.click(clear_everything, inputs=[pdf_file, summary_output, info], outputs=[pdf_file, summary_output, info], show_api=False)

app.queue(default_concurrency_limit=5).launch(show_api=True)
