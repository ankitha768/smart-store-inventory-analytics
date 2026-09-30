from rest_framework import viewsets
from .models import Sale
from .serializers import SaleSerializer
class SaleViewSet(viewsets.ModelViewSet):
    queryset=Sale.objects.select_related("product").order_by("-sold_at")
    serializer_class=SaleSerializer
    def perform_create(self,serializer):
        sale=serializer.save()
        product=sale.product
        product.stock_quantity=max(0,product.stock_quantity-sale.quantity)
        product.save(update_fields=["stock_quantity"])
