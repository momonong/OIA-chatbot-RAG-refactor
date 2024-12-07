import os
import json

# 主題映射
TOPIC_MAP = {
    "NHI.txt": "健康保險",
    "Visa.txt": "簽證資訊",
    "health_examination.txt": "健康檢查",
    "registration_process.txt": "註冊流程",
    "schoolarship_certificate.txt": "獎學金證明",
    "problem_of_stay.txt": "居留問題",
    "tution.txt": "學費相關",
    "registration_for_otherstudent.txt": "其他註冊資訊",
    "Scholarship.txt": "Scholarship Information",
    "NHI.txt": "Health Insurance",
    "Visa.txt": "Visa Information",
    "health_examination.txt": "Health Examination",
    "registration_process.txt": "Registration Process",
    "registration_for_foreignstudent.txt": "Other Registration Information",
    "enrollment_deferral.txt": "Enrollment Deferral",
}

DATA_LIST = ["docretrival_data/Chinese", "docretrival_data/English"]
OUTPUT_FILE = ["chinese_data.json", "english_data.json"]


def process_file(directory, topic_map):
    """
    處理指定目錄中的所有 .txt 檔案，將內容結構化。
    """
    documents = []
    for root, _, files in os.walk(directory):  # 遍歷目錄中的所有文件
        for file in files:  # 遍歷每個文件
            if file.endswith(".txt"):  # 只處理 .txt 文件
                topic = topic_map.get(file, "其他")  # 根據文件名設置主題
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read().strip()  # 讀取文件內容並去除首尾空白
                    paragraphs = content.split("\n\n")  # 按雙換行分割段落
                    for paragraph in paragraphs:  # 遍歷每個段落
                        if paragraph.strip():  # 過濾空段落
                            documents.append(
                                {
                                    "file_name": file,
                                    "topic": topic,
                                    "text": paragraph.strip(),
                                }
                            )
    return documents


def split_long_paragraphs(documents, max_length=200):
    """
    將過長段落拆分為較小段落，確保每段長度不超過 max_length。
    """
    split_documents = []
    for doc in documents:
        if len(doc["text"]) > max_length:
            sentences = doc["text"].split("。")
            for sentence in sentences:
                if sentence.strip():
                    split_documents.append(
                        {
                            "file_name": doc["file_name"],
                            "topic": doc["topic"],
                            "text": sentence.strip() + "。",
                        }
                    )
        else:
            split_documents.append(doc)
    return split_documents


def save_to_file(data, output_file):
    """
    將處理後的資料儲存為 JSON 格式。
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"數據已儲存至 {output_file}")


def main():
    """
    主流程：執行資料前處理並儲存結果。
    """
    for i, directory in enumerate(DATA_LIST):
        print(f"正在處理資料夾：{directory}")
        documents = process_file(directory, TOPIC_MAP)  # 處理資料目錄中的文件
        print(f"已從 {directory} 載入 {len(documents)} 段落。")

        documents = split_long_paragraphs(documents)  # 處理冗長段落
        print(f"段落已拆分為 {len(documents)} 段較短的段落。")

        save_to_file(documents, OUTPUT_FILE[i])  # 儲存結果


if __name__ == "__main__":
    main()
