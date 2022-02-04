from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    Grade_choices = (
        ('Y6','6세'),
        ('Y7','7세'),
        ('E1','1학년'),
        ('E2','2학년'),
        ('E3','3학년'),
        ('E4','4학년'),
        ('E5','5학년'),
        ('E6','6학년'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brother = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=20)
    grade = models.CharField(max_length=2, choices=Grade_choices)
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
    Grade_choices = (
        ('Y6', '6세'),
        ('Y7', '7세'),
        ('E1', '1학년'),
        ('E2', '2학년'),
        ('E3', '3학년'),
        ('E4', '4학년'),
        ('E5', '5학년'),
        ('E6', '6학년'),
    )

    class SugangType(models.TextChoices):
        Day3 = 'D3'
        Day4 = 'D4'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, choices=Grade_choices)
    sugang_type = models.CharField(max_length=2, choices=SugangType.choices)
    price = models.IntegerField()
    refund = models.IntegerField()
    start_mt = models.CharField(max_length=6, default='yyyymm')
    end_mt = models.CharField(max_length=6, default='999912')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)


class Sugang(models.Model):
    ClassId_choices = (
        ('MK','심미경'),
        ('AK','심애경'),
    )

    class Weekday(models.TextChoices):
        월요일 = 'MON'
        화요일 = 'TUE'
        수요일 = 'WED'
        목요일 = 'THU'
        금요일 = 'FRI'

    Time_choices = (
        ('1', '1시'),
        ('2', '2시'),
        ('3', '3시'),
        ('4', '4시'),
        ('5', '5시'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_id = models.CharField(max_length=2, choices=ClassId_choices)
    weekday = models.CharField(max_length=3, choices=Weekday.choices)
    time = models.CharField(max_length=1, choices=Time_choices)
    start_mt = models.CharField(max_length=6, default='yyyymm')
    end_mt = models.CharField(max_length=6, default='999912')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)


class Bill(models.Model):
    BillStatus_choices = (
        ('OP', '발행'),
        ('FP', '완납'),
        ('PP', '부분납'),
    )

    class PayType(models.TextChoices):
        김포페이 = 'KP'
        계좌이체 = 'AT'

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    bill_status = models.CharField(max_length=2, choices=BillStatus_choices)
    bill_mt = models.CharField(max_length=6)
    bill_amt = models.IntegerField(null=True, blank=True)
    base_amt = models.IntegerField(null=True, blank=True)
    brother_base_amt = models.IntegerField(null=True, blank=True, default=0)
    refund_amt = models.IntegerField(null=True, blank=True, default=0)
    brother_refund_amt = models.IntegerField(null=True, blank=True, default=0)
    brother_dc_amt = models.IntegerField(null=True, blank=True, default=0)
    recommend_dc_amt = models.IntegerField(null=True, blank=True, default=0)
    pay_amt = models.IntegerField(null=True, blank=True, default=0)
    pay_type = models.CharField(max_length=2, choices=PayType.choices, null=True, blank=True)
    pay_dt = models.CharField(max_length=8, null=True, blank=True)
    pay_id = models.IntegerField(null=True, blank=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(auto_now=True)


class Pay(models.Model):
    class PayType(models.TextChoices):
        김포페이 = 'KP'
        계좌이체 = 'AT'

    class PayStatus(models.TextChoices):
        등록 = 'OP'
        Close = 'CO'

    pay_type = models.CharField(max_length=2, choices=PayType.choices)
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

