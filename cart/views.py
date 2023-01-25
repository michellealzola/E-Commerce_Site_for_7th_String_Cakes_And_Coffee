from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product, SubProduct
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm


@require_POST
def cart_add(request, subproduct_id):
    cart = Cart(request)
    subproduct = get_object_or_404(SubProduct, id=subproduct_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(subproduct=subproduct,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, subproduct_id):
    cart = Cart(request)
    subproduct = get_object_or_404(SubProduct, id=subproduct_id)
    cart.remove(subproduct)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})
