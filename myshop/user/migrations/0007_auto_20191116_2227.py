# Generated by Django 2.2.3 on 2019-11-16 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20191029_2235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='image1',
        ),
        migrations.RemoveField(
            model_name='item',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='being_delivered',
        ),
        migrations.RemoveField(
            model_name='order',
            name='received',
        ),
        migrations.RemoveField(
            model_name='order',
            name='refund_granted',
        ),
        migrations.RemoveField(
            model_name='order',
            name='refund_requested',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
    ]
