from django.db import models
class Product(models.Model):
    name=models.CharField(max_length=150)
    sku=models.CharField(max_length=50,unique=True)
    category=models.CharField(max_length=100)
    unit_price=models.DecimalField(max_digits=10,decimal_places=2)
    stock_quantity=models.PositiveIntegerField(default=0)
    reorder_level=models.PositiveIntegerField(default=10)
    created_at=models.DateTimeField(auto_now_add=True)
    def needs_reorder(self): return self.stock_quantity <= self.reorder_level
    def __str__(self): return f"{self.sku} - {self.name}"
