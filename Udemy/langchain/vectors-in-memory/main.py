from dotenv import load_dotenv
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import (
    create_stuff_documents_chain,
)
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

if __name__ == "__main__":
    load_dotenv()

    pdf_path = "./Udemy/langchain/vectors-in-memory/React Paper.pdf"

    # Will chunk the document into pages - 33 pages in this case
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    # Need to split the text by characters to ensure we meet token requirements
    # Also also us to set overlap
    # Takes our 33 documents and splits them into 132 documents
    text_splitter = CharacterTextSplitter(
        chunk_size=1000, chunk_overlap=30, separator="\n"
    )
    docs = text_splitter.split_documents(documents=docs)

    embeddings = OpenAIEmbeddings()

    # Stored in RAM
    vectorstore = FAISS.from_documents(documents=docs, embedding=embeddings)
    vectorstore.save_local("./Udemy/langchain/vectors-in-memory/faiss_index_react")

    new_vectorstore = FAISS.load_local(
        "faiss_index_react", embeddings, allow_dangerous_deserialization=True
    )

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(
        OpenAI(), retrieval_qa_chat_prompt
    )

    retrieval_chain = create_retrieval_chain(
        new_vectorstore.as_retriever(), combine_docs_chain
    )

    res = retrieval_chain.invoke(
        input={"input": "Give me the gist of ReAct in 3 sentences."}
    )

    print(res["answer"])
