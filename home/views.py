from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

class InformationsView(TemplateView):
    template_name = 'home/informations.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

class DevInformationsView(TemplateView):
    template_name = 'home/devInformations.html'
    
    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)