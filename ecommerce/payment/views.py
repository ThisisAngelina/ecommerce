from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, redirect, render

from cart.cart import Cart # the Cart class

from .models import Order, OrderItem, ShippingAddress
from .forms import ShippingAddressForm

@login_required
def shipping(request):
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user) # the user already has a shipping address associated with them
    except ShippingAddress.DoesNotExist:
        shipping_address = None # there is not record of the user's address in the db yet

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_address) # the ModelForm updates the model instance with the values from request.POST
        if form.is_valid():
            shipping_address = form.save(commit=False) #update the user address in the database based on the information submitted through the form
            shipping_address.user = request.user
            shipping_address.save()
            return redirect('/')
        
    else:
        form = ShippingAddressForm(instance=shipping_address)
        return render(request, 'payment/shipping.html', {'form': form})

def checkout(request):
    pass

def complete_order(request):
    pass

def payment_success(request):
    pass

def payment_failure(request):
    pass

