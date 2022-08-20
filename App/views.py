from django.db import models
from django.views.generic.base import TemplateView

class Index(TemplateView):
    template_name = "index.html"
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
