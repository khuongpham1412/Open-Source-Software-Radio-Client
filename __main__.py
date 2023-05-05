import vlc
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps, ImageDraw
import os
import requests
import json
from modules.Gradian import GradientFrame
from modules.Constants import Constants
from urllib.request import urlopen
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
            url = "http://localhost:5000/play-music/" + str(path)
            media_player = Constants.media_player
            media = vlc.Media(url)
            media_player.set_media(media)
            media_player.play()
            # wait so the video can be played for 2.5 seconds
            # dem = 5
            # while(dem > 0):
            #     dem = dem - 1
            duration = media_player.get_length() / 1000
            while (duration > 0):
                duration = duration - 1
            # checking if it is playing
            value = media_player.is_playing()

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
            elif(Constants.index_select == len(Constants.list_music) - 1):
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
                # # Lấy kích thước của ảnh
                # width, height = 300, 300

                # # Tính đường kính của hình tròn cần cắt ra
                # diameter = min(width, height)

                # # Tạo ảnh mới kích thước bằng đường kính của hình tròn
                # new_img = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))

                # # Chèn ảnh gốc vào ảnh mới
                # new_img.paste(img, ((diameter - width) //
                #               2, (diameter - height) // 2))

                # # Bo tròn ảnh mới
                # mask = Image.new("L", (diameter, diameter), 0)
                # draw = ImageDraw.Draw(mask)
                # draw.ellipse((0, 0, diameter, diameter), fill=500)
                # new_img.putalpha(mask)

                # # Lưu ảnh mới
                # output_path = "test.png"
                # new_img.save(output_path)

                lbImage.configure(image=img)
                lbImage.image = img

            # print(selected_music['path'])
            # Hiển thị tên bài hát lên Label
            # img = ImageTk.PhotoImage(Image.open(image))
            # lbImage.configure(image=img, bg='#192533')
            # lbImage.image = img

            # imgPrev = ImageTk.PhotoImage(Image.open(
            #     r"D:\\SGU\\Opensource_Software\\radio-client\\assets\\pause.png"))
            # btnPaused.configure(image=imgPrev)
            # btnPaused.image = imgPrev
            handle_play_mp3(str(path))
            play_time()

        def choose_image(add_song_win, image_entry):
            imageFile = filedialog.askopenfilename(
                initialdir="/", title="chon file", filetypes=[("png file", "*.png"), ("jpg file", "*.jpg")])
            # print(imageFile)
            if(imageFile):
                imageFileName = open(imageFile, 'rb')
            else:
                return None
                # print(imageFileName.read())
            imageFileBaseName = os.path.basename(imageFile)
            image_entry.delete(0, 'end')  # clear any existing text
            image_entry.insert(0, imageFileBaseName)  # insert selected file path
            return imageFileName

        def choose_file(root, mp3file_entry):
            # dir = tk.filedialog.askopenfilename()
            mp3File = filedialog.askopenfilename(
                initialdir="/", title="chon file", filetypes=(("mp3 file", "*.mp3"), ("all file", "*.*")))
            # print("hello", mp3File)
            if(mp3File):
                mp3FileName = open(mp3File, 'rb')
            mp3FileBaseName = os.path.basename(mp3File)
            mp3file_entry.delete(0, 'end')
            mp3file_entry.insert(0, mp3FileBaseName)
            return mp3FileName
            # print(os.path.abspath(file_to_upload.filename))

            # file = {'file': open(dir, 'rb')}
            # data = {"name": "name test", "image": "image test"}
            # headers = {'Content-Type': 'multipart/form-data'}
            # r = requests.post("http://127.0.0.1:5000/uploads",
            #                   headers=headers, files=file)

            # r = requests.post('http://127.0.0.1:5000/uploads',
            #                   files=file, json=data)
            # print(r)

        import requests

        def handle_add_form(name, image_file, mp3_file):
            # print(name, image_file,mp3_file)

            try:
                url = "http://127.0.0.1:5000/uploads"

                # create a dictionary with the data to be sent in the POST request
                
                # json_data = {
                #     'name': name
                # }

                # create a dictionary for the files to be sent in the POST request

                files_data = {
                    "image": image_file,
                    "file": mp3_file,
                    'data': (None, json.dumps({'name':name}), 'application/json'), 
                }

                if image_file == None:
                    files_data = {
                        "file": mp3_file,
                        "data": (None, json.dumps({"name": name}), "application/json")
                    }

                # send the POST request
                response = requests.post(url, files=files_data)
                print(files_data)
                # print(json_data)
                print(response)
                if response.ok:
                    print("Upload successful")
                    self.listbox.insert(END, name)
                    Constants.list_music.insert(len(Constants.list_music), response.json())
                    return response.json()
                else:
                    print("Upload failed:", response.text)
                    return None
            except:
                print("Oh No ! Exception :(((")
                return None


       

        def handle_add_music():
            global select_file 
            global select_image
            select_file = None

            add_song_win = tk.Toplevel()
            # add_song_win.attributes('-topmost', True)
            add_song_win.geometry("300x100")
            add_song_win.title("Thêm bài hát")
            lb_name = tk.Label(add_song_win, text="Tên bài hát")
            name_entry = tk.Entry(add_song_win)

            lb_image = tk.Label(add_song_win, text="Ảnh")
            image_entry = tk.Entry(add_song_win)
            image_entry.insert(0, " Vui lòng chọn ảnh")
            bt_select_image = tk.Button(
                add_song_win, text="select", command=lambda: handle_select_image(add_song_win, image_entry))
            # bt_select_image.pack()
            # image_entry.delete(0)
            # image_entry.insert(0, dir)

            lb_mp3file = tk.Label(add_song_win, text="File nhạc")
            mp3file_entry = tk.Entry(add_song_win)
            mp3file_entry.insert(0, " Vui lòng chọn file nhạc")
            bt_select_file = tk.Button(
                add_song_win, text="select", command=lambda: handle_select_file(add_song_win, mp3file_entry))
            # bt_select_file.pack()
            # mp3file_entry.delete(0)
            # mp3file_entry.insert(0, dir)
            print(dir)

            btn_them = tk.Button(add_song_win, text="Thêm", command=lambda: handle_add_form(name_entry.get(), select_image, select_file))
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


        def handle_select_image(add_song_win, image_entry):
            global select_image
            select_image = choose_image(add_song_win, image_entry)

        def handle_select_file(add_song_win, mp3file_entry):
            global select_file
            select_file = choose_file(add_song_win, mp3file_entry)



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
            r"output.png"))

        lbImage = tk.Label(self.frameL, image=img,
                           width=300, height=300, bg='#192533')
        lbImage.image = img
        lbImage.pack(padx=50, pady=50, side="top")

        lb_music_name = tk.Label(self.frameL)
        # lb_music_name.pack()
        # lb_music_name.pack_forget()

        def on_seekbar_click(event):
            self.seekbar['value'] = event.x / 3
            # get position on seekbar tool
            position = self.seekbar.get()
            media_player = Constants.media_player
            time = ((media_player.get_length() / 1000) / 100) * position
            media_player.set_time(int(time * 1000))

        self.seekbar1 = tk.Label(self.frameL, text='', relief=GROOVE, anchor=E)
        self.seekbar1.pack(fill=X, side=BOTTOM, ipady=2)

        def slide(x):
            pass

        self.seekbar = ttk.Scale(
            self.frameL, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=300)
        self.seekbar.pack()
        self.seekbar.bind('<Button-1>', on_seekbar_click)

        # Tạo các button nằm ở hàng dưới cùng của frame 1
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

        # List in frame Right
        # self.entry_search = tk.Entry(self.frameR, bg="white", width=35)
        # self.entry_search.grid(row=0, column=0, padx=20, pady=45)
        # text = self.entry_search.get()
        # self.btnSearch = tk.Button(
        #     self.frameR, text="Search", command=handle_search)
        # self.btnSearch.grid(row=0, column=1, pady=45)

        self.listbox = tk.Listbox(self.frameR, width=50, height=25)
        self.listbox.grid(row=0, column=0, columnspan=3, padx=40, pady=50)
        res = requests.get(
            "http://127.0.0.1:5000/get-all-music")
        if (str(res.content).find("Empty", 0, len(str(res.content))) == -1):
            Constants.list_music = res.json()

        for music in Constants.list_music:
            self.listbox.insert(END, music['name'])
        self.listbox.bind('<<ListboxSelect>>', onselect)

        self.btnAdd = tk.Button(self.frameR, text="Add Music",
                                width=10, height=2, command=handle_add_music)
        self.btnAdd.grid(row=1, column=1)
        self.btnDelete = tk.Button(
            self.frameR, text="Delete Music", width=10, height=2, command=handle_delete_music)
        self.btnDelete.grid(row=1, column=2)


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    # root.wm_attributes('-topmost', True)
    # root.wm_attributes('-transparentcolor', '#192533')
    gui.mainloop()
