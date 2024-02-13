import json
import time
from datetime import datetime
import streamlit as st
import requests
from urllib.parse import urlparse, parse_qs
from streamlit_js_eval import streamlit_js_eval
import utils


utils.initialize_page_config("Update Document")
utils.load_asset("assets/styles.css")
utils.load_background_image()
utils.set_page_header("Wanna redeem yourself?")


def disable_doc_load_button():
    utils.set_session_var("doc_load_button_disabled", True)


def disable_doc_update_button():
    utils.set_session_var("doc_update_button_disabled", True)


@st.cache_data
def fetch_document(url):
    return requests.get(url)


def store_doc_load_response_msg_type(message_to_show, msg_type):
    utils.set_session_var("doc_load_message_to_show", message_to_show)
    utils.set_session_var("doc_load_msg_type", msg_type)


def store_doc_update_response_msg_type(message_to_show, msg_type):
    utils.set_session_var("doc_update_message_to_show", message_to_show)
    utils.set_session_var("doc_update_msg_type", msg_type)


def clean_doc_load_response_msg_type():
    utils.remove_session_var("doc_load_message_to_show")
    utils.remove_session_var("doc_load_msg_type")


def clean_doc_update_response_msg_type():
    utils.remove_session_var("doc_update_message_to_show")
    utils.remove_session_var("doc_update_msg_type")


def render_doc_update_form():
    fetched_doc = utils.get_session_var("fetched_doc")
    if fetched_doc is None:
        return

    fetched_doc_id = fetched_doc["doc_id"]
    session_doc_id = utils.get_session_var("current_doc_id")
    if fetched_doc_id != session_doc_id:
        st.error("Invalid doc id, please reload the page!")
        return

    selected_category = st.secrets["params"]["category_list"].index(fetched_doc["category"])
    title_val = fetched_doc["title"]
    tags_val = fetched_doc["tags"]
    md_content_val = fetched_doc["md_content"]
    created_by_val = fetched_doc["created_by"]
    created_at_ms_val = fetched_doc["created_at_ms"]
    created_time = datetime.fromtimestamp(int(int(created_at_ms_val) / 1000)).strftime("%d/%m/%Y, %H:%M:%S")

    form_container = st.container()
    with form_container:
        with st.form("doc_update_form"):
            update_category = st.selectbox("Category *", st.secrets["params"]["category_list"], index=selected_category)
            update_title = st.text_input("Title *", title_val)
            update_tags = st.text_input("Tags (Comma separated) *", tags_val)
            update_last_updated_by = st.text_input("Updated by *")
            update_created_by = st.markdown(f"**Created by:** {created_by_val} ({created_time})")
            update_md_content = st.text_area("Type in your markdown content *", md_content_val)
            update_submitted = st.form_submit_button("Update", on_click=disable_doc_update_button, disabled=utils.get_session_var("doc_update_button_disabled"))

    if update_submitted:
        if not update_category or not update_title or not update_tags or not update_last_updated_by or not update_md_content:
            store_doc_update_response_msg_type("Must provide all values!", "error")
        else:
            update_form_data = {
                "category": update_category,
                "title": update_title,
                "tags": update_tags,
                "md_content": update_md_content,
                "last_updated_by": update_last_updated_by,
            }
            try:
                update_url = f"{st.secrets['params']['api_base_endpoint']}/{st.secrets['params']['doc_path']}/{fetched_doc_id}"
                response = requests.put(update_url, data=json.dumps(update_form_data))
                parsed_response = response.json()
                if response.status_code == 200:
                    store_doc_update_response_msg_type(parsed_response.get("message"), "success")
                else:
                    store_doc_update_response_msg_type(parsed_response.get("message"), "error")
            except Exception as exp:
                store_doc_update_response_msg_type(exp, "error")
            finally:
                del update_form_data["last_updated_by"]
                fetched_doc.update(update_form_data)
                utils.set_session_var("fetched_doc", fetched_doc)
                fetch_document.clear()

        enable_doc_update_button()
        st.rerun()


def render_doc_load_response():
    if utils.get_session_var('doc_load_message_to_show') and utils.get_session_var('doc_load_msg_type'):
        if utils.get_session_var('doc_load_msg_type') == "error":
            st.error(utils.get_session_var('doc_load_message_to_show'))

        clean_doc_load_response_msg_type()


def render_doc_update_response():
    if utils.get_session_var('doc_update_message_to_show') and utils.get_session_var('doc_update_msg_type'):
        if utils.get_session_var('doc_update_msg_type') == "success":
            st.success(utils.get_session_var('doc_update_message_to_show'))
        else:
            st.error(utils.get_session_var('doc_update_message_to_show'))

        clean_doc_update_response_msg_type()


def enable_doc_load_button():
    utils.set_session_var("doc_load_button_disabled", False)


def enable_doc_update_button():
    utils.set_session_var("doc_update_button_disabled", False)


def process_document_load(url):
    response = fetch_document(url)
    parsed_response = response.json()
    if response.status_code == 200:
        utils.set_session_var("fetched_doc", parsed_response["data"])
        clean_doc_load_response_msg_type()
    else:
        store_doc_load_response_msg_type("No document found!", "error")
        utils.remove_session_var("fetched_doc")
        clean_doc_update_response_msg_type()


def extract_query_param():
    current_url = streamlit_js_eval(js_expressions="window.parent.location.href")
    parsed_url = urlparse(current_url)
    parsed_query = parse_qs(parsed_url.query)
    extracted_doc_id = parsed_query.get('doc_id', [''])[0]
    utils.set_session_var("current_doc_id", extracted_doc_id)
    if extracted_doc_id:
        doc_url = f"{st.secrets['params']['api_base_endpoint']}/{st.secrets['params']['doc_path']}/{utils.get_session_var('current_doc_id')}"
        process_document_load(doc_url)


utils.set_session_var("doc_load_button_disabled", False, dont_overwrite=True)
utils.set_session_var("doc_update_button_disabled", False, dont_overwrite=True)
if utils.get_session_var("doc_load_on_click") is None:
    extract_query_param()


doc_id_container = st.container()
with doc_id_container:
    with st.form("doc_id_form"):
        doc_load_id = st.text_input("Doc ID *", utils.get_session_var("current_doc_id"))
        doc_id_submitted = st.form_submit_button("Load Document", on_click=disable_doc_load_button, disabled=utils.get_session_var("doc_load_button_disabled"))


if doc_id_submitted:
    utils.set_session_var("current_doc_id", doc_load_id)
    utils.set_session_var("doc_load_on_click", True)

    if not doc_load_id:
        store_doc_load_response_msg_type("Must provide document id!", "error")
        utils.remove_session_var("fetched_doc")
        clean_doc_update_response_msg_type()
    else:
        get_url = f"{st.secrets['params']['api_base_endpoint']}/{st.secrets['params']['doc_path']}/{utils.get_session_var('current_doc_id')}"
        process_document_load(get_url)

    enable_doc_load_button()
    st.rerun()

render_doc_load_response()
render_doc_update_form()
render_doc_update_response()

