import os
import zipfile
import math

def create_folder(path):
    """
    Creates an empty folder in the local directory
    """
    
    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except Exception as e:
        print(f"Error while creating folder: {str(e)}")
        
def unzip_file(file):
    """
    Unzips a zipped file and puts it in a new folder called _content
    """
    
    content_loc = f"{file[:-4]}_content"
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(content_loc)
    return content_loc

def normal_round(n):
    """
    Rounds a number to the lowest integer if decimal is lower than 0.5
    and rounds it to the highest integer if decimal is higher than 0.5
    """
    
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)            
            
def save_report(path, df):
    """
    Saves a dataframe to a csv file inside a report folder
    """
    
    report_path = os.path.join(path, "report")
    create_folder(report_path)
    df.to_csv(os.path.join(report_path, "generated_video_files.csv"), index = False)