from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('diary', views.diary, name='diary'),
    path('bug/<str:card_name>', views.bug, name='bug'),
]