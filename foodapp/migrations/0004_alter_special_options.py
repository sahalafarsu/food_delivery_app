# Generated by Django 3.2 on 2022-05-30 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0003_special'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='special',
            options={'ordering': ('name',), 'verbose_name': 'special', 'verbose_name_plural': 'specials'},
        ),
    ]
