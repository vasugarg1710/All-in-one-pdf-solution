from tkinter import *
from tkinter.filedialog import askopenfile,askopenfiles
import tkinter.messagebox as tmsg
from PIL import Image
from pdf2image import convert_from_path
from fpdf import FPDF
import PyPDF2
import os
import threading
root = Tk()
root.title('PDF file utility')
root.geometry("444x430")
root.maxsize(444, 430)
root.minsize(444, 430)


def convert_jpg():
    filename = askopenfile(mode='r', filetypes=[('PDF Files', '*.pdf')])
    images_from_path = convert_from_path(filename.name, poppler_path=r'C:\Users\vasug\Downloads\release\poppler-0.90.1\bin')
    base_filename = os.path.splitext(os.path.basename(filename.name))[0] + '.jpg'
    os.mkdir('Converted')
    os.chdir(os.path.join(os.getcwd(),'Converted'))
    for index,page in enumerate(images_from_path):
        page.save(f'converted_{index}.jpg', 'JPEG')
    tmsg.showinfo('File converted', 'File is converted into jpg and is saved into the current working directory')


def convert_pdf():
    filename = askopenfile(mode ='r', filetypes =[('Image Files', '*.jpg')])
    image1 = Image.open(filename.name)
    im1 = image1.convert('RGB')
    im1.save(os.path.join(os.getcwd(), 'converted.pdf'))
    tmsg.showinfo('File converted', 'File is converted into pdf and is saved into the current working directory')


def merge_pdf():
    filename = askopenfiles(mode='r', filetypes =[('PDF Files', '*.pdf')])
    mergedObject = PyPDF2.PdfFileMerger()
    for index,item in enumerate(filename):
        mergedObject.append(PyPDF2.PdfFileReader(item.name))

    mergedObject.write("merged.pdf")
    tmsg.showinfo('PDF created', 'PDF files are merged and is saved into the current working directory')


def merge_jpg_in_one_pdf_file():
    images = askopenfiles(mode='r', filetypes=[('Image Files', '*.jpg')])
    imagelist = []
    for image in images:
        imagelist.append(image.name)
    pdf = FPDF()
    pdf.set_auto_page_break(0)
    # imagelist is the list with all image filenames
    for image in imagelist:
        pdf.add_page()
        pdf.image(image, w=190, h=297) # for A4 page
    pdf.output("mergedfile.pdf", "F")
    tmsg.showinfo('PDF created', 'JPG files are merged and is saved into the current working directory')


Label(text="All in one pdf solution", font="comicsans 25 bold").pack(padx=5,pady=5)
Button(text='Convert jpg to pdf', font="comicsans 20 bold",command=threading.Thread(target=convert_pdf).start, relief=SUNKEN,borderwidth=6).pack(padx=5,pady=5)
Button(text='Convert pdf to jpg',  font="comicsans 20 bold",command=threading.Thread(target=convert_jpg).start, relief=SUNKEN,borderwidth=6).pack(padx=5,pady=5)
Button(text='Merge jpg in 1 pdf',  font="comicsans 20 bold",command=threading.Thread(target=merge_jpg_in_one_pdf_file).start, relief=SUNKEN,borderwidth=6).pack(padx=5,pady=5)
Button(text='Merge pdf',  font="comicsans 20 bold",command=threading.Thread(target=merge_pdf).start, relief=SUNKEN,borderwidth=6).pack(padx=5,pady=5)
Label(text="Software created by Vasu", font="comicsans 15 bold",fg="red").pack(padx=5,pady=10)

root.mainloop()
