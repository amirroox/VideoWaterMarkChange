import os
import subprocess
import glob

# Search All Video in Input Path
path_to_videos = 'Input'  # Path Directory
path_out_to_videos = 'Output'  # Path Directory
video_extensions = ['.mp4', '.avi', '.mkv', '.mov']
search_pattern = f"{path_to_videos}/*[{'|'.join(video_extensions)}]"
video_files = glob.glob(search_pattern)  # All Files Name

if not video_files:
    print("\033[1;31;40m The input folder cannot be empty! \033[0;37;40m")
    exit()

user_text = input("Your Phone Number (list.txt): ")
user_time = int(input("Time to change the text (Just Number/Default 0) : "))
time_generate_sec = user_time if user_time != 0 else 60  # 60 Second

lines = []
if os.path.exists(user_text):
    with open(user_text, 'r') as file:
        for line in file:
            cleaned_line = line.strip()
            lines.append(cleaned_line)

else:
    lines.append('WaterMark')


for line in lines:
    if not os.path.exists(f"{path_out_to_videos}/{line}"):
        os.mkdir(f"{path_out_to_videos}/{line}")

    for video in video_files:
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", video,
            "-vf", f"drawtext=text='{line}':fontsize=24:fontcolor=white@0.3:fontfile=Fonts/IRANSans.ttf"
                   f":x=if(eq(mod(t\,{time_generate_sec})\,0)\,rand(0\,(w-text_w))\,x):y=if(eq(mod(t\,{time_generate_sec})\,"
                   f"0)\,rand(0\,"
                   f"(h-text_h))\,y):box=1:boxcolor=black@0.3:boxborderw=10",
            "-c:a", "copy",
            video.replace(path_to_videos, (path_out_to_videos + f"\\{line}"))
        ]
        subprocess.run(ffmpeg_cmd)

print("\033[1;32;40m Finish \033[0;37;40m")
