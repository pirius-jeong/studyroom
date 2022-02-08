from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q

from ..forms import StudentForm, AccountForm
from ..models import Student, Sugang


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


def detail(request, student_id):
    """
    학생 정보 출력
    """
    student = get_object_or_404(Student, pk=student_id)
    context = {'student': student}
    return render(request, 'studyroom/student_detail.html', context)


def sugang_table(request):
    """
    수강표 출력
    """
    name = request.GET.get('name', '')  # 검색어
    sugang_mt = request.GET.get('sugang_mt', '')  # 검색어

    sugang_list = Sugang.objects.order_by('class_id','time')

    if name:
        sugang_list = sugang_list.filter(
            Q(student__name__icontains=name)
        ).distinct()
    if sugang_mt:
        print(sugang_mt)
        sugang_list = sugang_list.filter(
            start_mt__lte = sugang_mt, end_mt__gte = sugang_mt
        ).distinct()
    context = {'sugang_list': sugang_list, 'name': name, 'sugang_mt': sugang_mt}
    return render(request, 'studyroom/sugang.html', context)

