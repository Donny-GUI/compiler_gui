import sys
import win32com.client
from fontTools.ttLib import TTFont
import subprocess
import os



class Font:
    OS = sys.platform[0]
    
    def get_font_list():
        match Font.OS:
            case 'w':
                objShell = win32com.client.Dispatch("Shell.Application")
                fonts_folder = objShell.Namespace(0x14)
                fonts = [fonts_folder.GetDetailsOf(font, 0) for font in fonts_folder.Items()]
                return fonts
            case 'l':
                command = "fc-list"
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, _ = process.communicate()
                output = output.decode("utf-8")
                fonts = []
                for line in output.splitlines():
                    font = line.split(":")[0].strip()
                    fonts.append(font)
                return fonts
            case 'd':
                fonts_dir = "/Library/Fonts/"
                fonts = []
                for file_name in os.listdir(fonts_dir):
                    if file_name.endswith(".ttf") or file_name.endswith(".otf"):
                        font_path = os.path.join(fonts_dir, file_name)
                        font = TTFont(font_path)
                        font_name = font["name"].getName(1, 3, 1, 1033).string.decode("utf-8")
                        fonts.append(font_name)
                return fonts
            case other:
                return []
        