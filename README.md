# Video Watermarking Script

This Python script allows you to add watermarks to videos with various customization options. It uses the FFmpeg tool to add text watermarks to video files.

## Features

- Adds customizable text watermarks to video files.
- Supports multiple video file formats, including .mp4, .avi, .mkv, and .mov.
- Allows customization of watermark text, font size, font color, opacity, and background color.
- Supports batch processing for videos located in subdirectories.

## Usage

1. Place your video files in the `Input` directory.
2. Run the script.
3. Follow the prompts to customize your watermark settings:
   - Enter the text for the watermark (default: "WaterMark").
   - Set the time interval for changing the watermark text (in seconds, default: 60 seconds).
   - Specify the font size (default: 24).
   - Choose the font color (hex or color name, e.g., #ff0000 or red).
   - Choose the background color (hex or color name, e.g., #000000 or black).
4. The script will process your videos, adding the watermark based on your settings, and save the watermarked videos in the `Output` directory.

## Example

Suppose you have a directory structure like this:

Input
└── S1
    ├── video1.mp4
    ├── video2.avi
    └── ...


