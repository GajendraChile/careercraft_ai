from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import faiss
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from dotenv import load_dotenv
import os

load_dotenv()
embedding_model = os.getenv("EMBEDDING_MODEL")
def vector_store(file_paths):
    embeddings = BedrockEmbeddings(model_id=embedding_model)
    all_splits = []
    index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

    store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    ) 
    print("outside for loop")
    print(",".join(file_paths))
    for file_path in file_paths:
        print(f"inside for loop {file_path}")
        loader = PyPDFLoader(file_path)

        #load the documents by pages
        docs = loader.load()

        text_splitters = RecursiveCharacterTextSplitter(
            chunk_size = 400,
            chunk_overlap = 50,
            add_start_index = True
        )
        
        splits = text_splitters.split_documents(docs)
        all_splits.extend(splits)
        
        store.add_documents(documents= all_splits)
    return store