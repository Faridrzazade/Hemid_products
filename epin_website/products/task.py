from celery import shared_task
from .models import *

@shared_task
def increment_product_views(product_id):
    product = Product.objects.get(id=product_id)
    product.views += 1
    product.save()