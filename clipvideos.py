import yaml
import os
import argparse

from dropboxutils import DropboxUtils
from videoutils import VideoProcessing
from postgresqlutils import Postgresql
from utils import save_report

def main(target_folder, url = None):
    """
    target_folder: Folder containing video files to process. 
        If url is not None it will be the destination folder to save dropbox files.
        
    url: Shared folder link from dropbox containing video files to process.
        Content will be saved in target_folder.
    """
    
    with open("config.yaml", "r") as f: # Load configuration file
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    if url: # It can process dropbox shared folder or local folders
        dropbox_utils = DropboxUtils(config['ACCESS_TOKEN'])
        dropbox_utils.download_shared_folder(url, target_folder)
        path = dropbox_utils.local_path
    else:
        path = os.path.join(os.getcwd(), target_folder)
    
    video_utils = VideoProcessing()
    video_utils.process_video_files(path)
    df = video_utils.create_dataframe()
    
    sql = Postgresql(config)
    
    sql.execute_command("DROP TABLE IF EXISTS video_data") # Drop table to assure it creates it in the next step
    print("\nTable doesn't exists...")
    sql.query_table("SELECT * FROM video_data")
    
    create_table = """CREATE TABLE IF NOT EXISTS video_data (
       clip_name TEXT,
       clip_file_extension VARCHAR(3),
       clip_duration INT,
       clip_location TEXT,
       insert_timestamp TIMESTAMP
    );

    """
    sql.execute_command(create_table) # Create empty table
    print("\nTable exists but it's empty...")
    print(sql.query_table("SELECT * FROM video_data"))
    
    sql.upload_table(df, "video_data") # Upload dataframe to table
    print("\nTable with data...")
    print(sql.query_table("SELECT * FROM video_data"))
    
    save_report(path, df) # Save the dataframe to the report csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_folder")
    parser.add_argument("--url", default=None)

    args = parser.parse_args()
    
    target_folder = args.target_folder
    url = args.url

    main(target_folder, url)