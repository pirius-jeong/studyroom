# Generated by Django 3.1.3 on 2022-02-28 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studyroom', '0020_auto_20220213_2323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='absence',
            name='absence_dt',
        ),
        migrations.AddField(
            model_name='absence',
            name='absence_days',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='absence',
            name='absence_mt',
            field=models.CharField(default='yyyymm', max_length=6),
        ),
    ]