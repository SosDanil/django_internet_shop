import json

from django.conf import settings
from django.core.management import BaseCommand
import os

from catalog.models import Product, Category


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        file_path = os.path.join(settings.BASE_DIR, 'fixtures', 'catalog_data.json')
        with open(file_path, 'r', encoding='UTF-8') as file:
            data = json.load(file)
        categories = []
        for element in data:
            if element.get('model') == "catalog.category":
                categories.append(element)

        return categories

    @staticmethod
    def json_read_products():
        file_path = os.path.join(settings.BASE_DIR, 'fixtures', 'catalog_data.json')
        with open(file_path, 'r', encoding='UTF-8') as file:
            data = json.load(file)
        products = []
        for element in data:
            if element.get('model') == "catalog.product":
                products.append(element)

        return products

    def handle(self, *args, **options):

        Product.objects.all().delete()
        Category.objects.all().delete()

        product_for_create = []
        category_for_create = []

        for category in Command.json_read_categories():
            category_fields = category.get('fields')
            category_for_create.append(
                Category(pk=category['pk'], name=category_fields['name'], description=category_fields['description'])
            )

        Category.objects.bulk_create(category_for_create)

        for product in Command.json_read_products():
            product_fields = product.get('fields')
            product_for_create.append(
                Product(name=product_fields['name'], description=product_fields['description'],
                        price=product_fields['price'], category=Category.objects.get(pk=product_fields['category']))
            )

        Product.objects.bulk_create(product_for_create)
