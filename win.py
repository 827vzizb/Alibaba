import glob
import os
import shutil
import time
import requests
import yt_dlp

os.system('')

# Terminal Colors
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

FB_COOKIE_STRING = "vpd=v1%3B796x384x2.8125; m_pixel_ratio=2.8125; locale=en_US; fbl_st=101028914%3BT%3A29804406; xs=45%3A1wt-K-u7qNR5zA%3A2%3A1788264357%3A-1%3A-1; wl_cbv=v2%3Bclient_version%3A3267%3Btimestamp%3A1788264366; fr=0H0BtkjXeF8vltAO6.AWcM9Q27KoW62uziKi-VGTsmcXBSaFiBudzsDFiSuegU0vOggvk.Bqlr94..AAA.0.0.Bqlr-z.AWcxgkfxWVFB1_Bw0LXC-j7UbQU; pas=100016037446408%3AwMODApRZdA; c_user=100016037446408; sb=eL-WalyMHnT18Zyif2voCYx1; wd=384x832; datr=eL-Wap4nfBD7BiYugNYOcOwY"

def prepare_cookie_file(cookie_str):
    cookie_path = 'temp_fb_cookie.txt'
    with open(cookie_path, 'w', encoding='utf-8') as f:
        f.write("# Netscape HTTP Cookie File\n")
        for item in cookie_str.split(';'):
            if '=' in item:
                name, value = item.strip().split('=', 1)
                f.write(f".facebook.com\tTRUE\t/\tFALSE\t0\t{name}\t{value}\n")
    return cookie_path

unique_id = int(time.time())
local_outtmpl = f'%(title).40s_{unique_id}.%(ext)s'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

print(f"{CYAN}============================================")
raw_url = input(f"{YELLOW}YouTube ya Facebook ke link dahi Tah: {RESET}").strip()
print(f"{CYAN}============================================{RESET}")

if "facebook.com/share/" in raw_url or "fb.watch" in raw_url:
    print(f"{YELLOW}[+] Resolving Horahal HAU...{RESET}")
    try:
        response = requests.get(raw_url, headers=headers, allow_redirects=True)
        final_url = response.url
    except Exception:
        final_url = raw_url
else:
    final_url = raw_url

format_option = 'bestvideo[ext=mp4][vcodec^=avc]+bestaudio[ext=m4a]/best[ext=mp4][vcodec^=avc]/best[ext=mp4]/best'

cookie_file = prepare_cookie_file(FB_COOKIE_STRING)

ydl_opts = {
    'format': format_option,
    'merge_output_format': 'mp4',  
    'outtmpl': local_outtmpl,      
    'http_headers': headers,
    'cookiefile': cookie_file,
    'overwrites': True,
    'nocheckcertificate': True,
    'quiet': False
}

try:
    print(f"\n{CYAN}[+] Downloading Horahal hau...{RESET}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([final_url])
    
    print(f"{YELLOW}[+] Moving safely to Windows Downloads folder...{RESET}")
    
   
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    downloaded_files = glob.glob(f"*{unique_id}*")
    for file in downloaded_files:
        if not file.endswith('.part') and not file.endswith('.ytdl'):
            destination = os.path.join(downloads_folder, file)
            shutil.move(file, destination)
            print(f"{GREEN}[+] Saved to: {destination}{RESET}")
            
    print(f"\n{GREEN}[SUCCESS] Download Complete, Download Folder dhekhi ta.{RESET}")

except Exception as e:
    print(f"\n{RED}[ERROR]: {e}{RESET}")

finally:
    if os.path.exists('temp_fb_cookie.txt'):
        os.remove('temp_fb_cookie.txt')
