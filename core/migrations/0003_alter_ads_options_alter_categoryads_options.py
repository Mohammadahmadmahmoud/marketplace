# Generated by Django 4.0.4 on 2022-04-27 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ads',
            options={'ordering': ['-date_added'], 'verbose_name': 'Ad'},
        ),
        migrations.AlterModelOptions(
            name='categoryads',
            options={'ordering': ['ordering'], 'verbose_name': 'CategoryAd'},
        ),
    ]
