from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from customer.models import Order
from django.views import View
from django.http import HttpResponseRedirect

@login_required
def driver_dashboard(request):
    if request.user.user_type != "driver":
        return redirect('/')  # Kein Zugriff für Nicht-Fahrer

    orders = Order.objects.filter(driver=request.user, status="on_the_way")
    return render(request, 'driver/dashboard.html', {'orders': orders})


class CompleteDelivery(View):
    def post(self, request, *args, **kwargs):
        order_id = request.POST.get("order_id")
        order = Order.objects.get(id=order_id, driver=request.user)
        order.status = "delivered"
        order.save()
        return HttpResponseRedirect("/driver/dashboard/")