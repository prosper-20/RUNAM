# Generated by Django 4.0.5 on 2023-10-20 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_alter_labreporttask_no_of_pages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labreporttask',
            name='due_date',
            field=models.DateField(),
        ),
    ]
