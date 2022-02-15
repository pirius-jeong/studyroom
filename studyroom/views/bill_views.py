from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q

from studyroom.models import Bill, Pay
from studyroom.com import bill_dml

import logging
logger = logging.getLogger('studyroom')

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
    bill_id = request.POST.get('bill_id', '')
    print('== 청구 재발행:',bill_id)
    bill_dml(bill_id)

    # 입력 파라미터
    page = request.GET.get('page', '')  # 페이지
    billmt = request.GET.get('billmt', '')  # 검색어
    billstatus = request.GET.get('billstatus', '')  # 검색어

    # 조회
    bill_list = Bill.objects.order_by('id')
    if billmt:
        bill_list = bill_list.filter(
            Q(bill_mt__icontains=billmt)  # 청구월 검색
        ).distinct()
    if billstatus:
        bill_list = bill_list.filter(
            Q(bill_status__icontains=billstatus)  # 청구상태 검색
        ).distinct()

    bml = Bill.objects.all().values('bill_mt').distinct()
    bsl = Bill.objects.all().values('bill_status').distinct()

    # 페이징처리
    paginator = Paginator(bill_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'bill_list': page_obj, 'page': page, 'billmt': billmt, 'billstatus': billstatus, 'bml': bml, 'bsl': bsl}
    return render(request, 'studyroom/bill_list.html', context)
