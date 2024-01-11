from django.shortcuts import render
from django.shortcuts import  get_object_or_404
from .models import Category, Product
from django.views.generic import ListView, DetailView,View
# Create your views here.

class all_products(ListView):
    template_name = 'Market/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Filter the products with is_active=True
        return Product.products.filter(is_active=True)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug,in_stock=True)
    return render(request,"Market/detail.html",{'product': product})
def category_list(request,category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products= Product.products.filter(category=category)
    return render(request,'Market/category.html',{'category': category,'products':products})