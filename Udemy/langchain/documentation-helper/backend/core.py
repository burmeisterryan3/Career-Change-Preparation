import os
from typing import Any

from dotenv import load_dotenv
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import (
    create_history_aware_retriever,
)
from langchain.chains.retrieval import create_retrieval_chain
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings


def run_llm(query: str, chat_history: list[dict[str, Any]]) -> Any:
    """Run the language model."""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = Chroma(
        collection_name=os.environ["INDEX_NAME"],
        embedding_function=embeddings,
        persist_directory=os.environ["EMBEDDINGS_DIR"],
    )

    llm = ChatOllama(model="llama3", verbose=True, temperature=0)

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    stuff_documents_chain = create_stuff_documents_chain(
        llm, retrieval_qa_chat_prompt
    )

    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
    history_aware_retriever = create_history_aware_retriever(
        llm=llm,
        retriever=vector_store.as_retriever(),
        prompt=rephrase_prompt,
    )
    qa = create_retrieval_chain(
        retriever=history_aware_retriever,
        combine_docs_chain=stuff_documents_chain,
    )

    result = qa.invoke(input={"input": query, "chat_history": chat_history})

    return {
        "query": result["input"],
        "result": result["answer"],
        "source_documents": result["context"],
    }


if __name__ == "__main__":
    load_dotenv()

    res = run_llm(query="What is a LangChain chain?", chat_history=[])
    print(res["result"])
