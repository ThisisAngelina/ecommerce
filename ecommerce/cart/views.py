import logging

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from store.models import ItemProxy
from .cart import Cart

logger = logging.getLogger(__name__)  

def cart_view(request):
    cart = Cart(request)
    context = {'cart': cart}
    return render(request, 'cart/cart_view.html', context)

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'POST': # data sent via AJAX from the item_detail page
        item_id = int(request.POST.get('item_id'))
        item_qty = int(request.POST.get('item_qty'))
    
        item = get_object_or_404(ItemProxy, id=item_id)
        
        cart.add(item=item, quantity=item_qty) # add the item to the session's cart instance 

        cart_qty = cart.__len__()

        response = JsonResponse({'qty': cart_qty, 'item': item.name})
    
        return response

def cart_update(request):
    cart = Cart(request)
     
    if request.POST.get('action') == 'POST':
        item_id = int(request.POST.get('item_id'))
        quantity = int(request.POST.get('item_qty'))
        cart.update(item_id=item_id, quantity=quantity)


        #recalculate the values for the cart total and the number of items in the cart 
        try:
            cart_qty = cart.__len__()
        except:
            logger.error('Error calculating the cart item quantity')
        try:
            cart_total = cart.get_total_value()
        except:
            logger.error('Error calculating the cart total')

        response = JsonResponse({'qty': cart_qty, 'total': cart_total})
        return response 
    



def cart_delete(request):
    cart = Cart(request)
     
    if request.POST.get('action') == 'POST':
        item_id = int(request.POST.get('item_id'))
        cart.delete(item_id=item_id)

        #recalculate the values for the cart total and the number of items in the cart 
        try:
            cart_qty = cart.__len__()
        except:
            logger.error('Error calculating the cart item quantity')
        try:
            cart_total = cart.get_total_value()
        except:
            logger.error('Error calculating the cart total')

        response = JsonResponse({'qty': cart_qty, 'total': cart_total})
        return response 
    
