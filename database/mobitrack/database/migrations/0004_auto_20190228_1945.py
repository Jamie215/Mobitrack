# Generated by Django 2.1.3 on 2019-03-01 00:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20181122_0441'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wearingsession',
            options={'ordering': ['timeStamp']},
        ),
    ]