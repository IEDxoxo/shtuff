import threading
import paramiko
from discord.ext import commands
import os
import time
import requests
import random
from colorama import init
import fade
from colored import fg
gray = fg('dark_gray')
yellow = fg('yellow')
white = fg('white')
digitalocean = [] #list of vps in here
# menu = """
# [1] GC
# [2] Update the sniper
# [3] Send a command
# [4] Fetch Times [NEW!]
# [5] Setup mass VPS [NEW!]
# [6] Mfa Queue [TESTING]
# [7] List Queue
# """

purple = fg('violet')
def menu():
    menu = f"""
 _________________________________________________
|                                                 |
|         [1] GC Queue                            |
|         [2] Times                               |
|         [3] Force Command                       |
|         [4] MFA Queue                           |
|         [5] List Queue (MFA)                    |
|         [6] Distribute Accounts                 |
|_________________________________________________|
"""
    print(fade.purplepink(menu))
def sshread(host, pw, target, servernum):
    global meowing
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host, username="root",
                        password=pw)
        stdin, stdout, stderr = ssh_client.exec_command(f"cd sniper;cat {target.lower()}.txt")
        # sftp_client = ssh_client.open_sftp()
        # file = sftp_client.open(f'/gc/{target.lower()}.txt')
        for line in stdout.readlines():
            meowing += line
        meowing += '================================END OF SERVER OUTPUT================================'
    except:
        print(f"Ran into an error! {host}")
def sshconn(host, pw, command):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host, username="root",
                        password=pw)
        stdin, stdout, stderr = ssh_client.exec_command(f"{command}")
        print(stdout.read())
    except:
        print(f"{host} is offline.")
def digitaloceanxd(host, pw, command, i):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host, username="root",
                        password=pw)
        stdin, stdout, stderr = ssh_client.exec_command(f"cd mfa;{command}", get_pty=True)
        stdin.write("\r\n")
        stdin.flush()
        print(stdout.read())
    except:
        print(f"{host} is offline.")
def digitaloceanmfa(host, pw, target, delay, i):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host, username="root",
                        password=pw)
        print(f"python3 mfa.py {target} {float(delay)} {i}")
        stdin, stdout, stderr = ssh_client.exec_command(f"cd mfa;python3 mfa.py {target} {float(delay)} {i}",  get_pty=True)
        print(f"{stdout.read()}")
        time.sleep(1)
    except:
        print(f"{host} is offline.")
def manual(host, pw, combolist):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host, username="root",
                        password=pw)
        newstr = ''
        for combo in combolist:
            newstr += combo + '\n'
        print(host)
        stdin, stdout, stderr = ssh_client.exec_command(f'cd mfa;echo -e "{newstr}" > mfas.txt',  get_pty=True)
        print(stdout.read())
    except Exception as e:
        print(f"Encountered error: {e}") 
import random
# delays = [813, 800, 760, 740, 720, 700, 715, 735, 750, 785]
while True:
    meowing = ""
    threads = []
    os.system("cls")
    menu()
    choice = int(input(f"{gray}[{yellow}+{gray}] {white}Enter choice > {yellow}"))
    if choice == 1:
        os.system("cls")
        target = input(f"{gray}[{yellow}+{gray}] {white}Enter Target > {yellow}")
        droptime = int(requests.get(f"http://api.star.shopping/droptime/{target.replace('95', '')}", headers={"User-Agent": "Sniper"}, timeout=1).json()['unix'])
        print(f"\033[90m[\033[93m*\033[90m]\033[39m Waiting for Drop.")
        time.sleep(droptime - time.time() - 45)
        for i in range(len(digitalocean)):
            item = digitalocean[i]
            item = item.split(":")
            host = item[0]
            pw = item[1]
            if target.endswith('95'):
                target = "Test"
            else:
                pass
            threads.append(threading.Thread(target=digitaloceanxd, args=(host, pw, f"cd gc;python3 gc.py {target} 35 {i + 1} {droptime}",)))
        start = time.time()
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        end = time.time()
        finished = round(end-start, 2)
        print(f"\033[90m[\033[93m*\033[90m]\033[39m Finished. Took {finished}s to queue.")
    if choice == 2:
        target = input(f"{gray}[{yellow}+{gray}] {white}Enter the name you want to fetch > {yellow}")
        # try:
        for i in range(len(allvps)):
            item = allvps[i]
            item = item.split(":")
            host = item[0]
            pw = item[1]
            threads.append(threading.Thread(target=sshread, args=(host, pw, f"{target}", i,)))
            start = time.time()
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        filewrite = open(f"ALL{target.lower()}.txt", "a+")
        for line in meowing:
            filewrite.write(line)
        filewrite.close()
        end = time.time()
        finished = round(end-start, 2)
        
        print(f"\033[90m[\033[93m*\033[90m]\033[39m Finished. Took {finished}s to send command.")





    if choice == 3:
        target = input(f"{gray}[{yellow}+{gray}] {white}Enter command > {yellow}")
        # try:
        start = time.time()
        for i in range(len(digitalocean)):
            item = digitalocean[i]
            item = item.split(":")
            host = item[0]
            pw = item[1]
            threads.append(threading.Thread(target=digitaloceanxd, args=(host, pw, f"{target}", target,)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        end = time.time()
        finished = round(end-start, 2)
        print(f"\033[90m[\033[93m*\033[90m]\033[39m Finished. Took {finished}s to send command.")
    if choice == 4:
        target = input(f"{gray}[{yellow}+{gray}] {white}Enter target > {yellow}")
        delay = int(input(f"{gray}[{yellow}+{gray}] {white}Enter Delay > {yellow}"))
        # delays = [33, 43, 80, 53, 16, 63, 73, 93, 26]
        # delay = float(input(f"{gray}[{yellow}+{gray}] {white}Enter Delay > {yellow}"))
        # try:
        droptime = int(requests.get(f"http://api.star.shopping/droptime/{target}", headers={"User-Agent": "Sniper"}, timeout=1).json()['unix'])
        print(f"\033[90m[\033[93m*\033[90m]\033[39m Waiting for Drop.")
        time.sleep(droptime - time.time() - 120)
        start = time.time()
        for i in range(len(digitalocean)):
            item = digitalocean[i]
            item = item.split(":")
            host = item[0]
            pw = item[1]
            threads.append(threading.Thread(target=digitaloceanmfa, args=(host, pw, f"{target}", delay, i,)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        end = time.time()
        finished = round(end-start, 2)
        print(f"\033[90m[\033[93m*\033[90m]\033[39m Finished. Took {finished}s to send command.")
    if choice == 5:
        namequeue = []
        amt = int(input("How many VPS do you want to queue with? > "))
        while True:
            names = input(f"{gray}[{yellow}+{gray}] {white}Enter name you want to add to queue > {yellow}")
            if names == "":
                break
            namequeue.append(names)
        for name in namequeue:
            indexnum = 0
            threads = []
            if name.lower() != 'test':
                droptime = int(requests.get(f"http://api.star.shopping/droptime/{name}", headers={"User-Agent": "Sniper"}, timeout=5).json()['unix'])
                print(f"\033[90m[\033[93m*\033[90m]\033[39m Waiting for Drop on {name}")
                try:
                    time.sleep(droptime - time.time() - 120)
                except Exception:
                    pass
            else:
                pass
            start = time.time()
            for i in range(amt):
                delay = 30 + (i*0.5)
                item = digitalocean[indexnum]
                item = item.split(":")
                host = item[0]
                pw = item[1]
                threads.append(threading.Thread(target=digitaloceanmfa, args=(host, pw, f"{name}", delay, indexnum,)))
                indexnum += 1
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            end = time.time()
            finished = round(end-start, 2)
            print(f"\033[90m[\033[93m*\033[90m]\033[39m Finished. Took {finished}s to queue {name}")
            time.sleep(30)
    if choice == 6:
        f = open('mfas.txt').read().splitlines()
        # idea
        # every 5 accounts are placed in every 3 vps's
        counter = 0 #to track vps numbers
        accindex = 0
        MEOWx = 0
        threads = []
        # I NEED TO PULL 5 accounts
        combolist = []
        try:
            for zy in range(70):
                threads = []
                combolist = []
                for x in range(5):
                    combolist.append(f[x + accindex])
                for i in range(3):
                    item = digitalocean[i + MEOWx]
                    item = item.split(":")
                    host = item[0]
                    pw = item[1]
                    threads.append(threading.Thread(target=manual, args=(host, pw, combolist,)))
                for t in threads:
                    t.start()
                for t in threads:
                    t.join()
                accindex += 5
                MEOWx += 3
        except:
            pass
    if choice == 7:
        start = time.time()
        for i in range(len(digitalocean)):
            item = digitalocean[i]
            item = item.split(":")
            host = item[0]
            pw = item[1]
            threads.append(threading.Thread(target=digitaloceanxd, args=(host, pw, f"screen -r python3 poseidon.py", i,)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        end = time.time()
        finished = round(end-start, 2)
        print(f"\033[90m[\033[93m*\033[90m]\033[39m Finished. Took {finished}s to send command.")