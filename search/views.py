from django.shortcuts import render
from django.views import View

from foodapp.models import Dish
from django.db.models import Q
# Create your views here.

# def SearchResult(request):
#     dishes=None
#     query=None
#     if 'q' in request.GET:
#         query=request.GET.get('q')
#         dishes=Dish.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))
#     return render(request,'search.html',{'query':query,'dishes':dishes})

class SearchResult(View):
    def get(self,request):
        dishes=None
        query=None
        if 'q' in request.GET:
            query=request.GET.get('q')
            dishes=Dish.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))
        return render(request,'search.html',{'query':query,'dishes':dishes})

