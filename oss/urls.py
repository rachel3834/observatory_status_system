from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'facility_status', views.FacilityStatusView)


urlpatterns = [
    path('', views.FacilityListView.as_view(), name='facilities_list'),
    path('', include(router.urls)),
    path('site/<int:pk>/', views.SiteDetailView.as_view(), name='site_summary'),
    path('telescope/<int:pk>/', views.TelescopeDetailView.as_view(), name='telescope_summary'),
    path('instrument/<int:pk>/', views.InstrumentDetailView.as_view(), name='instrument_summary'),
]
