# PDF -> Excel scaper
# Author: Stefan Stancu

import subprocess
import glob
import re
import xlrd

from page import Page

def check_dependencies():
    try:
        x = subprocess.Popen(["gs", "--version"], stdout=subprocess.PIPE)
    except OSError as e:
        if e.errno == 2:
            print("Error: GhostScript not installed or gs command not available")

def read_pdf(file_name):
    raw_text = []
    cmd = ["gs", "-sDEVICE=txtwrite", "-dNOPAUSE", "-dBATCH", "-sOutputFile=-", file_name]

    x = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text, err = x.communicate()
    if not err:
        print(err)
        exit()

    for page in text.split("Page"):
        raw_text.append(re.split("\r\n |\n ", page)[1:21])

    raw_text.pop(0)
    return raw_text


if __name__=="__main__":
    check_dependencies()
    for page in read_pdf("para01.pdf"):
        Page(page).print_page()
    
