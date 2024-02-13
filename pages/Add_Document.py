import json
import time
import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval
import utils


utils.initialize_page_config("Add Document", load_background=utils.should_load_bg(st.secrets["params"]["load_bg"]))
utils.load_asset("assets/styles.css")
utils.set_page_header("Wanna contribute?")


def disable_button():
    utils.set_session_var("button_disabled", True)


def store_response_msg_type(message_to_show, msg_type):
    utils.set_session_var("message_to_show", message_to_show)
    utils.set_session_var("msg_type", msg_type)


def show_response_msg_if_any():
    if utils.get_session_var('message_to_show') and utils.get_session_var('msg_type'):
        if utils.get_session_var('msg_type') == "success":
            st.success(utils.get_session_var('message_to_show'))
        else:
            st.error(utils.get_session_var('message_to_show'))

        utils.remove_session_var("message_to_show")
        utils.remove_session_var("msg_type")


def enable_button():
    utils.set_session_var("button_disabled", False)


utils.set_session_var("button_disabled", False, dont_overwrite=True)


form_container = st.container()
with form_container:
    with st.form("my_form"):
        category = st.selectbox("Category *", st.secrets["params"]["category_list"])
        title = st.text_input("Title *")
        tags = st.text_input("Tags (Comma separated) *")
        created_by = st.text_input("Created by *")
        md_content = st.text_area("Type in your markdown content *", "So, **How will it be**?")
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Submit", on_click=disable_button, disabled=utils.get_session_var("button_disabled"))

        with col2:
            reset = st.form_submit_button("Reset")


show_response_msg_if_any()


if reset:
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

if submitted:
    if not category or not title or not tags or not created_by or not md_content:
        store_response_msg_type("Must provide all values!", "error")
    else:
        form_data = {
            "category": category,
            "title": title,
            "tags": tags,
            "md_content": md_content,
            "created_by": created_by,
        }

        try:
            index_url = f"{st.secrets['params']['api_base_endpoint']}/{st.secrets['params']['doc_path']}"
            response = requests.post(index_url, data=json.dumps(form_data))
            parsed_response = response.json()
            if response.status_code == 200:
                store_response_msg_type(parsed_response.get("message"), "success")
            else:
                store_response_msg_type(parsed_response.get("message"), "error")

        except Exception as exp:
            store_response_msg_type(exp, "error")

    enable_button()
    st.rerun()
