from Market.models import Product
from decimal import Decimal
from django.conf import settings
from checkout.models import DeliveryOptions
class Basket():



    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}

        self.save()

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item
    


# Assume product_ids is [1, 2, 3]
# Example products in the database:
# Product(id=1, name='Item 1', price=10.99)
# Product(id=2, name='Item 2', price=19.99)
# Product(id=3, name='Item 3', price=5.99)

# Initial basket
# {'1': {'price': 10.99, 'qty': 2}, '2': {'price': 19.99, 'qty': 1}}

# After the code execution:

# Iteration 1:
#   product = Product(id=1, name='Item 1', price=10.99)
#   basket['1']['product'] = Product(id=1, name='Item 1', price=10.99)

# Iteration 2:
#   product = Product(id=2, name='Item 2', price=19.99)
#   basket['2']['product'] = Product(id=2, name='Item 2', price=19.99)

# Iteration 3:
#   product = Product(id=3, name='Item 3', price=5.99)
#   basket['3']['product'] = Product(id=3, name='Item 3', price=5.99)

# Final basket:
# {'1': {'price': 10.99, 'qty': 2, 'product': Product(id=1, name='Item 1', price=10.99)},
#  '2': {'price': 19.99, 'qty': 1, 'product': Product(id=2, name='Item 2', price=19.99)},
#  '3': {'price': 5.99, 'qty': 1, 'product': Product(id=3, name='Item 3', price=5.99)}}



    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())
    



    def save(self):
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def get_plus_price(self):
        newprice = 0.00
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        total = subtotal + Decimal(newprice)
        return total
    
    def get_delivery_price(self):
        newprice = 0.00

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        return newprice

    def delete(self, product):

        product_id = str(product)
      
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()  

    def update(self,product,qty):
         product_id = str(product)
         product_qty = qty
       

         self.basket[product_id]['qty']= product_qty
         self.save()
    def getprice(self,product,qty):
        product_id = str(product)
        products = Product.objects.get(id=product_id)
        return products.price*qty
        

    def clear(self):
        # Remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        del self.session["address"]
        del self.session["purchase"]
        self.save()



    def basket_update_delivery(self, deliveryprice=0):
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())
        total = subtotal + Decimal(deliveryprice)
        return total

        