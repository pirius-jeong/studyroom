from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q

from ..models import Bill
import logging
logger = logging.getLogger('studyroom')

def bill_list(request):
    logger.info("INFO 레벨로 출력")
    """
    학생 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    billmt = request.GET.get('billmt', '')  # 검색어
    billstatus = request.GET.get('billstatus', '')  # 검색어

    # 조회
    bill_list = Bill.objects.order_by('id')
    if billmt:
        bill_list = bill_list.filter(
            Q(bill_mt__icontains=billmt)   # 제목검색
        ).distinct()
    if billstatus:
        bill_list = bill_list.filter(
            Q(bill_status__icontains=billstatus)   # 제목검색
        ).distinct()
    # 페이징처리
    paginator = Paginator(bill_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'bill_list': page_obj, 'page': page, 'billmt': billmt, 'billstatus':billstatus}
    return render(request, 'studyroom/bill_list.html', context)