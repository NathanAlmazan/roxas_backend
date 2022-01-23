# Generated by Django 3.2.2 on 2021-05-09 01:46

from django.db import migrations, models
import report.models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='year',
            field=models.IntegerField(default=report.models.get_current_year),
        ),
    ]
