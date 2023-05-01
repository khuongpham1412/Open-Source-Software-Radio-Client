import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk, ImageOps, ImageDraw
from pydub import AudioSegment
from pydub.playback import play
import os
import requests
from modules.Gradian import GradientFrame
from urllib.request import urlopen
from io import BytesIO
from modules.Constants import Constants

import pygame
from mutagen.mp3 import MP3

os.add_dll_directory(os.getcwd())


class Music:
    def __init__(self, id, name, image_path):
        self.id = id
        self.name = name
        self.image_path = image_path


class GUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.configure(background='#192533')
        self.master.title("Radio app")
        self.master.geometry("800x600")

        def handle_play_mp3(path):
            pygame.init()
            pygame.mixer.init()

            url = "http://localhost:5000/play-music/" + str(path)

            response = requests.get(url)
            file = response.content

            # with open("temp.mp3", "wb") as f:
            #     f.write(file)

            # pygame.mixer.music.load("temp.mp3")
            pygame.mixer.music.play()
            print("hello")
            while pygame.mixer.music.get_busy():
                continue

            pygame.mixer.music.stop()
            pygame.quit()

        def handle_prev():
            if (Constants.index_select > 0 and Constants.index_select < len(Constants.list_music)):
                Constants.index_select = Constants.index_select - 1
                Constants.music_selected = Constants.list_music[Constants.index_select]
                # handle_play_mp3(Constants.music_selected['path'])

        def handle_paused():
            if (Constants.index_select >= 0 and Constants.index_select < len(Constants.list_music)):
                if (Constants.isPlay == False):
                    imgPrev = ImageTk.PhotoImage(Image.open(
                        r"D:\\SGU\\Opensource_Software\\radio-client\\assets\\pause.png"))
                    Constants.isPlay = True
                else:
                    imgPrev = ImageTk.PhotoImage(Image.open(
                        r"D:\\SGU\\Opensource_Software\\radio-client\\assets\\play.png"))
                    Constants.isPlay = False
                btnPaused.configure(image=imgPrev)
                btnPaused.image = imgPrev
                # pygame.mixer.music.pause()

        def handle_next():
            if (Constants.index_select < len(Constants.list_music) - 1 and Constants.index_select > -1):
                Constants.index_select = Constants.index_select + 1
                Constants.music_selected = Constants.list_music[Constants.index_select]
                # handle_play_mp3(Constants.music_selected['path'])

        def handle_search():
            Constants.list_music.append({"id": 1, "name": "Hôm nay tôi buồn",
                                         "image": "image", "path": "1682931939.569541.mp3"})
            self.listbox.insert(END, "Hôm nay tôi buồn")

        def onselect(evt):
            imgPrev = ImageTk.PhotoImage(Image.open(
                r"D:\\SGU\\Opensource_Software\\radio-client\\assets\\pause.png"))
            Constants.isPlay = True
            btnPaused.configure(image=imgPrev)
            btnPaused.image = imgPrev
            # pygame.mixer.music.pause()
            # Lấy index của dòng được chọn
            index = self.listbox.curselection()[0]
            # Lấy tên bài hát từ đối tượng Music tương ứng
            selected_music = Constants.list_music[index]
            (id, image, name,
             path) = selected_music['id'], selected_music['image'], selected_music['name'], selected_music['path']
            Constants.index_select = index
            Constants.music_selected = selected_music

            # print(selected_music['path'])
            # Hiển thị tên bài hát lên Label
            # img = ImageTk.PhotoImage(Image.open(image))
            # lbImage.configure(image=img, bg='#192533')
            # lbImage.image = img

            # imgPrev = ImageTk.PhotoImage(Image.open(
            #     r"D:\\SGU\\Opensource_Software\\radio-client\\assets\\pause.png"))
            # btnPaused.configure(image=imgPrev)
            # btnPaused.image = imgPrev
            pygame.init()
            pygame.mixer.init()
            handle_play_mp3(str(path))

        def choose_image(add_song_win):
            mp3file = tk.filedialog.askopenfilename(
                initialdir="/", title="chon file", filetypes=[("pnj file", "*.pnj"), ("jpg file", "*.jpg")])
            print(type(mp3file))
            return mp3file

        def choose_file(root):
            dir = tk.filedialog.askopenfilename()
            # dir = filedialog.askopenfilename(
            #     initialdir="/", title="chon file", filetypes=(("mp3 file", "*.mp3"), ("all file", "*.*")))
            print("hello")
            # print(os.path.abspath(file_to_upload.filename))

            file = {'file': open(dir, 'rb')}
            data = {"name": "name test", "path": "path"}
            print(file)
            print("hello")
            # headers = {'Content-Type': 'multipart/form-data'}
            # r = requests.post("http://127.0.0.1:5000/uploads",
            #                   headers=headers, files=file)

            r = requests.post('http://127.0.0.1:5000/uploads',
                              files=file, json=data)
            print(r)
            return dir

        def handle_add_music():
            add_song_win = tk.Toplevel()
            # add_song_win.attributes('-topmost', True)
            add_song_win.geometry("300x100")
            add_song_win.title("Thêm bài hát")
            lb_name = tk.Label(add_song_win, text="Tên bài hát")
            name_entry = tk.Entry(add_song_win)
            lb_image = tk.Label(add_song_win, text="Ảnh")
            image_entry = tk.Entry(add_song_win)
            image_entry.insert(0, "Vui lòng chọn ảnh")
            bt_select_image = tk.Button(
                add_song_win, text="select", command=choose_image)
            image_entry.delete(0)
            image_entry.insert(0, dir)
            lb_mp3file = tk.Label(add_song_win, text="File nhạc")
            mp3file_entry = tk.Entry(add_song_win)
            mp3file_entry.insert(0, "Vui lòng chọn file nhạc")
            bt_select_file = tk.Button(
                add_song_win, text="select", command=choose_file)
            mp3file_entry.delete(0)
            mp3file_entry.insert(0, dir)
            print(dir)
            btn_them = tk.Button(add_song_win, text="Thêm", command="")
            btn_huy = tk.Button(add_song_win, text="Hủy",
                                command=add_song_win.destroy)

            lb_name.grid(row=0, column=0)
            name_entry.grid(row=0, column=1)
            lb_image.grid(row=1, column=0)
            image_entry.grid(row=1, column=1)
            bt_select_image.grid(row=1, column=3)
            lb_mp3file.grid(row=2, column=0)
            mp3file_entry.grid(row=2, column=1)
            bt_select_file.grid(row=2, column=3)
            btn_them.grid(row=3, column=0)
            btn_huy.grid(row=3, column=1)

        # Frame left
        self.frameL = GradientFrame(self.master, width=500,
                                    height=600, borderwidth=1, relief="sunken")
        self.frameL.pack(side="left", fill="y")

        # Frame Right
        self.frameR = GradientFrame(self.master, width=300,
                                    height=600,
                                    borderwidth=1, relief="sunken")
        self.frameR.pack(side="right", fill="both", expand=True)

        # Label on top of frame Left

        img = ImageTk.PhotoImage(Image.open(
            r"D:\\SGU\\Opensource_Software\\radio-client\\assets\\output.png"))

        lbImage = tk.Label(self.frameL, image=img,
                           width=300, height=300, bg='#192533')
        lbImage.image = img
        # url = "https://scontent.fsgn8-3.fna.fbcdn.net/v/t1.6435-9/110317078_108873884247194_8632694263271216467_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=CYkmKjjJ3K8AX8Z-gb1&_nc_ht=scontent.fsgn8-3.fna&oh=00_AfD_bZk2d07vAhFPpfwLsst7J0AXCpZnB8e56o2Qe_QHIA&oe=6476F918"
        # image_bytes = urlopen(url).read()

        # image = Image.open(BytesIO(image_bytes))
        # img_width, img_height = image.size

        # # Tính đường kính của hình tròn
        # diameter = min(img_width, img_height)

        # # Tạo mask hình tròn
        # mask = Image.new('L', (diameter, diameter), 0)
        # draw = ImageDraw.Draw(mask)
        # draw.ellipse((0, 0, diameter, diameter), fill=255)

        # # Crop hình ảnh bằng mask hình tròn
        # img = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
        # img.putalpha(mask)

        # # Resize hình ảnh
        # img = img.resize((300, 300), Image.ANTIALIAS)

        # photo = ImageTk.PhotoImage(img)

        # lbImage = tk.Label(self.frameL, image=photo, bg='#192533')
        # lbImage.image = photo
        # lbImage.pack()

        lbImage.pack(padx=50, pady=50, side="top")

        # lbImage = GradientFrame(self.master, width=300,
        #                         height=600,
        #                         image=img,
        #                         borderwidth=1, relief="sunken")

        # Tạo các button nằm ở hàng dưới cùng của frame 1
        imgPrev = ImageTk.PhotoImage(Image.open(
            r"D:\\SGU\\Opensource_Software\\radio-client\\assets\\back-arrow.png"))
        btnPrev = tk.Button(self.frameL, image=imgPrev,
                            width=35, height=35, bg='#192533', border=0, command=handle_prev)
        btnPrev.image = imgPrev
        btnPrev.place(x=90, y=420, width=35, height=35)

        imgPaused = ImageTk.PhotoImage(Image.open(
            r"D:\\SGU\\Opensource_Software\\radio-client\\assets\\play.png"))
        btnPaused = tk.Button(
            self.frameL, image=imgPaused, width=35, height=35, command=handle_paused)
        btnPaused.image = imgPaused
        btnPaused.place(x=185, y=420, width=35, height=35)

        imgNext = ImageTk.PhotoImage(Image.open(
            r"D:\\SGU\\Opensource_Software\\radio-client\\assets\\next.png"))
        btnNext = tk.Button(self.frameL, image=imgNext,
                            width=35, height=35, command=handle_next)
        btnNext.image = imgNext
        btnNext.place(x=280, y=420, width=35, height=35)

        # List in frame Right
        self.entry_search = tk.Entry(self.frameR, bg="white", width=35)
        self.entry_search.grid(row=0, column=0, padx=20, pady=45)
        text = self.entry_search.get()
        self.btnSearch = tk.Button(
            self.frameR, text="Search", command=handle_search)
        self.btnSearch.grid(row=0, column=1, pady=45)

        self.listbox = tk.Listbox(self.frameR, width=50, height=20)
        self.listbox.grid(row=1, column=0, columnspan=2, padx=40, pady=10)
        Constants.list_music = requests.get(
            "http://127.0.0.1:5000/get-all-music").json()
        for music in Constants.list_music:
            self.listbox.insert(END, music['name'])
        self.listbox.bind('<<ListboxSelect>>', onselect)

        self.btnAdd = tk.Button(self.frameR, text="Add Music",
                                width=10, height=2, command=handle_add_music)
        self.btnAdd.grid(row=5, column=1, pady=45)
        # self.btnDelete = tk.Button(
        #     self.frameR, text="Delete Music", width=10, height=2)
        # self.btnDelete.grid(row=5, column=2, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    # root.wm_attributes('-topmost', True)
    # root.wm_attributes('-transparentcolor', '#192533')
    gui.mainloop()

# pygame.init()
    # pygame.mixer.init()

    # # Đặt đường dẫn đến tệp âm thanh mp3
    # mp3_file = "http://localhost:5000/play-music"

    # # Tạo một đối tượng âm thanh từ tệp mp3
    # sound = pygame.mixer.Sound(mp3_file)

    # # Phát âm thanh
    # sound.play()

    # # Chờ cho đến khi âm thanh kết thúc
    # while pygame.mixer.get_busy():
    #     pygame.time.wait(100)

    # # Tắt pygame
    # pygame.quit()

    # Đặt đường dẫn đến file mp3

    # mp3file = urllib3.urlopen("http://localhost:5000/play-music")
    # with open('./test.mp3', 'wb') as output:
    #     output.write(mp3file.read())

    # song = AudioSegment.from_mp3("./test.mp3")
    # play(song)
    # response = requests.get("http://127.0.0.1:5000/get-all-music")
    # print(response.content)
