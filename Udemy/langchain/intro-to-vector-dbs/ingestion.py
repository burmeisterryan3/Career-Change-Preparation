import os
from uuid import uuid4

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders.text import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

if __name__ == "__main__":
    load_dotenv()
    print("Starting...")

    loader = TextLoader(
        "./Udemy/langchain/intro-to-vector-dbs/mediumblog1.txt", encoding="utf-8"
    )
    document = loader.load()

    print("Splitting...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(document)
    print(f"Split into {len(texts)} chunks")

    print("Ingesting...")
    embeddings = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])

    persist_directory = os.environ["EMBEDDINGS_DIR"]
    if not os.path.exists(persist_directory):
        vector_store = Chroma.from_documents(
            documents=texts,
            collection_name=os.environ["INDEX_NAME"],
            embedding=embeddings,
            persist_directory=persist_directory,
            ids=[str(uuid4()) for _ in range(len(texts))],
        )
