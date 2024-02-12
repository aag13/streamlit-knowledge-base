import json
from datetime import datetime
import streamlit as st
import requests
import utils


utils.initialize_page_config("Search Documents", "Oi, show me something!")


def display_documents_in_expander(documents):
    for doc in documents:
        expander_title = f"{doc['title']}"
        with st.expander(expander_title, expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Doc ID:** {doc['doc_id']}")
            with col2:
                st.markdown(f"[Update](/Update_Document/?doc_id={doc['doc_id']})")
            st.markdown(f"**Category:** {doc['category']}")
            st.markdown(f"**Tag:** {doc['tags']}")
            st.markdown(f"**Content:** {doc['md_content']}")
            create_col1, update_col2 = st.columns(2)
            with create_col1:
                created_time = datetime.fromtimestamp(int(int(doc['created_at_ms'])/1000)).strftime("%d/%m/%Y, %H:%M:%S")
                st.markdown(f"**Created by:** {doc['created_by']} ({created_time})")
            with update_col2:
                updated_time = datetime.fromtimestamp(int(int(doc['last_updated_at_ms']) / 1000)).strftime(
                    "%d/%m/%Y, %H:%M:%S")
                st.markdown(f"**Last updated by:** {doc['last_updated_by']} ({updated_time})")


def disable_button():
    utils.set_session_var("button_disabled", True)


def store_response_msg_type(message_to_show, msg_type="default"):
    utils.set_session_var("message_to_show", message_to_show)
    utils.set_session_var("msg_type", msg_type)


def show_response_msg_if_any():
    if utils.get_session_var('message_to_show') is not None and utils.get_session_var('msg_type') is not None:
        if utils.get_session_var('msg_type') == "error":
            st.error(utils.get_session_var('message_to_show'))
        elif utils.get_session_var('msg_type') == "search_list":
            count_docs = utils.get_session_var('message_to_show')
            if count_docs.get('count') > 0:
                results_container.subheader(f"Found ({count_docs.get('count')})")
                display_documents_in_expander(count_docs.get('docs'))
            else:
                results_container.write("No results found.")

        utils.remove_session_var("message_to_show")
        utils.remove_session_var("msg_type")


def enable_button():
    utils.set_session_var("button_disabled", False)


utils.set_session_var("button_disabled", False, dont_overwrite=True)

form_container = st.container()
with form_container:
    with st.form("my_form"):
        category = st.selectbox("Category", ["All", *st.secrets["params"]["category_list"]])
        text = st.text_input("Search")
        submitted = st.form_submit_button("Submit", on_click=disable_button, disabled=utils.get_session_var("button_disabled"))

results_container = st.container()
show_response_msg_if_any()

if submitted:
    if not category or not text:
        store_response_msg_type("Must provide all values!", "error")
    else:
        form_data = {
            "category": category,
            "text": text,
        }
        try:
            search_url = f"{st.secrets['params']['api_base_endpoint']}/{st.secrets['params']['doc_path']}/search"
            headers = {"Content-Type": "application/json"}
            response = requests.post(search_url, data=json.dumps(form_data), headers=headers)
            parsed_response = response.json()

            if response.status_code == 200:
                count = parsed_response.get("data").get("count")
                docs = parsed_response.get("data").get("documents")
                store_response_msg_type({"count": count, "docs": docs}, "search_list")
            else:
                store_response_msg_type(parsed_response.get("message"), "error")
        except Exception as exp:
            store_response_msg_type(exp, "error")

    enable_button()
    st.rerun()
