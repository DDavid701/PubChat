version = '1.0.0' # Do not change this!
import os
from dotenv import load_dotenv
import socket as sock
import time
from threading import Thread
import colorama
colorama.init(autoreset=True)
load_dotenv('conf.env')
ip        = os.getenv('IP')
port      = os.getenv('PORT')
fallback  = os.getenv('FALLBACK_PORT')

print(colorama.Fore.BLUE + """                                        
                                        
     =====        +++++=+===============
    ======  =+++++++++++++==============
    ====  +++++++++++++++++++===========
    ==  =++++++++++++++++++++++=========
       ++++++++    --    ++++++++       
      +++++++  ----------  +++++++      
     +++++++ -------------- +++++++     
     ++++++ ---------------- ++++++     
    +++++++ ---------------- +++++++    
    +++++++ ---------------- +++++++    
     ++++++ ---------------- ++++++     
     +++++++ -------------- +++++++     
      +++++++  ----------  +++++++      
       ++++++++    --    ++++++++       
---------++++++++++++++++++++++=  ==    
----------=+++++++++++++++++++  ====    
-------------==++++++++++++=  ======    
----------------==+++++      ======   
   
                                        """)
print(colorama.Fore.RED + ">" + colorama.Fore.LIGHTGREEN_EX + " PubChat Server" + colorama.Fore.WHITE +f" {version}")

def connection(con, name, ip):
    for c in clients:
        c.send(f"{time.strftime('%H:%M')}|{name}|joined|join".encode())
    while True:
        try:
            msg = con.recv(1024).decode()
            for c in clients:
                c.send(f"{time.strftime('%H:%M')}|{name}|{msg}".encode())
        except Exception:
            print(colorama.Fore.RED + "> " + colorama.Fore.GREEN + f"{name}@{ip}" + colorama.Fore.LIGHTGREEN_EX + " disconnected")
            clients.remove(con)
            users.remove(name)
            print(colorama.Fore.RED + "> " + colorama.Fore.LIGHTGREEN_EX + f"Connected Users: {len(users)}")
            time.sleep(3)
            for c in clients:
                c.send(f"{time.strftime('%H:%M')}|{name}|left|leave".encode())
            break

try:
    server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    server.bind((ip, int(port)))
    print(colorama.Fore.RED + "> " + colorama.Fore.LIGHTGREEN_EX + f"Running on {ip}:{port}")
    server.listen(0)
    print(colorama.Fore.RED + "> " + colorama.Fore.LIGHTGREEN_EX + f"Waiting for connections")
except OSError:
    server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    server.bind((ip, int(fallback)))
    print(colorama.Fore.RED + "> " + colorama.Fore.LIGHTGREEN_EX + f"Running on {ip}:{fallback}")
    server.listen(0)
    print(colorama.Fore.RED + "> " + colorama.Fore.LIGHTGREEN_EX + f"Waiting for connections")

users   = []
clients = []

while True:
    con, addr = server.accept()
    usip_split      = str(addr).split(',')
    usip      = usip_split[0].replace("'", "")
    usip      = usip.removeprefix('(')
    clients.append(con)
    name = con.recv(1024).decode()
    uver = con.recv(1024).decode()
    if uver == version:
        con.send("Correct".encode('utf-8'))
        if name not in users:
            print(colorama.Fore.RED + "> " + colorama.Fore.GREEN + f"{name}@{ip}" + colorama.Fore.LIGHTGREEN_EX + " connected")
            con.send(f'{len(users)}'.encode('utf-8'))
            users.append(name)
            print(colorama.Fore.RED + "> " + colorama.Fore.LIGHTGREEN_EX + f"Connected Users: {len(users)}")
            newthread = Thread(target=connection, args=(con, name, ip,))
            newthread.start()
    else:
        con.send("Wrong".encode('utf-8'))