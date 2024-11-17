from TempSummary import generate_temp_summary

def generate_summary(llm, file):
    print("Generating Temporary Summary...")
    temp_summary, length_of_research_paper = generate_temp_summary(file)
    with open("temp_summary.txt", "w") as f:
        f.write(temp_summary)
    print("Temporary Summary Generated Successfully...")
    prompt = f'''Summarize the text from research paper to explain it to a school child, with suitable headings and in bullet points. The headings/titles of the bullet points section must start with # andshould follow the template:
     \\n\\n# title of summary
    \\nsmall summary in about 100-200 words

    \\n\\n## heading/title
    \\n- bullet point
    \\n    - sub-bullet point
    \\n
    Research Paper Text: \\"{temp_summary}\\"Do not include anything in the response, that is not the part of research paper.\\n  Importantly your output must use language \\"English\\"\\n\\n Example format:
    \\n\\n# title of summary
    \\nsmall summary in about 100-200 words

    \\n\\n## heading/title
    \\n- bullet point
    \\n    - sub-bullet point
    '''
    # prompt = f'''Summarize the text from research paper to explain it to a school child, with suitable headings and in bullet points. \\"{temp_summary}\\"Do not include anything in the response, that is not the part of research paper.\\n  Importantly your output must use language \\"English\\""'''
    print("Generating Final Summary...")
    response = llm.create_chat_completion(
        messages = [
            {"role": "system",
            'content': 'You are a helpful research assistant for generating well-formatted mindmaps in MarkDown format from scientific research papers.'},
            {'role':'user',
            'content': prompt}
        ],
        temperature=0.8,
        top_k=200,
        top_p=3.0,
    )
    print("Final Summary Generated Successfully...")
    try:
        summary = response['choices'][0]['message']['content']
    except:
        summary = response
    print(summary)
    return summary, length_of_research_paper

def summarize(llm, file):
    import time
    start_time = time.time()
    response, length_of_research_paper = generate_summary(llm, file)
    if "#" not in response:
        response, length_of_research_paper = generate_summary(llm, file)
    elif "##" not in response:
        response, length_of_research_paper = generate_summary(llm, file)
    elif "====" in response:
        response, length_of_research_paper = generate_summary(llm, file)
    elif "----" in response:
        response, length_of_research_paper = generate_summary(llm, file)
    else:
        response = response.strip()
    if "**" in response:
        response = response.strip()
        response = response.replace("- **", "### ")
        response = response.replace("**", "")
        response = response.replace("\n\n", "\n")
        response = response.replace("\\n\\n", "\\n")
    summary = ""
    for line in response.splitlines():
        if line.startswith("*"):
            line = line.replace("*", "-", 1)
        if line.startswith("###"):
            summary += "\n\n" + line
        else:
            summary += "\n" + line
    
    end_time = time.time()
    total_time_taken = end_time - start_time
    total_time_taken_minutes = round(total_time_taken / 60, 3)
    info = f"The research paper of {length_of_research_paper} characters long was summarized in {total_time_taken_minutes} minutes."
    return summary.strip(), info
