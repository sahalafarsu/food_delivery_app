# from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='restaurant', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'restaurant'
        verbose_name_plural = 'restaurants'

    def get_url(self):
        return reverse('foodapp:dishes_by_restaurant', args=[self.slug])

    def __str__(self):
        return '{}'.format(self.name)


class Dish(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='dish', blank=True)
    # stock = models.IntegerField()
    # available = models.BooleanField(default=True)
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now_add=True)

    def get_url(self):
        return reverse('foodapp:dishDetail', args=[self.restaurant.slug, self.slug])

    class Meta:
        ordering = ('name',)
        verbose_name = 'dish'
        verbose_name_plural = 'dishes'

    def __str__(self):
        return '{}'.format(self.name)
