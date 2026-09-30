from django.db import models
from inventory.models import Product
class Sale(models.Model):
    product=models.ForeignKey(Product,on_delete=models.PROTECT,related_name="sales")
    quantity=models.PositiveIntegerField()
    unit_price=models.DecimalField(max_digits=10,decimal_places=2)
    sold_at=models.DateTimeField(auto_now_add=True)
    @property
    def total(self): return self.quantity*self.unit_price
