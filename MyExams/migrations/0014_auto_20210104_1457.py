# Generated by Django 3.1.4 on 2021-01-04 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyExams', '0013_auto_20210104_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='MyExams.exam'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyExams.user'),
        ),
    ]
