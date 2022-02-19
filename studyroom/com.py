import sqlite3
import pandas as pd
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from studyroom.models import Bill, Student

def bill_dml(bill_id=''):
    con = sqlite3.connect("db.sqlite3")

    if bill_id != '': # 청구서 재발행
        print('=== bill-id:',bill_id,'청구서 재발행')
        bill = Bill.objects.get(pk=bill_id)
        bill_mt = bill.bill_mt
    else:
        bill_mt = (datetime.today() + relativedelta(months=1)).strftime("%Y%m")
    
    absence_mt = (date(int(bill_mt[:4]), int(bill_mt[4:6]), 1) + relativedelta(months=-1)).strftime("%Y%m")
    absence_fr = (date(int(bill_mt[:4]), int(bill_mt[4:6]), 1) + relativedelta(months=-1)).strftime("%Y%m") + '01'
    absence_to = (date(int(bill_mt[:4]), int(bill_mt[4:6]), 1) + relativedelta(months=-1)).strftime("%Y%m") + '31'

    base_amt_list = pd.read_sql("\
                                    select ac.id,  p.price as base_amt from \
                                    (select student_id,\'d\'||count(1) as sugang_type \
                                    from studyroom_sugang \
                                    where %s between start_mt and end_mt \
                                    group by student_id) a, studyroom_student b,studyroom_priceplan p, studyroom_account ac \
                                    where a.student_id = b.id \
                                    and a.sugang_type = p.sugang_type \
                                    and b.grade = p.grade \
                                    and %s between p.start_mt and p.end_mt \
                                    and a.student_id = ac.student_id" % (bill_mt, bill_mt), con, index_col=None)

    brother_base_amt_list = pd.read_sql("\
                                    select ac.id,  p.price as brother_base_amt from \
                                    (select student_id,\'d\'||count(1) as sugang_type \
                                    from studyroom_sugang \
                                    where %s between start_mt and end_mt \
                                    group by student_id) a, studyroom_student b,studyroom_priceplan p, studyroom_account ac, studyroom_student c \
                                    where a.student_id = b.id \
                                    and a.sugang_type = p.sugang_type \
                                    and b.grade = p.grade \
                                    and %s between p.start_mt and p.end_mt \
                                    and b.id = c.brother_id \
                                    and c.id = ac.student_id" % (bill_mt, bill_mt), con, index_col=None)

    recommend_dc_list = pd.read_sql("\
                                    select id, -10000 as recommend_dc_amt from studyroom_account \
                                    where %s between recommend_dc_start  and recommend_dc_end " % (bill_mt), con,
                                    index_col=None)

    brother_dc_list = pd.read_sql("\
                                    select a.id, -0.1 as brother_dc_rate from studyroom_account a, studyroom_student s \
                                    where a.student_id = s.id and s.brother_id is not null", con, index_col=None)

    refund_amt_list = pd.read_sql("\
                                    select ac.id, p.refund*count(1) as refund_amt  from \
                                    (select student_id,\'d\'||count(1) as sugang_type \
                                    from studyroom_sugang \
                                    where %s between start_mt and end_mt \
                                    group by student_id) a, studyroom_student b,studyroom_priceplan p, studyroom_account ac, studyroom_absence ab \
                                    where a.student_id = b.id \
                                    and a.sugang_type = p.sugang_type \
                                    and b.grade = p.grade \
                                    and %s between p.start_mt and p.end_mt \
                                    and a.student_id = ac.student_id \
                                    and ac.student_id = ab.student_id \
                                    and ab.absence_dt between %s and %s \
                                    group by ac.id" % (absence_mt, absence_mt, absence_fr, absence_to), con,
                                  index_col=None)

    brother_refund_amt_list = pd.read_sql("\
                                    select ac.id, p.refund*count(1) as brother_refund_amt  from \
                                    (select student_id,\'d\'||count(1) as sugang_type \
                                    from studyroom_sugang \
                                    where %s between start_mt and end_mt \
                                    group by student_id) a, studyroom_student b,studyroom_priceplan p, studyroom_account ac, studyroom_absence ab, studyroom_student c \
                                    where a.student_id = b.id \
                                    and a.sugang_type = p.sugang_type \
                                    and b.grade = p.grade \
                                    and %s between p.start_mt and p.end_mt \
                                    and a.student_id = ac.student_id \
                                    and c.brother_id = ab.student_id \
                                    and ac.student_id = c.id \
                                    and ab.absence_dt between %s and %s \
                                    group by ac.id" % (absence_mt, absence_mt, absence_fr, absence_to), con,
                                          index_col=None)

    merge1 = pd.merge(base_amt_list, brother_base_amt_list, how='outer', on='id')
    merge2 = pd.merge(merge1, recommend_dc_list, how='outer', on='id')
    merge3 = pd.merge(merge2, brother_dc_list, how='outer', on='id')
    merge4 = pd.merge(merge3, refund_amt_list, how='outer', on='id')
    merge5 = pd.merge(merge4, brother_refund_amt_list, how='outer', on='id')
    bill_list = merge5.fillna(0)

    if bill_id == '': # 정기 청구
        print('=== 정기청구 : bill_id',bill_id)
        for i in bill_list.index:
            account_id = bill_list.at[i, 'id']
            bill_status = 'OP'
            base_amt = bill_list.at[i, 'base_amt']
            brother_base_amt = bill_list.at[i, 'brother_base_amt']
            recommend_dc_amt = bill_list.at[i, 'recommend_dc_amt']
            refund_amt = bill_list.at[i, 'refund_amt']
            brother_refund_amt = bill_list.at[i, 'brother_refund_amt']
            brother_dc_amt = (base_amt + brother_base_amt + refund_amt + brother_refund_amt) * bill_list.at[
                i, 'brother_dc_rate']
            bill_amt = base_amt + brother_base_amt + refund_amt + brother_refund_amt + brother_dc_amt + recommend_dc_amt

            bill = Bill(bill_mt=bill_mt, account_id=account_id, bill_status=bill_status, bill_amt=bill_amt,
                        base_amt=base_amt, brother_base_amt=brother_base_amt, refund_amt=refund_amt,
                        brother_refund_amt=brother_refund_amt, brother_dc_amt=brother_dc_amt,
                        recommend_dc_amt=recommend_dc_amt, create_date=timezone.now())

            bill.save()
        print('== 정기 청구 : ', len(bill_list), '건, 청구월 : ', bill_mt)


    else:  # 청구서 재발행
        print('=== 청구서 재발행')
        bill = Bill.objects.get(pk=bill_id)
        account_id = bill.account.id
        rebill = bill_list.loc[bill_list['id'] == account_id]
        rebill.reset_index(drop=True, inplace=True)

        bill.bill_status = 'OP'
        bill.base_amt = rebill.iloc[0].base_amt
        bill.brother_base_amt = rebill.iloc[0].brother_base_amt
        bill.refund_amt = rebill.iloc[0].refund_amt
        bill.brother_refund_amt = rebill.iloc[0].brother_refund_amt
        bill.brother_dc_amt = (bill.base_amt + bill.brother_base_amt + bill.refund_amt + bill.brother_refund_amt) * rebill.iloc[0].brother_dc_rate
        bill.recommend_dc_amt = rebill.iloc[0].recommend_dc_amt
        bill.create_date = timezone.now()
        bill.bill_amt = bill.base_amt + bill.brother_base_amt + bill.refund_amt + bill.brother_refund_amt + bill.brother_dc_amt + bill.recommend_dc_amt
        bill.save()
