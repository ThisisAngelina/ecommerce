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
        sum = sum(item['qty'] for item in self.cart.values())
        print(f"there are {sum} items in the cart")
        return sum
    

    
    def add(self, item, quantity):
        item_id = str(item.id)

        if item_id not in self.cart: # if the product is not yet in the cart, add the product
            self.cart[item_id] = {'qty': quantity, 'price': str(item.price)}

        else: # otherwise, update the quantity
            self.cart[item_id]['qty'] = quantity

        self.session.modified = True

