import redis
from django.conf import settings
from .models import Product, SubProduct

# connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


class Recommender:
    def get_product_key(self, id):
        return f'product:{id}:purchased_with'

    def products_bought(self, subproducts):
        subproduct_ids = [p.id for p in subproducts]
        for subproduct_id in subproduct_ids:
            for with_id in subproduct_ids:
                # get the other products bought with each product
                if subproduct_id != with_id:
                    # increment score for product purchased together
                    r.zincrby(self.get_product_key(subproduct_id),
                              1,
                              with_id)


def suggest_products_for(self, subproducts, max_results=6):
    subproduct_ids = [p.id for p in subproducts]
    if len(subproducts) == 1:
        # only 1 product
        suggestions = r.zrange(
            self.get_product_key(subproduct_ids[0]),
            0, -1, desc=True)[:max_results]
    else:
        # generate a temporary key
        flat_ids = ''.join([str(id) for id in subproduct_ids])
        tmp_key = f'tmp_{flat_ids}'
        # multiple products, combine scores of all products
        # store the resulting sorted set in a temporary key
        keys = [self.get_product_key(id) for id in subproduct_ids]
        r.zunionstore(tmp_key, keys)
        # remove ids for the products the recommendation is for
        r.zrem(tmp_key, *subproduct_ids)
        # get the product ids by their score, descendant sort
        suggestions = r.zrange(tmp_key, 0, -1,
                               desc=True)[:max_results]
        # remove the temporary key
        r.delete(tmp_key)
    suggested_products_ids = [int(id) for id in suggestions]
    # get suggested products and sort by order of appearance
    suggested_products = list(SubProduct.objects.filter(
        id__in=suggested_products_ids))
    suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
    return suggested_products


def clear_purchases(self):
    for id in SubProduct.objects.values_list('id', flat=True):
        r.delete(self.get_product_key(id))
