from django.conf import settings
from django.core.cache import cache

from catalog.models import Product


def get_products_from_cache():
    """Получает данные по продуктам из кэша; если кэш пуст, то получает из БД"""
    if settings.CACHE_ENABLED:
        key = 'products_list'
        products_list = cache.get(key)
        if products_list is None:
            products_list = Product.objects.all()
            cache.set(key, products_list)
    else:
        products_list = Product.objects.all()

    return products_list
