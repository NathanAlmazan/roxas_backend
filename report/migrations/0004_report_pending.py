# Generated by Django 3.2.2 on 2021-05-23 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_alter_report_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='pending',
            field=models.BooleanField(default=False),
        ),
    ]