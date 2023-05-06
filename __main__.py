import vlc
import time
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps, ImageDraw
import os
import requests
from modules.Gradian import GradientFrame
from modules.Constants import Constants
from urllib.request import urlopen
import json
os.add_dll_directory(os.getcwd())


class Music:
    def __init__(self, id, name, image_path):
        self.id = id
        self.name = name
        self.image_path = image_path


class GUI(tk.Frame):
    file_image_selected = None
    file_mp3_selected = None
    input_name_music = ""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.configure(background='#192533')
        self.master.title("Radio app")
        self.master.geometry("800x600")

        # event Play mp3

        def handle_play_mp3(path):
            url = "http://localhost:5000/play-music/" + str(path)
            media_player = Constants.media_player
            media = vlc.Media(url)
            media_player.set_media(media)
            media_player.play()
            duration = media_player.get_length() / 1000
            while (duration > 0):
                duration = duration - 1

        # event Previous music
        def handle_prev():
            if (Constants.index_select > 0 and Constants.index_select < len(Constants.list_music)):
                self.seekbar['value'] = 0
                self.listbox.select_clear(Constants.index_select)
                Constants.index_select = Constants.index_select - 1
                Constants.music_selected = Constants.list_music[Constants.index_select]
                handle_play_mp3(Constants.music_selected['path'])
                self.listbox.select_set(Constants.index_select)
                if (Constants.music_selected['image'] == ""):
                    img = ImageTk.PhotoImage(Image.open(
                        r"output.png"))
                    lbImage.configure(image=img)
                    lbImage.image = img
                else:
                    URL = "http://127.0.0.1:5000/photo/" + \
                        str(Constants.music_selected['image'])
                    u = urlopen(URL)
                    raw_data = u.read()
                    u.close()
                    img = ImageTk.PhotoImage(data=raw_data)
                lbImage.configure(image=img)
                lbImage.image = img
                lb_music_name.configure(text=Constants.music_selected['name'])
                lb_music_name.pack()

        # event Pause/continue music
        def handle_paused():
            if (Constants.index_select >= 0 and Constants.index_select < len(Constants.list_music)):
                media_player = Constants.media_player
                # No play
                if (Constants.isPlay == False):
                    imgPrev = ImageTk.PhotoImage(Image.open(
                        r"assets\\pause.png"))
                    media_player.play()
                    Constants.isPlay = True
                # Playing
                else:
                    imgPrev = ImageTk.PhotoImage(Image.open(
                        r"assets\\play.png"))
                    media_player.pause()
                    Constants.isPlay = False
                btnPaused.configure(image=imgPrev)
                btnPaused.image = imgPrev

        # event next music
        def handle_next():
            if (Constants.index_select < len(Constants.list_music) - 1 and Constants.index_select > -1):
                self.seekbar['value'] = 0
                self.listbox.select_clear(Constants.index_select)
                Constants.index_select = Constants.index_select + 1
                Constants.music_selected = Constants.list_music[Constants.index_select]
                handle_play_mp3(Constants.music_selected['path'])
                self.listbox.select_set(Constants.index_select)
                if (Constants.music_selected['image'] == ""):
                    img = ImageTk.PhotoImage(Image.open(
                        r"output.png"))
                    lbImage.configure(image=img)
                    lbImage.image = img
                else:
                    URL = "http://127.0.0.1:5000/photo/" + \
                        str(Constants.music_selected['image'])
                    u = urlopen(URL)
                    raw_data = u.read()
                    u.close()
                    img = ImageTk.PhotoImage(data=raw_data)
                lbImage.configure(image=img)
                lbImage.image = img
                lb_music_name.configure(text=Constants.music_selected['name'])
                lb_music_name.pack()
            elif (Constants.index_select == len(Constants.list_music) - 1):
                self.seekbar['value'] = 0
                self.listbox.select_clear(Constants.index_select)
                Constants.index_select = 0
                Constants.music_selected = Constants.list_music[Constants.index_select]
                handle_play_mp3(Constants.music_selected['path'])
                self.listbox.select_set(Constants.index_select)
                if (Constants.music_selected['image'] == ""):
                    img = ImageTk.PhotoImage(Image.open(
                        r"output.png"))
                    lbImage.configure(image=img)
                    lbImage.image = img
                else:
                    URL = "http://127.0.0.1:5000/photo/" + \
                        str(Constants.music_selected['image'])
                    u = urlopen(URL)
                    raw_data = u.read()
                    u.close()
                    img = ImageTk.PhotoImage(data=raw_data)
                lbImage.configure(image=img)
                lbImage.image = img
                lb_music_name.configure(text=Constants.music_selected['name'])
                lb_music_name.pack()

        def handle_search():
            Constants.list_music.append({"id": 1, "name": "Hôm nay tôi buồn",
                                         "image": "image", "path": "1682931939.569541.mp3"})
            self.listbox.insert(END, "Hôm nay tôi buồn")

        # event Play mp3
        def onselect(evt):
            self.seekbar['value'] = 0
            imgPrev = ImageTk.PhotoImage(Image.open(
                r"assets\\pause.png"))
            btnPaused.configure(image=imgPrev)
            btnPaused.image = imgPrev
            # Lấy index của dòng được chọn
            index = self.listbox.curselection()[0]
            # Lấy tên bài hát từ đối tượng Music tương ứng
            selected_music = Constants.list_music[index]
            (id, image, name,
             path) = selected_music['id'], selected_music['image'], selected_music['name'], selected_music['path']
            Constants.index_select = index
            Constants.music_selected = selected_music
            lb_music_name.configure(text=name)
            lb_music_name.pack()
            if (Constants.solve != None):
                self.seekbar1.after_cancel(Constants.solve)
            if (image == ""):
                img = ImageTk.PhotoImage(Image.open(
                    r"output.png"))
                lbImage.configure(image=img)
                lbImage.image = img
            else:
                URL = "http://127.0.0.1:5000/photo/" + str(image)
                u = urlopen(URL)
                raw_data = u.read()
                u.close()
                img = ImageTk.PhotoImage(data=raw_data)
                lbImage.configure(image=img)
                lbImage.image = img
            handle_play_mp3(str(path))
            play_time()

        def upload_image():
            # [("pnj file", "*.pnj"), ("jpg file", "*.jpg")]
            f_types = [('Jpg Files', '*.jpg')]
            self.file_image_selected = filedialog.askopenfilename(
                initialdir=r'C:\\Downloads', filetypes=f_types)

        # event choose file mp3
        def upload_mp3():
            f_types = [('Jpg Files', '*.jpg')]
            self.file_mp3_selected = filedialog.askopenfilename(
                initialdir=r'C:\\Downloads')
            # dir = filedialog.askopenfilename(
            #     initialdir="/", title="chon file", filetypes=(("mp3 file", "*.mp3"), ("all file", "*.*")))

        def upload_data_to_server():
            files = {}
            if self.file_mp3_selected and self.name_entry.get():
                payload = {'name': self.name_entry.get().strip()}
                files = {
                    'data': (None, json.dumps(payload), 'application/json'),
                    'file': open(self.file_mp3_selected, 'rb'),
                }
                if self.file_image_selected:
                    files['image'] = open(self.file_image_selected, 'rb')
            else:
                tk.messagebox.showerror(
                    "Error", "Please enter fill input NAME and FILE MP3 !!!")
            # headers = {'Content-Type': 'multipart/form-data'}
            res = requests.post('http://127.0.0.1:5000/uploads',
                                files=files)
            if (res.status_code == 200):
                Constants.list_music.insert(
                    len(Constants.list_music), res.json())
                self.listbox.insert(END, res.json()['name'])
                self.add_song_win.destroy()
            else:
                tk.messagebox.showerror(
                    "Error", "Oh No ! What Wrong From Server !!!")

        # event upload mp3
        def handle_add_music():
            self.add_song_win = tk.Toplevel()
            # self.add_song_win.attributes('-topmost', True)
            self.add_song_win.geometry("300x130")
            self.add_song_win.title("Add Music")
            lb_name = tk.Label(self.add_song_win, text="Song Name")
            self.name_entry = tk.Entry(self.add_song_win)

            lb_mp3file = tk.Label(self.add_song_win, text="File mp3")
            mp3file_entry = tk.Entry(self.add_song_win)
            mp3file_entry.insert(0, "Please choose file mp3 !!!")
            bt_select_file = tk.Button(
                self.add_song_win, text="Select", command=upload_mp3)
            mp3file_entry.delete(0)
            mp3file_entry.insert(0, dir)

            lb_image = tk.Label(self.add_song_win, text="Image")
            image_entry = tk.Entry(self.add_song_win)
            image_entry.insert(0, "Please choose file image !!!")
            bt_select_image = tk.Button(
                self.add_song_win, text="Select", command=upload_image)
            image_entry.delete(0)
            image_entry.insert(0, dir)
            btn_them = tk.Button(self.add_song_win, text="Upload",
                                 command=upload_data_to_server)
            btn_huy = tk.Button(self.add_song_win, text="Cancel",
                                command=self.add_song_win.destroy)

            lb_name.grid(row=0, column=0)
            self.name_entry.grid(row=0, column=1)

            lb_mp3file.grid(row=1, column=0)
            mp3file_entry.grid(row=1, column=1)
            bt_select_file.grid(row=1, column=2)

            lb_image.grid(row=2, column=0)
            image_entry.grid(row=2, column=1)
            bt_select_image.grid(row=2, column=2)

            btn_huy.grid(row=3, column=1, pady=20)
            btn_them.grid(row=3, column=2)
            # self.input_name_music = name_entry.get()

        # event delete mp3
        def handle_delete_music():
            index = len(self.listbox.curselection())
            if (index != 0):
                # Lấy index của dòng được chọn
                index = self.listbox.curselection()[0]
                # Lấy tên bài hát từ đối tượng Music tương ứng
                selected_music = Constants.list_music[index]
                (id, image, name,
                 path) = selected_music['id'], selected_music['image'], selected_music['name'], selected_music['path']
                requests.get("http://127.0.0.1:5000/delete-music/"+str(id))
                self.listbox.delete(index)
                Constants.list_music.pop(index)
                Constants.index_select = -1
                Constants.isPlay = False
                Constants.music_selected = {}
                Constants.media_player.stop()
                img = ImageTk.PhotoImage(Image.open(
                    r"output.png"))
                lbImage.configure(image=img)
                lbImage.image = img
                lb_music_name.pack_forget()
                imgPause = ImageTk.PhotoImage(Image.open(
                    r"assets\\play.png"))
                btnPaused.configure(image=imgPause)
                btnPaused.image = imgPause

        # event scroll seekbar when play mp3
        def play_time():
            media_player = Constants.media_player
            if (media_player.is_playing() == 1):
                Constants.isPlay = True
                current_time = int(media_player.get_length() / 1000)
                current_length = float(media_player.get_length() / 1000)
                convert_current_time = time.strftime(
                    '%H:%M:%S', time.gmtime(float(media_player.get_time() / 1000)))
                convert_current_length = time.strftime(
                    '%H:%M:%S', time.gmtime(current_length))
                self.seekbar1.config(
                    text=str(convert_current_time) + "/" + str(convert_current_length))

                self.seekbar['value'] += float(100/current_time)
            Constants.solve = self.seekbar1.after(1000, play_time)

        # event click seekbar
        def on_seekbar_click(event):
            self.seekbar['value'] = event.x / 3
            # get position on seekbar tool
            position = self.seekbar.get()
            media_player = Constants.media_player
            time = ((media_player.get_length() / 1000) / 100) * position
            media_player.set_time(int(time * 1000))

        # Frame left (Play mp3)
        self.frameL = GradientFrame(self.master, width=500,
                                    height=600, borderwidth=1, relief="sunken")
        self.frameL.pack(side="left", fill="y")

        # Frame Right (List mp3)
        self.frameR = GradientFrame(self.master, width=300,
                                    height=600,
                                    borderwidth=1, relief="sunken")
        self.frameR.pack(side="right", fill="both", expand=True)

        # Label image music (Left)
        img = ImageTk.PhotoImage(Image.open(
            r"output.png"))
        lbImage = tk.Label(self.frameL, image=img,
                           width=300, height=300, bg='#192533')
        lbImage.image = img
        lbImage.pack(padx=50, pady=50, side="top")

        # Label name music (Left)
        lb_music_name = tk.Label(self.frameL)

        # Label show time music (Left)
        self.seekbar1 = tk.Label(self.frameL, text='', relief=GROOVE, anchor=E)
        self.seekbar1.pack(fill=X, side=BOTTOM, ipady=2)

        def slide(x):
            pass

        # Seekbar (Left)
        self.seekbar = ttk.Scale(
            self.frameL, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=300)
        self.seekbar.pack()
        self.seekbar.bind('<Button-1>', on_seekbar_click)

        # btn previous, pause, next... (Left)
        imgPrev = ImageTk.PhotoImage(Image.open(
            r"assets\\back-arrow.png"))
        btnPrev = tk.Button(self.frameL, image=imgPrev,
                            width=35, height=35, border=0, command=handle_prev)
        btnPrev.image = imgPrev
        btnPrev.place(x=90, y=480, width=35, height=35)

        imgPaused = ImageTk.PhotoImage(Image.open(
            r"assets\\play.png"))
        btnPaused = tk.Button(
            self.frameL, image=imgPaused, width=35, height=35, command=handle_paused)
        btnPaused.image = imgPaused
        btnPaused.place(x=185, y=480, width=35, height=35)

        imgNext = ImageTk.PhotoImage(Image.open(
            r"assets\\next.png"))
        btnNext = tk.Button(self.frameL, image=imgNext,
                            width=35, height=35, command=handle_next)
        btnNext.image = imgNext
        btnNext.place(x=280, y=480, width=35, height=35)

        # List music (Right)
        self.listbox = tk.Listbox(self.frameR, width=50, height=25)
        self.listbox.grid(row=0, column=0, columnspan=3, padx=40, pady=50)
        res = requests.get(
            "http://127.0.0.1:5000/get-all-music")
        if (str(res.content).find("Empty", 0, len(str(res.content))) == -1):
            Constants.list_music = res.json()

        for music in Constants.list_music:
            self.listbox.insert(END, music['name'])
        self.listbox.bind('<<ListboxSelect>>', onselect)

        self.btnDelete = tk.Button(
            self.frameR, text="Delete Music", width=10, height=2, command=handle_delete_music)
        self.btnDelete.grid(row=1, column=1)
        self.btnAdd = tk.Button(self.frameR, text="Add Music",
                                width=10, height=2, command=handle_add_music)
        self.btnAdd.grid(row=1, column=2)


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    # root.wm_attributes('-topmost', True)
    # root.wm_attributes('-transparentcolor', '#192533')
    gui.mainloop()
