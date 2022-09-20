from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from App.Modules.Formularios.forms import formularioDocumentos, formularioFirma
from django.views.generic.base import  View
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
import datetime
import os
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from Usuarios.models import SeguimientoDocumentacion, Usuarios, Documento
from uicApp import settings
modelo = Documento
# Create your tests here.
# Define your data
source_html = "<html><body><p>To PDF or not to PDF</p></body></html>"
output_filename = "test.pdf"

# Utility function
def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return False on success and True on errors
    return pisa_status.err

# Main program
if __name__ == "__main__":
    pisa.showLogging()
    convert_html_to_pdf(source_html, output_filename)