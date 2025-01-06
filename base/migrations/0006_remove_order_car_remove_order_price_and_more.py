# Generated by Django 5.1 on 2024-12-28 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='car',
        ),
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
        migrations.AddField(
            model_name='order',
            name='card_number',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_city',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_postal_code',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], default='Pending', max_length=20),
        ),
    ]
