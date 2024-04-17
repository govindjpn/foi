
from langchain_community.embeddings import OpenAIEmbeddings 
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain_community.memory import ConversationBufferMemory
from langchain_community.chains import ConversationalRetrievalChain
from langchain_community.llms import OpenAI
import pandas as pd 
import pickle
import os
import util.log as log 
import base64 

 
def get_vectorstore(text_chunks):
    log.log_write(f"get_vectorstore ->")
    embeddings = OpenAIEmbeddings()       
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding = embeddings)
    log.log_write(f"get_vectorstore <- :: vectorstore")
    return vectorstore

def get_conversation_chain(vectorstore) :
    log.log_write(f"get_conversation_chain -> ")
    memory = ConversationBufferMemory(memory_key = "chat_history", return_messages =True) 
    llm = ChatOpenAI()
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
        )
    log.log_write(f"get_conversation_chain :: conversation_chain = {type(conversation_chain)}")
    return conversation_chain


def main() : 
    pass

if __name__ == "__main__" :
    main()
