import streamlit as st
from components.transactions import TransactionComponent, TransactionsContainer
from datetime import datetime
import streamlit.components.v1 as components


st.set_page_config(layout="centered")

st.title("📊 Transactions")
tabs = st.tabs(["📜 Transactions", "📈 Statistics"])
with tabs[0]:
    # st.write("List of transactions")
    # Sample usage
    transactions = [
        TransactionComponent("OpenAI", datetime(2024, 7, 23, 22, 28), -22.00, "€", "Subscription"),
        TransactionComponent("Leisan B", datetime(2024, 7, 6, 17, 42), -2000.00, "€", "Transfer"),
        TransactionComponent("Vanda Irkhuzhyna", datetime(2024, 7, 6, 16, 44), -209.88, "€", "Transfer"),
        TransactionComponent("Vladislav Sobolev", datetime(2024, 7, 4, 10, 10), 4000.00, "€", "Income"),
        TransactionComponent("aleksandr.star", datetime(2024, 6, 30, 10, 10), 250.00, "€", "Transfer")
    ]

    container = TransactionsContainer(transactions)
    # components.html(container.render(), height='100%')
    st.html(container.render())

with tabs[1]:
    st.write("Statistics")
