# Generated by Django 4.2.4 on 2023-09-11 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_rename_number_snapshot_big_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snapshot',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
