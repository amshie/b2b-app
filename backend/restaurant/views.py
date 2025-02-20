from django.shortcuts import render
from django.views import View
from .models import Medication ,Order, Category
from django.core.mail import send_mail


class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "customer/about.html")


class OrderView(View):
    def get(self, request, *args, **kwargs):
        # Verwende das richtige related_name ('medications') für ManyToManyField
        categories = Category.objects.prefetch_related('medications').all()

        # Erstelle ein Dictionary mit den Medikamenten für jede Kategorie
        category_dict = {category.name: category.medications.all() for category in categories}

        return render(request, "customer/order.html", {"categories": category_dict})

    def post(self, request):
      selected_items = request.POST.getlist('items[]')
      total_price = sum(Medication.objects.get(pk=item_id).price for item_id in selected_items)
      name = request.POST.get("name")
      email = request.POST.get("email")
      street = request.POST.get("street")
      city = request.POST.get("city")
      state = request.POST.get("state")
      zip_code = request.POST.get("zip")

      order = Order.objects.create(
        name=name,
        email=email,
        street=street,
        city=city,
        state=state,
        zip_code=zip_code,
        price=total_price)
      
      order.medications.add(*selected_items)
      send_mail(
        "Bestellbestätigung – Ihre Medikamente",
        f"Hallo {name},\n\nIhre Bestellung wurde erfolgreich aufgenommen.\n"
        f"Gesamtpreis: {total_price} €\n"
        f"Lieferadresse: {street}, {city}, {state}, {zip_code}\n\n"
        "Vielen Dank für Ihre Bestellung!",
        "noreply@apotheke.de",
        [email],
        fail_silently=False,)
      context = {'items': Medication.objects.filter(pk__in=selected_items), 'price': total_price}
      return render(request, 'customer/order_confirmation.html', context)
    