from django.core import serializers
from rest_framework import serializers
from .models import Pay, Account

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = ['pay_status', 'pay_type', 'pay_date', 'pay_amt', 'payer', 'create_date']

    pay_type = serializers.CharField()
    pay_date = serializers.CharField()
    pay_amt = serializers.IntegerField()
    payer = serializers.CharField()
    pay_status = serializers.CharField()
    create_date = serializers.DateTimeField()