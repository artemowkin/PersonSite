# Generated by Django 3.2.5 on 2021-08-07 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=255, unique=True, verbose_name='product title'),
        ),
    ]