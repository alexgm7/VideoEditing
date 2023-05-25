import os
import math
import moviepy
import datetime
import pandas as pd

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip

from utils import unzip_file, create_folder, normal_round

class VideoProcessing():
    """
    A class used to handle the video processing functions
    """
    
    def __init__(self, clip_duration = 60):
        self.clip_duration = clip_duration
        self.data = []
        
    # Setter for attribute clip_duration
    @property
    def clip_duration(self):
        return self._clip_duration
    
    @clip_duration.setter
    def clip_duration(self, value):
        self._clip_duration = value
    
    def process_video_files(self, path):
        """
        Iterates over the files in given path and creates the subclips
        """
        
        files = [os.path.join(path, file) for file in os.listdir(path)]
        for file in files:
            if file.endswith(".zip"):
                subfolder = unzip_file(file)
                self.process_video_files(subfolder)
            elif file.endswith(".mp4"):
                self.create_subclips(file, path)

    def create_subclips(self, file, local_path = ""):
        """
        Creates the subclips from the main video and saves the metadata
        """
        
        video = VideoFileClip(file)
        duration = video.duration
        fps = video.fps
        total_clips = math.ceil(duration / self.clip_duration)
        print(f"Duration: {duration // 60} min, {round(duration % 60, 3)} sec, Total of clips: {total_clips}")
        create_folder(os.path.join(local_path, "video_clips"))
        start = 0
        for num in range(total_clips):
            if num == total_clips:
                end = start + (duration % self.clip_duration)
            else:
                end = start + self.clip_duration 
            frame = normal_round(start * fps) # Rounding of frames with given fps in main video
            name = f"{frame}thFrame.mp4"
            target_name = os.path.join(local_path, "video_clips", f"{frame}thFrame.mp4")
            print(f"orig: {target_name}")
            ffmpeg_extract_subclip(file, start, end, targetname = target_name)
            self.data.append({"name" : name[:-4], "extension" : name[-3:], "duration" : end - start, "loc" : target_name})
            start = end
            
    def create_dataframe(self):
        """
        Creates a dataframe with the metadata collected from the subclips
        """
        
        df = pd.json_normalize(self.data)
        df.rename({"name":"clip_name", 
                   "extension":"clip_file_extension", 
                   "duration":"clip_duration", 
                   "loc":"clip_location"}, axis=1, inplace=True)
        df["insert_timestamp"] = datetime.datetime.now()
        return df
