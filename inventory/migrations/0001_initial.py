from django.db import migrations,models
class Migration(migrations.Migration):
    initial=True
    dependencies=[]
    operations=[migrations.CreateModel(name="Product",fields=[
        ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
        ("name",models.CharField(max_length=150)),
        ("sku",models.CharField(max_length=50,unique=True)),
        ("category",models.CharField(max_length=100)),
        ("unit_price",models.DecimalField(decimal_places=2,max_digits=10)),
        ("stock_quantity",models.PositiveIntegerField(default=0)),
        ("reorder_level",models.PositiveIntegerField(default=10)),
        ("created_at",models.DateTimeField(auto_now_add=True))
    ])]
