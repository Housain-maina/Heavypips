# Generated by Django 3.0.1 on 2020-10-27 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signalsection', '0002_auto_20201027_0639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True),
        ),
    ]
