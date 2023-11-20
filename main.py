from PIL import Image
import os
import platform
import subprocess
import shutil

R, G, B, A = 0, 1, 2, 3
ARCH = platform.architecture()[0]
if ARCH == "32bit":
    vtfcmd = "./bin/x86/VTFCmd.exe"
if ARCH == "64bit":
    vtfcmd = "./bin/x64/VTFCmd.exe"


def bump2normal(file):
    source = Image.open(file)
    converted = Image.new(source.mode, source.size)

    source = source.split()
    converted = converted.split()

    converted[R].paste(im=source[B])
    converted[G].paste(im=source[A])
    converted[B].paste(im=source[G])
    converted[A].paste(im=source[R])

    im = Image.merge(mode='RGBA', bands=converted)
    im.save(f"{file[:-4]}.tga")


def tga2vtf(path, file): 
    command = [vtfcmd, "-file", f"{path}/{file}", "-format", "DXT5"]
    subprocess.call(command)

def clean(path):
    if not os.path.exists("output"):
        os.makedirs("output")
    for file in os.listdir(path):
        if file.endswith(".vtf"):
            shutil.copy(f"{path}/{file}", "output")
            os.remove(f"{path}/{file}")
        if file.endswith(".tga"):
            os.remove(f"{path}/{file}")

def main():
    path = input("Folder: ")
    for file in os.listdir(path):
        if file.endswith(".dds"):
            bump2normal(f"{path}/{file}")
            tga2vtf(path, f"{file[:-4]}.tga")
    clean(path)

main()