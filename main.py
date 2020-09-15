from tkinter import *
from tkinter.filedialog import askopenfile, askopenfiles
import tkinter.messagebox as tmsg
from tkinter import simpledialog
from PIL import Image
from pdf2image import convert_from_path
from fpdf import FPDF
import PyPDF2
import os
import threading

root = Tk()
root.title('PDF file utility')
root.geometry("444x560")
root.maxsize(444, 560)
root.minsize(444, 560)


def convert_jpg():
    filename = askopenfile(mode='r', filetypes=[('PDF Files', '*.pdf')])
    images_from_path = convert_from_path(filename.name,
                                         poppler_path=r'C:\Users\vasug\Downloads\release\poppler-0.90.1\bin') # Enter the poppler path here
    os.mkdir('Converted')
    os.chdir(os.path.join(os.getcwd(), 'Converted'))
    for index, page in enumerate(images_from_path):
        page.save(f'converted_{index}.jpg', 'JPEG')
    tmsg.showinfo('File converted', 'File is converted into jpg and is saved into the current working directory')


def convert_pdf():
    filename = askopenfile(mode='r', filetypes=[('Image Files', '*.jpg')])
    image1 = Image.open(filename.name)
    im1 = image1.convert('RGB')
    im1.save(os.path.join(os.getcwd(), 'converted.pdf'))
    tmsg.showinfo('File converted', 'File is converted into pdf and is saved into the current working directory')


def merge_pdf():
    filename = askopenfiles(mode='r', filetypes=[('PDF Files', '*.pdf')])
    mergedObject = PyPDF2.PdfFileMerger()
    for index, item in enumerate(filename):
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
        pdf.image(image, w=190, h=297)  # for A4 page
    pdf.output("mergedfile.pdf", "F")
    tmsg.showinfo('PDF created', 'JPG files are merged and is saved into the current working directory')


def base_split(pageNum):
    pdf_file_path = askopenfile(mode='r', filetypes=[('PDF Files', '*.pdf')])
    pdf_file_path = pdf_file_path.name

    pdf = PyPDF2.PdfFileReader(pdf_file_path)

    pdfWriter = PyPDF2.PdfFileWriter()
    for page_num in pageNum:
        print(page_num)
        pdfWriter.addPage(pdf.getPage(int(page_num)-1))

    f = open("subset.pdf", "wb")
    pdfWriter.write(f)
    f.close()

    tmsg.showinfo('We have splitted your pdf', 'We have splitted your pdf')


def split_pdf():
    newWin = Tk()
    newWin.withdraw()
    answer = simpledialog.askstring("Enter the page range",
                                    "Enter the page range or specific pages separated by commas.",
                                    parent=newWin)
    newWin.destroy()

    if str(answer) != "":
        if "-" in str(answer):
            pageNum = str(answer).split("-")
            # print(pageNum)
            final_pages = []
            for page_num in range(int(pageNum[0]), int(pageNum[1]) + 1):
                final_pages.append(pageNum)

            print(final_pages)
            base_split(final_pages)

        elif "," in str(answer):
            pageNum = str(answer).split(",")
            base_split(pageNum)

        else:
            base_split(list(answer))
    else:
        tmsg.showinfo('Enter something', 'Please enter something. You have submitted it blank')
        exit()

def rate():
    input = tmsg.askyesno('Was your experience good?','Was your experience good?')
    if input:
        tmsg.showinfo("Nice to hear that","Nice to hear that")

    else:
        tmsg.showinfo("Tell your problem to us at vasugarg1710@gmail.com","Tell your problem to us at vasugarg1710@gmail.com")


if __name__ == '__main__':
    Label(text="All in one pdf solution", font="comicsans 25 bold").pack(padx=5, pady=5)
    Button(text='Convert jpg to pdf', font="comicsans 20 bold", command=threading.Thread(target=convert_pdf).start,
           relief=SUNKEN, borderwidth=6).pack(padx=5, pady=5)
    Button(text='Convert pdf to jpg', font="comicsans 20 bold", command=threading.Thread(target=convert_jpg).start,
           relief=SUNKEN, borderwidth=6).pack(padx=5, pady=5)
    Button(text='Merge jpg in 1 pdf', font="comicsans 20 bold",
           command=threading.Thread(target=merge_jpg_in_one_pdf_file).start, relief=SUNKEN, borderwidth=6).pack(padx=5,
                                                                                                                pady=5)
    Button(text='Merge pdf', font="comicsans 20 bold", command=threading.Thread(target=merge_pdf).start, relief=SUNKEN,
           borderwidth=6).pack(padx=5, pady=5)
    Button(text='Split pdf', font="comicsans 20 bold", command=threading.Thread(target=split_pdf).start, relief=SUNKEN,
           borderwidth=6).pack(padx=5, pady=5)
    Button(text='Rate us', font="comicsans 20 bold", command=threading.Thread(target=rate).start, relief=SUNKEN,
           borderwidth=6).pack(padx=5, pady=5)
    Label(text="Software created by Vasu", font="comicsans 15 bold", fg="red").pack(padx=5, pady=10)
    root.mainloop()
