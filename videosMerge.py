from moviepy.editor import VideoFileClip, concatenate_videoclips
import glob
import os
import argparse
import os
from os.path import join
# from datetime import datetime

parser = argparse.ArgumentParser(description='Object Detection using YOLO in OPENCV')
parser.add_argument('--folder', help='Path to folder.')

fileTypes =('*.avi', '*.mp4','*.webm',"*.ts")
args = parser.parse_args()

files = []
if (args.folder):
    if os.path.exists(args.folder):    
        
        output_folder= join(args.folder, 'newtest')
        outfile  = 'outputVideo.mp4'
        output_file = join(output_folder, outfile)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        for ext in fileTypes:
            files.extend(glob.glob(join(args.folder, ext)))

print(output_file)
clips =[]
for file in files :
    print(file)
    clip_1 = VideoFileClip(file)
    clips.append(clip_1)
print("asdf")
print(clips)
final_clip = concatenate_videoclips(clips)
final_clip.write_videofile(output_file)