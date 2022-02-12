from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from datetime import datetime
from ..models import Student, Sugang

@login_required(login_url='common:login')
def index(request):
    """
    학생 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    name = request.GET.get('name', '')  # 검색어

    # 조회
    student_list = Student.objects.order_by('-id')
    if name:
        student_list = student_list.filter(
            Q(name__icontains=name)
        ).distinct()


    # 페이징처리
    paginator = Paginator(student_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'student_list': page_obj, 'page': page, 'name': name}
    return render(request, 'studyroom/student_list.html', context)

@login_required(login_url='common:login')
def detail(request, student_id):
    """
    학생 상세정보(계정,수강) 출력
    """
    work_mt = datetime.today().strftime("%Y%m")
    student = get_object_or_404(Student, pk=student_id)
    sugang_list = Sugang.objects.order_by('class_id', 'time').filter(student=student, end_mt__gte = work_mt)

    context = {'student': student, 'sugang_list': sugang_list}
    return render(request, 'studyroom/student_detail.html', context)
