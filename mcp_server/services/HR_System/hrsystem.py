from vector_store.vectorstore import vector_store
from utils.fileutil import get_all_file_paths, make_directory, remove_directory
from utils.filestoreutil import FileStore
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

class HRSystem:
    def __init__(self):
        self.store = self.load_store()

    def load_store(self, ):
        fldr = str(uuid.uuid4())
        base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        make_directory(base_path, fldr)
        filestr = FileStore()
        filestr.load_files(os.getenv("HR_FOLDER"), os.path.join(base_path, fldr))
        src_files = get_all_file_paths(os.path.join(base_path, fldr))
        store = vector_store(src_files)
        remove_directory(base_path, fldr)
        return store

    def search(self, query):
        return self.store.similarity_search(query)
