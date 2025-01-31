from decimal import Decimal

from store.models import ItemProxy

class Cart():
    def __init__(self, request) -> None:

        # Grab the cart from the cookies. If there is not initialized cart, create one and add it to the cookies
        self.session = request.session

        cart = self.session.get('session_cart_key') #session_key is the key chosen to store the cart object under

        if not cart:
            cart = self.session['session_cart_key'] = {}

        self.cart = cart

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())
    
    def __iter__(self):
        item_ids = self.cart.keys()
        items = ItemProxy.objects.filter(id__in=item_ids)
        cart = self.cart.copy() # create a shallow copy of the cart

        for item in items:
            cart[str(item.id)]['item'] = item # assign the entire item object to the 'item' key of the cart dictionary

        for item in cart.values():  
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['qty']
            yield item


    def add(self, item, quantity):
        item_id = str(item.id)

        if item_id not in self.cart: # if the product is not yet in the cart, add the product
            self.cart[item_id] = {'qty': quantity, 'price': str(item.price)}

        else: # otherwise, update the quantity
            self.cart[item_id]['qty'] = quantity

        self.session.modified = True

    def delete(self, item_id):
        item_id = str(item_id)


        if item_id in self.cart:
            del self.cart[item_id]
            self.session.modified = True

    def update(self, item_id, quantity):
        item_id = str(item_id)
        quantity = quantity


        if item_id in self.cart:
            self.cart[item_id]['qty'] = quantity
            self.session.modified = True

    def get_total_value(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

 