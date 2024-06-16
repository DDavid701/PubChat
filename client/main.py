version = '1.0.0'

import time
from customtkinter import *
import socket
from threading import Thread
from PIL import ImageTk
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

def login():
    global Client
    global usname
    global online
    usname     = entry_name.get()
    serverip   = entry_ip.get()

    try:
        Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Client.connect((serverip, 2401))
        Client.send(f'{usname}'.encode('utf-8'))
        time.sleep(0.1)
        Client.send(f'{version}'.encode('utf-8'))
        isver = Client.recv(1024).decode()
        if isver == 'Correct':
            online = Client.recv(1024).decode()
        else:
            login_frame.title("PubChat | Can't connect...!")
            raise Exception
    except ConnectionRefusedError:
        Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Client.connect((serverip, 2402))
        Client.send(f'{usname}'.encode('utf-8'))
        time.sleep(0.1)
        Client.send(f'{version}'.encode('utf-8'))
        isver = Client.recv(1024).decode()
        if isver == 'Correct':
            online = Client.recv(1024).decode()
        else:
            login_frame.title("PubChat | Can't connect...!")
            raise Exception

    login_frame.destroy()

def stop():
    global running
    app.destroy()
    running = False
    raise SystemExit


def send():
    inp = messages_entry.get()
    Client.send(f"{inp}".encode('utf-8'))
    entry_text_variable.set('')


def recieve():
    while True:
        if running == False:
            break
        msg = Client.recv(1024).decode()
        msg_parts = msg.split('|')
        if msg_parts[2] != '':
            try:
                if msg_parts[3]:
                    get_message(time=msg_parts[0],
                                name=msg_parts[1],
                                message=msg_parts[2],
                                mode=msg_parts[3],
                                )
                    messages_frame._parent_canvas.yview_moveto(1.0)
            except IndexError:
                get_message(time=msg_parts[0],
                            name=msg_parts[1],
                            message=msg_parts[2],
                            mode="",
                            )
                messages_frame._parent_canvas.yview_moveto(1.0)
        else:
            pass

def get_message(name, time, message, mode):
    global online
    if mode == "join":
        frame = CTkFrame(master=messages_frame, width=580, height=34, fg_color='#2E8B57', corner_radius=0)
        join_text = CTkLabel(master=frame, text=f'{name} has joined the server!', font=('Ubuntu', 20))
        time = CTkLabel(master=frame, text=time, font=('Ubuntu', 12))

        frame.pack(pady=1,
                   padx=1, )
        join_text.place(x=2,
                        y=2)
        time.place(x=537,
                   y=0)

        online += 1
        app.title(f'PubChat × {online} online')

    elif mode == "leave":
        frame = CTkFrame(master=messages_frame, width=580, height=34, fg_color='#DC143C', corner_radius=0)
        join_text = CTkLabel(master=frame, text=f'{name} has left the server!', font=('Ubuntu', 20))
        time = CTkLabel(master=frame, text=time, font=('Ubuntu', 12))

        frame.pack(pady=1,
                   padx=1, )
        join_text.place(x=2,
                        y=2)
        time.place(x=537,
                   y=0)

        online -= 1
        app.title(f'PubChat × {online} online')

    else:
        frame = CTkFrame(master=messages_frame, width=580, height=54, fg_color='grey', corner_radius=0)
        name = CTkLabel(master=frame, text=name, font=('Ubuntu', 22))
        time = CTkLabel(master=frame, text=time, font=('Ubuntu', 12))
        message = CTkLabel(master=frame, text=message, font=('Ubuntu', 16))

        frame.pack(pady=1,
                   padx=1, )
        name.place(x=2,
                   y=2)
        time.place(x=537,
                   y=0)
        message.place(x=2,
                      y=25)

login_frame = CTk()
login_frame.title('PubChat × Connect')
login_frame.resizable(False, False)
login_frame.geometry('300x200')
try:
    path = resource_path('./logo.png')
    icon = ImageTk.PhotoImage(file=path)
    login_frame.iconphoto(True, icon)
except Exception:
    pass

entry_name = CTkEntry(master=login_frame, width=200, height=20, placeholder_text='Username')
entry_ip = CTkEntry(master=login_frame, width=200, height=20, placeholder_text='Server Address')
login_button = CTkButton(master=login_frame, command=login, text="Join", corner_radius=4)

entry_name.pack(pady=2)
entry_ip.pack(pady=0)
login_button.pack(pady=30)

login_frame.mainloop()


app = CTk()
app.geometry('600x400')
app.resizable(False, False)
app.title(f'PubChat × {online} online')
online = int(online)
app.protocol('WM_DELETE_WINDOW', stop)

running = True

entry_text_variable = StringVar(master=app)

messages_frame = CTkScrollableFrame(master=app, width=600, height=350, corner_radius=0)
messages_entry_frame = CTkFrame(master=app, width=600, height=45, corner_radius=0)
messages_entry = CTkEntry(master=messages_entry_frame, width=555, textvariable=entry_text_variable, corner_radius=0)
messages_entry_send = CTkButton(master=messages_entry_frame, width=28, height=28, text="➤", command=send,
                                font=('System', 15), corner_radius=0, fg_color='grey', hover_color='darkgrey')

messages_frame.pack()
messages_entry_frame.pack(pady=5)
messages_entry.place(x=5,
                     y=6)
messages_entry_send.place(x=565,
                          y=6)

recv_thrd = Thread(target=recieve)
recv_thrd.start()

app.mainloop()