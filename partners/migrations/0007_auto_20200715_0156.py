# Generated by Django 2.2.12 on 2020-07-15 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0006_auto_20200702_0340'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partner',
            options={'ordering': ['company']},
        ),
    ]
