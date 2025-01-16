from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from store.models import ItemProxy
from .cart import Cart

def cart_view(request):
    return render(request, 'cart/cart_view.html')

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'POST': # data sent via AJAX from the item_detail page
        item_id = int(request.POST.get('item_id'))
        item_qty = int(request.POST.get('item_qty'))
    
        item = get_object_or_404(ItemProxy, id=item_id)
        
        cart.add(item=item, quantity=item_qty) # add the item to the session's cart instance 

        cart_qty = cart.__len__()

        response = JsonResponse({'qty': cart_qty, 'item': item.name})
        print('the cart quantity is ' + str(cart_qty))
        return response

def cart_update(request):
    pass

def cart_delete(request):
    pass
