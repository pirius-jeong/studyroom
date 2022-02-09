from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import AbsenceForm
from ..models import Student, Absence

import logging
logger = logging.getLogger('studyroom')

@login_required(login_url='common:login')
def absence_create(request, student_id):
    """
    결석 등록
    """
    student = get_object_or_404(Student, pk=student_id)
    if request.method == "POST":
        form = AbsenceForm(request.POST)
        if form.is_valid():
            absence = form.save(commit=False)
            absence.user = request.user
            absence.create_date = timezone.now()
            absence.student = student
            absence.save()
            return redirect('studyroom:detail', student_id=student.id)
    else:
        form = AbsenceForm()
    context = {'student': student, 'form': form}
    return render(request, 'studyroom/absence_form.html', context)

@login_required(login_url='common:login')
def absence_delete(request, absence_id):
    """
    결석 삭제
    """
    absence = get_object_or_404(Absence, pk=absence_id)
    student_id = absence.student.id
    absence.delete()
    return redirect('studyroom:detail', student_id=student_id)