from django.urls import path

from .views import base_views, student_views, account_views, bill_views

app_name = 'studyroom'

urlpatterns = [
    # base_views.py
    path('',
         base_views.index, name='index'),
    path('<int:student_id>/',
         base_views.detail, name='detail'),
    path('sugang_table/',
         base_views.sugang_table, name='sugang_table'),

    # student_views.py
    path('student/create/',
         student_views.student_create, name='student_create'),
    path('student/modify/<int:student_id>/',
         student_views.student_modify, name='student_modify'),
    path('student/delete/<int:student_id>/',
         student_views.student_delete, name='student_delete'),
    
    # account_views.py
    path('account/create/<int:student_id>/',
         account_views.account_create, name='account_create'),

    # bill_views.py
    path('bill/',
         bill_views.bill_list, name='bill_list'),
]
