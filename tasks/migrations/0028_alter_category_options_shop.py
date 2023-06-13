# Generated by Django 4.1.7 on 2023-06-13 16:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0027_task_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('rating', models.CharField(max_length=10)),
                ('subscribers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('tasks', models.ManyToManyField(to='tasks.task')),
            ],
        ),
    ]