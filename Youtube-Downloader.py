import tkinter
import customtkinter
from pytubefix import YouTube
import ffmpeg
import os


def get_downloadFolder():
    home = os.path.expanduser("~")
    return os.path.join(home, "Downloads")

#Trim video when needed
def trim (in_file, out_file, start, end):
    dir = get_downloadFolder()
    # changing to directory where file will be stored
    os.chdir(dir)
    

    file = ffmpeg.input(in_file)

    
    pts = "PTS-STARTPTS"
    video = file.trim(start= start, end=end).setpts(pts)

    audio = (file.filter_("atrim", start = start, end = end).filter_("asetpts", pts))
    
    final = ffmpeg.concat(video, audio, v=1,a=1)
    output = ffmpeg.output(final, out_file)
    
    output.run()


# Download Function
def startDownload(): 
    try:
        dir = get_downloadFolder()
        start = startTime.get()
        end = endTime.get()
        dwn = dwnTitle.get() 

        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)

        if ( dwn != ""):
            var = dwn
        else:
            var = ytObject.title

        

        video = ytObject.streams.get_highest_resolution()

        title.configure(text=ytObject.title, text_color="white")
        finishLabel.configure(text="")
       

        video.download(output_path=(dir), filename=var + '.mp4', max_retries=0)

        

        finishLabel.configure(text = "Downloaded!", text_color ="green")

        if (start !="" and end != ""):
            trim(in_file= var +'.mp4', out_file= var + "trim.mp4", start=start, end = end)
    except Exception as e: 
        finishLabel.configure(text=e, text_color = "red")
        
    
 
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size *100
    per = str(int(percentage_of_completion))
    pPercentage.configure(text=per + '%')
    pPercentage.update()

    #Update Progress Bar
    progressBar.set(float(percentage_of_completion/100))
    

# System Settings
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# App frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Youtube Downloader")


#Entry for Specific time frame Start and End buttons
startTitle = customtkinter.CTkLabel(app, text = "Start Time")
startTitle.place(x = 195, y = 110)
start= tkinter.StringVar()
startTime = customtkinter.CTkEntry(app, width= 100, height = 20, textvariable= start)
startTime.place(x = 175, y = 135)

EndTitle = customtkinter.CTkLabel(app, text= "End Time")
EndTitle.place(x= 455, y= 110)
end = tkinter.StringVar()
endTime = customtkinter.CTkEntry(app, width = 100, height = 20, textvariable= end)
endTime.place(x = 430, y = 135)

# UI elements
title = customtkinter.CTkLabel(app, text="Insert Youtube Link")
title.pack(padx = 10, pady = 10)

#Title input
dwn = tkinter.StringVar()
dwnTitle = customtkinter.CTkEntry(app, width= 400, height = 40, textvariable=dwn)
dwnTitle.place(x = 165, y = 350)

newTitle = customtkinter.CTkLabel(app, text= "Name File")
newTitle.place(x= 325, y =300 )

#link input
url = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width = 400, height = 40, textvariable=url)
link.pack(pady = 20)

#Finished Downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()


# Progress Percentage

pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

progressBar= customtkinter.CTkProgressBar(app, width =400)
progressBar.set(0)
progressBar.pack(padx= 10, pady=10)


# Download button   
Download = customtkinter.CTkButton(app, text="Download", command=startDownload)
Download.pack(padx = 10, pady = 10)


# run  app
app.mainloop()
