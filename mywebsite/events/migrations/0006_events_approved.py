# Generated by Django 4.2.1 on 2023-07-12 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_venue_venue_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
