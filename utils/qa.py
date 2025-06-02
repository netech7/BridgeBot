from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def get_answer(query, index_path="faiss_index"):
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    db = FAISS.load_local(index_path, embeddings)
    
    docs = db.similarity_search(query)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")  # Can also try gpt-4
    chain = load_qa_chain(llm, chain_type="stuff")
    
    result = chain.run(input_documents=docs, question=query)
    return result
