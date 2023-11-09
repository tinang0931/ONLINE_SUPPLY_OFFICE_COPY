from django.urls import path
from . import views 


urlpatterns = [
   path('',views.homepage, name='homepage'),
   path('main/',views.main, name='main'),
   path('bac/',views.bac, name='bac'),
   path('login/',views.login, name='login'),
   path('register/',views.register, name='register'),
   path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
   path('logout_user/',views.logout_user, name='logout_user'),
   path('requester/' , views.requester, name="requester"),
   path('addItem/',views.addItem, name='addItem'),
   path('reset-password/', views.handle_reset_request, name='handle_reset_request'),
   path('verify-code/', views.verify_code, name='verify_code'),
   path('tracker/',views.tracker, name='tracker'),
   path('about/',views.about, name='about'),
   path('history/',views.history, name='history'),
   path('profile/',views.profile, name='profile'),
   path('bac_about/',views.bac_about, name='bac_about'),
   path('bac_history/',views.bac_history, name='bac_history'),
   path('bac_home/',views.bac_home, name='bac_home'),
   path('prof/',views.prof, name='prof'),
   path('preqform/',views.preqform, name='preqform'),
   path('category/',views.category, name='category'),

   
]
