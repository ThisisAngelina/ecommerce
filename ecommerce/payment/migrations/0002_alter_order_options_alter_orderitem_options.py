# Generated by Django 5.1.4 on 2025-01-23 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created']},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['-id']},
        ),
    ]
