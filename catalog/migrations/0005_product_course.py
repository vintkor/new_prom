# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-01 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_product_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='course',
            field=models.DecimalField(blank=True, decimal_places=5, default=1, max_digits=12, null=True, verbose_name='Курс валют'),
        ),
    ]