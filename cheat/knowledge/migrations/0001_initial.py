# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cmd', models.CharField(unique=True, max_length=255)),
                ('detail', models.CharField(max_length=2048, null=True, blank=True)),
            ],
        ),
    ]
