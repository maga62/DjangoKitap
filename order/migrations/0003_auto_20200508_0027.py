# Generated by Django 3.0.5 on 2020-05-07 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20200507_2347'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopcart',
            old_name='product',
            new_name='kitap',
        ),
    ]
