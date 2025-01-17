# Generated by Django 5.1.3 on 2024-11-19 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('agency', models.CharField(blank=True, max_length=100, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('comment', models.TextField(blank=True)),
                ('supervisor_name', models.CharField(blank=True, max_length=100, null=True)),
                ('supervisor_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('supervisor_email', models.EmailField(blank=True, max_length=100, null=True)),
                ('duration_days', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MahasiswaProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nim', models.CharField(max_length=20, unique=True)),
                ('full_name', models.CharField(max_length=255)),
                ('birth_date', models.DateField()),
                ('study_mode', models.CharField(choices=[('Fulltime', 'Fulltime'), ('Parttime', 'Parttime')], max_length=10)),
                ('primary_discipline', models.CharField(max_length=100)),
                ('mobile_phone', models.CharField(max_length=15)),
                ('campus_email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
    ]
