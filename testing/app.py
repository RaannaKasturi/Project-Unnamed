import os
import sys
from generate_markdown import load_llm_model, generate_markdown, sanitize_markdown
from generate_mindmap import generate_mindmap
import gradio as gr
import subprocess

def generate(file):
    print(f"Generating mindmap for {file.name}")
    unformatted_markdown = True
    summary = "This is a summary of the research paper"
    mindmap_markdown = generate_markdown(llm, file)
    print('mindmap_markdown:', mindmap_markdown)
    
    while unformatted_markdown:
        if mindmap_markdown.startswith("#") and '-' in mindmap_markdown:
            unformatted_markdown = False
            mindmap_svg, mindmap_pdf = generate_mindmap(mindmap_markdown)
        else:
            unformatted_markdown = True
            mindmap_markdown = sanitize_markdown(llm, mindmap_markdown)
    
    print("Mindmap generated successfully")
    return summary, mindmap_markdown, mindmap_svg, mindmap_svg, mindmap_pdf, mindmap_pdf

theme = gr.themes.Soft(
    primary_hue="purple",
    secondary_hue="cyan",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont('Syne'), gr.themes.GoogleFont('Poppins')],
)

with gr.Blocks(theme=theme, title="Binary Biology") as app:
    with gr.Row():
        file = gr.File(file_count='single', label='Upload Research Paper PDF file', file_types=['.pdf'])
        with gr.Column():
            submit = gr.Button(value='Submit')
            clear = gr.ClearButton(value='Clear')
    
    with gr.Row():
        summary = gr.TextArea(label='Summary', lines=5, interactive=False, show_copy_button=True)
        markdown_mindmap = gr.Textbox(label='Mindmap', lines=5, interactive=False, show_copy_button=True)
    
    with gr.Row():
        with gr.Column():
            svg_mindmap = gr.File(label='Graphical SVG Mindmap', interactive=False)
            download_svg_mindmap = gr.File(label='Download SVG Mindmap', interactive=False)
        
        with gr.Column():
            pdf_mindmap = gr.File(label='Graphical PDF Mindmap', interactive=False)
            download_pdf_mindmap = gr.File(label='Download PDF Mindmap', interactive=False)

    submit.click(
        generate,
        inputs=[file],
        outputs=[summary, markdown_mindmap, svg_mindmap, download_svg_mindmap, pdf_mindmap, download_pdf_mindmap],
        scroll_to_output=True,
        show_progress='minimal',
        queue=True,
    )
    
    clear.click(
        lambda: (None, None, None, None, None, None),
        inputs=[file],
        outputs=[summary, markdown_mindmap, svg_mindmap, download_svg_mindmap, pdf_mindmap, download_pdf_mindmap]
    )

if __name__ == "__main__":
    try:
        env = os.environ.copy()
        env["CMAKE_ARGS"] = "-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS"
        subprocess.run(["pip", "install", "llama-cpp-python"], env=env)
    except Exception as e:
        print(f"Failed to install llama-cpp-python: {e}")
    
    try:
        subprocess.run(['apt', 'install', '-y', 'graphviz'])
        print("Graphviz installed successfully")
    except Exception:
        try:
            subprocess.run(['sudo', 'apt', 'install', '-y', 'graphviz'])
            print("Graphviz installed successfully using sudo")
        except:
            print("Graphviz installation failed")
            sys.exit(1)
    
    print("Graphviz loaded successfully")
    llm = load_llm_model()
    print("Model loaded successfully")
    app.queue(default_concurrency_limit=1).launch(show_error=True)
