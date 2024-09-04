import streamlit as st
from dotenv import load_dotenv
from streamlit_chat import message  # noqa: F401

from backend.core import run_llm  # noqa: F401

load_dotenv()

if (
    "user_prompt_history" not in st.session_state
    and "chat_answer_history" not in st.session_state
    and "user_history" not in st.session_state
):
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_answer_history"] = []
    st.session_state["chat_history"] = []


def create_sources_string(source_urls: set[str]) -> str:
    if not source_urls:
        return ""

    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string


st.header("LangChain Udemy Course - Documentation Helper Bot")
prompt = st.text_input(
    "Prompt", placeholder="Ask me anything about LangChain!"
)

if prompt:
    with st.spinner("Generating response..."):
        response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )
        sources = set(
            [doc.metadata["source"] for doc in response["source_documents"]]
        )

        formatted_response = (
            f"{response["result"]}\n\n{create_sources_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answer_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", response["result"]))

if st.session_state["user_prompt_history"]:
    st.subheader("Chat History")
    for prompt, response in zip(
        st.session_state["user_prompt_history"],
        st.session_state["chat_answer_history"],
    ):
        message(prompt, is_user=True)
        message(response)
