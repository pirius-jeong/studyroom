from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q

from ..forms import  AccountForm
from ..models import Student, Account

import logging
logger = logging.getLogger('studyroom')

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

def account_list(request):
    logger.info("INFO 레벨로 출력")
    """
    계정 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    name = request.GET.get('name', '')  # 검색어

    # 조회
    account_list = Account.objects.order_by('id')
    if name:
        account_list = account_list.filter(
            Q(student__name__icontains=name) |  # 학생이름 검색
            Q(student__brother__name__icontains=name)  # 학생이름 검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(account_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'account_list': page_obj, 'page': page, 'name': name}
    return render(request, 'studyroom/account_list.html', context)

@login_required(login_url='common:login')
def account_modify(request, account_id):
    """
    pybo 질문수정
    """
    account = get_object_or_404(Account, pk=account_id)

    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            account = form.save(commit=False)
            account.modify_date = timezone.now()  # 수정일시 저장
            account.save()
            return redirect('studyroom:detail', student_id=account.student.id)
    else:
        form = AccountForm(instance=account)
    context = {'form': form}
    return render(request, 'studyroom/account_form.html', context)


@login_required(login_url='common:login')
def account_delete(request, account_id):
    """
    pybo 질문삭제
    """
    account = get_object_or_404(Account, pk=account_id)
    student_id = account.student.id
    account.delete()
    return redirect('studyroom:detail', student_id=student_id)