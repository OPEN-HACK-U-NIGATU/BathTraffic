
# Generated by Django 4.2.4 on 2023-09-09 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_snapshot_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='snapshot',
            old_name='number',
            new_name='big_number',
        ),
        migrations.AddField(
            model_name='snapshot',
            name='small_number',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2.4 on 2023-09-09 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_snapshot_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='snapshot',
            old_name='number',
            new_name='big_number',
        ),
        migrations.AddField(
            model_name='snapshot',
            name='small_number',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
    ]

