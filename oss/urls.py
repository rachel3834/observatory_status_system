from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from django.contrib.auth.views import LoginView, LogoutView
from . import views, api_views

router = routers.DefaultRouter()
router.register(r'update_facility_status', api_views.UpdateFacilityStatusView)


urlpatterns = [
    path('', views.FacilityListView.as_view(), name='facilities_list'),
    path('', include(router.urls)),
    path('site/<int:pk>/', views.SiteDetailView.as_view(), name='site_summary'),
    path('telescope/<int:pk>/', views.TelescopeDetailView.as_view(), name='telescope_summary'),
    path('instrument/<int:pk>/', views.InstrumentDetailView.as_view(), name='instrument_summary'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('set_facility_status', views.FacilityStatusCreate.as_view(), name='set_facility_status'),
]
