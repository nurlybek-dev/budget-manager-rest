# Generated by Django 3.2.4 on 2021-06-06 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210405_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='actual_amount',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='account',
            name='planned_amount',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
