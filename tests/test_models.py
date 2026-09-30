import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","config.settings")
import django
django.setup()
import pytest
from inventory.models import Product
@pytest.mark.django_db
def test_reorder_flag():
    product=Product.objects.create(name="Test",sku="TEST-1",category="Demo",unit_price=10,stock_quantity=2,reorder_level=5)
    assert product.needs_reorder() is True
