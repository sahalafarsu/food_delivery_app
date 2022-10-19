# from django.contrib import admin

# Register your models here.
from django.contrib import admin
# from django.contrib.admin import ModelAdmin

from .models import Restaurant, Dish, Special


# Register your models here.
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Restaurant,RestaurantAdmin)

class DishAdmin(admin.ModelAdmin):
    list_display = ['name','price']
    list_editable = ['price']
    prepopulated_fields = {'slug':('name',)}
    list_per_page = 20
admin.site.register(Dish,DishAdmin)

admin.site.register(Special)
