# Generated by Django 3.2 on 2021-05-06 15:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TODO_list', '0008_auto_20210506_1549'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='parent_tasks',
            new_name='parent_task',
        ),
        migrations.AlterField(
            model_name='project',
            name='percentage',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='task',
            name='estimation',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
