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


def should_load_bg(val):
    return bool(val)


def initialize_page_config(page_title, load_background=False, image_url=None):
    st.set_page_config(
        page_title=page_title,
        page_icon="👋",
    )
    if load_background:
        load_background_image(image_url)


def load_asset(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def load_background_image(image_url=None):
    if image_url is None:
        # image_url = "https://images.unsplash.com/photo-1528460033278-a6ba57020470"
        # image_url = "https://images.unsplash.com/photo-1487147264018-f937fba0c817"
        # image_url = "https://images.unsplash.com/photo-1551554781-c46200ea959d"
        # image_url = "https://images.unsplash.com/photo-1528459584353-5297db1a9c01"
        # image_url = "https://images.unsplash.com/photo-1531685250784-7569952593d2"
        image_url = "https://images.unsplash.com/photo-1568738351265-c7065f5d4293"

    page_bg_img = f"""
    <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
        }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)


def set_page_header(page_header):
    st.markdown(f"<h1 class='form-heading'>{page_header}</h1>", unsafe_allow_html=True)
