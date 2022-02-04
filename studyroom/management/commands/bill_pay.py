from django.core.management.base import BaseCommand
from django.utils import timezone

import sqlite3
import pandas as pd
from pandas import Series, DataFrame
from datetime import datetime
from dateutil.relativedelta import relativedelta

from studyroom.models import Bill, Pay

class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):

        con = sqlite3.connect("db.sqlite3")

        bill_mt = '202202'
        pay_mt = '202201'
        bill_status = 'FP'
        pay_status = 'CO'

        sql = "select sb.id as bill_id, sb.account_id, sp.id as pay_id, sp.pay_amt , substring(sp.pay_date ,1,8) as pay_dt \
        from studyroom_bill sb, studyroom_pay sp \
        where sb.bill_mt = \'" + bill_mt + "\' and sb.bill_status = \'OP\' \
        and sp.pay_status = \'OP\' and substring(sp.pay_date,1,6) = \'" + pay_mt + "\' \
        and sb.account_id = sp.account_id and sb.bill_amt = sp.pay_amt"

        pay_list = pd.read_sql(sql, con, index_col=None)

        for i in pay_list.index:
            bill = Bill.objects.get(pk= pay_list.at[i, 'bill_id'])
            #account_id = pay_list.at[i, 'account_id']
            bill.pay_id = pay_list.at[i, 'pay_id']
            bill.pay_amt = pay_list.at[i, 'pay_amt']
            bill.pay_dt = pay_list.at[i, 'pay_dt']
            bill.bill_status = 'FP'
            bill.save()

            pay = Pay.objects.get(pk= pay_list.at[i, 'pay_id'])
            pay.pay_status = 'CO'

            pay.save()