from pathlib import Path

import streamlit as st

from app.faq import ingest_faq, faq_chain
from app.router import router
from app.sql import sql_chain
from app.small_talk import talk

BASE_DIR = Path(__file__).parent
FAQ_PATH = BASE_DIR / "app" / "resources" / "faq_data.csv"


def initialize_faq():
    ingest_faq(FAQ_PATH)


initialize_faq()


def ask(query):
    route = router(query).name

    if route == "faq":
        return faq_chain(query)
    elif route == 'sql':
        return sql_chain(query)
    elif route == 'small_talk':
        return talk(query)

    return f"This {route} route is not implemented yet"


st.title("Ecom Chat Bot")


if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


query = st.chat_input("Write your query")


if query:

    # Display user message
    with st.chat_message("user"):
        st.markdown(query)

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # Generate response
    response = ask(query)

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })