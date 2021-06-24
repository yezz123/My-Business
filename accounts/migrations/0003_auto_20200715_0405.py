# Generated by Django 2.2.12 on 2020-07-15 04:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('accounts', '0002_auto_20200620_0044'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['first_name']},
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('duration', models.IntegerField()),
                ('date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shifts', to='projects.Project')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shifts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
