import os
from pathlib import Path
from urllib.parse import urljoin
from uuid import uuid4

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import (  # noqa
    BSHTMLLoader,
)
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import CharacterTextSplitter

if __name__ == "__main__":
    load_dotenv()
    print("Starting...")

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vector_store = Chroma(
        collection_name=os.environ["INDEX_NAME"],
        embedding_function=embeddings,
        persist_directory=os.environ["EMBEDDINGS_DIR"],
    )

    for root, _, files in os.walk(Path(os.environ["DOCUMENTS_DIR"])):
        for file in files:
            full_path = os.path.join(root, file)
            loader = BSHTMLLoader(full_path, open_encoding="utf-8")
            document = loader.load()

            text_splitter = CharacterTextSplitter(
                chunk_size=600, chunk_overlap=50
            )
            docs = text_splitter.split_documents(document)

            url_path = str(full_path).replace(
                str(Path(os.environ["DOCUMENTS_DIR"])), ""
            )
            new_url = urljoin(
                os.environ["LANGCHAIN_URL_PREFIX"],
                url_path.replace("\\", "/")[1:],
            )
            for doc in docs:
                doc.metadata.update({"source": new_url})

            vector_store.add_documents(
                documents=docs,
                ids=[str(uuid4()) for _ in range(len(docs))],
            )

    print("Done!")
