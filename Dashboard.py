import json
from datetime import datetime
import streamlit as st
import requests
import utils


utils.initialize_page_config("Dashboard", "🎉 Welcome to Knowledge Base App! 🎉")

with st.expander("What is it?", expanded=True):
    st.markdown("""
    This is a demo **Knowledge Base** app built with **Streamlit** as the *frontend* and  **Amazon Opensearch** as the underlying *search engine*. 
    The app is hosted on AWS and uses API Gateway and Lambda to connect the frontend app with the Opensearch. 
    """)

with st.expander("How can I use it?", expanded=True):
    st.markdown("""
    Since the app is hosted on AWS for *demo purpose only*, you **must not** use this app for any real use cases. You can look around and 
    get inspired on how to implement ADD, GET, UPDATE, and SEARCH with Streamlit. You can also **use the code for free** to create 
    and host your own knowledge base/search engine. 🎆
    
    Just give credit to the author (**me, me**) 🙌
    """)

with st.expander("Where to find the code?", expanded=True):
    st.markdown("""
    You can find the entire code in this Github repo [knowledge-base-streamlit-opensearch](https://github.com/CloudBazar/opensearch-knowledge-base) 
    """)


