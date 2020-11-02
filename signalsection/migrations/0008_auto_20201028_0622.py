# Generated by Django 3.0.1 on 2020-10-28 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signalsection', '0007_auto_20201027_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='email',
            field=models.EmailField(error_messages={'unique': 'This email is already registered in the database.'}, max_length=50, null=True, unique=True),
        ),
    ]
