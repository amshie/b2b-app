from django.contrib import admin
from .models import Medication, Category, Order

admin.site.register(Medication)
admin.site.register(Category)
admin.site.register(Order)