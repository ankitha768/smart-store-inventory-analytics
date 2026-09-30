from django.db.models import Sum,F,ExpressionWrapper,DecimalField
from rest_framework.views import APIView
from rest_framework.response import Response
from inventory.models import Product
from sales.models import Sale
class SummaryView(APIView):
    def get(self,request):
        products=Product.objects.all()
        sales=Sale.objects.all()
        revenue=sales.aggregate(total=Sum(ExpressionWrapper(F("quantity")*F("unit_price"),output_field=DecimalField())))["total"] or 0
        reorder=list(products.filter(stock_quantity__lte=F("reorder_level")).values("sku","name","stock_quantity","reorder_level"))
        return Response({"product_count":products.count(),"units_in_stock":sum(p.stock_quantity for p in products),"sales_count":sales.count(),"revenue":revenue,"reorder_alerts":reorder})
