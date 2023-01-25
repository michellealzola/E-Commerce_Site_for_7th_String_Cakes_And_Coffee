from decimal import Decimal
from django.conf import settings
from shop.models import Product, SubProduct
from coupons.models import Coupon


class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        self.coupon_id = self.session.get('coupon_id')

    def add(self, subproduct, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        subproduct_id = str(subproduct.id)
        if subproduct_id not in self.cart:
            self.cart[subproduct_id] = {'quantity': 0,
                                        'price': str(subproduct.price)}
        if override_quantity:
            self.cart[subproduct_id]['quantity'] = quantity
        else:
            self.cart[subproduct_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, subproduct):
        """
        Remove a product from the cart.
        """
        subproduct_id = str(subproduct.id)
        if subproduct_id in self.cart:
            del self.cart[subproduct_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        subproduct_ids = self.cart.keys()
        # get the product objects and add them to the cart
        subproducts = SubProduct.objects.filter(id__in=subproduct_ids)
        cart = self.cart.copy()
        for subproduct in subproducts:
            cart[str(subproduct.id)]['subproduct'] = subproduct
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    # def get_total_price(self):
    #     return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_gst(self):

        return "{:0.2f}".format(float(self.get_sub_total_price()) * .05)

    def get_sub_total_price(self):

        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_price(self):

        return "{:0.2f}".format(float(self.get_sub_total_price()) + float(self.get_gst()))

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return "{:0.2f}".format(float(self.coupon.discount) / (float(Decimal(100))) * (float(self.get_total_price())))
        return "{:0.2f}".format(float(Decimal(0)))

    def get_total_price_after_discount(self):
        return "{:0.2f}".format(float(self.get_total_price()) - float(self.get_discount()))

