# Generated by Django 5.1.2 on 2024-12-30 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carservice', '0010_alter_service_learn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='learn',
            field=models.CharField(max_length=200),
        ),
    ]
