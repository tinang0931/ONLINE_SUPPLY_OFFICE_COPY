from django.urls import path
from django.contrib import admin
from . import views 
from .views import *


urlpatterns = [
   path('',views.homepage, name='homepage'),
   path('purchaseorder/',views.purchaseorder, name='purchaseorder'),
   path('main/',views.main, name='main'),
   path('bac/',views.bac, name='bac'),
   path('addItem/',views.addItem, name='addItem'),
   path('login/',views.login, name='login'),
   path('item/<int:pk>/list/', views.item_list, name='item_list'),
   path('register/',views.register, name='register'),
   path('register_user/',views.register_user, name='register_user'),
   path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
   path('logout_user/',views.logout_user, name='logout_user'),
   path('requester/', RequesterView.as_view(), name='requester'),
   path('request/',views.request, name='request'),
   path('reset-password/', views.handle_reset_request, name='handle_reset_request'),
   path('verify-code/', views.verify_code, name='verify_code'),
   path('tracker/',views.tracker, name='tracker'),
   path('about/',views.about, name='about'),
   path('bac_prof/',views.bac_prof, name='bac_prof'),
    path('bac_profile/',views.bac_profile, name='bac_profile'),
   path('profile/',views.profile, name='profile'),
   path('bac_about/',views.bac_about, name='bac_about'),
   path('bac_home/',views.bac_home, name='bac_home'),
   path('prof/',views.prof, name='prof'),
   path('preqform/<str:pr_id>/', PreqFormView.as_view(), name='preqform'),
   path('np/',views.np, name='np'),
   path('bids/',views.bids, name='bids'),
   path('noa/',views.noa, name='noa'),
   path('notif/',views.notif, name='notif'),
   path('inspection/',views.inspection, name='inspection'),
   path('purchaseorder/',views.purchaseorder, name='purchaseorder'),
   path('property/',views.property, name='property'),
   path('abstract/',views.abstract, name='abstract'),
   path('history/',views.history, name='history'),
   path('delete/<int:id>/', delete, name='delete'),
   path('bo/',views.bo, name='bo'),
   path('boabout/',views.boabout, name='boabout'),
   path('bohistory/',views.bohistory, name='bohistory'),
   path('cd/',views.cd, name='cd'),
   path('cdabout/',views.cdabout, name='cdabout'),
   path('cdhome/',views.cdhome, name='cdhome'),
   path('cdpurchase/',views.cdpurchase, name='cdpurchase'),
   path('cdresolution/',views.cdresolution, name='cdresolution'),
   path('resolution/',views.resolution, name='resolution'),
   path('bac_dashboard/',views.bac_dashboard, name='bac_dashboard'),
   path('admin_home/',views.admin_home, name='admin_home'),
   path('adminabout/',views.adminabout, name='adminabout'),
   path('user/',views.user, name='user'),
   path('add_new_item/', add_new_item, name='add_new_item'),
   path('update_item/<int:id>/', views.update_item, name='update_item'),
   path('upload_file/',views.upload_file, name='upload_file'),
   path('Procurement/',views.Procurement, name='Procurement'),
   path('handle_uploaded_file/',views.handle_uploaded_file, name='handle_uploaded_file'),
   path('delete_item/<int:id>/', delete_item, name='delete_item'),
   path('delete_category/<str:Category>/', delete_category, name='delete_category'),
   path('update_user/<str:username>/', views.update_user, name='update_user'),
   path('delete_user/<str:username>/', views.delete_user, name='delete_user'),
   path('bo/',views.bo, name='bo'),
   path('boabout/',views.boabout, name='boabout'),
   path('bohistory/',views.bohistory, name='bohistory'),
 
   path('bohome/',views.bohome, name='bohome'),
   path('preqform_bo/<str:pr_id>/', PreqForm_boView.as_view(), name='preqform_bo'),
   path('approve_checkout/<pr_id>/', update_checkout_status, {'new_status': True}, name='approve_checkout'),
   path('disapprove_checkout/<pr_id>/', update_checkout_status, {'new_status': False}, name='disapprove_checkout'),
]