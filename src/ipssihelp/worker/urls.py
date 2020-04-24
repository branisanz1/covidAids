from django.urls import re_path, path
from . import views

app_name = 'worker'

urlpatterns = [
    re_path('^$', views.home, name='home'),
    re_path('supply', views.supply, name='supply'),
    re_path('demand', views.demand, name='demand'), 
    re_path(r'detail/(?P<id>[\w-]+)/$', views.detail, name='detail'), 
    path('account/signup/', views.signup, name='signup'),
    path('account/login/', views.login_view, name='login_view'),
    path('account/logout/', views.logout_view, name='logout_view'),
    path('account/profil/', views.profil, name='profil'),
    path('account/announces/', views.announces, name='announces'),
    path('account/announces/add', views.add_announce, name='add_announce'),
    re_path(r'conversation/(?P<id>[\w-]+)/$', views.conversation, name='conversation'),


]