# Generated by Django 5.1.4 on 2025-01-27 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_alter_order_options_alter_orderitem_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created'], 'verbose_name': 'order', 'verbose_name_plural': 'orders'},
        ),
    ]
