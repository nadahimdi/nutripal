# Generated by Django 4.2.5 on 2023-10-22 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='updated',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
