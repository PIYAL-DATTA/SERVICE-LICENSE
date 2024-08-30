# Generated by Django 5.0.6 on 2024-06-05 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('service_name', models.CharField(max_length=255)),
                ('service_type', models.CharField(max_length=255)),
                ('active_date', models.CharField(max_length=255)),
                ('renewal_date', models.CharField(max_length=255)),
                ('owner', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=255)),
                ('days', models.CharField(max_length=255)),
            ],
        ),
    ]
