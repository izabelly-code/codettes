import pandas as pd
import vertexai
from vertexai.generative_models import GenerativeModel

project_id = "gemini-project-analyzer"

vertexai.init(project=project_id, location="us-central1")

model = GenerativeModel("gemini-1.5-flash-001")

def read_txt_to_string(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def summarize_csv(file_path):
    df = pd.read_csv(file_path)

    file_path = "news.txt"

    text_content = read_txt_to_string(file_path)

    csv_content = ""
    for index, row in df.iterrows():
        csv_content += " ".join(map(str, row.values)) + "\n"

    response = model.generate_content(
        f"Por favor escreva uma newsletter chamada codettes com base no seguinte conteudo (utilize apenas o que tem no conteudo e separe em seçoes proximos eventos de tecnologia, palestras e cursos com): \n{csv_content}, devolver apenas a newsletter sem comentarios adicionais."
    )

    return response.text

file_path = "search_results.csv"

summary = summarize_csv(file_path)

md_file_path = "newsletter-pronta.md"
with open(md_file_path, 'w', encoding='utf-8') as file:
    file.write(summary)