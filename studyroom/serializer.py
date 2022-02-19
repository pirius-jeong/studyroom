from django.core import serializers
from rest_framework import serializers
from .models import Pay, Account
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = ['pay_status', 'pay_type', 'pay_date', 'pay_amt', 'payer', 'account', 'create_date']
