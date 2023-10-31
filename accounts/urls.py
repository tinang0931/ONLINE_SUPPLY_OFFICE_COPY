from django.urls import path
from . import views 

urlpatterns = [
   path('',views.homepage, name='homepage'),
   path('main/',views.main, name='main'),
   path('login/',views.login, name='login'),
   path('register/',views.register, name='register'),
   path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
   path('logout_user/',views.logout_user, name='logout_user'),
   path('requester/',views.requester, name='requester'),
   path('transaction_history/', views.transaction_history, name='transaction_history'),
   path('reset-password/', views.handle_reset_request, name='handle_reset_request'),
   path('verify-code/', views.verify_code, name='verify_code'),
   path('notif/',views.notification, name='notification'),
   path('tracker/',views.tracker, name='tracker'),
   path('about/',views.about, name='about'),
   path('history/',views.history, name='history'),
   path('profile/',views.profile, name='profile'),
   path('prof/',views.prof, name='prof'),
   path('BAC_about/',views.about_bac, name='about_bac'),
   path('BAC_home/',views.home_bac, name='home_bac'),
   path('BAC_purchase_request/',views.purchase_bac, name='purchase_bac'),
]