import streamlit as st

st.set_page_config(layout="centered")

st.title("➕ Add Transaction")
account = st.selectbox("Account", ["Account 1", "Account 2"])
amount = st.number_input("Amount")
income = st.checkbox("Income")
if st.button("Add"):
    st.success(f"Transaction added: {account} - {amount} {'Income' if income else 'Expense'}")
