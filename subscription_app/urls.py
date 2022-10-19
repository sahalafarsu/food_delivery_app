from django.urls import path
from . import views

# from django.contrib import admin
# from membership import views

app_name = 'subscription_app'

urlpatterns = [

    path('auth/settings', views.settings, name='settings'),
    path('join', views.join, name='join'),
    path('checkout', views.checkout, name='checkout'),
    path('success', views.success, name='success'),
    path('premium', views.premium, name='premium'),
    path('special', views.special, name='special'),
    path('cancel', views.cancel, name='cancel'),
    path('updateaccounts', views.updateaccounts, name='updateaccounts'),
    path('pausesubscription', views.pausesubscription, name='pausesubscription'),
    path('resumesubscription', views.resumesubscription, name='resumesubscription'),
    path('updateplan',views.updatesubscription,name='updateplan'),
]
