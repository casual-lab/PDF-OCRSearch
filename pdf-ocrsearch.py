# Requires Python 3.6 or higher due to f-strings
# reference: https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/

# Import libraries
import platform
from tempfile import TemporaryDirectory, NamedTemporaryFile
from pathlib import Path

import pytesseract
from PIL import Image
import fitz  # fitz就是pip install PyMuPDF
import os

SEARCHING_TARGET = "软件"

# We may need to do some additional downloading and setup...
# Windows needs a PyTesseract Download
# https://github.com/UB-Mannheim/tesseract/wiki/Downloading-Tesseract-OCR-Engine

pytesseract.pytesseract.tesseract_cmd = (
	r"D:\\MyZone\\downlaoded\\Tesseract-OCR-backend\\tesseract.exe"
)


PDF_file = Path(r"test.pdf")
print(os.path.abspath(PDF_file))


def main():
	''' Main execution point of the program'''

	pdf_doc = fitz.open(PDF_file)
	for page_enumeration, page in enumerate(pdf_doc.pages(),start=1):
		pix = page.get_pixmap(dpi=500)

		with NamedTemporaryFile() as fp:
			pix.save(fp)  # 将图片写入指定的文件夹内

			text = str(((pytesseract.image_to_string(Image.open(fp), lang="chi_sim"))))
			text = text.replace(" ","")
			findx = text.find(SEARCHING_TARGET)
			if findx != -1:
				print("found {} in page {}. prefix index: {}".format(
						SEARCHING_TARGET, 
						page_enumeration,
						findx))
			else:
				print("Noting found in page {}".format(page_enumeration))

if __name__ == "__main__":
	# We only want to run this if it's directly executed!
	main()
