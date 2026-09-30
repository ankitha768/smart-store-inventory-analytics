from rest_framework import serializers
from .models import Sale
class SaleSerializer(serializers.ModelSerializer):
    total=serializers.ReadOnlyField()
    class Meta:
        model=Sale
        fields="__all__"
