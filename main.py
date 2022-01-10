from PIL import Image
import os
import platform
import subprocess

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
    output = f"{path}\\{file}"
    if not os.path.exists(output):
        os.mkdir(output)
    command = [vtfcmd, "-file", f"{path}\\{file}", "-alphaformat", "DXT5", "-output", output]
    subprocess.call(command)


def main():
    path = input("Folder: ")
    for file in os.listdir(path):
        if file.endswith(".dds"):
            bump2normal(f"{path}\\{file}")
            tga2vtf(path, f"{file[:-4]}.tga")
            os.remove(f"{path}\\{file[:-4]}.tga")

main()