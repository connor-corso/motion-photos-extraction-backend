
from ffmpeg import Progress, FFmpeg
import os


def transcode_video2(filepath):
    curr_dir = os.getcwd() + "/"
    outputfilepath = str(curr_dir+"converted" + str(filepath))
    print(curr_dir)
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(filepath)
        .output(
            "converted" + filepath,
            {"codec:v": "libx264"},
            vf="format: yuv420p",
            preset="veryslow",
            crf=18,
        )
    )
    print("hello")
    ffmpeg.execute()
    
def transcode_video(f):
    print("start")
    os.system("ffmpeg -y -i TESTING.mp4  -c:v libx264 -crf 18 -vf format=yuv420p -c:a copy out.mp4")
    print("hi")

transcode_video("TESTING.mp4")