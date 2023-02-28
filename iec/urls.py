from django.urls import path
from .views import IecList,CustomLoginView,IecDetail,IecRequest,IecUpdate,DeleteView,TaskReorder,IecListDownloadView
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
   

    path('', IecList.as_view(), name='home'),
    path('iec/<int:pk>/', IecDetail.as_view(), name='iec-detail'),
    path('iec-request', IecRequest.as_view(), name='iec-request'),
    path('iec-update/<int:pk>/', IecUpdate.as_view(), name='iec-update'),
    path('iec-delete/<int:pk>/', DeleteView.as_view(), name='iec-delete'),
    path('iec-reorder/', TaskReorder.as_view(), name='iec-reorder'),

    path('main', views.main, name='main'),
    path('hg', views.hg, name='hg'),
    path('hiv-tb', views.hiv_tb, name='hiv-tb'),
    path('wlpr', views.wlpr, name='wlpr'),
    path('silu', views.silu, name='silu'),
    path('download-hg', views.print_iec, name='download-hg'),
    path('download-hiv', views.download_hiv, name='download-hiv'),
    path('download-wlpr', views.download_wlpr, name='download-wlpr'),
    path('download-srhr', views.download_srhr, name='download-srhr'),
    path('download-silu', views.download_silu, name='download-silu'),
    path('request-download', IecListDownloadView.as_view(), name='request-download'),

]