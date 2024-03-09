import streamlit as st 
import base64


def show_pdf(file_path):
    pass
    # with open(file_path,"rb") as f:
    #     base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    # st.markdown(pdf_display, unsafe_allow_html=True)

docs_df = st.session_state["files_df"] 
user_name = st.session_state["user_name"]
user_df = docs_df[docs_df["user"] == user_name]
st.table(data=user_df)
