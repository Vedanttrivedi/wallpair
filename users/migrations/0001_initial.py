# Generated by Django 3.1.2 on 2021-03-10 08:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('poll', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='profile_pics/user.png', upload_to='profile_pics')),
                ('bio', models.TextField(default='hey there i am using this blog site')),
                ('link', models.TextField(null=True)),
                ('typee', models.IntegerField(default=0, null=True)),
                ('pref', models.IntegerField(default=0)),
                ('clone', models.IntegerField(default=0)),
                ('following', models.ManyToManyField(related_name='follow', to=settings.AUTH_USER_MODEL)),
                ('follwers', models.ManyToManyField(related_name='follwe', to=settings.AUTH_USER_MODEL)),
                ('mysave', models.ManyToManyField(related_name='mysaved', to='poll.Questions')),
                ('pending', models.ManyToManyField(related_name='pending', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]