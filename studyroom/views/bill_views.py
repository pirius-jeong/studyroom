from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from studyroom.models import Bill, Pay
#from studyroom.com import bill_dml

import sqlite3
import pandas as pd
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from studyroom.models import Bill, Student, Account, Absence, Sugang, PricePlan

import logging
logger = logging.getLogger('studyroom')


def bill_dml(bill_id):

    print('===  청구서 재발행 bill-id:', bill_id)
    bill = Bill.objects.get(pk=bill_id)
    account = Account.objects.get(pk=bill.account_id)
    student = Student.objects.get(pk=account.student_id)
    bill_mt = bill.bill_mt
    print("청구월:", bill_mt)
    absence_mt = (date(int(bill_mt[:4]), int(bill_mt[4:6]), 1) + relativedelta(months=-1)).strftime("%Y%m")
    print("결석월:", absence_mt)


    s = Sugang.objects.raw("select id,\'d\'||count(1) as sugang_type from studyroom_sugang \
                                            where %s between start_mt and end_mt \
                                            and student_id = %s", [bill_mt, student.id])[0]
    print("수강Type:", s.sugang_type)

    brother_base_amt = 0
    brother_refund_amt = 0
    brother_dc_amt = 0

    sp = PricePlan.objects.raw("select id, price from studyroom_priceplan \
                                        where grade = %s and sugang_type = %s \
                                        and %s between start_mt and end_mt", [student.grade, s.sugang_type, bill_mt])[0]
    base_amt = sp.price
    print("수강료:", base_amt)

    srp = PricePlan.objects.raw("select id, refund from studyroom_priceplan \
                                                        where grade = %s and sugang_type = %s \
                                                        and %s between start_mt and end_mt",
                                [student.grade, s.sugang_type, absence_mt])[0]
    print("환불기준:", srp.refund)

    sa = Absence.objects.raw("select id, absence_days from studyroom_absence \
                                                where student_id = %s and absence_mt = %s", [student.id, absence_mt])
    if len(sa) == 0:
        absence_days = 0
    else:
        absence_days = sa[0].absence_days
    refund_amt = absence_days * srp.refund
    print("환불금:", refund_amt)

    r = Account.objects.raw("select id, -10000 as recommend_dc_amt from studyroom_account \
                                    where %s between recommend_dc_start and recommend_dc_end \
                                    and id = %s", [bill_mt, account.id])
    if len(r) == 0:
        recommend_dc_amt = 0
    else:
        recommend_dc_amt = r.recommend_dc_amt
    print("추천할인:", recommend_dc_amt)
    if student.brother_id :
        print("이름:", student.name, "형제:", student.brother.name)
        b = Sugang.objects.raw("select id,\'d\'||count(1) as sugang_type from studyroom_sugang \
                                                where %s between start_mt and end_mt \
                                                and student_id = %s", [bill_mt, student.brother_id])[0]
        print("형제 수강Type:", b.sugang_type)

        bp = PricePlan.objects.raw("select id, price from studyroom_priceplan \
                                    where grade = %s and sugang_type = %s \
                                    and %s between start_mt and end_mt", [student.brother.grade, s.sugang_type, bill_mt])[0]
        brother_base_amt = bp.price
        print("형제수강료:", brother_base_amt)

        brp = PricePlan.objects.raw("select id, refund from studyroom_priceplan \
                                            where grade = %s and sugang_type = %s \
                                            and %s between start_mt and end_mt",
                                   [student.brother.grade, s.sugang_type, absence_mt])[0]
        print("형제환불기준:", brp.refund)

        ba = Absence.objects.raw("select id, absence_days from studyroom_absence \
                                    where student_id = %s and absence_mt = %s", [student.brother_id, absence_mt])
        if len(ba) == 0:
            brother_absence_days = 0
        else:
            brother_absence_days = ba[0].absence_days
        brother_refund_amt = brother_absence_days * brp.refund
        print("형제환불금:", brother_refund_amt)

        brother_dc_amt = (base_amt + brother_base_amt + refund_amt + brother_refund_amt) * -0.1


    bill_status = 'OP'

    bill_amt = base_amt + brother_base_amt + refund_amt + brother_refund_amt + brother_dc_amt + recommend_dc_amt
    bill.bill_status = bill_status
    bill.bill_amt = bill_amt
    bill.base_amt = base_amt
    bill.brother_base_amt = brother_base_amt
    bill.refund_amt = refund_amt
    bill.brother_refund_amt = brother_refund_amt
    bill.brother_dc_amt = brother_dc_amt
    bill.recommend_dc_amt = recommend_dc_amt
    bill.save()



@login_required(login_url='common:login')
def bill_list(request):
    logger.info("INFO 레벨로 출력")
    """
    청구 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '')  # 페이지
    billmt = request.GET.get('billmt', '')  # 검색어
    billstatus = request.GET.get('billstatus', '')  # 검색어

    # 조회
    bill_list = Bill.objects.order_by('id')
    if billmt:
        bill_list = bill_list.filter(
            Q(bill_mt__icontains=billmt)   # 청구월 검색
        ).distinct()
    if billstatus:
        bill_list = bill_list.filter(
            Q(bill_status__icontains=billstatus)   # 청구상태 검색
        ).distinct()

    bml = Bill.objects.all().values('bill_mt').distinct()
    bsl = Bill.objects.all().values('bill_status').distinct()

    # 페이징처리
    paginator = Paginator(bill_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'bill_list': page_obj, 'page': page, 'billmt': billmt, 'billstatus':billstatus, 'bml':bml, 'bsl':bsl}
    return render(request, 'studyroom/bill_list.html', context)

@login_required(login_url='common:login')
def bill_pay_list(request):
    logger.info("INFO 레벨로 출력")
    """
    청구 목록 출력
    """

    # 입력 파라미터
    billmt = request.GET.get('billmt', '')  # 검색어
    paydate =  request.GET.get('paydate', '')  # 검색어

    # 조회
    bill_list = Bill.objects.exclude(bill_status='FP')
    pay_list = Pay.objects.filter(pay_status='OP')

    if billmt:
        bill_list = bill_list.filter(
            Q(bill_mt__icontains=billmt)  # 청구월 검색
        ).distinct()

    if paydate:
        pay_list = pay_list.filter(pay_date__startswith=paydate).distinct()

    bml = Bill.objects.all().values('bill_mt').distinct()

    context = {'bill_list': bill_list, 'billmt': billmt, 'bml': bml, 'pay_list': pay_list, 'paydate': paydate}
    return render(request, 'studyroom/bill_pay_list.html', context)

@login_required(login_url='common:login')
def bill_pay_con(request):
    """
    청구-수납 연결하기
    """
    # checked 검색
    bill_id = request.POST.get('bill_id', '')
    pay_id = request.POST.get('pay_id', '')

    bill = Bill.objects.get(pk=bill_id)
    pay = Pay.objects.get(pk=pay_id)

    bill.pay_amt = bill.pay_amt + pay.pay_amt
    bill.pay_type = pay.pay_type
    bill.pay_dt = pay.pay_date[:8]
    bill.pay_id = pay.id
    if bill.bill_amt == bill.pay_amt:
        bill.bill_status = 'FP'
    else:
        bill.bill_status = 'PP'
    bill.save()

    pay.pay_status = 'CO'
    pay.bill = bill
    pay.save()

    # 조회
    bill_list = Bill.objects.exclude(bill_status='FP')
    pay_list = Pay.objects.filter(pay_status='OP')
    bml = Bill.objects.all().values('bill_mt').distinct()

    context = {'bill_list': bill_list, 'billmt': '', 'bml': bml, 'pay_list': pay_list, 'paydate': ''}
    return render(request, 'studyroom/bill_pay_list.html', context)

@login_required(login_url='common:login')
def bill_save(request):
    """
    청구 재발행
    """
    # checked 청구 재발행
    if request.method == 'POST':
        bill_id = request.POST.get('bill_id', '')
        print('Call Function bill_dml(), Bill_id:', bill_id)
        bill_dml(bill_id)
        return redirect('studyroom:bill_list')
    else:
        # 조회
        name = request.GET.get('name', '')  # 검색어
        bill_list = Bill.objects.order_by('id')
        if name:
            bill_list = bill_list.filter(
                Q(account__student__name__icontains=name) |  # 학생이름 검색
                Q(account__student__brother__name__icontains=name)  # 학생이름 검색
            ).distinct()


        context = {'bill_list':bill_list, 'name':name}
        return render(request, 'studyroom/bill_save.html', context)
