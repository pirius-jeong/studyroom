from django.urls import path

from .views import base_views, student_views, account_views, bill_views, sugang_views, pay_views

app_name = 'studyroom'

urlpatterns = [
    # base_views.py
    path('',
         base_views.index, name='index'),
    path('<int:student_id>/',
         base_views.detail, name='detail'),

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

    # bill_views.py
    path('bill/',
         bill_views.bill_list, name='bill_list'),
]
