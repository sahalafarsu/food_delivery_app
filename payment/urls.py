from django.urls import path
from . import views
from .views import CancelView, SuccessView

app_name = 'payment'
urlpatterns = [
    path('create-checkout-session', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
]
