# Generated by Django 4.1.4 on 2022-12-31 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_subproduct_image_alter_subproduct_product'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='subproduct',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='shop.subproduct'),
            preserve_default=False,
        ),
    ]