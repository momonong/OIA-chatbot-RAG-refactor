import os  # 匯入操作系統模組


def process_file(directory):
    documents = []  # 初始化一個空的文件列表
    for root, _, files in os.walk(directory):  # 遍歷目錄中的所有文件
        for file in files:  # 遍歷每個文件
            if file.endswith(".txt"):  # 如果文件是以 .txt 結尾
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:  # 以讀取模式打開文件
                    content = f.read().strip()  # 讀取文件內容並去除首尾空白
                    paragraphs = content.split("\n\n")  # 以雙換行符分割段落
                    for paragraph in paragraphs:  # 遍歷每個段落
                        if paragraph.strip():  # 如果段落不是空的
                            documents.append({"text": paragraph.strip(), "file": file})  # 將段落和文件名加入文件列表
    return documents  # 返回文件列表


data_dir = "docretrival_data/Chinese"  # 設定資料目錄
documents = process_file(data_dir)  # 處理資料目錄中的文件
print(f"Loaded {len(documents)} paragraphs.")  # 打印總段落數
print("Sample document:", documents[0])  # 打印第一個段落
