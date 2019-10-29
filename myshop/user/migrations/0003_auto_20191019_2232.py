# Generated by Django 2.2.3 on 2019-10-19 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20191013_0008'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='one_click_purchasing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]