from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('search', views.search, name='search'),
    path('reset', views.reset_page, name='reset_page'),
]
