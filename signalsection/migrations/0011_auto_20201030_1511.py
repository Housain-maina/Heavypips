# Generated by Django 3.0.1 on 2020-10-30 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signalsection', '0010_auto_20201030_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signal',
            name='body',
            field=models.TextField(),
        ),
    ]
