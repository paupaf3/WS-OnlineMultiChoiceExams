# Generated by Django 3.1.4 on 2021-01-07 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyExams', '0014_auto_20210104_1457'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='grade',
            unique_together={('exam', 'user')},
        ),
    ]
