import streamlit as st

st.set_page_config(layout="wide")

st.title("⚙️ Settings")


def main():
    if 'page' not in st.session_state:
        st.session_state.page = "main"

    if st.session_state.page == "main":
        show_main_settings()
    elif st.session_state.page == "current_budget":
        show_current_budget()
    elif st.session_state.page == "automatic_bank_parsers":
        show_automatic_bank_parsers()
    elif st.session_state.page == "categories":
        show_categories()
    elif st.session_state.page == "limits":
        show_limits()
    elif st.session_state.page == "logout":
        show_logout()


def show_main_settings():
    if st.button("Current Budget"):
        st.session_state.page = "current_budget"
        st.rerun()
    if st.button("Automatic Bank Account Parsers"):
        st.session_state.page = "automatic_bank_parsers"
        st.rerun()
    if st.button("Categories"):
        st.session_state.page = "categories"
        st.rerun()
    if st.button("Limits"):
        st.session_state.page = "limits"
        st.rerun()
    if st.button("Logout"):
        st.session_state.page = "logout"
        st.rerun()


def show_back_button():
    if st.button("Back"):
        st.session_state.page = "main"
        st.rerun()


def show_current_budget():
    show_back_button()
    st.header("Current Budget")
    st.write("Here you can manage your current budget settings.")


def show_automatic_bank_parsers():
    show_back_button()
    st.header("Automatic Bank Account Parsers")
    st.write("Here you can manage your automatic bank account parsers settings.")


def show_categories():
    show_back_button()
    st.header("Categories")
    st.write("Here you can manage your categories settings.")


def show_limits():
    show_back_button()
    st.header("Limits")
    st.write("Here you can manage your limits settings.")


def show_logout():
    show_back_button()
    st.header("Logout")
    st.write("You have been logged out.")


if __name__ == "__main__":
    main()
