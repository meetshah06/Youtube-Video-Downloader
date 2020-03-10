from pytube import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from PIL import Image, ImageTk
from threading import *
import subprocess
import os

file_size = 0
path_to_save_video = "./Videos"
path_to_save_audio = "./Audios"


# For updating percentage that is downloaded
def progress(stream=None, chunk=None, remaining=None):
    # Get the percentage of the file that has been downloaded
    # print(stream, chunk)
    file_downloaded = (file_size - remaining)
    percentage = (file_downloaded / file_size) * 100
    downloadButton.config(text= "{:00.0f} % downloaded".format(percentage))

# Parameters: Youtube object, resolution
def getStream(ob, res, url):
    print("In try")
    name = ob.title
    # streams = ob.streams.all()
    # for s in streams:
    #     print(s)
    strm = ob.streams.filter(progressive=True, res=res)
    if len(strm) != 0:
        return strm.first(), False

    else:
        # Create new object to download the audio
        obj = YouTube(url)
        strmaud = obj.streams.get_audio_only()
        print(strmaud)
        print(strmaud.filesize, strmaud.title)
        print(path_to_save_audio)
        strmaud.download(path_to_save_audio, filename='audio')
        print('Audio Done..')

        strm = ob.streams.filter(res=res)
        # Check if video of specified resolution exists
        if len(strm) != 0:
            return strm.first(), True
        else:
            return ob.streams.filter(progressive=True).first(), False

def merge_audio_and_video(name, path):
    video_stream = './Videos/video.mp4'
    print(video_stream)
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    audio_stream = './Audios/audio.mp4'
    print(audio_stream)
    print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
    output_stream = path + '/' + name + '.mp4'
    print(output_stream)
    # ffmpeg.concat(video_stream, audio_stream, v=1, a=1).output('./Final/finished_video.mp4').run()
    cmd = f'ffmpeg -i {video_stream} -i {audio_stream} -c copy output.mp4'
    print('ccccccccccccccccccccccccccccccc')
    subprocess.run(cmd)
    print("Successfully Merged")
    os.rename('output.mp4', output_stream)
    os.remove('./Audios/audio.mp4')
    os.remove('./Videos/video.mp4')

def startDownload():
    global file_size
    try:
        # Get the url which has been written
        url = urlField.get()
        print(url)
        # Get the resolution selected
        res = str(var.get()) + 'p'
        print("Resolution =", res)

        # Changing Button Text
        downloadButton.config(text='Please Wait...')
        downloadButton.config(state=DISABLED)
        # path_to_save = "C:\\Users\\Meet\\Desktop\\New folder (2)\\YouDown\\Videos"
        # Get the folder selected
        path_to_save = askdirectory()
        print(path_to_save)

        if path_to_save is None:
            return

        # Create youtube object with url
        ob = YouTube(url, on_progress_callback=progress)

        # streams = ob.streams.all()
        # for s in streams:
        #     print(s)

        strm, merge = getStream(ob, res, url)

        # Get the stream which has both audio and video
        # strm = ob.streams.filter(progressive=True).first()
        print(strm, merge)
        # Set file_size to the total size of the video
        file_size = strm.filesize
        # Display the title of the video
        videoTitle.config(text=strm.title)
        videoTitle.pack(side=TOP)
        print(strm.filesize, strm.title)
        # print(ob.description)
        # Download the video to the specified path
        if merge:
            strm.download(path_to_save_video, filename='video')
            merge_audio_and_video(strm.title, path_to_save)

        else:
            strm.download(path_to_save)
    
        print('done..')
        
        # Reset the configuration
        downloadButton.config(text='Start Download', state=NORMAL)
        showinfo("Download Finished", "Downloaded Successfuly")
        # Clear the previous URL
        urlField.delete(0, END)
        # Clear the title
        videoTitle.pack_forget()

    except Exception as e:
        print(e)
        print("error")


# Create a separate thread to donwload the video so that the GUI may work on another thread
def startDownloadThread():
    # Create Thread
    thread = Thread(target=startDownload)
    thread.start()


# Starting GUI 
main = Tk()
# Set the title
main.title("Youtube Downloader")
# Set the icon
main.iconbitmap('./Image/youtube_icon.ico')
# Size of the window
main.geometry("500x700")

# Heading Icon

# PhotoImage class by default only accepts GIF or PGM/PPM images; hence use Pillow to convert
image = Image.open('./Image/youtube_icon.jpg')
photo = ImageTk.PhotoImage(image)
headingIcon = Label(main, image=photo)
headingIcon.pack(side=TOP)

# URL Text Field
urlField = Entry(main, font=('comicsans', 18), justify=CENTER)
urlField.pack(side=TOP, fill=X, padx=10, pady=10)

# Resolution Radio Button
var = IntVar()
radio_360 = Radiobutton(main, text='360p', variable=var, value=360, font=('comicsans', 18))
radio_480 = Radiobutton(main, text='480p', variable=var, value=480, font=('comicsans', 18))
radio_720 = Radiobutton(main, text='720p', variable=var, value=720, font=('comicsans', 18))
radio_1080 = Radiobutton(main, text='1080p', variable=var, value=1080, font=('comicsans', 18))
radio_360.select()
radio_360.pack(side=TOP)
radio_480.pack(side=TOP)
radio_720.pack(side=TOP)
radio_1080.pack(side=TOP)

# Download Button on click will execute the startDownloadThread function
downloadButton = Button(main, text="Start Download", font=('comicsans', 18), relief='ridge', command=startDownloadThread)
downloadButton.pack(side=TOP, pady=10)

# Video Title
videoTitle = Label(main, text="Video Title")
# videoTitle.pack(side=TOP)
main.mainloop()

# startDownload('https://www.youtube.com/watch?v=RBumgq5yVrA')