from django.urls import path

from .views import base_views, student_views, account_views, bill_views, sugang_views, pay_views, absence_views, sms_views

app_name = 'studyroom'

urlpatterns = [
    # base_views.py
    path('',
         base_views.index, name='index'),
    path('<int:student_id>/',
         base_views.detail, name='detail'),
    path('priceplan/',
         base_views.priceplan, name='priceplan'),
    path('priceplan/create/',
         base_views.priceplan_create, name='priceplan_create'),
    path('hometax/',
         base_views.hometax, name='hometax'),

    # student_views.py
    path('student/create/',
         student_views.student_create, name='student_create'),
    path('student/modify/<int:student_id>/',
         student_views.student_modify, name='student_modify'),
    path('student/delete/<int:student_id>/',
         student_views.student_delete, name='student_delete'),

    # sugang_views.py
    path('sugang/',
         sugang_views.sugang_list, name='sugang_list'),
    path('sugang/create/<int:student_id>/',
         sugang_views.sugang_create, name='sugang_create'),
    path('sugang/modify/<int:student_id>/',
         sugang_views.sugang_modify, name='sugang_modify'),


    # account_views.py
    path('account/',
         account_views.account_list, name='account_list'),
    path('account/create/<int:student_id>/',
         account_views.account_create, name='account_create'),
    path('account/modify/<int:account_id>/',
         account_views.account_modify, name='account_modify'),
    path('account/delete/<int:account_id>/',
         account_views.account_delete, name='account_delete'),

    # absence_views.py
    path('absence/create/<int:student_id>/',
         absence_views.absence_create, name='absence_create'),
    path('absence/delete/<int:absence_id>/',
         absence_views.absence_delete, name='absence_delete'),

    # bill_views.py
    path('bill/',
         bill_views.bill_list, name='bill_list'),
    path('bill/bill_pay/',
         bill_views.bill_pay_list, name='bill_pay_list'),
    path('bill/bill_pay_con/',
         bill_views.bill_pay_con, name='bill_pay_con'),
    path('bill/bill_save/',
         bill_views.bill_save, name='bill_save'),

    # pay_views.py
    path('pay/',
         pay_views.pay_list, name='pay_list'),

    # sms_views.py
    path('sms/',
         sms_views.sms_list, name='sms_list'),
    path('sms/send/',
         sms_views.sms_send, name='sms_send'),
    path('sms/sendsms/',
         sms_views.send_sms, name='send_sms'),
]
