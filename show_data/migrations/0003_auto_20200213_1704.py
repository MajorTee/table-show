# Generated by Django 2.2.10 on 2020-02-13 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show_data', '0002_auto_20200213_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datainfo',
            name='FLGB_data',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='datainfo',
            name='LGB_data',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='datainfo',
            name='XGB_data',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='datainfo',
            name='real_data',
            field=models.CharField(max_length=50, null=True),
        ),
    ]