from django.core import serializers
from rest_framework import serializers
from .models import Pay, Account

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = ['pay_status', 'pay_type', 'pay_date', 'pay_amt', 'payer', 'account', 'create_date']

    pay_type = serializers.CharField()
    pay_date = serializers.CharField()
    pay_amt = serializers.IntegerField()
    payer = serializers.CharField()
    pay_status = serializers.CharField()
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    create_date = serializers.DateTimeField()