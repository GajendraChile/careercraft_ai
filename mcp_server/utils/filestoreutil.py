from cloudpathlib import CloudPath
from dotenv import load_dotenv
import os

load_dotenv()

class FileStore:

    def download_all(self, cloud_folder, local_dir):
        """
        Download all files from a cloud storage 'folder' to a local directory.

        Args:
            cloud_folder: S3Path or GSPath (e.g. S3Path("s3://bucket/folder/"))
            local_dir: str (e.g. "./downloads")
        """
        os.makedirs(local_dir, exist_ok=True)

        for f in cloud_folder.rglob("*"):
            if f.is_file():
                local_path = os.path.join(local_dir, f.name)
                print(f"Downloading {f} -> {local_path}")
                f.download_to(local_path)

    def load_cloud_files(self, src_folder, local_dir):
        folder = CloudPath(f"{os.getenv("FILE_BASEPATH")}/{src_folder}")
        self.download_all(folder, local_dir)

    def load_files(self, src_folder, local_dir):
        self.load_cloud_files(src_folder, local_dir)