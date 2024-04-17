import streamlit as st 
import base64 
import os 



def view_pdf(file_path):
    pass
    # with open(file_path,"rb") as f:
    #     base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    # st.markdown(pdf_display, unsafe_allow_html=True)
    if "pdf_file_name" in st.session_state and st.session_state.pdf_file_name is not None: 
        pdf_file_name = st.session_state.pdf_file_name
        with open(os.path.join("docs",pdf_file_name), "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="inherit" height="1000" type="application/pdf"></iframe>'
        #print(f"Displaying PDF {pdf_file_name}")
        st.markdown(pdf_display, unsafe_allow_html=True)