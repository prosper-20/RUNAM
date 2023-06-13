# Generated by Django 4.1.7 on 2023-06-13 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0028_alter_category_options_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='description',
            field=models.TextField(default='new'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shop',
            name='location',
            field=models.CharField(default='10 obe street', max_length=100),
            preserve_default=False,
        ),
    ]
