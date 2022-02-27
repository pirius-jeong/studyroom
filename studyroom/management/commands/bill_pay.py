from django.core.management.base import BaseCommand

import sqlite3
import pandas as pd
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

from studyroom.models import Bill, Pay

class Command(BaseCommand):
    help = 'bill, pay concatenate'

    def handle(self, *args, **options):

        con = sqlite3.connect("db.sqlite3")

        pay_list = pd.read_sql("select sb.id as bill_id, sb.bill_mt, sp.id as pay_id, sp.pay_amt , substr(sp.pay_date ,1,8) as pay_dt \
                                from studyroom_bill sb, studyroom_pay sp, studyroom_account sa \
                                where sb.bill_status = \'OP\' and sp.pay_status = \'OP\'  \
                                and sb.account_id = sa.id \
                                and sa.payer_phone_num = sp.payer and sb.bill_amt = sp.pay_amt", \
                    con, index_col=None)

        print("============ bill_pay ===========================================")

        for i in pay_list.index:
            pay_dt = pay_list.at[i, 'pay_dt'][-2:]
            pay_mt = pay_list.at[i, 'pay_dt'][4:6]
            pay_yt = pay_list.at[i, 'pay_dt'][:4]
            if pay_dt < '10':
                bill_mt = str(pay_yt) + str(pay_mt)
            else:
                bill_mt = (date(int(pay_yt), int(pay_mt), int(pay_dt)) + relativedelta(months=1)).strftime("%Y%m")

            if pay_list.at[i, 'bill_mt'] == bill_mt:
                print(datetime.today(),'bill_mt:', pay_list.iloc[i].bill_mt,'pay_dt:', pay_list.iloc[i].pay_dt,'pay_mt:', bill_mt, '==> Bill-Pay concatenated')

                bill = Bill.objects.get(pk=pay_list.at[i, 'bill_id'])
                bill.pay_id = pay_list.at[i, 'pay_id']
                bill.pay_amt = pay_list.at[i, 'pay_amt']
                bill.pay_dt = pay_list.at[i, 'pay_dt']
                bill.bill_status = 'FP'
                bill.save()

                pay = Pay.objects.get(pk=pay_list.at[i, 'pay_id'])
                pay.pay_status = 'CO'
                pay.bill = bill
                pay.save()

            else:
                print(datetime.today(),'bill_mt:', pay_list.iloc[i].bill_mt,'pay_dt:',pay_list.iloc[i].pay_dt,'pay_mt:', bill_mt, '==> Bill-Pay mismatch')
