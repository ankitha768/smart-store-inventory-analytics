from django.db import migrations,models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial=True
    dependencies=[("inventory","0001_initial")]
    operations=[migrations.CreateModel(name="Sale",fields=[
        ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
        ("quantity",models.PositiveIntegerField()),
        ("unit_price",models.DecimalField(decimal_places=2,max_digits=10)),
        ("sold_at",models.DateTimeField(auto_now_add=True)),
        ("product",models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name="sales",to="inventory.product"))
    ])]
