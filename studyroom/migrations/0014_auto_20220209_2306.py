# Generated by Django 3.1.3 on 2022-02-09 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studyroom', '0013_auto_20220201_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absence',
            name='absence_detail',
            field=models.CharField(default='결석사유:', max_length=60),
        ),
    ]
