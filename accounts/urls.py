from django.urls import path
from . import views 

urlpatterns = [
   path('',views.homepage, name='homepage'),
   path('main/',views.main, name='main'),
   path('login/',views.login, name='login'),
   path('register/',views.register, name='register'),
   path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'), 
   path('logout_user/',views.logout_user, name='logout_user'),
   path('requester/',views.requester, name='requester'),
   path('register/',views.register, name='register'),
   path('forgot/',views.forgot, name='forgot'),
   path('tracker/',views.tracker, name='tracker'),
   path('prof/' ,views.prof, name='prof'),
   path('reset/',views.reset, name='reset'),
   path('notif/',views.notification, name='notification'),
   path('verify/',views.verify, name='verify'),
   path('about/',views.about, name='about'),
   path('history/',views.history, name='history'),
   path('profile/',views.profile, name='profile'),
   path('pro_file/',views.pro_file, name='pro_file'),
   path('profile_html/', views.profile_html, name='profile_html'),
   path('notif/', views.notification_html, name='notification_html'),
   path('about_cash/',views.about_cash, name='about_cash'),
   path('cash_disbursement/',views.cash_disbursement, name='cash_disbursement'),
   path('home_cash/',views.home_cash, name='home_cash'),
   path('purchase_request_cash/',views.prequest, name='prequest'),
   path('form/',views.form, name='form'),
   path('reward_cash/',views.reward_cash, name='reward_cash'),
   path('BAC_home/',views.home_bac, name='home_bac'),
   path('BAC_purchase_request/',views.purchase_bac, name='purchase_bac'),
   path('campus_director/requester/', views.campus_director_requester,name='campusD_requester'),
   path('campus_director/notification/', views.campus_director_notification,name='campusD_notification'),
   path('campus_director/resolution/', views.campus_director_resolution,name='campusD_resolution'),
   path('campus_director/history/', views.campus_director_historycd,name='campusD_history'),
   path('campus_director/about/', views.campus_director_about,name='campusD_about'),
   path('supply_office/home/', views.supply_office_home,name='supply_office_home'),
   path('supply_office/notification/', views.supply_office_notification,name='supply_office_notification'),
   path('supply_office/history/', views.supply_office_history,name='supply_office_history'),
   path('supply_office/about/', views.supply_office_about,name='supply_office_about'),
   path('supply_office/inventory/', views.supply_office_inventory,name='supply_office_inventory'),
   path('notice_of_reward/',views.notice_of_reward, name='notice_of_reward'),  
]