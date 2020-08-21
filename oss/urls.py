from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.FacilityListView.as_view(), name='facilities_list'),
    path('site/<int:pk>/', views.SiteDetailView.as_view(), name='site_summary'),
]
