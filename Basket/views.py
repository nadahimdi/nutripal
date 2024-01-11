from django.shortcuts import render
from .basket import Basket
from django.shortcuts import get_list_or_404,get_object_or_404
from  Market.models import Product
from django.http import JsonResponse

# Create your views here.
def yourbasket(request):
    basket = Basket(request)
    return render(request,'basket/yourbasket.html', {'basket': basket})
def basketadd(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)
        basketqty=basket.__len__()
        response = JsonResponse({'qty':basketqty})
        return response


def basket_delete(request):
    basket = Basket(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()

        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)
        
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        totalprice=basket.getprice(product=product_id, qty=product_qty)
        total = basket.get_plus_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal,'totalprice': totalprice, 'total': total})
        return response