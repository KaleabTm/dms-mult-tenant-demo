# Generated by Django 5.0.6 on 2025-04-14 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobtitle',
            name='titer',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Job Title (Titer)'),
        ),
    ]
