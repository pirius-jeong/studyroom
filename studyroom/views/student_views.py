from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import StudentForm, AccountForm
from ..models import Student


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
    student.delete()
    return redirect('studyroom:index')