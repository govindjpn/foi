import re, string
import random 
import bcrypt 
import streamlit as st
from dotenv import load_dotenv

import smtplib
from email.mime.text import MIMEText

import time
import pickle

user_dict = pickle.load(open("user_dict.pkl","rb"))
def sql_add_user (email, hashedpw, username,active_flag) :
    user_dict[email] = (hashedpw, username, active_flag)
    pickle.dump (open("user_dict.pkl","wb",encoding="utf-8"))
def sql_get_user (email) :
    if email in user_dict.keys():
        return user_dict[email]
    else:
        return None

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()


def create_strong_password(pw_len:int = 16) :
    # starts with a letter and ends with a letter 
    letter =  string.ascii_letters
    scope = string.ascii_letters + string.digits + "!#_-@" 
    password = random.choice(letter) + ''.join(random.choice(scope) for i in range(pw_len - 2)) + random.choice(letter)
    return password


def send_password_reset_mail (to_email ):
    # Taking inputs
    SENDER_EMAIL = ""
    SENDER_PASSWORD = ""
    load_dotenv()
    email_sender = SENDER_EMAIL
    email_receiver = to_email
    subject = "Password Reset Request"
    body = ""
    password = SENDER_PASSWORD 

    if st.button("Send Email"):
        try:
            msg = MIMEText(body)
            msg['From'] = email_sender
            msg['To'] = email_receiver
            msg['Subject'] = subject

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_sender, password)
            server.sendmail(email_sender, email_receiver, msg.as_string())
            server.quit()
        
            st.success('Email sent successfully! 🚀')
        except Exception as e:
            st.error(f"Error in sending EMail : {e}")

def validate_username(username:str): 
    regexp = r"^[a-zA-Z0-9_-]{1,20}$"  
    # ^ to negate, [] Square braces for disjunction of characters 
    # {} curly braces for counter $ matches end of line 
    return bool(re.match(regexp, username))
def validate_emailID(emailID: str): 
    regexp = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' 
    # \b word boundary ^ to negate, {} for counter $ matches end of line 
    return bool(re.match(regexp, emailID))
def hash_password(pw:str): 
    # https://en.wikipedia.org/wiki/Bcrypt
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
def check_password(pw, hash): 
    # https://en.wikipedia.org/wiki/Bcrypt
    return bcrypt.checkpw(bytes(pw,"utf-8"), bytes(hash,"utf-8"))

def login_clicked(email, password): 
    if not validate_emailID(email) : 
        st.session_state["loggedIn"] = False
        st.error("Please enter the email ID in the format <user>@<domain>.<suffix>")
    else :
        if (user_details := sql_get_user (email)) is None: 
            st.session_state["loggedIn"] = False
            st.error("Email / Password incorrect.") 
        else : 
            db_hashedpw, username, active_flag  = user_details 
            #print (password, db_hashedpw)
            if check_password(password, db_hashedpw):
                st.session_state["loggedIn"] = True
                st.session_state["user_name"] = email
                if active_flag == 1 :
                    show_main_page()
                else: 
                     st.error("Email / Password incorrect.") 


def logout_clicked(): 
    st.session_state["loggedIn"] = False 
    st.session_state["user_name"] = ""

def create_clicked(email, password, username): 
    if not validate_emailID(email):
        st.error("Please enter the email ID in the format <user>@<domain>.<suffix>")
    else : 
        if not validate_username(username):
            st.error("Please enter the name within 20 characters")
        else : 
            hasshedpw = hash_password(password)
            active_flag = 1 
            user = sql_add_user(email, hasshedpw, username, active_flag)
            st.session_state["loggedIn"] = True
            st.session_state["user_name"] = email
            st.success("Account Created successfully")
            show_main_page()

def show_login_page(): 
    with loginSection : 
        if st.session_state["loggedIn"] == False : 
            choice = st.selectbox("Login / Signup", ("Login", "Signup")) 
            if choice == "Login":
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password")
                st.button("Login", on_click =login_clicked, args=(email, password))
            else : 
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password")
                verify_password = st.text_input("Reenter Password", type="password")
                username = st.text_input("How do we call you?") 

                if verify_password != password:
                    st.error ("Please reenter password")
                st.button("Create User", on_click =create_clicked, args=(email, password, username))
                   

def show_logout_page(): 
    loginSection.empty()
    with logOutSection:
        st.button("Logout", key="logout", on_click=logout_clicked)

def show_main_page():
    #pass
    st.page_link("pages/1_foi.py", label="FOI")
    
def app(): 

    with headerSection : 
        #print ("within Header Section - Start")
        st.title ("Friends of Insurance")
        ## first run will not have logged-in user details 
        if "loggedIn" not in st.session_state:
            st.session_state["loggedIn"] = False
            show_login_page()
            #print ("within Header Section - After Login")
        else :
            if st.session_state["loggedIn"]:
                #print ("within Header Section - LoggedIn True")
                show_logout_page()
                show_main_page()
            else :
                #print ("within Header Section - LoggedIn False")
                show_login_page()
        #print ("within Header Section - End")
       

if __name__ == "__main__":
    
    app()