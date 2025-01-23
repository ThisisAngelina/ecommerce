from decimal import Decimal
import stripe 

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import get_list_or_404, redirect, render

from django.conf import settings

from cart.cart import Cart # the Cart class

from .models import Order, OrderItem, ShippingAddress
from .forms import ShippingAddressForm


# needed for stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


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
    if request.user.is_authenticated: # pre-fill their shipping address
        shipping_address, _ = ShippingAddress.objects.get_or_create(user=request.user)
        return render(request, 'payment/checkout.html', {'shipping_address': shipping_address})
    return render(request, 'payment/checkout.html')

def complete_order(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country') 
        zip = request.POST.get('zip')

        cart = Cart(request) # create a Cart instance
        cart_total = cart.get_total_value()

        shipping_address, _ = ShippingAddress.objects.get_or_create(
                    user=request.user,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'address': address,
                        'city': city,
                        'country': country,
                        'zip': zip
                    }
                )
        # create Stripe session data for Stripe checkout
        session_data = {
                    'mode': 'payment',
                    'success_url': request.build_absolute_uri(reverse('payment:payment_success')),
                    'cancel_url': request.build_absolute_uri(reverse('payment:payment_failure')),
                    'line_items': []
                }

        if request.user.is_authenticated: # associate a user with the order if the user is known
            user = request.user
        else:
            user = None
            
        order = Order.objects.create(user=user, shipping_address=shipping_address, amount=cart_total)


        for article in cart:
            OrderItem.objects.create(user=user, order=order, item=article['item'], price=article['price'], quantity=article['qty'])
            
            # add information on the item purchased for stripe
            session_data['line_items'].append({
                            'price_data': {
                                'unit_amount': int(article['price'] * Decimal(100)),
                                'currency': 'usd',
                                'product_data': {
                                    'name': article['item']
                                },
                            },
                            'quantity': article['qty'],
                        })
            
            session_data['client_reference_id'] = order.id
            session = stripe.checkout.Session.create(**session_data)
            return redirect(session.url, code=303) # redirect the user to the success or the cancel url, based on the outcome
    return render(request, 'payment/checkout.html')

def payment_success(request):
    for key in list(request.session.keys()):
        if key == 'session_cart_key':
            del request.session[key] # clear the cart by deleting the associated cookies
    return render(request, 'payment/payment_success.html')

def payment_failure(request):
    return render(request, 'payment/payment_failure.html')

