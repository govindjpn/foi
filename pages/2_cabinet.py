import streamlit as st 
import base64




docs_df = st.session_state["files_df"] 
user_name = st.session_state["user_name"]
user_df = docs_df[docs_df["user"] == user_name]
st.table(data=user_df)
