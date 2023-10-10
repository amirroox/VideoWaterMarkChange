import os
import subprocess
import glob
import time
import shutil

from colorama import Fore, Back, Style, init


path_to_videos = 'Input'  # Path Directory
path_out_to_videos = 'Output'  # Path Directory
video_extensions = ['.mp4', '.avi', '.mkv', '.mov']  # Videos Extensions Allowed


def main():
    init()
    # Search All Video in Input Path
    search_pattern = f"{path_to_videos}/*[{'|'.join(video_extensions)}]"
    video_files = glob.glob(search_pattern)  # All Files Name

    subdirectories = [subdir for subdir in os.listdir(path_to_videos) if os.path.isdir(os.path.join(path_to_videos, subdir))]  # Sub Directories

    if not subdirectories and not video_files:  # If there is no video available
        print(Fore.RED + "The input folder cannot be empty!" + Style.RESET_ALL)
        exit()

    # noinspection PyBroadException
    try:
        user_text = input("Your Phone Number (list.txt): " + Fore.GREEN)  # WaterMark Lists (Phone Numbers)
        user_text = 'list.txt' if user_text == '' else user_text

        user_time = input(Style.RESET_ALL + "Time to change the text (Just Number/Second - Default 60 Second) : " + Fore.GREEN)
        user_time = 60 if user_time == '' else int(user_time)
        user_time = user_time if user_time != 0 else 60  # 60 Second

        user_opacity = input(Style.RESET_ALL + "Please Enter Opacity (Between 0.0 to 1.0 - Default 0.2) : " + Fore.GREEN)
        user_opacity = 0.2 if user_opacity == '' else float(user_opacity)
        user_opacity = user_opacity if (1.0 >= user_opacity > 0) else 0.5

        user_size = input(Style.RESET_ALL + "Please Enter Font Size (Default 22) : " + Fore.GREEN)
        user_size = 22 if user_size == '' else int(user_size)
        user_size = user_size if (80 >= user_size >= 6) else 16

        user_color = input(Style.RESET_ALL + "Please Enter Text Color (hex => #ffffff Or color => white - default white) : " + Fore.GREEN)
        user_color = 'white' if user_color == '' else user_color
        user_bg_color = input(Style.RESET_ALL + "Please Enter Background Color (hex => #000000 or color => black - default black) : " + Fore.GREEN)
        user_bg_color = 'black' if user_bg_color == '' else user_bg_color
        print(Style.RESET_ALL)
    except:
        print('')
        print(Back.BLACK + Fore.RED + 'Be sure to pay attention to the type of value you enter' + Style.RESET_ALL)
        exit()

    lines = []

    if os.path.exists(user_text):  # Check Existed Text User (UserFile => list.txt)
        with open(user_text, 'r') as file:
            for line in file:
                cleaned_line = line.strip()
                lines.append(cleaned_line)
    else:
        lines.append('WaterMark')

    if video_files:
        for line in lines:
            if not os.path.exists(f"{path_out_to_videos}/{line}"):
                os.mkdir(f"{path_out_to_videos}/{line}")

            loopWaterMark(video_files, line, user_size, user_color, user_opacity, user_time, user_bg_color)

    if subdirectories:
        for line in lines:
            if not os.path.exists(f"{path_out_to_videos}/{line}"):
                os.mkdir(f"{path_out_to_videos}/{line}")

            for subdir in subdirectories:
                input_subdir = os.path.join(path_to_videos, subdir)
                output_subdir = os.path.join(f"{path_out_to_videos}/{line}", subdir)

                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)

                video_files = glob.glob(os.path.join(input_subdir, f"*[{'|'.join(video_extensions)}]"))

                if not video_files:
                    print(Fore.RED + f"No video files found in {input_subdir}" + Style.RESET_ALL)
                    continue

                loopWaterMark(video_files, line, user_size, user_color, user_opacity, user_time, user_bg_color)

                all_files = os.listdir(input_subdir)
                for file_name in all_files:
                    source_file_path = os.path.join(input_subdir, file_name)
                    destination_file_path = os.path.join(output_subdir, file_name)

                    file_extension = os.path.splitext(file_name)[1]

                    if file_extension not in video_extensions:
                        if os.path.isfile(source_file_path):
                            shutil.copy(source_file_path, destination_file_path)
                        elif os.path.isdir(source_file_path):
                            shutil.copytree(source_file_path, destination_file_path)

    print("Finish")


def loopWaterMark(videos_file, line, user_size, user_color, user_opacity, user_time, user_bg_color):
    for video in videos_file:
        # Changing the position of the text according to the user's second as animation
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", video,
            "-vf",
            f"drawtext=text='{line}':fontsize={user_size}:fontcolor={user_color}@{user_opacity}:fontfile=Fonts/IRANSans.ttf"
            f":x='if(eq(mod(t,{user_time}),0),rand(0,(w-text_w)),x')"
            f":y='if(eq(mod(t,{user_time}),0),rand(0,(h-text_h)),y)'"
            # f":x='if(gte(t,{user_time}), (w-text_w)-mod((t-{user_time})*15, (w-text_w)), (w-text_w)/2)'"
            # f":y='if(gte(t,{user_time}), (h-text_h)-mod((t-{user_time})*15, (h-text_h)), (h-text_h)/2)'"
            f":box=1:boxcolor={user_bg_color}@{user_opacity}:boxborderw=10",
            "-c:a", "copy",
            video.replace(path_to_videos, (path_out_to_videos + f"\\{line}"))
        ]
        subprocess.run(ffmpeg_cmd)
        print(" ")
        print(Fore.GREEN + f"{video} complete!" + Style.RESET_ALL)
        print(" ")
        time.sleep(2)


if __name__ == "__main__":
    main()
