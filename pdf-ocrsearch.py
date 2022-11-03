# Requires Python 3.6 or higher due to f-strings
# reference: https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/

# Import libraries
from __future__ import print_function, division
from pathlib import Path
from tempfile import TemporaryDirectory

import pytesseract
from PIL import Image
import fitz  # pip install PyMuPDF
import os
import time
from multiprocessing import Pool, cpu_count


# We may need to do some additional downloading and setup...
# Windows needs a PyTesseract Download
# https://github.com/UB-Mannheim/tesseract/wiki/Downloading-Tesseract-OCR-Engine

pytesseract.pytesseract.tesseract_cmd = (
    r"D:\\MyZone\\downlaoded\\Tesseract-OCR-backend\\tesseract.exe"
)


SEARCHING_TARGET = "软件"
PDF_file = Path(r"test.pdf")


def one_page(tempdir, page_id, page):
    pix = page.get_pixmap(dpi=500)


    filename = f"{tempdir}\page_{page_id:03}.jpg"

    pix.save(filename)  # 将图片写入指定的文件夹内

    text = str(((pytesseract.image_to_string(Image.open(filename), lang="chi_sim"))))
    text = text.replace(" ","")
    indx = text.find(SEARCHING_TARGET)
    if indx != -1:
        print("found {} in page {}. prefix index: {}".format(
                        SEARCHING_TARGET, 
                        filename,
                        indx))
    # else:
    #     print("Noting found in page {}".format(filename))



# choose a version specific timer function (bytes == str in Python 2)
mytime = time.clock if str is bytes else time.perf_counter


def one_job(vector):
    # recreate the arguments
    idx = vector[0]  # this is the segment number we have to process
    cpu = vector[1]  # number of CPUs
    filename = vector[2]  # document filename
    doc = fitz.open(filename)  # open the document
    num_pages = doc.page_count  # get number of pages

    # pages per segment: make sure that cpu * seg_size >= num_pages!
    seg_size = int(num_pages / cpu + 1)
    seg_from = idx * seg_size  # our first page number
    seg_to = min(seg_from + seg_size, num_pages)  # last page number
    with TemporaryDirectory() as tempdir:
        for i in range(seg_from, seg_to):  # work through our page segment
            page = doc.load_page(i)
            one_page(tempdir, i, page)
    print("Processed page numbers %i through %i" % (seg_from, seg_to - 1))


def multithread_main():
    filename = PDF_file
    cpu = cpu_count()

    # make vectors of arguments for the processes
    vectors = [(i, cpu, filename) for i in range(cpu)]
    print("Starting %i processes for '%s'." % (cpu, filename))

    pool = Pool()  # make pool of 'cpu_count()' processes
    pool.map(one_job, vectors, 1)  # start processes passing each a vector


def traditional_main():
    ''' Main execution point of the program'''
    with TemporaryDirectory() as tempdir:
        pdf_doc = fitz.open(PDF_file)
        for page_enumeration, page in enumerate(pdf_doc.pages(),start=1):
            one_page(tempdir, page_enumeration, page)


def speed_test():
    t0 = mytime()  # start a timer
    
    multithread_main()

    t1 = mytime()  # stop the timer
    print("Total time %g seconds" % round(t1 - t0, 2))
    
    t0 = mytime()  # start a timer
    
    traditional_main()

    t1 = mytime()  # stop the timer
    print("Total time %g seconds" % round(t1 - t0, 2))


if __name__ == "__main__":
    speed_test()
