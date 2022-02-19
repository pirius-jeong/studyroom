from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import HttpResponse
from ..serializer import PostSerializer


from ..models import Student, Sugang, PricePlan, Account, Pay

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

@login_required(login_url='common:login')
def priceplan(request):
    """
    요금표 출력
    """
    pricepln_list = PricePlan.objects.order_by('grade', 'sugang_type')

    context = {'priceplan_list': pricepln_list}
    return render(request, 'studyroom/priceplan.html', context)

@login_required(login_url='common:login')
def priceplan_create(request):
    """
        요금표 생성
    """
    grade = request.POST.get('grade', '')  # 검색어
    sugang_type = request.POST.get('sugang_type', '')  # 검색어
    price = request.POST.get('price', '')  # 검색어
    refund = request.POST.get('refund', '')  # 검색어
    start_mt = request.POST.get('start_mt', '')  # 검색어

    print('==== create priceplan : ',grade, sugang_type, price, refund, start_mt)

    priceplan = PricePlan.objects.get(grade=grade, sugang_type=sugang_type, end_mt='999912')

    if priceplan.start_mt >= start_mt:
        print('==== error : start_mt alread exist')
    else:
        start_yy = start_mt[:4]
        start_mm = start_mt[-2:]
        end_mt = (date(int(start_yy), int(start_mm), 1) + relativedelta(months=-1)).strftime("%Y%m")
        priceplan.end_mt = end_mt
        priceplan.save()

        new_priceplan = PricePlan(grade=grade, sugang_type=sugang_type, price=price, refund=refund, start_mt=start_mt,
                                  end_mt='999912', create_date=timezone.now())
        new_priceplan.save()

    """
    요금표 출력
    """
    pricepln_list = PricePlan.objects.order_by('grade', 'sugang_type')

    context = {'priceplan_list': pricepln_list}
    return render(request, 'studyroom/priceplan.html', context)


@api_view(['POST'])
def hometax(request):
    print('=== hometax post api start ===')
    if request.method == 'GET':
        return HttpResponse(status=200)
    if request.method == 'POST':
        serializer = PostSerializer(data = request.data, required=False)
        serializer.create_date = timezone.now()
        try:
            serializer.account = Account.objects.get(payer_phone_num__contains=serializer.payer)
        except:
            print('=== account is None ')

        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data ,status=200)
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)






