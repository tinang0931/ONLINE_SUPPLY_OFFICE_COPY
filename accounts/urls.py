from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('userlanding', views.userlanding, name='userlanding'),
    path('login', views.login, name='login'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('register', views.register, name='register'),
    path('ppmp101', views.ppmp101, name='ppmp101'),
    path('purchase', views.purchase, name='purchase'),
    path('tracker', views.tracker, name='tracker'),
    path('purchasetracker', views.purchasetracker, name='purchasetracker'),
    path('about', views.about, name='about'),
    path('ppmp', views.ppmp, name='ppmp'),
    path('catalogue', views.catalogue, name='catalogue'),
    path('user_add_new_item', views.user_add_new_item, name='user_add_new_item'),
    path('approved_ppmp', views.approved_ppmp, name='approved_ppmp'),
    
    
]
