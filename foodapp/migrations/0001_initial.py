# Generated by Django 3.2 on 2022-04-11 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='restaurant')),
            ],
            options={
                'verbose_name': 'restaurant',
                'verbose_name_plural': 'restaurants',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, upload_to='product')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodapp.restaurant')),
            ],
            options={
                'verbose_name': 'dish',
                'verbose_name_plural': 'dishes',
                'ordering': ('name',),
            },
        ),
    ]
