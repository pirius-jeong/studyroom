from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q

from ..models import Sms
import logging
logger = logging.getLogger('studyroom')

def sms_list(request):
    logger.info("INFO 레벨로 출력")
    """
    SMS 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    name = request.GET.get('name', '')  # 검색어

    # 조회
    sms_list = Sms.objects.order_by('-requestTime')
    if name:
        sms_list = sms_list.filter(
            Q(account__student__name__icontains=name)   # 학생이름검색
        ).distinct()
    # 페이징처리
    paginator = Paginator(sms_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'sms_list': page_obj, 'page': page, 'name': name}
    return render(request, 'studyroom/sms_list.html', context)
