import streamlit as st 
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings 
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import OpenAI
from langchain_community.llms import HuggingFaceHub
from langchain_community.chat_models.huggingface import ChatHuggingFace
import pandas as pd 
import pickle
import os
import util.log as log 
import base64 

from huggingface_hub import InferenceClient



from htmlTemplates import css, bot_template, user_template, pdf_display


def get_pdf_text(pdf_file): 
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages :
        text += page.extract_text()
    #log.log_write(text)
    st.session_state.pdf_file_name = pdf_file.name
    st.session_state.pdf_page_count = len(pdf_reader.pages) 
    log.log_write(f"get_pdf_text:: {pdf_file.name} #pages = {len(pdf_reader.pages)}")
    return text, len(pdf_reader.pages)

def get_text_chunks (raw_text) :  
    text_splitter  = CharacterTextSplitter(
            separator = "\n",
            chunk_size = 1000,
            chunk_overlap = 200,
            length_function = len
    )
    chunks = text_splitter.split_text(raw_text)
    log.log_write(f"get_text_chunks:: {len(raw_text)}")
    return chunks 

def get_vectorstore(model, text_chunks):
    log.log_write(f"get_vectorstore ->:: model = {model}")
    match model : 
        case "OpenAI": 
            embeddings = OpenAIEmbeddings()
        case "HuggingFace" : 
            embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")
        case "Gemma" :
            embeddings = HuggingFaceInstructEmbeddings(model_name = "google/gemma-2b")
        case _ : 
            embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")        
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding = embeddings)
    log.log_write(f"get_vectorstore <- :: vectorstore")
    return vectorstore

def get_conversation_chain(model, vectorstore) :
    log.log_write(f"get_conversation_chain :: Model = {model}")
    memory = ConversationBufferMemory(memory_key = "chat_history", return_messages =True) 
    match model : 
        case "OpenAI": 
            llm = ChatOpenAI()
            conversation_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=vectorstore.as_retriever(),
                memory=memory
                )
        case "HuggingFace" : 
            llm = HuggingFaceHub(repo_id="hkunlp/instructor-xl",
                                 task= "conversational",
                                 model_kwargs={ "temperature":0.5,"max_length":512})
            chat_model = ChatHuggingFace(llm=llm)

        case "Gemma" :
            llm = HuggingFaceHub(repo_id="google/gemma-2b",
                                 task= "conversational",
                                 model_kwargs={"task": "conversational","temperature":0.5,"max_length":512})
        case _ :   
            llm = HuggingFaceHub(repo_id="google/flan-t5-xxl",model_kwargs={"task": "conversational","temperature":0.5,"max_length":512})
   
    log.log_write(f"get_conversation_chain :: conversation_chain = {type(conversation_chain)}")
    return conversation_chain


def handle_userinput (user_question, chat_history_con) : 
    if "conversation" not in st.session_state or st.session_state.conversation is None:
        st.write("Please select and read a file before asking questions")
    else :
        with chat_history_con: 
            log.log_write(f"handle_userinput:: chat history(before) = {st.session_state.chat_history}")
            response = st.session_state.conversation({'question': user_question})
            st.session_state.chat_history = response['chat_history']
            log.log_write(f"handle_userinput:: chat history(after) = {st.session_state.chat_history}")
            file_details = "You have uploaded " + st.session_state.pdf_file_name + "(" + str(st.session_state.pdf_page_count) + " pages)"
            st.write(bot_template.replace("{{MSG}}", file_details), unsafe_allow_html=True)
            for i, message in enumerate(st.session_state.chat_history): 
                if i%2 == 0 : 
                    st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
                else :
                    st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def view_pdf(): 
    pass
    
def clear_questions():
    st.session_state.chat_history = []
    # keys = list(st.session_state.chat_history)
    # print (keys)
    # for key in keys:
    #     st.session_state.chat_history.pop(key)
    # if "conversation" not in st.session_state:
    #     st.session_state.conversation = None
    # if 'chat_history' not in st.session_state:
    #      st.session_state.chat_history = None

column_names = [ "user","name","page_count", "doc_type", "summary"]
if "files_df" not in st.session_state: 
    #if os.path.exists("files_df.pkl"): 
    #    docs_df =pickle.load(open("files_df.pkl","rb"))    
    #else : 
    docs_df = pd.DataFrame(columns = column_names)
else :
    docs_df = st.session_state["files_df"] 

def add_file_to_df (user_name, row):
    global docs_df
    if row[0] not in list(docs_df[docs_df["user"] == user_name]["name"]) : 
        docs_df.loc[docs_df.shape[0]] = [user_name] + [a for a in list(row)]
        print (f"docs = {docs_df}")
        log.log_write(f"Files = {docs_df}")
        pickle.dump( obj=docs_df, file=open("files_df.pkl","wb"))
        st.session_state["files_df"] = docs_df
       

def read_files(pdf_file, model, chat_history_con): 
    ## get PDF text  
    raw_text, page_count = get_pdf_text(pdf_file)
    ## divide text to chunks 
    text_chunks = get_text_chunks(raw_text)

    ## create a vector store with the embeddings 
    vectorstore = get_vectorstore(model, text_chunks)

    ## Create conversation c    hain 
    st.session_state.conversation = get_conversation_chain(model, vectorstore)

   
    with open(os.path.join("docs",pdf_file.name),"wb") as f: 
      f.write(pdf_file.getbuffer())     
    add_file_to_df (st.session_state.user_name, (pdf_file.name , page_count, "category", "summary"))
    
    user_question = f"I have uploaded {pdf_file.name} ({page_count} pages)."
    #response = st.session_state.conversation({'question': user_question}) 
    user_question = f"Please provide the policy details with the coverage, the insured and risk location"
    handle_userinput(user_question, chat_history_con)


def main() : 
    if "loggedIn" not in st.session_state or  not st.session_state["loggedIn"]:
        st.error ("Please login through the login page")
    else : 
        load_dotenv()
        st.set_page_config(page_title="Know your Insurance", page_icon=":books:", 
                        initial_sidebar_state="expanded", layout="wide",
                        menu_items = {
                            'Get help' : 'http://en.wikipedia.org/wiki/insurance',
                            'About': '# Learn the minute details of your insurance policy'
                        }
                    )
        # set up the CSS 
        st.write(css, unsafe_allow_html=True)
        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = None

        #c1, c2 = st.columns(2)
        
       

        #with c2 : 
        st.header("Chat with your Policy Wordings :books:")
        chat_history_con = st.container(height=500)
        user_question = st.text_input("Ask any question about your policies")
        if user_question:
            handle_userinput(user_question, chat_history_con)

        with st.sidebar: 
            st.markdown('<img src="./app/static/images/foi.png" height="50px" />', unsafe_allow_html=True)
            model = st.selectbox("Select your Model", ("OpenAI", "HuggingFace", "Gemma"))

            st.subheader("Your Policies")
            pdf_file = st.file_uploader ("Upload your policy documents here and click on Read", accept_multiple_files=False)
            #for pdf in pdf_docs :
            #           print (pdf.name, pdf.size)
            if st.button ("Read"): 
                if not pdf_file :
                    st.error("Please load the file again")
                else: 
                    with st.spinner("Reading.."): 
                        read_files(pdf_file, model,chat_history_con)
                                          
                  
            if st.button ("View"): 
                view_pdf()

            if st.button("Clear Questions"): 
                clear_questions()
                #st.session_state.conversation = get_conversation_chain(model, vectorstore)

if __name__ == "__main__" :
    main()
