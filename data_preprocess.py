import os
from pydoc import doc
from xml.dom.minidom import Document

def process_file(directory):
    documents = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    paragraphs = content.split('\n\n')
                    for paragraph in paragraphs:
                        if paragraph.strip():
                            documents.append({'text': paragraph.strip(), 'file': file})
    return documents

data_dir = 'docretrival_data/Chinese'
documents = process_file(data_dir)
print(f"Loaded {len(documents)} paragraphs.")  # 打印總段落數
print("Sample document:", documents[0])  # 打印第一個段落
