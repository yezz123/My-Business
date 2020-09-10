# Generated by Django 2.2.14 on 2020-07-29 20:48

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0007_auto_20200715_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='country',
            field=django_countries.fields.CountryField(default='US', max_length=2),
            preserve_default=False,
        ),
    ]