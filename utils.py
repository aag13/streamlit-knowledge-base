import streamlit as st


def set_session_var(var_name, var_val, dont_overwrite=False):
    if dont_overwrite and var_name in st.session_state:
        return

    st.session_state[var_name] = var_val


def get_session_var(var_name):
    if var_name in st.session_state:
        return st.session_state[var_name]

    return None


def remove_session_var(var_name):
    if var_name in st.session_state:
        del st.session_state[var_name]


def initialize_page_config(page_title, page_header):
    st.set_page_config(
        page_title=page_title,
        page_icon="👋",
    )

    st.markdown("""
    <style>
    .form-heading {
      text-align: center;
      font-size: 2rem;
      margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"<h1 class='form-heading'>{page_header}</h1>", unsafe_allow_html=True)



