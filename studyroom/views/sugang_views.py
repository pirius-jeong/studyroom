from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from ..models import Student, Sugang

@login_required(login_url='common:login')
def sugang_list(request):
    """
    수강표 출력
    """
    name = request.GET.get('name', '')  # 검색어
    sugang_mt = request.GET.get('sugang_mt', '')  # 검색어

    sugang_list = Sugang.objects.order_by('class_id', 'time')

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
    수강 등록
    """
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        weekday_time = request.POST.getlist('weekday_time')
        class_id = request.POST.getlist('class_id')[0]
        start_mt = request.POST.getlist('start_mt')[0]
        end_mt = request.POST.getlist('end_mt')[0]
        user = request.user
        for i in weekday_time:
            sugang = Sugang()
            sugang.student = student
            sugang.class_id = class_id
            sugang.start_mt = start_mt
            sugang.end_mt = end_mt
            sugang.weekday = i.split('_')[0]
            sugang.time = i.split('_')[1]
            sugang.user = user
            sugang.create_date = timezone.now()
            #print(sugang.student.name, sugang.class_id, sugang.start_mt, sugang.end_mt, sugang.weekday, sugang.time, sugang.user, sugang.create_date  )
            sugang.save()

        return redirect('studyroom:detail', student_id=student.id)
    else:
        context = {'student': student, 'crud': 'create'}
        return render(request, 'studyroom/sugang_form.html', context)


@login_required(login_url='common:login')
def sugang_modify(request, student_id):
    """
    수강 변경
    """
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        print('==== sugang_modify ====')
        weekday_time = request.POST.getlist('weekday_time')
        class_id = request.POST.getlist('class_id')[0]
        start_mt = request.POST.getlist('start_mt')[0]
        end_mt = request.POST.getlist('end_mt')[0]
        user = request.user

        old_sugang_list = Sugang.objects.filter(student=student, end_mt='999912')
        for old_sugang in old_sugang_list:
            start_mt_date = datetime(int(start_mt[:4]), int(start_mt[-2:]), 1)
            old_sugang.end_mt = (start_mt_date + relativedelta(months=-1)).strftime("%Y%m")
            print('old : ',old_sugang.start_mt, old_sugang.end_mt, old_sugang.weekday, old_sugang.time)
            old_sugang.modify_date = timezone.now()
            old_sugang.save()

        for i in weekday_time:
            sugang = Sugang()
            sugang.student = student
            sugang.class_id = class_id
            sugang.start_mt = start_mt
            sugang.end_mt = end_mt
            sugang.weekday = i.split('_')[0]
            sugang.time = i.split('_')[1]
            sugang.user = user
            sugang.create_date = timezone.now()
            print('new:', sugang.student.name, sugang.class_id, sugang.start_mt, sugang.end_mt, sugang.weekday, sugang.time, sugang.user, sugang.create_date  )
            sugang.save()
        return redirect('studyroom:detail', student_id=student.id)
    else:

        # context에 student 추가
        context = {'student': student, 'crud': 'modify'}
        return render(request, 'studyroom/sugang_form.html', context)


