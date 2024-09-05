import streamlit as st

add_page = st.Page("_pages/add.py", title="Add Transaction", icon="➕")
transactions_page = st.Page("_pages/transaction.py", title="Transactions", icon="📊", default=True)
goals_page = st.Page("_pages/goals.py", title="Goals", icon="🎯")
settings_page = st.Page("_pages/settings.py", title="Settings", icon="⚙️")
logout_page = st.Page("_pages/logout.py", title="Logout", icon="🚪")

pages = [add_page, transactions_page, goals_page, settings_page]

st.session_state['logged_in'] = True
if 'logged_in' in st.session_state:
    pages.append(logout_page)

pg = st.navigation(pages)

pg.run()


# def main() -> None:

#     st.markdown(
#         """
#         # Welcome to Budguette! 🥖

#         Budguette is an open-source budget tracker.

#         **👈 Select a demo from the sidebar** to see some examples
#         of what Streamlit can do!

#         ### Want to learn more?

#         - Check out [streamlit.io](https://streamlit.io)
#         - Jump into our [documentation](https://docs.streamlit.io)
#         - Ask a question in our [community forums](https://discuss.streamlit.io)

#         ### See more complex demos

#         - Use a neural net to [analyze the Udacity Self-driving Car Image Dataset](https://github.com/streamlit/demo-self-driving)
#         - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
#     """
#     )


# if __name__ == "__main__":
#     main()
