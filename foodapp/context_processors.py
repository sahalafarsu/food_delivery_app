from .models import Restaurant

def menu_links(request):
    links=Restaurant.objects.all()
    return dict(links=links)