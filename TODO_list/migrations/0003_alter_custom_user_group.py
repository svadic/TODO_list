# Generated by Django 3.2 on 2021-05-03 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TODO_list', '0002_auto_20210503_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custom_user',
            name='group',
            field=models.ManyToManyField(related_name='group', to='TODO_list.Custom_Group'),
        ),
    ]
