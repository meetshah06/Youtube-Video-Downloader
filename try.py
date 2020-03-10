from pytube import *
# import ffmpeg
import subprocess

def save():
    path = ''
    video_stream = './Videos/video.mp4'
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    audio_stream = './Audios/audio.mp4'
    print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbb")

    # ffmpeg.concat(video_stream, audio_stream, v=1, a=1).output('./Final/finished_video.mp4').run()
    cmd = f'ffmpeg -i {video_stream} -i {audio_stream} -c copy output.mp4'
    print('ccccccccccccccccccccccccccccccc')
    subprocess.run(cmd)

url = 'https://www.youtube.com/watch?v=nCkpzqqog4k'
# path_to_save_video = "C:\\Users\\Meet\\Desktop\\New folder (2)\\YouDown\\Videos"
# path_to_save_audio = "C:\\Users\\Meet\\Desktop\\New folder (2)\\YouDown\\Audios"
ob = YouTube(url)
streams = ob.streams.all()
for s in streams:
    print(s)

# Get the stream which has both audio and video
# strm = ob.streams.filter(progressive=True).first()
# strmvid = ob.streams.filter(res='720p').first()
# print(strmvid)
# print(strmvid.filesize, strmvid.title)
# strmvid.download(path_to_save_video, filename='video')
# print('Video Done')

# print("Audio")
# strmaud = ob.streams.get_audio_only()
# print(strmaud)
# print(strmaud.filesize, strmaud.title)
# strmaud.download(path_to_save_audio, filename='audio')
# print('Audio Done')

# name = strmvid.title

# save()