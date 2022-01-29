from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import StudentForm, AccountForm
from ..models import Student
import logging
logger = logging.getLogger('studyroom')


def index(request):
    logger.info("INFO 레벨로 출력")
    """
    학생 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지

    # 조회
    student_list = Student.objects.order_by('-id')

    # 페이징처리
    paginator = Paginator(student_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'student_list': page_obj}
    return render(request, 'studyroom/student_list.html', context)


def detail(request, student_id):
    """
    학생 정보 출력
    """
    student = get_object_or_404(Student, pk=student_id)
    accounts = student.account_set.all()
    context = {'student': student, 'accounts': accounts}
    return render(request, 'studyroom/student_detail.html', context)


@login_required(login_url='common:login')
def student_create(request):
    """
    학생 등록
    """
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.create_date = timezone.now()
            student.save()
            return redirect('studyroom:index')
    else:
        form = StudentForm()
    context = {'form': form}
    return render(request, 'studyroom/student_form.html', context)


@login_required(login_url='common:login')
def account_create(request, student_id):
    """
    계정 등록
    """
    student = get_object_or_404(Student, pk=student_id)
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.create_date = timezone.now()
            account.student = student
            account.save()
            return redirect('studyroom:detail', student_id=student.id)
    else:
        form = AccountForm()
    context = {'student': student, 'form': form}
    return render(request, 'studyroom/student_detail.html', context)


@login_required(login_url='common:login')
def student_modify(request, student_id):
    """
    pybo 질문수정
    """
    student = get_object_or_404(Student, pk=student_id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.modify_date = timezone.now()  # 수정일시 저장
            student.save()
            return redirect('studyroom:detail', student_id=student.id)
    else:
        form = StudentForm(instance=student)
    context = {'form': form}
    return render(request, 'studyroom/student_form.html', context)


@login_required(login_url='common:login')
def student_delete(request, student_id):
    """
    pybo 질문삭제
    """
    student = get_object_or_404(Student, pk=student_id)
    if request.user != student.user:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('studyroom:detail', student_id=student.id)
    student.delete()
    return redirect('studyroom:index')