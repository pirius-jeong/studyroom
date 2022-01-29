from django.urls import path

from .views import base_views, student_views, account_views

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
    
    # account_views.py
    path('account/create/<int:student_id>/',
         account_views.account_create, name='account_create'),
]
