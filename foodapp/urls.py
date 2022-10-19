from . import views
from django.urls import path

from .views import SpecialListView

app_name = "foodapp"

urlpatterns = [
    # path('',views.index,name='index'),
    path('', views.Index.as_view(), name='index'),
    path('allDishRest/', views.allDishRest, name='allDishRest'),
    path('<slug:r_slug>/', views.allDishRest, name='dishes_by_restaurant'),
    path('<slug:r_slug>/<slug:dish_slug>/', views.dishDetail, name='dishDetail'),
    # path('login',views.login,name='login'),
    path('loginview', views.LoginView.as_view(), name='loginview'),
    path('registerview', views.RegisterView.as_view(), name='registerview'),
    # path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('specials', SpecialListView.as_view(), name='specials'),
]
