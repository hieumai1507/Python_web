# Generated by Django 5.1 on 2024-09-21 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_wishlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='razorpay_order_id',
            new_name='order_id',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='razorpay_payment_id',
            new_name='payment_id',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='razorpay_payment_status',
            new_name='payment_status',
        ),
    ]
