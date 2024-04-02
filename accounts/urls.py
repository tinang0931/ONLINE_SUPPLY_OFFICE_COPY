from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('userlanding/', views.userlanding, name='userlanding'),
    path('login/', views.login, name='login'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('register/', views.register, name='register'),
    path('ppmp101/', views.ppmp101, name='ppmp101'),
    path('purchase/', views.purchase, name='purchase'),
    path('tracker/', views.tracker, name='tracker'),
    path('purchasetracker/', views.purchasetracker, name='purchasetracker'),
    path('about/', views.about, name='about'),
    path('ppmp/', views.ppmp, name='ppmp'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('user_add_new_item/', views.user_add_new_item, name='user_add_new_item'),
    path('approved_ppmp/', views.approved_ppmp, name='approved_ppmp'),
    path('baclanding/', views.baclanding, name='baclanding'),
    path('bac_home/', views.bac_home, name='bac_home'),
    path('bac_request/', views.bac_request, name='bac_request'),
    path('bac_dashboard/', views.bac_dashboard, name='bac_dashboard'),
    path('bac_abou/', views.bac_about, name='bac_about'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('add_new_item/', views.add_new_item, name='add_new_item'),
    path('delete/<int:item>/', views.delete, name='delete'),
    path('bolanding/', views.bolanding, name='bolanding'),
    path('bohome/', views.bohome, name='bohome'),
    path('boabout/', views.boabout, name='boabout'),
    path('preqform_bo/<str:pr_id>/', views.preqform_bo, name='preqform_bo'),
    path('boppmp/', views.boppmp, name='boppmp'),
    path('cdlanding/', views.cdlanding, name='cdlanding'),
    path('cdppmp/', views.cdppmp, name='cdppmp'),
    path('cdhistory/', views.cdhistory, name='cdhistory'),
    path('cdabout/', views.cdabout, name='cdabout'),
    path('cdpurchase/', views.cdpurchase, name='cdpurchase'),
    path('cdresolution/', views.cdresolution, name='cdresolution'),
    path('cdppmp_approval/<str:pr_id>/', views.cdppmp_approval, name='cdppmp_approval'),
    path('myppmp/<str:pr_id>/', views.myppmp, name='myppmp'),
    
    
    
    
]
