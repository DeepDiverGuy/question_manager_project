# Generated by Django 4.2.3 on 2023-07-27 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='idname',
            field=models.CharField(max_length=250),
        ),
    ]
