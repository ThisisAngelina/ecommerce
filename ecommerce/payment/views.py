import logging
from decimal import Decimal
import stripe 
import weasyprint
from django.contrib import messages
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404, HttpResponse
from django.urls import reverse
from django.shortcuts import get_list_or_404, redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.templatetags.static import static

from django.conf import settings

from cart.cart import Cart # the Cart class

from .models import Order, OrderItem, ShippingAddress
from .forms import ShippingAddressForm


# needed for stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

logger = logging.getLogger(__name__) 

def checkout(request):
    
    if request.user.is_authenticated:
        user=request.user
    else:
        user = None # handle cases of users that are not authenticated making a purchase #TODO to check if this works 
    try:
        shipping_address = ShippingAddress.objects.get(user=user) # the user already has a shipping address associated with them
    except ShippingAddress.DoesNotExist:
        shipping_address = None # there is not record of the user's address in the db yet

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_address) # the ModelForm updates the model instance with the values from request.POST
        if form.is_valid():
            shipping_address = form.save(commit=False) #update the user address in the database based on the information submitted through the form
            shipping_address.user = user
            shipping_address.save()

            cart = Cart(request) # create a Cart instance
            try:
                cart_total = cart.get_total_value()
            except:
                logger.error("Error calculating the total value of the cart at checkout")

            order = Order.objects.create(user=user, shipping_address=shipping_address, amount=cart_total) # create a new order instance

            # create Stripe session data for Stripe checkout
            session_data = {
                    'mode': 'payment',
                    'success_url': request.build_absolute_uri(reverse('payment:payment_success')),
                    'cancel_url': request.build_absolute_uri(reverse('payment:payment_failure')),
                    'line_items': []
                }
            
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

            try:
                session = stripe.checkout.Session.create(**session_data)
            except:
                logger.error('Error creating a Stripe checkout session at checkout')
            return redirect(session.url, code=303) # redirect the user to the success or the cancel url, based on the outcome
        else:
            # the submitted form was not valid
            messages.error(request, "There was an error with your shipping details. Please check the form.")
            logger.warning(f"Checkout form validation failed for user {user}: {form.errors}") 

    else: # request method is not POST:
        form = ShippingAddressForm(instance=shipping_address)
        return render(request, 'payment/checkout.html', {'form': form})

def payment_success(request):
    for key in list(request.session.keys()):
        if key == 'session_cart_key':
            del request.session[key] # clear the cart by deleting the associated cookies
    return render(request, 'payment/payment_success.html')

def payment_failure(request):
    return render(request, 'payment/payment_failure.html')


# admin functionality

@staff_member_required
def admin_order_pdf(request, order_id):
    ''' allows the admin to generate a pdf recap of an order '''

    try:
        order = Order.objects.select_related('user', 'shipping_address').get(id=order_id)
    except Order.DoesNotExist:
        raise Http404("This order wasn't found")
    html = render_to_string('payment/order/pdf/pdf_invoice.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    css_path = finders.find('payment/css/admin_order_pdf.css')
    stylesheets = [weasyprint.CSS(css_path)]
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=stylesheets)
    try:
        return response
    except Exception as e:  
        logger.error(f"Error generating admin order PDF: {e}")  