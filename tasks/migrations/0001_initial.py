# Generated by Django 4.0.5 on 2023-09-06 19:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bidder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('rating', models.CharField(default=10, max_length=10)),
                ('is_verified', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='the_shop_owner', to='users.customuser')),
                ('subscribers', models.ManyToManyField(blank=True, to='users.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='ShopDocuments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='shop_documents')),
            ],
        ),
        migrations.CreateModel(
            name='ShopImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='shop_images')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('bidding_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='task_images')),
                ('is_active', models.BooleanField(default=True)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('picked_up', models.BooleanField(default=False)),
                ('being_delivered', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.category')),
                ('keywords', models.ManyToManyField(blank=True, to='tasks.keyword')),
                ('messenger', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='the_task_messenger', to='users.customuser')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='users.customuser')),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.shop')),
                ('task_bidders', models.ManyToManyField(blank=True, related_name='single_task_bidders', to='tasks.bidder')),
            ],
            options={
                'ordering': ('-date_posted',),
            },
        ),
        migrations.CreateModel(
            name='TaskReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('errandee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.customuser')),
                ('errander', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_errander', to='users.customuser')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='task_images')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='tasks.task')),
            ],
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Inquiry', 'Inquiry'), ('Complaint', 'Complaint'), ('Others', 'Others')], max_length=20)),
                ('message', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='ShopProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('documents', models.ManyToManyField(to='tasks.shopdocuments')),
                ('other_images', models.ManyToManyField(blank=True, to='tasks.shopimages')),
                ('shop', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tasks.shop')),
            ],
        ),
        migrations.AddField(
            model_name='shop',
            name='tasks',
            field=models.ManyToManyField(blank=True, related_name='shop_subscribers', to='tasks.task'),
        ),
        migrations.CreateModel(
            name='NewBidder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=150)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customuser')),
            ],
        ),
        migrations.AddField(
            model_name='bidder',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task'),
        ),
        migrations.AddField(
            model_name='bidder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customuser'),
        ),
        migrations.CreateModel(
            name='AcceptTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_picked', models.DateTimeField(auto_now_add=True)),
                ('receiver_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='users.customuser')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='tasks.task')),
            ],
        ),
    ]
