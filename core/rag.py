from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
RETRIEVAL_K = 4


def build_vectorstore(pdf_path: str, embeddings):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(documents)


    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)
    return vectorstore, len(documents), len(chunks)


def format_docs(docs) -> str:
    return "\n\n".join(d.page_content for d in docs)


def retrieve_context(retriever, query: str, k: int = RETRIEVAL_K):
    docs = retriever.invoke(query)
    return format_docs(docs), docs
