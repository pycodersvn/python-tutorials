from django.urls import path

from . import views

urlpatterns = [
    # ex: /export/
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('render', views.render, name='render'),
]