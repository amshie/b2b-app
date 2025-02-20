from django.views import View
from django.shortcuts import render
from restaurant.models import Order, Medication

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "customer/index.html")

class AboutView(View):  
    def get(self, request, *args, **kwargs):
        return render(request, "customer/about.html")
