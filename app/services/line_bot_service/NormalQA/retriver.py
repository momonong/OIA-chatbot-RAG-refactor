import os
from langchain.chat_models import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_openai import AzureOpenAI
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


class Retriever:
    def __init__(self):
        load_dotenv()
        self.embeddings = AzureOpenAIEmbeddings(
            azure_deployment="text-embedding-3-large",
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            openai_api_version="2023-05-15",
            azure_endpoint = os.getenv('AZURE_ENDPOINT_EMBEDDINGS'))
        self.llm = AzureChatOpenAI(
            azure_deployment="gpt-4o",
            api_version="2024-02-15-preview",
            top_p=1,
            presence_penalty=2,
            temperature=0,
            max_tokens=3500,
            api_key=os.getenv('OPENAI_API_KEY'),
            azure_endpoint=os.getenv('AZURE_ENDPOINT_LLM'))
        self.chains = {}
        for key in [1, -1, 2, -2, 3, -3]:
            self.chains[key] = self._create_chain(key)
        self.match_lists = {
            "oversea_chinese_students_en": 1,
            "oversea_chinese_students_zh": -1,
            "international_students_en": 2,
            "international_students_zh": -2,
            "chinese_students_en": 3,
            "chinese_students_zh": -3
        }

    def _create_chain(self, key):
        index_name = {
            1: "faiss_index_oversea_chinese",
            -1: "faiss_index_oversea_chinese",
            2: "faiss_index_international",
            -2: "faiss_index_international",
            3: "faiss_index_chinese",
            -3: "faiss_index_chinese"
        }[key]

        student_type = {
            1: "oversea Chinese", -1: "oversea Chinese",
            2: "international", -2: "international",
            3: "China", -3: "China"
        }[key]

        language = "English" if key > 0 else "Chinese"

        vectorstore = FAISS.load_local(os.path.join(os.path.dirname(
            __file__), index_name), self.embeddings, allow_dangerous_deserialization=True)

        prompt_template = f"""
        You are a chatbot specialized in assisting and providing thorough answers to {student_type} students. Use "{{context}}" to comprehensively and officially answer the question.
        And if you are asked about something irrelevant to "{{context}}", you should answer that it is not within your scope.
        The most important thing is to answer correctly, this is very important to me. Fabricating answers is absolutely not allowed.

        {{context}}
        Question: {{question}}
        You can only answer general greetings, registration, tuition, registration processes, health examination, ARC, visa, scholarship certificate, health insurance(NHI), scholarship, stay, medical check up, school related questions within two hundred words.
        Questions from other similar fields can also be answered.
        Please default the identity of the other side to be a {student_type} student of National Cheng Kung University.
        Reply question in {language} concisely and correctly.
        """


        prompt_template1 = f"""
        Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that it is recommended to ask the International Office staff, don't try to make up an answer.And if you are asked about something irrelevant to "{{context}}" , you should answer that it is not within your scope.
                
                {{context}}

                Question: {{question}}
                Answer in {language}:
        """

        prompt = PromptTemplate(template=prompt_template1, input_variables=["context", "question"])
        return RetrievalQA.from_chain_type(
            self.llm,
            retriever=vectorstore.as_retriever(),
            chain_type_kwargs={"prompt": prompt}
        )

    def get_reply(self, student_type, question):
        return self.chains[self.match_lists[student_type]].run(question)

if __name__ == "__main__":
    retriever = Retriever()
    print(retriever.get_reply("oversea_chinese_students_en", "How to apply for a scholarship?"))
