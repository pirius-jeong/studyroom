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

    def __str__(self):
        if self.brother:
            template = '{0.name} {0.grade} {0.brother.name}'
            return template.format(self)
        template = '{0.name} {0.grade}'
        return template.format(self)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brother = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=20)
    grade = models.CharField(max_length=2, choices=Grade_choices)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    delete_yn = models.CharField(max_length=1, default='n')


class Account(models.Model):
    def __str__(self):
        if self.student.brother:
            return (self.student.name, self.student.brother.name)
        return (self.student.name)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payer = models.CharField(max_length=40, null=True, blank=True)
    payer_phone_num = models.CharField(max_length=11, null=True, blank=True)
    sms_phone_num = models.CharField(max_length=11, null=True, blank=True)
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

    def __str__(self):
        return (self.grade, self.sugang_type, self.start_mt, self.end_mt)

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

    def __str__(self):
        return (self.student.name, self.class_id, self.weekday, self.time, self.start_mt, self.end_mt)
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

    def __str__(self):
        return (self.account.student.name, self.bill_mt)

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

    def __str__(self):
        return (self.pay_date, self.pay_type, self.pay_amt)
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
    absence_detail = models.CharField(max_length=60,default='결석사유:')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(auto_now=True)

class Sms(models.Model):
    statusCode_choices = (
        ('200', 'OK'),
        ('202', 'Accept'),
        ('400', 'Bad Request'),
        ('401', 'Unauthorized'),
        ('403', 'Forbidden'),
        ('404', 'Not Found'),
        ('429', 'Too Many Requests'),
        ('500', 'Internal Server Error'),
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    smstype = models.CharField(max_length=3)
    to = models.CharField(max_length=11)
    subject = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField(max_length=2000)
    requestId = models.CharField(max_length=32, null=True, blank=True)
    requestTime = models.CharField(max_length=50, null=True, blank=True)
    statusCode = models.CharField(max_length=3, null=True, blank=True, choices=statusCode_choices)
    statusName = models.CharField(max_length=10, null=True, blank=True)
    messageId = models.CharField(max_length=23, null=True, blank=True)
    messageStatus = models.CharField(max_length=15, null=True, blank=True)
    create_date = models.DateTimeField()

