import os
import subprocess
import glob
from colorama import Fore, Back, Style, init


def main():
    init()
    # Search All Video in Input Path
    path_to_videos = 'Input'  # Path Directory
    path_out_to_videos = 'Output'  # Path Directory
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov']
    search_pattern = f"{path_to_videos}/*[{'|'.join(video_extensions)}]"
    video_files = glob.glob(search_pattern)  # All Files Name

    if not video_files:  # If there is no video available
        print(Fore.RED + "The input folder cannot be empty!" + Style.RESET_ALL)
        exit()

    user_text = input("Your Phone Number (list.txt): " + Fore.GREEN)

    user_time = int(input(Style.RESET_ALL + "Time to change the text (Just Number/Second) : " + Fore.GREEN))
    user_time = user_time if user_time != 0 else 60  # 60 Second

    user_opacity = float(input(Style.RESET_ALL + "Please Enter Opacity (Between 0.0 to 1.0) : " + Fore.GREEN))
    user_opacity = user_opacity if (1.0 >= user_opacity > 0) else 0.5

    user_size = int(input(Style.RESET_ALL + "Please Enter Font Size (Default 24) : " + Fore.GREEN))
    user_size = user_size if (60 >= user_size >= 6) else 16

    user_color = input(Style.RESET_ALL + "Please Enter Text Color (hex => #ff0000) : " + Fore.GREEN)
    user_bg_color = input(Style.RESET_ALL + "Please Enter Background Color (hex => #ff0000) : " + Fore.GREEN)
    print(Style.RESET_ALL)

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
                "-vf",
                f"drawtext=text='{line}':fontsize={user_size}:fontcolor={user_color}@{user_opacity}:fontfile=Fonts"
                f"/IRANSans.ttf"
                f":x=if(eq(mod(t\,{user_time})\,0)\,rand(0\,(w-text_w))\,x):y=if(eq(mod(t\,{user_time})\,"
                f"0)\,rand(0\,(h-text_h))\,y):box=1:boxcolor={user_bg_color}@{user_opacity}:boxborderw=10",
                "-c:a", "copy",
                video.replace(path_to_videos, (path_out_to_videos + f"\\{line}"))
            ]
            subprocess.run(ffmpeg_cmd)

    print("Finish")


if __name__ == "__main__":
    main()
