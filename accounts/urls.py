from django.urls import path
from . import views


urlpatterns = [
   path('',views.homepage, name='homepage'),
   path('requester/',views.requester, name='requester'),
   path('products/',views.products, name='products'),
   path('status/',views.status, name='status'),
   path('register/',views.register, name='register'),
   path('login/',views.login, name='login'),
   path('tracker/',views.tracker, name='tracker'),
   path('forgot/',views.forgot, name='forgot'),
   path('login/',views.login, name='login'),
   path('notif/',views.notification, name='notification'),
   path('about/',views.about, name='about'),  
   path('verify/',views.verify, name='verify'),
   path('about/',views.about, name='about'),
   path('history/',views.history, name='history'),
   path('profile/',views.profile, name='profile'),
]