from django.urls import path
from . import views 
from .views import *


urlpatterns = [
   path('',views.homepage, name='homepage'),
   path('purchaseorder/',views.purchaseorder, name='purchaseorder'),
   path('main/',views.main, name='main'),
   path('bac/',views.bac, name='bac'),
   path('addItem/',views.addItem, name='addItem'),
   path('login/',views.login, name='login'),
   # path('item/<int:pk>/edit/', views.item_edit, name='item_edit'),
   path('item/<int:pk>/list/', views.item_list, name='item_list'),
   path('register/',views.register, name='register'),
   path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
   path('logout_user/',views.logout_user, name='logout_user'),
   path('requester/', RequesterView.as_view(), name='requester'),
   path('request/',views.request, name='request'),
   path('reset-password/', views.handle_reset_request, name='handle_reset_request'),
   path('verify-code/', views.verify_code, name='verify_code'),
   path('tracker/',views.tracker, name='tracker'),
   path('about/',views.about, name='about'),
   path('purchase_request_history/', PurchaseRequestHistoryView.as_view(), name='purchase_request_history'),
   path('profile/',views.profile, name='profile'),
   path('bac_about/',views.bac_about, name='bac_about'),
   path('bac_history/',views.bac_history, name='bac_history'),
   path('bac_home/',views.bac_home, name='bac_home'),
   path('prof/',views.prof, name='prof'),
   path('preqform/', views.preqform, name='preqform'),
   path('np/',views.np, name='np'),
   path('bids/',views.bids, name='bids'),
   path('noa/',views.noa, name='noa'),
   path('notif/',views.notif, name='notif'),
   path('item/<uuid:request_id>/delete/', views.item_delete, name='item_delete'),
   path('inspection/',views.inspection, name='inspection'),
   path('purchaseorder/',views.purchaseorder, name='purchaseorder'),
   path('property/',views.property, name='property'),
   path('abstract/',views.abstract, name='abstract'),

]