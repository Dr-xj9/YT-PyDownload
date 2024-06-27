import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import filedialog
from pytube import YouTube
from tkinter import PhotoImage
import os
# changed client from default ANDROID_MUSIC
from pytube.innertube import _default_clients
_default_clients["ANDROID_MUSIC"] = _default_clients["WEB"]

class Interfaz():
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("350x240")
        self.root.resizable(0,0)
        #icono = PhotoImage(file='archives\logo.png')
        #self.root.iconphoto(False, icono)
        
        self.outVar = tk.StringVar()
        Label(self.root, text="YouTube URL").pack(pady=(10, 5), padx=10)
        
        self.link = tk.StringVar()
        self.URL = Entry(self.root, width=50, textvariable=self.link)
        self.URL.pack(pady=(0,12), padx=15)
        
        Label(self.root, text="Format").pack(pady=(0,5), padx=10)
        self.Formato = tk.StringVar()
        FormatOptions = ttk.Combobox(self.root, textvariable=self.Formato, state="readonly")
        FormatOptions['values'] = ("Video", "Audio")
        FormatOptions.pack(padx=10, pady=(0,15))
        self.Formato.set("Video") # Default value
        
        self.barProgress = ttk.Progressbar(self.root, orient='horizontal',
                                        mode='indeterminate', length=350, maximum=100)
        self.barProgress.pack(padx=10, pady=(5,10))
        
        self.label = Label(self.root, text="")
        self.label.pack(pady=(0,5),padx=(10))
        
        self.downloadButton = Button(self.root, text="Download", command=self.downloadFile)
        self.downloadButton.pack(padx=10, pady=(0,15))
    
    def progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size *100
        
        self.barProgress['value'] = percentage_of_completion
        self.label.config(text=f"{percentage_of_completion:.2f}%")
        self.root.update_idletasks()
        print(percentage_of_completion)
        if percentage_of_completion >= 100.0:
            self.downloadButton.config(state="normal")
    
    def downloadFile(self):
        path = filedialog.askdirectory()
        if path is None:  # Verifica si se seleccionó una carpeta
           messagebox.showinfo("Default", "The default ouput is the same as the program")
            
        try:
            link = self.URL.get()
            yt = YouTube(link, on_progress_callback=self.progress)
            self.downloadButton.config(state="disabled")
            
            if self.Formato.get() == "Video":
                video = yt.streams.get_highest_resolution()
                video.download(output_path=path)
                
            elif self.Formato.get() == "Audio":
                stream = yt.streams.filter(only_audio=True)
                audio = stream.get_by_itag(251)
                out_file = audio.download(output_path=path)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
            
            self.label.config(text="Downloaded!", fg='green')
        except Exception as e:
            print(f"Error : {e}")
            self.label.config(text=f"Download Error: {e}", fg='red')
            self.downloadButton.config(state="normal")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()