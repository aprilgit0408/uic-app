from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from App.Modules.Formularios.forms import formularioDocumentos
from App.models import Documento
from django.views.generic.base import  View
from django.http.response import HttpResponse, JsonResponse
from django.urls import reverse_lazy
import datetime
import os
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from Usuarios.models import Usuarios
from uicApp import settings
modelo = Documento
formulario = formularioDocumentos
entidad = 'Documentos'
main = 'main.html'
url = reverse_lazy(f'app:{entidad.lower()}')


class listarDocumentos(LoginRequiredMixin, ListView):
    model = modelo
    template_name = f'{entidad}/listado.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encabezado'] = ['#','nombre del documento', 'archivo']
        context['items'] = modelo.objects.all()
        context['title'] = f'{entidad}'
        context['listado'] = f'Listado de {entidad}'
        return context
    def post(self, request, *args, **kwargs):
        data = []
        try:
            cont = 1
            for i in modelo.objects.all():
                data.append([
                    cont,
                    i.nombre,
                    'file',
                    i.archivo.url[-5:].split('.')[1],
                    i.archivo.url,
                ])
                cont +=1
        except Exception as e:
            print(f'Error {entidad} l-43 ',e)
            data = {}
        return JsonResponse(data, safe=False)


class addDocumentos(LoginRequiredMixin, CreateView):
    model = modelo
    form_class = formulario
    template_name = main
    success_url = url

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{entidad}'
        context['accion'] = f'Añadir {entidad}'
        context['agregar'] = f'Añadir {entidad}'
        return context


class editDocumentos(LoginRequiredMixin, UpdateView):
    model = modelo
    form_class = formulario
    template_name = main
    success_url = url

    def post(self, request, *args, **kwargs):
        form = formulario(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{entidad}'
        context['accion'] = f'Edición de {entidad}'
        return context


class deleteDocumentos(LoginRequiredMixin, DeleteView):
    model = modelo
    form_class = formulario
    template_name = main
    success_url = url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{entidad}'
        context['accion'] = f'Eliminar {entidad}'
        context['eliminar'] = kwargs
        return context

class generarPDF(LoginRequiredMixin, View):
    def link_callback(self, uri, rel):
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path
    def get(self, request, *args, **kwargs):
        usuario = Usuarios.objects.get(pk = request.user.pk)
        nombreArchivo = Documento.objects.get(pk = self.kwargs['pk']).nombre
        data = {
            'usuario': usuario,
            'fecha': datetime.datetime.now().date(),
            'encabezado' : f'{settings.STATIC_URL}images/encabezado.jpg',
            'imagenCentro' : f'{settings.STATIC_URL}images/imagenCentro.jpg',
            'piePagina' : f'{settings.STATIC_URL}images/piePagina.jpg'
        }
        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = f'attachment; filename="{nombreArchivo}.pdf"'
        template = get_template(f'{entidad}/{nombreArchivo}.html')

        html = template.render(data)
         # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response,
        link_callback=self.link_callback
        )
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

        # return JsonResponse(data, safe=False)