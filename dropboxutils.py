import dropbox
import os
import pandas as pd

from utils import create_folder

class DropboxUtils():
    """
    Class that handles the connections and downloading from dropbox
    """
    
    def __init__(self, ACCESS_TOKEN):
        self.dbx = dropbox.Dropbox(ACCESS_TOKEN)
        self.local_path = ""
    
    def list_files(self, path = "", shared_link = None):
        """
        Lists all the files inside the shared folder
        """
        
        try:
            files = self.dbx.files_list_folder(path = path, shared_link = shared_link).entries
            files_list = []
            for file in files:
                metadata = {
                    'name': file.name,
                    'path_display': file.path_display
                }
                files_list.append(metadata)
            df = pd.DataFrame.from_records(files_list)
            return df
        except Exception as e:
            print(f"Error while getting list of files: {str(e)}")     
        
    def download_shared_folder(self, url, target_path):
        """
        Iterates over the files and downloads all the .mp4 and .zip files from the shared folder
        """
        
        shared_link = dropbox.files.SharedLink(url = url)
        files = self.list_files(path = "", shared_link = shared_link)
        self.local_path = os.path.join(os.getcwd(), target_path)
        create_folder(self.local_path)

        for file_name in files["name"]:
            if file_name.endswith(".zip") or file_name.endswith(".mp4"):
                path = os.path.join(self.local_path, file_name)
                self.download_shared_file(shared_link, file_name, path)

        print(f"File(s) downloaded to: {self.local_path}")
        
    def download_shared_file(self, shared_link, file_name, target_path):
        """
        Writes the shared file to the local path
        """
        
        try:
            with open(target_path, 'wb') as f:
                metadata, result = self.dbx.sharing_get_shared_link_file(url = shared_link.url, path="/" + file_name)
                f.write(result.content)
        except Exception as e:
            print(f"Error while downloading file: {str(e)}")
