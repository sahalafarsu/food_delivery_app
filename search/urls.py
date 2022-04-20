from django.urls import path
from .import views

app_name='search'
urlpatterns=[
    # path('',views.SearchResult,name='SearchResult'),
    path('',views.SearchResult.as_view(),name='SearchResult'),
]