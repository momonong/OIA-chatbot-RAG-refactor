import os
from langchain.chat_models import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_openai import AzureOpenAI
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

def answer_question(question,key):
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_KEY"] = "9cbc0ba8236e4b10ba5d8a2a351d0170"
    os.environ["OPENAI_API_VERSION"] = "2023-05-15"
    os.environ["AZURE_ENDPOINT"] = "https://gdsc-chatbot-useast.openai.azure.com/"
    
    embeddings = AzureOpenAIEmbeddings(
    azure_deployment="GDSC-Chatbot-USeast-text-embedding-ada-002",
    openai_api_version="2023-05-15",
    azure_endpoint = os.getenv('AZURE_ENDPOINT'))
    
    llm = AzureOpenAI(
                deployment_name="GDSC-USeast-gpt-35-turbo-instruct",
                temperature=0,
                max_tokens=4097,
                azure_endpoint=os.getenv('AZURE_ENDPOINT'))
    
    
    match key:
        case 1:
            vectorstore = FAISS.load_local("faiss_index_oversea_chinese", embeddings)
            prompt_template = """
            You are a chatbot specialized in assisting and providing thorough answers to oversea Chinese students. Use "{context}" to comprehensively and officially answer the the question.
            And if you are asked about something irrelevant to "{context}" , you should answer that it is not within your scope.
            The most important thing is to answer correctly,this is very important to me.Fabricating answers is absolutely not allowed.

            {context}
            Question: {question}
            You can only answer general greetings,registration,tuition,registration processes,health examination,ARC,visa,scholarship certificate,health insurance(NHI),scholarship,stay,medical check up,school related questions within two hunred words.
            Questions from other similar fields can also be answered.
            Please default the identity of the other side to be a oversea Chinese student of National Cheng Kung University.
            Reply question in English concisely and correctly .
            """
            
        case -1:
            vectorstore = FAISS.load_local("faiss_index_oversea_chinese", embeddings)
            prompt_template = """
            You are a chatbot specialized in assisting and providing thorough answers to oversea Chinese students. Use "{context}" to comprehensively and officially answer the the question.
            And if you are asked about something irrelevant to "{context}" , you should answer that it is not within your scope.
            The most important thing is to answer correctly,this is very important to me.Fabricating answers is absolutely not allowed.

            {context}
            Question: {question}
            You can only answer general greetings,registration,tuition,registration processes,health examination,ARC,visa,scholarship certificate,health insurance(NHI),scholarship,stay,medical check up,school related questions within two hunred words.
            Questions from other similar fields can also be answered.
            Please default the identity of the other side to be a oversea Chinese student of National Cheng Kung University.
            Reply question in Chinese concisely and correctly .
            """
            
        case 2:
            vectorstore = FAISS.load_local("faiss_index_international", embeddings)
            prompt_template = """
            You are a chatbot specialized in assisting and providing thorough answers to international students. Use "{context}" to comprehensively and officially answer the the question.
            And if you are asked about something irrelevant to "{context}" , you should answer that it is not within your scope.
            The most important thing is to answer correctly,this is very important to me.Fabricating answers is absolutely not allowed.

            {context}
            Question: {question}
            You can only answer general greetings,registration,tuition,registration processes,health examination,ARC,visa,scholarship certificate,health insurance(NHI),scholarship,stay,medical check up,school related questions within two hunred words.
            Questions from other similar fields can also be answered.
            Please default the identity of the other side to be a international student of National Cheng Kung University.
            Reply question in English concisely and correctly .
            """
            
        case -2:
            vectorstore = FAISS.load_local("faiss_index_international", embeddings)
            prompt_template = """
            You are a chatbot specialized in assisting and providing thorough answers to international students. Use "{context}" to comprehensively and officially answer the the question.
            And if you are asked about something irrelevant to "{context}" , you should answer that it is not within your scope.
            The most important thing is to answer correctly,this is very important to me.Fabricating answers is absolutely not allowed.

            {context}
            Question: {question}
            You can only answer general greetings,registration,tuition,registration processes,health examination,ARC,visa,scholarship certificate,health insurance(NHI),scholarship,stay,medical check up,school related questions within two hunred words.
            Questions from other similar fields can also be answered.
            Please default the identity of the other side to be a international student of National Cheng Kung University.
            Reply question in Chinese concisely and correctly .
            """
            
        case 3:
            vectorstore = FAISS.load_local("faiss_index_chinese", embeddings)
            prompt_template = """
            You are a chatbot specialized in assisting and providing thorough answers to China students. Use "{context}" to comprehensively and officially answer the the question.
            And if you are asked about something irrelevant to "{context}" , you should answer that it is not within your scope.
            The most important thing is to answer correctly,this is very important to me.Fabricating answers is absolutely not allowed.

            {context}
            Question: {question}
            You can only answer general greetings,registration,tuition,registration processes,health examination,ARC,visa,scholarship certificate,health insurance(NHI),scholarship,stay,medical check up,school related questions within two hunred words.
            Questions from other similar fields can also be answered.
            Please default the identity of the other side to be a China student of National Cheng Kung University.
            Reply question in English concisely and correctly .
            """
            
        case -3:
            vectorstore = FAISS.load_local("faiss_index_chinese", embeddings)
            prompt_template = """
            You are a chatbot specialized in assisting and providing thorough answers to China students. Use "{context}" to comprehensively and officially answer the the question.
            And if you are asked about something irrelevant to "{context}" , you should answer that it is not within your scope.
            The most important thing is to answer correctly,this is very important to me.Fabricating answers is absolutely not allowed.

            {context}
            Question: {question}
            You can only answer general greetings,registration,tuition,registration processes,health examination,ARC,visa,scholarship certificate,health insurance(NHI),scholarship,stay,medical check up,school related questions within two hunred words.
            Questions from other similar fields can also be answered.
            Please default the identity of the other side to be a China student of National Cheng Kung University.
            Reply question in Chinese concisely and correctly .
            """
            
    PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
    )
    qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": PROMPT})
    
    res = qa_chain.run(question)
    
    return res