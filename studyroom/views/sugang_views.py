from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q
from ..forms import StudentForm, AccountForm, SugangForm
from ..models import Student, Sugang


def sugang_list(request):
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
    return render(request, 'studyroom/sugang_list.html', context)

@login_required(login_url='common:login')
def sugang_create(request, student_id):
    """
    학생 등록
    """
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        form = SugangForm(request.POST)
        if form.is_valid():
            sugang = form.save(commit=False)
            sugang.student = student
            sugang.user = request.user
            sugang.create_date = timezone.now()
            sugang.save()
            return redirect('studyroom:sugang')
    else:
        form = SugangForm()
    context = {'form': form}
    return render(request, 'studyroom/student_detail.html', context)


@login_required(login_url='common:login')
def sugang_modify(request, student_id):
    """
    pybo 질문수정
    """
    student = get_object_or_404(Student, pk=student_id)
    sugang = Sugang.objects.get().filter(student=student)
    if request.method == "POST":
        form = SugangForm(request.POST, instance=sugang)
        if form.is_valid():
            sugang = form.save(commit=False)
            sugang.modify_date = timezone.now()  # 수정일시 저장
            sugang.save()
            return redirect('studyroom:detail', student_id=student.id)
    else:
        form = SugangForm(instance=sugang)
    context = {'form': form}
    return render(request, 'studyroom/sugang_form.html', context)


@login_required(login_url='common:login')
def sugang_delete(request, student_id):
    """
    pybo 질문삭제
    """
    student = get_object_or_404(Student, pk=student_id)
    #sugang =
    #sugang.delete()
    return redirect('studyroom:index')