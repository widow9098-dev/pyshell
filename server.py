import socket
import threading
import time
import os
hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
port = 5000
port2 = 5001
globals()['can_command'] = True
globals()['can_run'] = True
def serversend(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    c, addr = s.accept()
    print("CONNECTION FROM:", str(addr))
    os.system("cls")
    print("connected to client")
    while globals()['can_run'] == True:
        if globals()['can_command'] == True:
            msg = input(">")
            globals()['can_command'] = False
            c.send(msg.encode())
def serverin(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    js = False
    while js == False:
        try:
            s.connect((host, port))
            js = True
        except:
            pass
    msg = s.recv(1024)
    while msg:
        if globals()['can_run'] == True:
            
            if msg.decode() == "killed server...":
                print("client offline")
                print("please press enter to kill the server now")
                input("")
                globals()['can_run'] = False
                exit()
            elif msg.decode() == "invalid cmd":
                print(msg.decode())
                globals()['can_command'] = True
            else:
                if msg.decode() == "done":
                    globals()['can_command'] = True
                else:
                    print(msg.decode())
                time.sleep(0.2)
            msg = s.recv(1024)

t1 = threading.Thread(target=serversend, args=(host, port))
t2 = threading.Thread(target=serverin, args=(host, port2))
t1.start()
t2.start()
print("waiting for a conection from a client...\n")
print("server conection info: \n\n   host:" + host + " \n   port:" + str(port) + "\n   port2:" + str(port2))