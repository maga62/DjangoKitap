# Generated by Django 3.0.5 on 2020-05-03 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitap', '0004_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='title',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
