import os

os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")

from weasyprint import HTML

HTML('https://weasyprint.org/').write_pdf('weasyprint-website.pdf')