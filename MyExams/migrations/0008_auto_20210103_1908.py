# Generated by Django 3.1.4 on 2021-01-03 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyExams', '0007_auto_20210103_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='location',
            field=models.CharField(default='Lleida', max_length=40),
        ),
        migrations.AlterField(
            model_name='exam',
            name='time',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
