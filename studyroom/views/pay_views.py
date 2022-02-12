from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q

from ..models import Pay
import logging
logger = logging.getLogger('studyroom')

@login_required(login_url='common:login')
def pay_list(request):
    logger.info("INFO 레벨로 출력")
    """
    수납 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    name = request.GET.get('name', '')  # 검색어

    # 조회
    pay_list = Pay.objects.order_by('id')
    if name:
        pay_list = pay_list.filter(
            Q(account__student__name__icontains=name)   # 학생이름검색
        ).distinct()
    # 페이징처리
    paginator = Paginator(pay_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'pay_list': page_obj, 'page': page, 'name': name}
    return render(request, 'studyroom/pay_list.html', context)
