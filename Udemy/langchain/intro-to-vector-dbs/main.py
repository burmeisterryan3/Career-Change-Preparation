import os

from dotenv import load_dotenv
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import (
    create_stuff_documents_chain,
)
from langchain_chroma import Chroma
from langchain_core.documents.base import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnablePassthrough,
)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def format_docs(docs: Document) -> str:
    """Format the retrieved documents into a single string."""
    return "\n\n".join([doc.page_content for doc in docs])


def without_rag(prompt: PromptTemplate, llm: ChatOpenAI):
    """Use the llm chain without RAG."""
    chain = prompt | llm
    res = chain.invoke(input={})
    print(res.content)


def with_rag_chain(llm: ChatOpenAI, vector_store: Chroma):
    """Use the LangChain tools to create a RAG chain."""
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(
        llm, retrieval_qa_chat_prompt
    )
    retrieval_chain = create_retrieval_chain(
        retriever=vector_store.as_retriever(),
        combine_docs_chain=combine_docs_chain,
    )

    res = retrieval_chain.invoke(input={"input": query})
    print(res["answer"])


if __name__ == "__main__":
    load_dotenv()
    print("Retrieving...")

    embeddings = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])
    llm = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"])

    query = "What is Pinecone in machine learning?"
    prompt = PromptTemplate(template=query)

    # without_rag()

    vector_store = Chroma(
        collection_name=os.environ["INDEX_NAME"],
        embedding_function=embeddings,
        persist_directory=os.environ["EMBEDDINGS_DIR"],
    )

    # with_rag_chain(llm, vector_store)

    # Custom RAG prompt and without LangChain built-in chain tools
    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know. Don't try to make up an answer.
    Use three sentences maximum and keep the answer as concise as possible.
    Always say "thanks for asking!" at the end.

    {context}

    Question: {question}

    Helpful answer:"""

    custom_rag_prompt = PromptTemplate(
        template=template, input_variables=["context", "question"]
    )

    rag_chain = (
        {
            "context": vector_store.as_retriever() | format_docs,
            "question": RunnablePassthrough(),
        }
        | custom_rag_prompt
        | llm
    )
    res = rag_chain.invoke(query)

    print(res)
