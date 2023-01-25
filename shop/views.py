from django.shortcuts import render, get_object_or_404
from .models import Category, Product, SubProduct
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    subproduct = SubProduct.objects.all()
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'subproduct': subproduct, 'cart_product_form': cart_product_form})


# def subproduct_detail(request):
#     subproduct = SubProduct.objects.name
#
#     return render(request,
#                   'shop/product/subproduct_detail.html',
#                   {'subproduct': subproduct})
