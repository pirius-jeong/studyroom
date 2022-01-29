from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import StudentForm, AccountForm
from ..models import Student


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
