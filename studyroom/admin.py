from django.contrib import admin
from .models import Absence, Account, Bill, PricePlan, Pay, Student, Sugang, Sms

admin.site.register(Absence)
admin.site.register(Account)
admin.site.register(Bill)
admin.site.register(PricePlan)
admin.site.register(Pay)
admin.site.register(Student)
admin.site.register(Sugang)
admin.site.register(Sms)