from django.contrib import admin
from django.urls import path, include
from studyroom import base_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('studyroom/', include('studyroom.urls')),
    path('common/', include('common.urls')),
    path('', base_views.index, name='index'),  # '/' 에 해당되는 path
]