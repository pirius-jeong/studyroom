from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    class Grade(models.TextChoices):
        YEAR_6 = 'Y6'
        YEAR_7 = 'Y7'
        ELEMENTARY_1 = 'E1'
        ELEMENTARY_2 = 'E2'
        ELEMENTARY_3 = 'E3'
        ELEMENTARY_4 = 'E4'
        ELEMENTARY_5 = 'E5'
        ELEMENTARY_6 = 'E6'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brother = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=20)
    grade = models.CharField(max_length=2, choices=Grade.choices)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    delete_yn = models.CharField(max_length=1, default='n')


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sub_student_id = models.IntegerField(null=True, blank=True)
    payer = models.CharField(max_length=40, null=True, blank=True)
    payer_phone_num = models.CharField(max_length=11, null=True, blank=True)
    brother_dc_yn = models.CharField(max_length=1, default='n')
    recommend_dc_start = models.CharField(max_length=6, null=True, blank=True, default='yyyymm')
    recommend_dc_end = models.CharField(max_length=6, null=True, blank=True, default='yyyymm')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)


class PricePlan(models.Model):
    class Grade(models.TextChoices):
        YEAR_6 = 'Y6'
        YEAR_7 = 'Y7'
        ELEMENTARY_1 = 'E1'
        ELEMENTARY_2 = 'E2'
        ELEMENTARY_3 = 'E3'
        ELEMENTARY_4 = 'E4'
        ELEMENTARY_5 = 'E5'
        ELEMENTARY_6 = 'E6'

    class SugangType(models.TextChoices):
        Day3 = 'D3'
        Day4 = 'D4'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, choices=Grade.choices)
    sugang_type = models.CharField(max_length=2, choices=SugangType.choices)
    price = models.IntegerField()
    refund = models.IntegerField()
    start_mt = models.CharField(max_length=6, default='yyyymm')
    end_mt = models.CharField(max_length=6, default='999912')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)


class Sugang(models.Model):
    class ClassId(models.TextChoices):
        Mikyoung = 'MK'
        Aekyoung = 'AK'

    class Weekday(models.TextChoices):
        Monday = 'MON'
        Tuesday = 'TUE'
        Wednesday = 'WED'
        Thursday = 'THU'
        Friday = 'FRI'

    class Time(models.TextChoices):
        One_Oclock = '1'
        Two_Oclock = '2'
        Three_Oclock = '3'
        Four_Oclock = '4'
        Five_Oclock = '5'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_id = models.CharField(max_length=2, choices=ClassId.choices)
    weekday = models.CharField(max_length=3, choices=Weekday.choices)
    time = models.CharField(max_length=1, choices=Time.choices)
    start_mt = models.CharField(max_length=6, default='yyyymm')
    end_mt = models.CharField(max_length=6, default='999912')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)


class Bill(models.Model):
    class BillStatus(models.TextChoices):
        Open = 'OP'
        Full_Payment = 'FP'
        Partial_Payment = 'PP'

    class PayType(models.TextChoices):
        KimpoPay = 'KP'
        AccountTransfer = 'AT'

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    bill_status = models.CharField(max_length=2, choices=BillStatus.choices)
    bill_mt = models.CharField(max_length=6)
    bill_amt = models.IntegerField(null=True, blank=True)
    base_amt = models.IntegerField(null=True, blank=True)
    refund_amt = models.IntegerField(null=True, blank=True)
    brother_dc_amt = models.IntegerField(null=True, blank=True)
    recommend_dc_amt = models.IntegerField(null=True, blank=True)
    pay_amt = models.IntegerField(null=True, blank=True)
    pay_type = models.CharField(max_length=2, choices=PayType.choices, null=True, blank=True)
    pay_dt = models.CharField(max_length=8, null=True, blank=True)
    pay_id = models.IntegerField(null=True, blank=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(auto_now=True)


class Pay(models.Model):
    class PayType(models.TextChoices):
        KimpoPay = 'KP'
        AccountTransfer = 'AT'

    class PayStatus(models.TextChoices):
        Open = 'OP'
        Close = 'CO'

    pay_date = models.CharField(max_length=14, default='yyyymmddhhmmss')
    pay_amt = models.IntegerField()
    payer = models.CharField(max_length=30, null=True, blank=True)
    pay_status = models.CharField(max_length=2, choices=PayStatus.choices)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(auto_now=True)


class Absence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    absence_dt = models.CharField(max_length=8, default='yyyymmdd')
    absence_detail = models.TextField(default='결석사유:')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(auto_now=True)

