from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q

from ..models import Bill,Pay
import logging
logger = logging.getLogger('studyroom')

def pay_list(request):
    logger.info("INFO 레벨로 출력")
    """
    학생 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    paymt = request.GET.get('paymt', '')  # 검색어
    paystatus = request.GET.get('paystatus', '')  # 검색어

    # 조회
    pay_list = Bill.objects.order_by('id')
    if paymt:
        pay_list = pay_list.filter(
            Q(pay_mt__icontains=paymt)   # 제목검색
        ).distinct()
    if paystatus:
        pay_list = pay_list.filter(
            Q(pay_status__icontains=paystatus)   # 제목검색
        ).distinct()
    # 페이징처리
    paginator = Paginator(pay_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'pay_list': page_obj, 'page': page, 'paymt': paymt, 'paystatus':paystatus}
    return render(request, 'studyroom/pay_list.html', context)

