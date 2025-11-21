import streamlit as st


def init_session_state():
    """
    Uygulama ilk açıldığında kullanılacak
    veri yapısını (boş hâlde) oluşturur.
    """
    defaults = {
        "transport": {},
        "energy": {},
        "water": {},
        "food": {},
        "waste": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
