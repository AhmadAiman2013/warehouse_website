# Generated by Django 5.1.1 on 2024-10-01 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_inbound_inventory_outbound'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outbound',
            name='status',
            field=models.CharField(default='shipped', max_length=50),
        ),
    ]
