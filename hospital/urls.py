from django.urls import path
from hospital import views

urlpatterns = [
    path('',views.home,name='hospitalsnearby'),
]