import streamlit as st


def login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return True

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if (
            username == "admin"
            and password == "admin123"
        ):

            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("Invalid credentials")

    return False