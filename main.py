import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
from pyzbar.pyzbar import decode
from PIL import Image
from pdf2image import convert_from_path

def get_codes_from_file(codes_file):
    codes_list = []
    with open(codes_file, "r") as file1:
        for line in file1:
            codes_list.append(line.strip())
    return codes_list


def check(file, outputDir, codes_list):
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    
    erorrs_codes = []
    pages = convert_from_path(file, poppler_path='C:\\Program Files\\poppler-0.68.0\\bin')
    count = 1
    for page in pages:
        count+=1
        png_file = 'image' + str(count) + '.png'
        page.save(png_file, 'PNG')
        code = decode(Image.open(png_file))[0].data.decode("utf-8")
        if not code in codes_list:
            erorrs_codes.append([png_file, code])
        os.remove(png_file)
    os.rmdir(outputDir)
    return erorrs_codes


def print_error_barcodes(erorrs_codes):
    codes = ''
    if len(erorrs_codes) != 0:
        for i in erorrs_codes:
            codes += (' ' + i[0] + ' ' + i[1] + '\n')
    return codes



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def file_dialog():
    return filedialog.askopenfilename(initialdir = "/",title = "Select file")

def btn_find_pdf_path():
    path = file_dialog()
    entry_path_pdf.delete(0, tk.END)
    entry_path_pdf.insert(0, path)

def btn_find_codes_path():
    path = file_dialog()
    entry_path_codes.delete(0, tk.END)
    entry_path_codes.insert(0, path)

def check_barcodes():
    errors_codes = get_pdf_path()
    error = print_error_barcodes(errors_codes)
    if len(errors_codes) == 0:
        messagebox.showerror(title='All correct', message='All correct')
    else:
        messagebox.showerror(title='Error', message='error\n' + error)

def get_pdf_path():
    path_pds = entry_path_pdf.get()
    path_codes = entry_path_codes.get()
    codes_list = get_codes_from_file(path_codes)
    erorrs_codes = check(path_pds, "imag/", codes_list)
    return erorrs_codes

window = tk.Tk()

window['bg'] = '#000000'
window.title('Barcode Checker')
window.geometry('500x250')
window.resizable(width=False, height=False)

canvas = tk.Canvas(
    window, bg = "#FFFFFF", height = 250, width = 500,
    bd = 0, highlightthickness = 0, relief = "ridge")
canvas.place(x = 0, y = 0)


tv_path_pdf = tk.Label(
    text="Путь до pdf файла со штрих кодами", bg="#FFFFFF",
    font=("Arial-BoldMT", int(14.0)))
tv_path_pdf.place(x=43.0, y=17.0)

tv_path_codes = tk.Label(
    text="Путь до txt файла с кодами", bg="#FFFFFF",
    font=("Arial-BoldMT", int(14.0)))
tv_path_codes.place(x=43.0, y=117.0)


text_box_bg = tk.PhotoImage(file=relative_to_assets("TextBox_Bg.png"))
entry_path_pdf_img = canvas.create_image(28.0+170, 144.5+15, image=text_box_bg)
entry_path_codes_img = canvas.create_image(28.0+170, 44.5+15, image=text_box_bg)

entry_path_pdf = tk.Entry(bd=0, bg="#EBEBEB", highlightthickness=0)
entry_path_pdf.place(x=28.0, y=44.0, width=340.0, height=30.0)

entry_path_codes = tk.Entry(bd=0, bg="#EBEBEB", highlightthickness=0)
entry_path_codes.place(x=28.0, y=144.0, width=340.0, height=30.0)


btn_find_pdf_image = tk.PhotoImage(file=relative_to_assets("btn_find_pdf.png"))
btn_find_pdf = tk.Button(
    image=btn_find_pdf_image, borderwidth=0, highlightthickness=0,
    command=btn_find_pdf_path, relief="flat", bg="#FFFFFF")
btn_find_pdf.place(x=402.0, y=44.0, width=80.0, height=32.0)

btn_find_codes_image = tk.PhotoImage(file=relative_to_assets("btn_find_codes.png"))
btn_find_codes = tk.Button(
    image=btn_find_codes_image, borderwidth=0, highlightthickness=0,
    command=btn_find_codes_path, relief="flat", bg="#FFFFFF")
btn_find_codes.place(x=402.0, y=144.0, width=80.0, height=32.0)

btn_check_image = tk.PhotoImage(file=relative_to_assets("btn_check.png"))
btn_check = tk.Button(
    image=btn_check_image, borderwidth=0, highlightthickness=0,
    command=check_barcodes, relief="flat", bg="#FFFFFF")
btn_check.place(x=191.0, y=200.0, width=118.0, height=32.0)


window.mainloop()

pdf_file = 'barcodes.pdf'
outputDir = "imag/"
codes_file = 'codes.txt'

# https://www.figma.com/file/94Ajf8yEiHxwv64Uwqj4Vs/Untitled?node-id=0%3A1
# 211309-cfe3a76a-9ad9-41f9-afdf-6ac29b949884