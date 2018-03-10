# PDF -> Excel scaper
# Author: Stefan Stancu

import subprocess
import glob
import re

def check_dependencies():
    try:
        x = subprocess.Popen(["gs", "--version"], stdout=subprocess.PIPE)
    except OSError as e:
        if e.errno == 2:
            print("Error: GhostScript not installed or gs command not available")

def read_pdfs():
    #pdf_file_names = glob.glob("*.pdf")
    pdf_file_names = ["para01.pdf"]

    raw_text = []
    for i, file_name in enumerate(pdf_file_names):
        cmd = ["gs", "-sDEVICE=txtwrite", "-dNOPAUSE", "-dBATCH", "-sOutputFile=-", file_name]
        x = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        text, err = x.communicate()
        if not err:
            print(err)
            exit()

        for page_index, page_text in enumerate(text.split("Page")):
            raw_text.insert(page_index, [])
            for line_index, line_text in enumerate(re.split("\r\n |\n ", page_text)):
                raw_text[page_index].insert(line_index, line_text)

        for line in raw_text[2]:
            print(line)

if __name__=="__main__":
    check_dependencies()
    read_pdfs()
