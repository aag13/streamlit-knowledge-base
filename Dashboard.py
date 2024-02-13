import json
from datetime import datetime
import streamlit as st
import requests
import utils


utils.initialize_page_config("Dashboard")
utils.load_asset("assets/styles.css")
utils.load_background_image()
utils.set_page_header("🎉 Welcome to Knowledge Base App! 🎉")


with st.expander("What is it?", expanded=True):
    st.markdown("""
    This is a demo **Knowledge Base** app built with **Streamlit** as the *frontend* and  **Amazon Opensearch** as the underlying *search engine*. 
    The app is hosted on AWS and uses API Gateway and Lambda to connect the frontend app with the Opensearch. 
    """)

with st.expander("How can I use it?", expanded=True):
    st.markdown("""
    Since the app is hosted on AWS for *demo purpose only*, you **must not** use this app for any real-world use cases. You can look around and 
    get ideas on how to implement different Http methods with Streamlit. You can also **use the code for free** to create 
    and host your own knowledge base or search engine. 🎆
    
    Don't forget to give credit to the author (**me, me**) 😊
    """)

with st.expander("Where to find the code?", expanded=True):
    st.markdown("""
    You can find the SAM template to deploy services on AWS and all the *Lambda* functions for relevant APIs in this GitHub repo ➡️ 
    [Opensearch Knowledge Base](https://github.com/CloudBazar/opensearch-knowledge-base)
    
    And the entire code for this Streamlit app can be found in this GitHub repo ➡️ 
    [Streamlit Knowledge Base](https://github.com/aag13/streamlit-knowledge-base)
    
    *Follow the instructions in respective GitHub repos to deploy both the frontend and backend apps.*
    """)

